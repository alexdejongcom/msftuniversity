/* Microsoft 365 roadmap — Azure Function (SWA managed).
 *
 * GET /api/roadmap → the most recently added Microsoft 365 roadmap items as
 * JSON: [{ id, title, product, status, ga, link, added }]
 * Source: the public JSON API behind microsoft.com/microsoft-365/roadmap.
 * Dynamics 365 and Power Platform items are left out — they're not what we
 * teach. Cached in memory for 3 hours.
 */
const { app } = require("@azure/functions");

const API = "https://www.microsoft.com/releasecommunications/api/v2/m365?top=200&skip=0&orderby=created%20desc";
const SKIP = /^(Dynamics 365|Power (Apps|Automate|Pages|BI)|Microsoft Power Platform|Microsoft Contact Center|Microsoft Sustainability)/i;
const MAX_ITEMS = 40;
const CACHE_MS = 3 * 60 * 60 * 1000;

let cache = { at: 0, items: null };

function clean(title, products) {
  let t = String(title || "").replace(/\s+/g, " ").trim();
  for (const p of products) {
    if (t.toLowerCase().startsWith(p.toLowerCase() + ":")) { t = t.slice(p.length + 1).trim(); break; }
  }
  t = t.charAt(0).toUpperCase() + t.slice(1);
  return t.length > 120 ? t.slice(0, 117).replace(/\s+\S*$/, "") + "…" : t;
}

async function load() {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 10000);
  try {
    const res = await fetch(API, { signal: ctrl.signal, headers: { "User-Agent": "msftuniversity.com roadmap widget", Accept: "application/json" } });
    if (!res.ok) throw new Error("roadmap http " + res.status);
    const data = await res.json();
    return (data.value || [])
      .filter((x) => x && x.id && x.title && Array.isArray(x.products) && x.products.length && !x.products.every((p) => SKIP.test(p)))
      .slice(0, MAX_ITEMS)
      .map((x) => {
        const products = x.products.filter((p) => !SKIP.test(p));
        return {
          id: x.id,
          title: clean(x.title, x.products),
          product: products[0],
          status: x.status || "",
          ga: /^\d{4}-\d{2}$/.test(x.generalAvailabilityDate || "") ? x.generalAvailabilityDate : "",
          link: "https://www.microsoft.com/microsoft-365/roadmap?id=" + encodeURIComponent(x.id),
          added: x.created,
        };
      });
  } finally {
    clearTimeout(timer);
  }
}

app.http("roadmap", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      if (!cache.items || Date.now() - cache.at > CACHE_MS) {
        try {
          const items = await load();
          if (items.length) cache = { at: Date.now(), items };
        } catch (e) {
          if (!cache.items) throw e; // serve stale data if we have it
          context.warn("roadmap refresh failed, serving cache:", e.message);
        }
        if (!cache.items) throw new Error("roadmap empty");
      }
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=1800" },
        body: JSON.stringify(cache.items),
      };
    } catch (err) {
      context.error("roadmap failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "roadmap unavailable" }) };
    }
  },
});
