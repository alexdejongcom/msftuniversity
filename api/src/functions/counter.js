/* Visitor counter — Azure Function (SWA managed) + Azure Table Storage.
 *
 * GET  /api/counter  → returns the current count (no increment)
 * POST /api/counter  → increments and returns the new count
 *
 * Requires app setting COUNTER_STORAGE = storage account connection string.
 * Uses table "counters", entity PartitionKey="site" / RowKey="visits".
 * Optimistic concurrency with ETag retry, so concurrent visitors don't
 * lose counts. Total cost: roughly one coffee per decade.
 */
const { app } = require("@azure/functions");
const { TableClient } = require("@azure/data-tables");

const TABLE = "counters";
const PK = "site";
const RK = "visits";

function client() {
  const conn = process.env.COUNTER_STORAGE;
  if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
  return TableClient.fromConnectionString(conn, TABLE);
}

async function getEntity(tc) {
  try {
    return await tc.getEntity(PK, RK);
  } catch (err) {
    if (err.statusCode === 404) return null;
    throw err;
  }
}

app.http("counter", {
  methods: ["GET", "POST"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const tc = client();
      await tc.createTable(); // no-op if it already exists

      if (request.method === "GET") {
        const e = await getEntity(tc);
        return json({ count: e ? Number(e.count) : 0 });
      }

      // POST → increment with ETag retry (max 5 attempts)
      for (let attempt = 0; attempt < 5; attempt++) {
        const e = await getEntity(tc);
        try {
          if (!e) {
            await tc.createEntity({ partitionKey: PK, rowKey: RK, count: 1 });
            return json({ count: 1 });
          }
          const next = Number(e.count) + 1;
          await tc.updateEntity(
            { partitionKey: PK, rowKey: RK, count: next },
            "Replace",
            { etag: e.etag }
          );
          return json({ count: next });
        } catch (err) {
          // 412 = someone else incremented first, 409 = create race — retry
          if (err.statusCode !== 412 && err.statusCode !== 409) throw err;
        }
      }
      return json({ error: "too much traffic, nice problem to have" }, 503);
    } catch (err) {
      context.error("counter failed:", err.message);
      return json({ error: "counter unavailable" }, 500);
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
