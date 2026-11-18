/* Microsoft 365 roadmap — Azure Function (SWA managed).
 *
 * GET /api/roadmap → newest Microsoft 365 roadmap entries (Dynamics 365 and
 * Power Platform left out): [{ id, title, product, status, ga, link, added }]
 * — 3-hour cache.
 * Data and caching live in ../lib/feeds.js (shared with the newsletter).
 */
const { app } = require("@azure/functions");
const { getRoadmap } = require("../lib/feeds");

app.http("roadmap", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const items = (await getRoadmap((m) => context.warn(m)));
      return {
        status: 200,
        headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=1800" },
        body: JSON.stringify(items),
      };
    } catch (err) {
      context.error("roadmap failed:", err.message);
      return { status: 503, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ error: "roadmap unavailable" }) };
    }
  },
});
