/* Microsoft news feed — Azure Function (SWA managed).
 *
 * GET /api/news → latest posts from official Microsoft blogs, merged and
 * sorted, as JSON: [{ title, link, date, source }].
 *
 * The browser can't read these RSS feeds directly (CORS), so this function
 * proxies them server-side. Responses are cached in memory for 15 minutes,
 * so warm instances hit Microsoft at most 4×/hour regardless of traffic.
 * No storage, no keys — nothing to configure.
 */
const { app } = require("@azure/functions");

const FEEDS = [
  { url: "https://blogs.microsoft.com/feed/",                        source: "Official Microsoft Blog" },
  { url: "https://www.microsoft.com/en-us/microsoft-365/blog/feed/", source: "Microsoft 365" },
  { url: "https://azure.microsoft.com/en-us/blog/feed/",             source: "Azure" },
];
const MAX_ITEMS = 12;
const CACHE_MS = 15 * 60 * 1000;

let cache = { at: 0, items: null };

function text(xml, tag) {
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

function parse(xml, source) {
  const items = [];
  const re = /<item[\s>][\s\S]*?<\/item>/gi;
  let m;
  while ((m = re.exec(xml)) && items.length < MAX_ITEMS) {
    const it = m[0];
    const title = text(it, "title");
    const link = text(it, "link");
    const date = new Date(text(it, "pubDate"));
    if (title && /^https:\/\//.test(link) && !isNaN(date)) {
      items.push({ title, link, date: date.toISOString(), source });
    }
  }
  return items;
}

async function fetchFeed(feed) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 8000);
  try {
    const res = await fetch(feed.url, {
      signal: ctrl.signal,
      headers: { "User-Agent": "msftuniversity.com news widget", Accept: "application/rss+xml, application/xml" },
    });
    if (!res.ok) return [];
    return parse(await res.text(), feed.source);
  } finally {
    clearTimeout(t);
  }
}

app.http("news", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      if (!cache.items || Date.now() - cache.at > CACHE_MS) {
        const results = await Promise.allSettled(FEEDS.map(fetchFeed));
        const items = results
          .flatMap((r) => (r.status === "fulfilled" ? r.value : []))
          .sort((a, b) => (a.date < b.date ? 1 : -1))
          .slice(0, MAX_ITEMS);
        if (items.length) cache = { at: Date.now(), items };
        else if (!cache.items) throw new Error("no feeds reachable");
      }
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=300" },
        body: JSON.stringify(cache.items),
      };
    } catch (err) {
      context.error("news feed failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "news unavailable" }) };
    }
  },
});
