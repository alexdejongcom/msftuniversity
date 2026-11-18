/* The Briefing — self-hosted newsletter on Azure.
 *
 * Public
 *   POST /api/newsletter/subscribe    { email, website }  → double opt-in mail
 *   POST /api/newsletter/confirm      { token }
 *   POST /api/newsletter/unsubscribe  { token } | ?t=token (RFC 8058 one-click)
 *   GET  /api/newsletter/archive      → [{ id, subject, sentAt }]
 *   GET  /api/newsletter/issue?id=…   → a sent issue as a web page
 * Admin (role "newsletter-admin", enforced in staticwebapp.config.json AND here)
 *   GET  /api/newsletter/admin/state
 *   GET  /api/newsletter/admin/issue?id=…
 *   GET  /api/newsletter/admin/preview?id=…   rendered HTML of any issue
 *   POST /api/newsletter/admin/draft          build a fresh draft from the feeds
 *   POST /api/newsletter/admin/save           { id, subject, intro, outro, items, events }
 *   POST /api/newsletter/admin/delete         { id }   (drafts only)
 *   POST /api/newsletter/admin/test           { id }   → preview to NL_ADMIN_EMAIL
 *   POST /api/newsletter/admin/send           { id }   → queue for all subscribers
 *   GET  /api/newsletter/admin/subscribers.csv
 * Scheduler (GitHub Actions, header x-nl-key = NL_CRON_KEY) or admin
 *   POST /api/newsletter/tick   sends the next batch within the ACS rate
 *                               limits, purges stale sign-ups, reminds Alex
 *                               when a new issue is due.
 *
 * Confirm and unsubscribe links in mails open a page with a button (POST),
 * never a GET that changes state: link scanners such as Defender Safe Links
 * open every link in a mail, which would otherwise confirm — or unsubscribe —
 * people automatically.
 */
const crypto = require("crypto");
const { app } = require("@azure/functions");
const store = require("../lib/nl-store");
const mail = require("../lib/nl-mail");
const { render, confirmMail } = require("../lib/nl-render");
const { buildDraft } = require("../lib/nl-draft");

const SITE = () => (process.env.NL_SITE_URL || "https://msftuniversity.com").replace(/\/$/, "");
const ROLE = "newsletter-admin";
const CYCLE_DAYS = 14;
const DAY = 86400e3;

