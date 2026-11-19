/* Shared news sources for the Resources page widgets and the newsletter.
 *
 *   getWhatsNew() → Learn release notes (Copilot, Defender, Sentinel, Purview)
 *   getRoadmap()  → newest Microsoft 365 roadmap entries
 *   getBlogs()    → official Microsoft blog posts (RSS)
 *
 * Each keeps its own in-memory cache and serves stale data if a refresh
 * fails. They throw only when there is nothing at all to return.
 */
const { parse, summarize } = require("./learn-whatsnew");

function cached(ms, load) {
  let cache = { at: 0, items: null };
  return async function get(log) {
    if (cache.items && Date.now() - cache.at < ms) return cache.items;
    try {
      const items = await load();
      if (items.length) cache = { at: Date.now(), items };
    } catch (e) {
      if (!cache.items) throw e;
      if (log) log("refresh failed, serving cache: " + e.message);
    }
    if (!cache.items) throw new Error("source empty");
    return cache.items;
  };
}

async function fetchText(url, accept, ms = 10000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { "User-Agent": "msftuniversity.com news", Accept: accept } });
    if (!res.ok) throw new Error(url + " → http " + res.status);
    return await res.text();
  } finally {
    clearTimeout(t);
  }
}

/* ---------- Learn release notes ---------- */
const L = "https://learn.microsoft.com/en-us/";
const LEARN = [
  { source: "Microsoft 365 Copilot",   mode: "category-title", url: L + "microsoft-365/copilot/release-notes?tabs=all" },
  { source: "Defender for Office 365", mode: "li-strong", url: L + "defender-office-365/defender-for-office-365-whats-new" },
  { source: "Defender for Endpoint",   mode: "table",     url: L + "defender-endpoint/whats-new-in-microsoft-defender-endpoint" },
  { source: "Defender for Identity",   mode: "h3",        url: L + "defender-for-identity/whats-new" },
  { source: "Defender for Cloud Apps", mode: "h3",        url: L + "defender-cloud-apps/release-notes" },
  { source: "Defender for Cloud",      mode: "h3",        url: L + "azure/defender-for-cloud/release-notes" },
  { source: "Microsoft Sentinel",      mode: "h3",        url: L + "azure/sentinel/whats-new" },
  { source: "Microsoft Purview",       mode: "category",  url: L + "purview/whats-new" },
];
const PER_FEED = 6;

const getWhatsNew = cached(6 * 3600e3, async () => {
  const results = await Promise.allSettled(LEARN.map(async (f) => parse(await fetchText(f.url, "text/html"), f, PER_FEED)));
  // newest month first; within a month keep product order, then page order
  return results
    .flatMap((r, f) => (r.status === "fulfilled" ? r.value.map((it, i) => ({ ...it, _o: f * 100 + i })) : []))
    .sort((a, b) => (a.key === b.key ? a._o - b._o : a.key < b.key ? 1 : -1))
    .map(({ _o, ...it }) => it);
});

/* ---------- Microsoft 365 roadmap ---------- */
const ROADMAP_API = "https://www.microsoft.com/releasecommunications/api/v2/m365?top=200&skip=0&orderby=created%20desc";
// Dynamics 365 and Power Platform items are left out — not what we teach.
const SKIP = /^(Dynamics 365|Power (Apps|Automate|Pages|BI)|Microsoft Power Platform|Microsoft Contact Center|Microsoft Sustainability)/i;

function cleanTitle(title, products) {
  let t = String(title || "").replace(/\s+/g, " ").trim();
  for (const p of products) {
    if (t.toLowerCase().startsWith(p.toLowerCase() + ":")) { t = t.slice(p.length + 1).trim(); break; }
  }
  t = t.charAt(0).toUpperCase() + t.slice(1);
  return t.length > 120 ? t.slice(0, 117).replace(/\s+\S*$/, "") + "…" : t;
}

const getRoadmap = cached(3 * 3600e3, async () => {
  const data = JSON.parse(await fetchText(ROADMAP_API, "application/json"));
  return (data.value || [])
    .filter((x) => x && x.id && x.title && Array.isArray(x.products) && x.products.length && !x.products.every((p) => SKIP.test(p)))
    .slice(0, 40)
    .map((x) => ({
      id: x.id,
      title: cleanTitle(x.title, x.products),
      product: x.products.filter((p) => !SKIP.test(p))[0],
      status: x.status || "",
      ga: /^\d{4}-\d{2}$/.test(x.generalAvailabilityDate || "") ? x.generalAvailabilityDate : "",
      link: "https://www.microsoft.com/microsoft-365/roadmap?id=" + encodeURIComponent(x.id),
      added: x.created,
      // roadmap descriptions often open with an "Overview" heading paragraph
      summary: summarize(String(x.description || "").replace(/<p>\s*(Overview|What's New|Summary)\s*<\/p>/gi, " ").replace(/<\/p>/gi, " </p>")),
    }));
});

/* ---------- Official Microsoft blogs (RSS) ---------- */
const BLOGS = [
  { url: "https://blogs.microsoft.com/feed/",                        source: "Official Microsoft Blog" },
  { url: "https://www.microsoft.com/en-us/microsoft-365/blog/feed/", source: "Microsoft 365" },
  { url: "https://azure.microsoft.com/en-us/blog/feed/",             source: "Azure" },
];

function rssText(xml, tag) {
  const m = xml.match(new RegExp("<" + tag + "[^>]*>([\\s\\S]*?)</" + tag + ">", "i"));
  if (!m) return "";
  return m[1]
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)))
    .replace(/&(quot|#8221|#8220);/g, '"').replace(/&(apos|#8217|#8216);/g, "'")
    .replace(/&nbsp;/g, " ")
    .trim();
}

function parseRss(xml, source, max) {
  const items = [];
  const re = /<item[\s>][\s\S]*?<\/item>/gi;
  let m;
  while ((m = re.exec(xml)) && items.length < max) {
    const it = m[0];
    const title = rssText(it, "title");
    const link = rssText(it, "link");
    const date = new Date(rssText(it, "pubDate"));
    const desc = rssText(it, "description").replace(/The post .* appeared first on .*$/i, "").replace(/\[(…|\.\.\.|&#8230;)\]\s*$/, "…");
    if (title && /^https:\/\//.test(link) && !isNaN(date)) items.push({ title, link, date: date.toISOString(), source, summary: summarize(desc) });
  }
  return items;
}

const getBlogs = cached(15 * 60e3, async () => {
  const results = await Promise.allSettled(BLOGS.map(async (f) => parseRss(await fetchText(f.url, "application/rss+xml, application/xml", 8000), f.source, 12)));
  return results
    .flatMap((r) => (r.status === "fulfilled" ? r.value : []))
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .slice(0, 24);
});

module.exports = { getWhatsNew, getRoadmap, getBlogs };
