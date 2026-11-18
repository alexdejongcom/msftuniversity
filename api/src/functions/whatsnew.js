/* Security & compliance "what's new" — Azure Function (SWA managed).
 *
 * GET /api/whatsnew → latest changes from Microsoft Learn release-notes pages
 * for Defender, Sentinel and Purview, as JSON:
 *   [{ title, link, month, key, stage, source }]
 * Learn has no RSS for these pages, so the function reads the HTML server-side
 * and parses the month sections (see ../lib/learn-whatsnew.js). Cached in
 * memory for 6 hours: the pages change a few times a week at most.
 */
const { app } = require("@azure/functions");
const { parse } = require("../lib/learn-whatsnew");

const L = "https://learn.microsoft.com/en-us/";
const FEEDS = [
  { source: "Defender for Office 365", mode: "li-strong", url: L + "defender-office-365/defender-for-office-365-whats-new" },
  { source: "Defender for Endpoint",   mode: "table",     url: L + "defender-endpoint/whats-new-in-microsoft-defender-endpoint" },
  { source: "Defender for Identity",   mode: "h3",        url: L + "defender-for-identity/whats-new" },
  { source: "Defender for Cloud Apps", mode: "h3",        url: L + "defender-cloud-apps/release-notes" },
  { source: "Defender for Cloud",      mode: "h3",        url: L + "azure/defender-for-cloud/release-notes" },
  { source: "Microsoft Sentinel",      mode: "h3",        url: L + "azure/sentinel/whats-new" },
  { source: "Microsoft Purview",       mode: "category",  url: L + "purview/whats-new" },
];
const PER_FEED = 6;
const CACHE_MS = 6 * 60 * 60 * 1000;

let cache = { at: 0, items: null };

async function fetchFeed(feed) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 10000);
  try {
    const res = await fetch(feed.url, { signal: ctrl.signal, headers: { "User-Agent": "msftuniversity.com what's-new widget", Accept: "text/html" } });
    if (!res.ok) return [];
    return parse(await res.text(), feed, PER_FEED);
  } finally {
    clearTimeout(t);
  }
}

app.http("whatsnew", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      if (!cache.items || Date.now() - cache.at > CACHE_MS) {
        const results = await Promise.allSettled(FEEDS.map(fetchFeed));
        // newest month first; within a month keep product order, then page order
        const items = results
          .flatMap((r, f) => (r.status === "fulfilled" ? r.value.map((it, i) => ({ ...it, _o: f * 100 + i })) : []))
          .sort((a, b) => (a.key === b.key ? a._o - b._o : a.key < b.key ? 1 : -1))
          .map(({ _o, ...it }) => it);
        if (items.length) cache = { at: Date.now(), items };
        else if (!cache.items) throw new Error("no Learn pages reachable");
      }
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=1800" },
        body: JSON.stringify(cache.items),
      };
    } catch (err) {
      context.error("whatsnew failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "what's new unavailable" }) };
    }
  },
});
