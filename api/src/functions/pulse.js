/* Class pace pulse — Azure Function (SWA managed) + Azure Table Storage.
 *
 * POST /api/pulse  body {vote:"slow"|"good"|"fast"} → registers a vote,
 *                  returns today's counts.
 * GET  /api/pulse  → returns today's counts.
 *
 * Reuses the COUNTER_STORAGE connection string. Table "pulse",
 * PartitionKey="pulse", RowKey=<YYYY-MM-DD> — one row per day, so history
 * is kept per course day. ETag retry for concurrent votes.
 */
const { app } = require("@azure/functions");
const { TableClient } = require("@azure/data-tables");

const TABLE = "pulse";
const PK = "pulse";
const VOTES = ["slow", "good", "fast"];

function client() {
  const conn = process.env.COUNTER_STORAGE;
  if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
  return TableClient.fromConnectionString(conn, TABLE);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

async function getEntity(tc, rk) {
  try {
    return await tc.getEntity(PK, rk);
  } catch (err) {
    if (err.statusCode === 404) return null;
    throw err;
  }
}

function counts(e, date) {
  return {
    date,
    slow: e ? Number(e.slow || 0) : 0,
    good: e ? Number(e.good || 0) : 0,
    fast: e ? Number(e.fast || 0) : 0,
  };
}

app.http("pulse", {
  methods: ["GET", "POST"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const tc = client();
      await tc.createTable();
      const rk = today();

      if (request.method === "GET") {
        return json(counts(await getEntity(tc, rk), rk));
      }

      const body = await request.json().catch(() => ({}));
      const vote = String(body.vote || "");
      if (VOTES.indexOf(vote) === -1) return json({ error: "invalid vote" }, 400);

      for (let attempt = 0; attempt < 5; attempt++) {
        const e = await getEntity(tc, rk);
        const next = counts(e, rk);
        next[vote] += 1;
        try {
          if (!e) {
            await tc.createEntity({ partitionKey: PK, rowKey: rk, slow: next.slow, good: next.good, fast: next.fast });
          } else {
            await tc.updateEntity(
              { partitionKey: PK, rowKey: rk, slow: next.slow, good: next.good, fast: next.fast },
              "Replace",
              { etag: e.etag }
            );
          }
          return json(next);
        } catch (err) {
          if (err.statusCode !== 412 && err.statusCode !== 409) throw err;
        }
      }
      return json({ error: "vote storm — try again" }, 503);
    } catch (err) {
      context.error("pulse failed:", err.message);
      return json({ error: "pulse unavailable" }, 500);
    }
  },
});

function json(body, status) {
  return {
    status: status || 200,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
    body: JSON.stringify(body),
  };
}
