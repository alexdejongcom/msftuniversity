/* Release notes "what's new" — Azure Function (SWA managed).
 *
 * GET /api/whatsnew → latest changes from the Microsoft Learn release-notes
 * pages for Microsoft 365 Copilot, Defender, Sentinel and Purview:
 *   [{ title, link, month, key, stage, source }] — 6-hour cache.
 * Data and caching live in ../lib/feeds.js (shared with the newsletter).
 */
const { app } = require("@azure/functions");
const { getWhatsNew } = require("../lib/feeds");

app.http("whatsnew", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const items = (await getWhatsNew((m) => context.warn(m)));
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=1800" },
        body: JSON.stringify(items),
      };
    } catch (err) {
      context.error("whatsnew failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "whatsnew unavailable" }) };
    }
  },
});
