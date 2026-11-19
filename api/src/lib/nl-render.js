/* Newsletter rendering — one issue → { subject, html, text }.
 * Table-based, inline-styled HTML so it survives Outlook, Gmail and Apple
 * Mail. Everything user- or feed-supplied is escaped.
 */
const SITE = () => (process.env.NL_SITE_URL || "https://msftuniversity.com").replace(/\/$/, "");

const e = (s) => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
const safeUrl = (u) => (/^https:\/\//i.test(String(u || "")) ? String(u) : SITE());
// Paragraphs from plain text: blank line = new paragraph, single newline = <br>
const paras = (t, style) => String(t || "").trim().split(/\n\s*\n/).filter(Boolean)
  .map((p) => '<p style="' + style + '">' + e(p).replace(/\n/g, "<br>") + "</p>").join("");

const COLORS = {
  "Microsoft 365 Copilot": "#8661c5", "Defender for Office 365": "#c43e1c", "Defender for Endpoint": "#0f6cbd",
  "Defender for Identity": "#5c2d91", "Defender for Cloud Apps": "#008575", "Defender for Cloud": "#0078d4",
  "Microsoft Sentinel": "#004e8c", "Microsoft Purview": "#0b7a75",
};
const SECTIONS = [
  ["release", "Release notes", "What changed this fortnight, straight from Microsoft Learn"],
  ["roadmap", "On the roadmap", "Newly announced for Microsoft 365"],
  ["blog", "From the Microsoft blogs", ""],
];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
function dateRange(ev) {
  const d = new Date(ev.date + "T00:00:00Z"), f = (x) => x.getUTCDate() + " " + MON[x.getUTCMonth()];
  if (!ev.end || ev.end === ev.date) return f(d);
  const z = new Date(ev.end + "T00:00:00Z");
  return d.getUTCMonth() === z.getUTCMonth() ? d.getUTCDate() + "–" + f(z) : f(d) + " – " + f(z);
}
function longDate(iso) {
  const d = new Date(iso);
  return d.getUTCDate() + " " + ["January","February","March","April","May","June","July","August","September","October","November","December"][d.getUTCMonth()] + " " + d.getUTCFullYear();
}

function render(issue, ctx = {}) {
  const items = (issue.items || []).filter((i) => i.include);
  const events = (issue.events || []).filter((v) => v.include !== false);
  const site = SITE();
  const subject = issue.subject || "The Redmond Report";
  const unsub = ctx.unsubscribeUrl || site + "/newsletter.html";
  const web = ctx.webUrl || "";
  const FONT = "font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;";
  const pre = ctx.preheader || (items[0] ? items.length + " updates: " + items[0].title : "News from Microsoft University");

  const h = [];
  h.push('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>' + e(subject) + "</title></head>");
  h.push('<body style="margin:0;padding:0;background:#f2f4f7;">');
  h.push('<div style="display:none;max-height:0;overflow:hidden;opacity:0;">' + e(pre) + "</div>");
  h.push('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f2f4f7;"><tr><td align="center" style="padding:24px 12px;">');
  h.push('<table role="presentation" width="640" cellpadding="0" cellspacing="0" style="width:100%;max-width:640px;background:#ffffff;border-radius:10px;overflow:hidden;">');
  // header
  h.push('<tr><td style="background:#0b1a30;padding:28px 32px 26px;">');
  h.push('<table role="presentation" cellpadding="0" cellspacing="0"><tr>' +
    '<td style="padding-right:12px;"><table role="presentation" cellpadding="0" cellspacing="2"><tr><td width="10" height="10" style="background:#f25022;font-size:0;">&nbsp;</td><td width="10" height="10" style="background:#7fba00;font-size:0;">&nbsp;</td></tr><tr><td width="10" height="10" style="background:#00a4ef;font-size:0;">&nbsp;</td><td width="10" height="10" style="background:#ffb900;font-size:0;">&nbsp;</td></tr></table></td>' +
    '<td style="' + FONT + 'color:#b8cce4;font-size:14px;">microsoft<b style="color:#fff;">university</b><span style="color:#4fb3f6;">.com</span></td></tr></table>');
  h.push('<div style="' + FONT + 'color:#00a4ef;font-size:12px;font-weight:700;letter-spacing:1.5px;margin-top:22px;">THE REDMOND REPORT · ' + e(longDate(issue.sentAt || issue.createdAt || new Date().toISOString()).toUpperCase()) + "</div>");
  h.push('<div style="' + FONT + 'color:#ffffff;font-size:26px;line-height:1.25;font-weight:700;margin-top:6px;">' + e(subject) + "</div>");
  h.push("</td></tr>");
  if (web) h.push('<tr><td style="' + FONT + 'padding:10px 32px 0;font-size:12px;color:#8a8a8a;text-align:right;"><a href="' + e(web) + '" style="color:#8a8a8a;">View in your browser</a></td></tr>');
  // intro
  if ((issue.intro || "").trim()) {
    h.push('<tr><td style="padding:22px 32px 4px;">' + paras(issue.intro, FONT + "margin:0 0 14px;font-size:16px;line-height:1.6;color:#1f1f1f;") + "</td></tr>");
  }
  // sections
  for (const [kind, title, sub] of SECTIONS) {
    const rows = items.filter((i) => i.kind === kind);
    if (!rows.length) continue;
    h.push('<tr><td style="padding:22px 32px 4px;"><div style="' + FONT + 'font-size:19px;font-weight:700;color:#0b1a30;">' + e(title) + "</div>" +
      (sub ? '<div style="' + FONT + 'font-size:13px;color:#6b6b6b;margin-top:2px;">' + e(sub) + "</div>" : "") + "</td></tr>");
    for (const it of rows) {
      const col = COLORS[it.source] || "#3b4a5c";
      h.push('<tr><td style="padding:10px 32px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-left:3px solid ' + col + ';"><tr><td style="padding:2px 0 2px 14px;">' +
        '<div style="' + FONT + 'font-size:11.5px;font-weight:700;color:' + col + ';text-transform:uppercase;letter-spacing:.6px;">' + e(it.source) + (it.meta ? ' <span style="color:#8a8a8a;font-weight:600;">· ' + e(it.meta) + "</span>" : "") + "</div>" +
        '<a href="' + e(safeUrl(it.link)) + '" style="' + FONT + 'font-size:16px;font-weight:600;line-height:1.4;color:#0067b8;text-decoration:none;">' + e(it.title) + "</a>" +
        ((it.summary || "").trim() ? '<p style="' + FONT + 'margin:5px 0 0;font-size:14.5px;line-height:1.55;color:#3d3d3d;">' + e(it.summary.trim()) + "</p>" : "") +
        ((it.note || "").trim() ? '<p style="' + FONT + 'margin:8px 0 0;font-size:14.5px;line-height:1.55;color:#0b1a30;background:#eef5fc;border-radius:6px;padding:8px 12px;"><b>Alex&rsquo;s take:</b> ' + e(it.note.trim()).replace(/\n/g, "<br>") + "</p>" : "") +
        "</td></tr></table></td></tr>");
    }
  }
  // events
  if (events.length) {
    h.push('<tr><td style="padding:22px 32px 4px;"><div style="' + FONT + 'font-size:19px;font-weight:700;color:#0b1a30;">Upcoming courses &amp; events</div></td></tr>');
    h.push('<tr><td style="padding:6px 32px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">');
    for (const ev of events) {
      h.push('<tr><td style="' + FONT + 'padding:8px 12px 8px 0;font-size:14px;font-weight:700;color:#0b1a30;white-space:nowrap;vertical-align:top;width:90px;">' + e(dateRange(ev)) + "</td>" +
        '<td style="' + FONT + 'padding:8px 0;font-size:14.5px;color:#1f1f1f;vertical-align:top;border-bottom:1px solid #eeeeee;"><a href="' + e(safeUrl(ev.url || site + "/events.html")) + '" style="color:#1f1f1f;font-weight:600;text-decoration:none;">' + e(ev.title) + '</a><br><span style="color:#6b6b6b;font-size:13px;">' + e([ev.venue, ev.city].filter(Boolean).join(" · ")) + "</span></td></tr>");
    }
    h.push('</table><div style="' + FONT + 'font-size:13.5px;margin-top:10px;"><a href="' + e(site) + '/events.html" style="color:#0067b8;">See all events →</a></div></td></tr>');
  }
  // outro
  if ((issue.outro || "").trim()) {
    h.push('<tr><td style="padding:22px 32px 0;">' + paras(issue.outro, FONT + "margin:0 0 12px;font-size:15px;line-height:1.6;color:#1f1f1f;") + "</td></tr>");
  }
  h.push('<tr><td style="padding:18px 32px 28px;' + FONT + 'font-size:15px;color:#1f1f1f;">— Alex<br><span style="color:#6b6b6b;font-size:13px;">Alex de Jong · Microsoft Certified Trainer</span></td></tr>');
  // footer
  h.push('<tr><td style="background:#f7f8fa;padding:20px 32px;' + FONT + 'font-size:12px;line-height:1.6;color:#6b6b6b;">' +
    "You get this because you subscribed at " + e(site.replace(/^https:\/\//, "")) + ". " +
    '<a href="' + e(unsub) + '" style="color:#6b6b6b;">Unsubscribe</a> · <a href="' + e(site) + '/privacy.html" style="color:#6b6b6b;">Privacy</a><br>' +
    "Microsoft University · alexdejong.com · Bergeijk, the Netherlands · KvK 17175279<br>" +
    "Microsoft and related marks are trademarks of the Microsoft group of companies. This independent newsletter is not affiliated with or endorsed by Microsoft." +
    "</td></tr>");
  h.push("</table></td></tr></table></body></html>");

  // plain-text alternative
  const t = [subject.toUpperCase(), "The Redmond Report · " + longDate(issue.sentAt || issue.createdAt || new Date().toISOString()), ""];
  if (web) t.push("View in your browser: " + web, "");
  if ((issue.intro || "").trim()) t.push(issue.intro.trim(), "");
  for (const [kind, title] of SECTIONS) {
    const rows = items.filter((i) => i.kind === kind);
    if (!rows.length) continue;
    t.push("== " + title + " ==", "");
    rows.forEach((it) => {
      t.push("* [" + it.source + "] " + it.title, "  " + safeUrl(it.link));
      if ((it.summary || "").trim()) t.push("  " + it.summary.trim());
      if ((it.note || "").trim()) t.push("  Alex's take: " + it.note.trim().replace(/\n/g, "\n  "));
      t.push("");
    });
  }
  if (events.length) {
    t.push("== Upcoming courses & events ==", "");
    events.forEach((ev) => t.push("* " + dateRange(ev) + "  " + ev.title + (ev.city ? " (" + ev.city + ")" : "")));
    t.push("", site + "/events.html", "");
  }
  if ((issue.outro || "").trim()) t.push(issue.outro.trim(), "");
  t.push("— Alex", "", "Unsubscribe: " + unsub, "Microsoft University · alexdejong.com · Bergeijk, the Netherlands · KvK 17175279");

  return { subject, html: h.join("\n"), text: t.join("\n") };
}

function confirmMail(confirmUrl) {
  const site = SITE();
  const FONT = "font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;";
  const html = '<!doctype html><html><body style="margin:0;background:#f2f4f7;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:32px 12px;">' +
    '<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="width:100%;max-width:560px;background:#fff;border-radius:10px;"><tr><td style="padding:32px;' + FONT + 'color:#1f1f1f;">' +
    '<div style="font-size:22px;font-weight:700;color:#0b1a30;">One click to confirm</div>' +
    '<p style="font-size:15.5px;line-height:1.6;">Someone (hopefully you) asked to receive <b>The Redmond Report</b> from Microsoft University — the Microsoft news that matters, every other Thursday.</p>' +
    '<p style="margin:26px 0;"><a href="' + e(confirmUrl) + '" style="background:#0067b8;color:#fff;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:6px;display:inline-block;">Yes, subscribe me</a></p>' +
    '<p style="font-size:13px;color:#6b6b6b;line-height:1.6;">Didn\'t ask for this? Just ignore this email — you won\'t hear from us again, and we delete unconfirmed sign-ups after 7 days.</p>' +
    '<p style="font-size:12px;color:#8a8a8a;">Microsoft University · alexdejong.com · Bergeijk, the Netherlands · <a href="' + e(site) + '/privacy.html" style="color:#8a8a8a;">Privacy</a></p>' +
    "</td></tr></table></td></tr></table></body></html>";
  const text = "Confirm your subscription to The Redmond Report from Microsoft University:\n\n" + confirmUrl +
    "\n\nDidn't ask for this? Ignore this email — unconfirmed sign-ups are deleted after 7 days.\n\nMicrosoft University · alexdejong.com · Bergeijk, the Netherlands";
  return { subject: "Confirm your subscription to The Redmond Report", html, text };
}

module.exports = { render, confirmMail, esc: e };
