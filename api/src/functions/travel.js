/* Live travel feed — proxies Alex's PUBLIC Polarsteps profile so the
 * events globe can draw the real tour trail.
 *
 * GET /api/travel → { updated, trip, stats, lastSeen, trail }
 *
 * Notes:
 * - Uses the public web endpoint (no credentials); only data Alex has
 *   made public on his profile is available here anyway.
 * - Unofficial API: if Polarsteps changes it, this returns 503 and the
 *   site degrades gracefully (globe simply shows no trail).
 * - Response is cached in-memory for 30 minutes to be polite.
 */
const { app } = require("@azure/functions");

const USERNAME = "AlexDejong2345";
const SOURCE = "https://www.polarsteps.com/api/users/byusername/" + USERNAME;
const TTL_MS = 30 * 60 * 1000;
const MAX_TRAIL_POINTS = 300;

let cache = { at: 0, data: null };

app.http("travel", {
  methods: ["GET"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      if (cache.data && Date.now() - cache.at < TTL_MS) return json(cache.data);

      const r = await fetch(SOURCE, {
        headers: { "Polarsteps-API-Version": "60", "User-Agent": "msftuniversity.com tour globe" },
      });
      if (!r.ok) throw new Error("polarsteps returned " + r.status);
      const u = await r.json();

      const trips = Array.isArray(u.trips) ? u.trips : [];
      const trip =
        trips.filter((t) => !t.end_date).sort((a, b) => new Date(b.start_date) - new Date(a.start_date))[0] ||
        trips.sort((a, b) => new Date(b.start_date) - new Date(a.start_date))[0] ||
        null;

      const steps = ((trip && trip.steps) || [])
        .filter((s) => s.location && isFinite(s.location.lat) && isFinite(s.location.lon))
        .sort((a, b) => new Date(a.start_time) - new Date(b.start_time));

      // thin the trail to a sane number of points
      const stride = Math.max(1, Math.ceil(steps.length / MAX_TRAIL_POINTS));
      const trail = steps
        .filter((s, i) => i % stride === 0 || i === steps.length - 1)
        .map((s) => [Number(s.location.lon.toFixed(4)), Number(s.location.lat.toFixed(4))]);

      const last = steps[steps.length - 1] || null;
      const stats = u.stats || {};

      const data = {
        updated: new Date().toISOString(),
        trip: trip
          ? { name: String(trip.name || "").slice(0, 120), start: trip.start_date || null }
          : null,
        stats: {
          countries: Number(stats.country_count) || 0,
          km: Math.round(Number(stats.km_count) || 0),
          continents: Array.isArray(stats.continents) ? stats.continents.length : 0,
        },
        lastSeen: last
          ? {
              locality: String(last.location.locality || last.location.name || "").slice(0, 80),
              country: String(last.location.country || "").slice(0, 80),
              lat: Number(last.location.lat),
              lon: Number(last.location.lon),
              time: last.start_time || null,
            }
          : null,
        trail,
      };

      cache = { at: Date.now(), data };
      return json(data);
    } catch (err) {
      context.error("travel feed failed:", err.message);
      if (cache.data) return json(cache.data); // stale is better than nothing
      return json({ error: "travel feed unavailable" }, 503);
    }
  },
});

function json(body, status) {
  return {
    status: status || 200,
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=900" },
    body: JSON.stringify(body),
  };
}