const json = (status, body) => ({ status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" }, body: JSON.stringify(body) });
const now = () => new Date().toISOString();
async function body(req) { try { return await req.json(); } catch { return {}; } }

/* ---------- helpers ---------- */
function isAdmin(req) {
  try {
    const p = JSON.parse(Buffer.from(req.headers.get("x-ms-client-principal") || "", "base64").toString("utf8"));
    return Array.isArray(p.userRoles) && p.userRoles.includes(ROLE);
  } catch { return false; }
}
function isCron(req) {
  const want = process.env.NL_CRON_KEY || "", got = req.headers.get("x-nl-key") || "";
  if (want.length < 24 || got.length !== want.length) return false;
  return crypto.timingSafeEqual(Buffer.from(want), Buffer.from(got));
}
const EMAIL = /^[^\s@<>()",;:]{1,64}@[A-Za-z0-9.-]{1,190}\.[A-Za-z]{2,}$/;

const hits = new Map(); // ip → [timestamps]  (per instance; good enough against bursts)
function tooMany(ip) {
  const t = Date.now(), list = (hits.get(ip) || []).filter((x) => t - x < 10 * 60e3);
  list.push(t); hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return list.length > 5;
}

function issueOut(e) {
  if (!e) return null;
  return {
    id: e.rowKey, status: e.status, subject: e.subject || "", intro: e.intro || "", outro: e.outro || "",
    items: JSON.parse(e.items || "[]"), events: JSON.parse(e.events || "[]"),
    createdAt: e.createdAt, updatedAt: e.updatedAt || "", sentAt: e.sentAt || "",
    total: e.total || 0, sent: e.sent || 0, failed: e.failed || 0,
  };
}
async function issues() {
  return (await store.list("PartitionKey eq 'issue'")).sort((a, b) => (a.rowKey < b.rowKey ? 1 : -1));
}
const webUrl = (id) => SITE() + "/api/newsletter/issue?id=" + encodeURIComponent(id);
const unsubUrl = (token) => SITE() + "/newsletter.html?unsubscribe=" + encodeURIComponent(token);
const oneClickUrl = (token) => SITE() + "/api/newsletter/unsubscribe?t=" + encodeURIComponent(token);

/* ---------- public ---------- */
app.http("nlSubscribe", {
  route: "newsletter/subscribe", methods: ["POST"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    const b = await body(req);
    const email = String(b.email || "").trim();
    const ok = json(200, { ok: true, message: "Check your inbox to confirm." });
    if (b.website) return ok;                         // honeypot: bots fill every field
    if (email.length > 254 || !EMAIL.test(email)) return json(400, { ok: false, message: "That doesn't look like an email address." });
    if (tooMany(req.headers.get("x-forwarded-for") || "?")) return json(429, { ok: false, message: "Too many attempts — try again in a few minutes." });
    try {
      const rk = store.subKey(email);
      let sub = await store.get("sub", rk);
      if (sub && sub.status === "active") return ok;  // never reveal who is subscribed
      if (sub && sub.lastMailAt && Date.now() - Date.parse(sub.lastMailAt) < 10 * 60e3) return ok;
      sub = { partitionKey: "sub", rowKey: rk, email, status: "pending", secret: (sub && sub.secret) || store.newSecret(), createdAt: (sub && sub.createdAt) || now(), lastMailAt: now() };
      await store.upsert(sub);
      const m = confirmMail(SITE() + "/newsletter.html?confirm=" + encodeURIComponent(store.tokenOf(sub)));
      try {
        await mail.send({ to: email, ...m });
      } catch (e) {
        await store.merge({ partitionKey: "sub", rowKey: rk, lastMailAt: "" }); // let them retry right away
        if (e.statusCode === 429) return json(503, { ok: false, message: "We're sending a lot of mail right now — please try again in a minute." });
        throw e;
      }
      await mail.record(1);
      return ok;
    } catch (e) {
      ctx.error("subscribe failed:", e.message);
      return json(503, { ok: false, message: "Sign-up is temporarily unavailable. Please try again later." });
    }
  },
});

app.http("nlConfirm", {
  route: "newsletter/confirm", methods: ["POST"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    try {
      const sub = await store.subByToken((await body(req)).token);
      if (!sub) return json(404, { ok: false, message: "This link has expired. Please sign up again." });
      if (sub.status !== "active") await store.merge({ partitionKey: "sub", rowKey: sub.rowKey, status: "active", confirmedAt: now() });
      return json(200, { ok: true });
    } catch (e) { ctx.error("confirm failed:", e.message); return json(503, { ok: false, message: "Please try again later." }); }
  },
});

app.http("nlUnsubscribe", {
  route: "newsletter/unsubscribe", methods: ["POST"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    try {
      const q = new URL(req.url).searchParams.get("t");
      const token = q || (await body(req)).token;
      const sub = await store.subByToken(token);
      if (sub) await store.remove("sub", sub.rowKey);  // gone means gone
      return json(200, { ok: true });                  // same answer either way
    } catch (e) { ctx.error("unsubscribe failed:", e.message); return json(503, { ok: false, message: "Please try again later." }); }
  },
});

app.http("nlArchive", {
  route: "newsletter/archive", methods: ["GET"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    try {
      const list = (await issues()).filter((e) => e.status === "sent").slice(0, 24).map((e) => ({ id: e.rowKey, subject: e.subject, sentAt: e.sentAt }));
      return { status: 200, headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=600" }, body: JSON.stringify(list) };
    } catch (e) { ctx.error("archive failed:", e.message); return json(503, { error: "archive unavailable" }); }
  },
});

app.http("nlIssue", {
  route: "newsletter/issue", methods: ["GET"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    const id = new URL(req.url).searchParams.get("id") || "";
    if (!/^\d{10,16}$/.test(id)) return { status: 404, body: "Not found" };
    const issue = issueOut(await store.get("issue", id));
    if (!issue || issue.status !== "sent") return { status: 404, body: "Not found" };
    const { html } = render(issue, { unsubscribeUrl: SITE() + "/newsletter.html" });
    return { status: 200, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=3600" }, body: html };
  },
});

/* ---------- sending ---------- */
async function tick(ctx, { allowRemind = true } = {}) {
  const out = { sentNow: 0, pending: 0, waitSeconds: 0, reminded: false, purged: 0 };

  // 1. purge unconfirmed sign-ups older than 7 days
  const cutoff = new Date(Date.now() - 7 * DAY).toISOString();
  const stale = await store.list("PartitionKey eq 'sub' and status eq 'pending' and createdAt lt '" + cutoff + "'", ["PartitionKey", "RowKey"], 50);
  for (const s of stale) await store.remove("sub", s.rowKey);
  out.purged = stale.length;

  // 2. continue an issue that is being sent
  const all = await issues();
  const sending = all.find((e) => e.status === "sending");
  if (sending) {
    const issue = issueOut(sending), pk = "q-" + issue.id;
    const { left } = await mail.budget();
    const batch = left ? await store.list("PartitionKey eq '" + pk + "' and status eq 'queued'", null, Math.min(left, 25)) : [];
    let sent = 0, failed = 0, rateHit = false;
    for (const q of batch) {
      const sub = await store.get("sub", q.rowKey);
      if (!sub || sub.status !== "active") { await store.remove(pk, q.rowKey); continue; } // left meanwhile
      const token = store.tokenOf(sub);
      const m = render(issue, { unsubscribeUrl: unsubUrl(token), webUrl: webUrl(issue.id) });
      try {
        await mail.send({ to: sub.email, ...m, unsubscribeUrl: oneClickUrl(token) });
        await store.merge({ partitionKey: pk, rowKey: q.rowKey, status: "sent" });
        sent++;
      } catch (e) {
        if (e.statusCode === 429) { rateHit = true; break; }
        ctx.warn("send failed:", e.message);
        await store.merge({ partitionKey: pk, rowKey: q.rowKey, status: "failed", error: String(e.message || "").slice(0, 200) });
        failed++;
      }
    }
    await mail.record(sent + failed);
    out.sentNow = sent;
    const remaining = await store.list("PartitionKey eq '" + pk + "' and status eq 'queued'", ["RowKey"], 100000);
    out.pending = remaining.length;
    const upd = { partitionKey: "issue", rowKey: issue.id, sent: issue.sent + sent, failed: issue.failed + failed };
    if (!remaining.length) { upd.status = "sent"; upd.sentAt = now(); }
    await store.merge(upd);
    if (out.pending) {
      const after = await mail.budget();
      out.waitSeconds = rateHit ? 65 : after.left ? 2 : after.waitSeconds || 65;
    }
    return out;
  }

  // 3. remind Alex when an issue is due
  if (allowRemind && process.env.NL_ADMIN_EMAIL) {
    const last = all.find((e) => e.status === "sent");
    const due = !last || Date.now() - Date.parse(last.sentAt) >= (CYCLE_DAYS - 1) * DAY;
    const cycle = last ? last.rowKey : "first";
    const r = await store.get("meta", "remind");
    if (due && (!r || r.cycle !== cycle)) {
      const hasDraft = all.some((e) => e.status === "draft" && (!last || e.rowKey > last.rowKey));
      if (!hasDraft) await createDraft();
      const { left } = await mail.budget();
      if (left) {
        const site = SITE();
        await mail.send({
          to: process.env.NL_ADMIN_EMAIL,
          subject: "Your next Briefing draft is ready",
          text: "It's been two weeks — a fresh draft of The Briefing is waiting.\n\nReview, add your take and send:\n" + site + "/newsletter-admin.html\n",
          html: '<p style="font-family:Segoe UI,Arial,sans-serif;font-size:15px">It\'s been two weeks — a fresh draft of <b>The Briefing</b> is waiting.</p><p><a href="' + site + '/newsletter-admin.html" style="font-family:Segoe UI,Arial,sans-serif;background:#0067b8;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none">Review &amp; send</a></p>',
        });
        await mail.record(1);
        await store.upsert({ partitionKey: "meta", rowKey: "remind", cycle, at: now() });
        out.reminded = true;
      }
    }
  }
  return out;
}

async function createDraft() {
  const all = await issues();
  const sent = all.filter((e) => e.status === "sent");
  const seen = new Set();
  sent.slice(0, 6).forEach((e) => JSON.parse(e.items || "[]").forEach((i) => i.include && seen.add(i.link)));
  const d = await buildDraft({ lastSent: sent[0] ? { sentAt: sent[0].sentAt } : null, seen });
  const id = String(Date.now());
  await store.upsert({
    partitionKey: "issue", rowKey: id, status: "draft", subject: d.subject, intro: "", outro: "",
    items: JSON.stringify(d.items), events: JSON.stringify(d.events), createdAt: now(), updatedAt: now(), total: 0, sent: 0, failed: 0,
  });
  return issueOut(await store.get("issue", id));
}

app.http("nlTick", {
  route: "newsletter/tick", methods: ["POST"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    if (!isCron(req) && !isAdmin(req)) return json(401, { error: "unauthorized" });
    try { return json(200, await tick(ctx, { allowRemind: isCron(req) })); }
    catch (e) { ctx.error("tick failed:", e.message); return json(503, { error: e.message }); }
  },
});

/* ---------- admin ---------- */
const clip = (s, n) => String(s == null ? "" : s).slice(0, n);
function cleanItems(items) {
  return (Array.isArray(items) ? items : []).slice(0, 80).map((i) => ({
    id: clip(i.id, 40), kind: ["release", "roadmap", "blog"].includes(i.kind) ? i.kind : "blog",
    source: clip(i.source, 80), title: clip(i.title, 200), link: /^https:\/\//.test(i.link || "") ? clip(i.link, 600) : "",
    meta: clip(i.meta, 80), include: !!i.include, note: clip(i.note, 1500),
  })).filter((i) => i.link && i.title);
}
function cleanEvents(evs) {
  return (Array.isArray(evs) ? evs : []).slice(0, 12).map((v) => ({
    date: /^\d{4}-\d{2}-\d{2}$/.test(v.date) ? v.date : "", end: /^\d{4}-\d{2}-\d{2}$/.test(v.end || "") ? v.end : "",
    title: clip(v.title, 200), city: clip(v.city, 80), venue: clip(v.venue, 120),
    url: /^https:\/\//.test(v.url || "") ? clip(v.url, 600) : "", include: v.include !== false,
  })).filter((v) => v.date && v.title);
}

app.http("nlAdmin", {
  route: "newsletter/admin/{action}", methods: ["GET", "POST"], authLevel: "anonymous",
  handler: async (req, ctx) => {
    if (!isAdmin(req)) return json(403, { error: "forbidden" });
    const action = req.params.action;
    try {
      if (req.method === "GET" && action === "state") {
        const subs = await store.list("PartitionKey eq 'sub'", ["status"]);
        const list = (await issues()).slice(0, 20).map((e) => { const o = issueOut(e); delete o.items; delete o.events; delete o.intro; delete o.outro; return o; });
        return json(200, {
          subscribers: { active: subs.filter((s) => s.status === "active").length, pending: subs.filter((s) => s.status === "pending").length },
          issues: list,
          configured: { acs: !!process.env.ACS_CONNECTION_STRING, from: process.env.NL_FROM || "", admin: !!process.env.NL_ADMIN_EMAIL, cron: (process.env.NL_CRON_KEY || "").length >= 24 },
          limits: { minute: +process.env.NL_RATE_MINUTE || 30, hour: +process.env.NL_RATE_HOUR || 100 },
        });
      }
      if (req.method === "GET" && action === "issue") {
        const it = issueOut(await store.get("issue", new URL(req.url).searchParams.get("id") || ""));
        return it ? json(200, it) : json(404, { error: "not found" });
      }
      if (req.method === "GET" && action === "preview") {
        const it = issueOut(await store.get("issue", new URL(req.url).searchParams.get("id") || ""));
        if (!it) return json(404, { error: "not found" });
        return { status: 200, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" }, body: render(it, { unsubscribeUrl: SITE() + "/newsletter.html" }).html };
      }
      if (req.method === "GET" && action === "subscribers.csv") {
        const subs = await store.list("PartitionKey eq 'sub' and status eq 'active'", ["email", "confirmedAt"]);
        const csv = "email,confirmed\n" + subs.map((s) => '"' + String(s.email).replace(/"/g, '""') + '",' + (s.confirmedAt || "")).join("\n");
        return { status: 200, headers: { "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": 'attachment; filename="briefing-subscribers.csv"', "Cache-Control": "no-store" }, body: csv };
      }
      if (req.method !== "POST") return json(405, { error: "method not allowed" });
      const b = await body(req);

      if (action === "draft") return json(200, await createDraft());

      const cur = b.id ? await store.get("issue", String(b.id)) : null;
      if (!cur) return json(404, { error: "issue not found" });

      if (action === "save") {
        if (cur.status !== "draft") return json(409, { error: "only drafts can be edited" });
        await store.merge({
          partitionKey: "issue", rowKey: cur.rowKey, subject: clip(b.subject, 150) || cur.subject,
          intro: clip(b.intro, 6000), outro: clip(b.outro, 3000),
          items: JSON.stringify(cleanItems(b.items)), events: JSON.stringify(cleanEvents(b.events)), updatedAt: now(),
        });
        return json(200, issueOut(await store.get("issue", cur.rowKey)));
      }
      if (action === "delete") {
        if (cur.status !== "draft") return json(409, { error: "only drafts can be deleted" });
        await store.remove("issue", cur.rowKey);
        return json(200, { ok: true });
      }
      if (action === "test") {
        if (!process.env.NL_ADMIN_EMAIL) return json(400, { error: "NL_ADMIN_EMAIL is not configured" });
        const { left } = await mail.budget();
        if (!left) return json(429, { error: "send limit reached — try again in a minute" });
        const m = render(issueOut(cur), { unsubscribeUrl: SITE() + "/newsletter.html" });
        await mail.send({ to: process.env.NL_ADMIN_EMAIL, ...m, subject: "[TEST] " + m.subject });
        await mail.record(1);
        return json(200, { ok: true, to: process.env.NL_ADMIN_EMAIL });
      }
      if (action === "send") {
        if (cur.status !== "draft") return json(409, { error: "this issue was already sent" });
        if ((await issues()).some((e) => e.status === "sending")) return json(409, { error: "another issue is still being sent" });
        const issue = issueOut(cur);
        if (!issue.items.some((i) => i.include)) return json(400, { error: "select at least one item" });
        const subs = await store.list("PartitionKey eq 'sub' and status eq 'active'", ["RowKey", "email"]);
        if (!subs.length) return json(400, { error: "no confirmed subscribers yet" });
        await store.batchInsert("q-" + cur.rowKey, subs.map((s) => ({ rowKey: s.rowKey, email: s.email, status: "queued" })));
        await store.merge({ partitionKey: "issue", rowKey: cur.rowKey, status: "sending", total: subs.length, sent: 0, failed: 0, sentAt: now() });
        const t = await tick(ctx, { allowRemind: false });
        return json(200, { ok: true, total: subs.length, ...t });
      }
      return json(404, { error: "unknown action" });
    } catch (e) {
      ctx.error("admin " + action + " failed:", e.message);
      return json(500, { error: e.message });
    }
  },
});

module.exports = { _tick: tick, _createDraft: createDraft };
