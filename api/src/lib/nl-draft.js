/* Newsletter draft builder.
 *
 * Collects everything new since the last sent issue — Learn release notes,
 * roadmap entries, blog posts — skips anything a recent issue already
 * carried, pre-selects a balanced handful and adds upcoming public events
 * from the site's own js/events.js. Alex reviews, comments and sends.
 */
const vm = require("vm");
const feeds = require("./feeds");

const SITE = () => (process.env.NL_SITE_URL || "https://msftuniversity.com").replace(/\/$/, "");
const DAY = 86400e3;

async function upcomingEvents(now) {
  try {
    const res = await fetch(SITE() + "/js/events.js", { headers: { Accept: "application/javascript" } });
    if (!res.ok) return [];
    // Our own file; evaluated in an empty sandbox with a time limit.
    const src = (await res.text()) + "\n;({ EVENTS: typeof EVENTS !== 'undefined' ? EVENTS : [] })";
    const { EVENTS } = vm.runInNewContext(src, {}, { timeout: 200 });
    const today = new Date(now).toISOString().slice(0, 10);
    const until = new Date(now + 75 * DAY).toISOString().slice(0, 10);
    return (EVENTS || [])
      .filter((ev) => ev && ev.date > today && ev.date <= until && !ev.soldout && !/\(internal\)/i.test(ev.title || ""))
      .sort((a, b) => (a.date < b.date ? -1 : 1))
      .slice(0, 6)
      .map((ev) => ({ date: ev.date, end: ev.end || "", title: ev.title, city: ev.city || "", venue: ev.venue || "", url: /^https:\/\//.test(ev.url || "") ? ev.url : "", include: true }));
  } catch {
    return [];
  }
}

function pickBalanced(list, n) {
  // first pass: one per source, newest first; second pass: fill up
  const chosen = new Set(), sources = new Set();
  for (const it of list) if (chosen.size < n && !sources.has(it.source)) { chosen.add(it); sources.add(it.source); }
  for (const it of list) if (chosen.size < n) chosen.add(it);
  return chosen;
}

/* lastSent: the most recent sent issue (or null); seen: Set of links already sent */
async function buildDraft({ lastSent, seen, now = Date.now() }) {
  const since = lastSent && lastSent.sentAt ? Date.parse(lastSent.sentAt) : now - 14 * DAY;
  const sinceMonth = new Date(since).toISOString().slice(0, 7); // release notes are month-precise
  const items = [];
  const add = (kind, rows, preselect) => {
    const chosen = pickBalanced(rows, preselect);
    rows.forEach((r, i) => items.push({ id: kind + "-" + i, kind, include: chosen.has(r), note: "", ...r.out }));
  };

  const [wn, rm, bl] = await Promise.allSettled([feeds.getWhatsNew(), feeds.getRoadmap(), feeds.getBlogs()]);

  if (wn.status === "fulfilled") {
    const rows = wn.value
      .filter((x) => !seen.has(x.link) && x.key.slice(0, 7) >= sinceMonth)
      .slice(0, 24)
      .map((x) => ({ source: x.source, out: { source: x.source, title: x.title, link: x.link, meta: [x.stage, x.month].filter(Boolean).join(" · ") } }));
    add("release", rows, 6);
  }
  if (rm.status === "fulfilled") {
    const rows = rm.value
      .filter((x) => !seen.has(x.link) && Date.parse(x.added) >= since)
      .slice(0, 16)
      .map((x) => {
        const ga = /^(\d{4})-(\d{2})$/.exec(x.ga || "");
        const when = ga ? "GA " + ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][+ga[2] - 1] + " " + ga[1] : "";
        return { source: x.product, out: { source: x.product, title: x.title, link: x.link, meta: [x.status, when].filter(Boolean).join(" · ") } };
      });
    add("roadmap", rows, 4);
  }
  if (bl.status === "fulfilled") {
    const rows = bl.value
      .filter((x) => !seen.has(x.link) && Date.parse(x.date) >= since)
      .slice(0, 10)
      .map((x) => ({ source: x.source, out: { source: x.source, title: x.title, link: x.link, meta: "" } }));
    add("blog", rows, 3);
  }

  const d = new Date(now);
  const nice = d.getUTCDate() + " " + ["January","February","March","April","May","June","July","August","September","October","November","December"][d.getUTCMonth()] + " " + d.getUTCFullYear();
  return {
    subject: "The Redmond Report — " + nice,
    intro: "",
    outro: "",
    items,
    events: await upcomingEvents(now),
  };
}

module.exports = { buildDraft, upcomingEvents };
