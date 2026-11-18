/* Microsoft news feed — Azure Function (SWA managed).
 *
 * GET /api/news → latest posts from the official Microsoft blogs, merged and
 * sorted, as JSON: [{ title, link, date, source }]. RSS proxied server-side
 * (CORS), 15-minute cache.
 * Data and caching live in ../lib/feeds.js (shared with the newsletter).
 */
const { app } = require("@azure/functions");
const { getBlogs } = require("../lib/feeds");

app.http("news", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const items = (await getBlogs((m) => context.warn(m))).slice(0, 12);
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=300" },
        body: JSON.stringify(items),
      };
    } catch (err) {
      context.error("news failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "news unavailable" }) };
    }
  },
});
