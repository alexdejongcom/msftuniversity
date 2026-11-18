/* Parser for Microsoft Learn "What's new" / release-notes pages.
 *
 * Learn pages share one skeleton — a month heading (<h2 id="october-2026">)
 * followed by that month's changes — but each product team writes the
 * changes differently. MODE tells the parser which shape to expect:
 *   h3        one <h3> per feature                (MDI, MDA, MDC, Sentinel)
 *   li-strong bulleted <li><strong>Title</strong>  (Defender for Office 365)
 *   table     Type | Feature | Preview/GA | Desc   (Defender for Endpoint)
 *   category  <h3> per workload, <li> per change   (Purview)
 * Pure string functions, no DOM: runs the same in Node and in a browser.
 */
const MONTHS = ["january","february","march","april","may","june","july","august","september","october","november","december"];

function decode(s) {
  return String(s || "")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, " ")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)))
    .replace(/\s+/g, " ").trim();
}

// "October 2026" / "Aug 2025" → { label: "October 2026", key: "2026-10" }
function month(text) {
  const m = decode(text).match(/^([A-Za-z]+)\.?\s+(\d{4})$/);
  if (!m) return null;
  const i = MONTHS.findIndex((n) => n.startsWith(m[1].toLowerCase().slice(0, 3)));
  if (i < 0) return null;
  return { label: MONTHS[i][0].toUpperCase() + MONTHS[i].slice(1) + " " + m[2], key: m[2] + "-" + String(i + 1).padStart(2, "0") };
}

function stageOf(text) {
  const t = text.toLowerCase();
  if (/\bpreview\b/.test(t)) return "Preview";
  if (/\bga\b|general availability|generally available/.test(t)) return "GA";
  if (/retir|deprecat/.test(t)) return "Retiring";
  return "";
}

function clip(s, n) {
  if (s.length <= n) return s;
  const cut = s.slice(0, n);
  return cut.slice(0, cut.lastIndexOf(" ")).replace(/[,;:.\s-]+$/, "") + "…";
}

// Split the article into month sections: [{ month, id, html }]
function sections(html) {
  const out = [];
  const re = /<h2[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h2>/gi;
  const heads = [];
  let m;
  while ((m = re.exec(html))) heads.push({ id: m[1], text: m[2], start: m.index, end: re.lastIndex });
  heads.forEach((h, i) => {
    const mo = month(h.text);
    if (mo) out.push({ month: mo, id: h.id, html: html.slice(h.end, i + 1 < heads.length ? heads[i + 1].start : undefined) });
  });
  return out;
}

function parse(html, feed, perFeed) {
  const items = [];
  const push = (sec, title, anchor, stage) => {
    title = clip(title.replace(/\s*\((preview|ga)\)\s*$/i, ""), 110);
    if (title && items.length < perFeed)
      items.push({ title, link: feed.url + "#" + anchor, month: sec.month.label, key: sec.month.key, stage: stage || "", source: feed.source });
  };
  for (const sec of sections(html)) {
    if (items.length >= perFeed) break;
    const body = sec.html;
    if (feed.mode === "h3") {
      const re = /<h3[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h3>/gi; let m;
      while ((m = re.exec(body))) { const t = decode(m[2]); push(sec, t, m[1], stageOf(t)); }
    } else if (feed.mode === "li-strong") {
      const re = /<li>\s*(?:<p>)?\s*<strong>([\s\S]*?)<\/strong>([\s\S]{0,400})/gi; let m;
      while ((m = re.exec(body))) { const t = decode(m[1]); push(sec, t, sec.id, stageOf(t + " " + decode(m[2]))); }
    } else if (feed.mode === "table") {
      const re = /<tr>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>/gi; let m;
      while ((m = re.exec(body))) {
        const type = decode(m[1]);
        if (!/^feature/i.test(type)) continue; // skip per-platform build releases
        const st = decode(m[3]);
        push(sec, decode(m[2]), sec.id, /preview/i.test(st) ? "Preview" : /ga/i.test(st) ? "GA" : "");
      }
    } else if (feed.mode === "category") {
      const parts = body.split(/<h3[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h3>/i);
      // parts: [pre, id1, head1, chunk1, id2, head2, chunk2, ...]
      for (let i = 1; i < parts.length; i += 3) {
        const cat = decode(parts[i + 1]), chunk = parts[i + 2] || "";
        const re = /<li>\s*(?:<p>)?\s*<strong>([\s\S]*?)<\/strong>\s*:?\s*([\s\S]*?)<\/li>/gi; let m;
        while ((m = re.exec(chunk))) {
          const label = decode(m[1]);
          const text = decode(m[2]).replace(/^:\s*/, "");
          const first = (text.match(/^.*?[.!?](\s|$)/) || [text])[0].replace(/\s+$/, "");
          push(sec, cat + ": " + first.replace(/\.$/, ""), parts[i], stageOf(label));
        }
      }
    }
  }
  return items;
}

module.exports = { parse, sections, month, decode };
