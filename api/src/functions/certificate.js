/* Certificate registry — Azure Function (SWA managed) + Azure Table Storage.
 *
 * POST /api/certificate  → records that a certificate of attendance was
 *                          generated (name, course, certificate ID).
 * GET  /api/certificate?code=MU-...  → verifies a certificate ID and returns
 *                          the course + issue date (name is NOT returned).
 *
 * Reuses the COUNTER_STORAGE connection string (same storage account as the
 * visitor counter). Table "certificates", PartitionKey="cert", RowKey=<code>.
 * Regenerating the same name+course upserts the same row and bumps `count`,
 * so the table stays one-row-per-certificate.
 */
const { app } = require("@azure/functions");
const { TableClient } = require("@azure/data-tables");

const TABLE = "certificates";
const PK = "cert";
const CODE_RE = /^MU-\d{8}-[0-9A-F]{8}$/;

function client() {
  const conn = process.env.COUNTER_STORAGE;
  if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
  return TableClient.fromConnectionString(conn, TABLE);
}

app.http("certificate", {
  methods: ["GET", "POST"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const tc = client();
      await tc.createTable(); // no-op if it already exists

      if (request.method === "GET") {
        const code = (new URL(request.url).searchParams.get("code") || "").trim().toUpperCase();
        if (!CODE_RE.test(code)) return json({ valid: false, error: "malformed code" }, 400);
        try {
          const e = await tc.getEntity(PK, code);
          return json({
            valid: true,
            course: e.course,
            courseDate: e.courseDate,
            firstIssued: e.firstIssued,
          });
        } catch (err) {
          if (err.statusCode === 404) return json({ valid: false });
          throw err;
        }
      }

      // POST → register a generated certificate
      const body = await request.json().catch(() => ({}));
      const name = String(body.name || "").trim().slice(0, 200);
      const code = String(body.code || "").trim().toUpperCase();
      const course = String(body.course || "").slice(0, 300);
      const courseDate = String(body.date || "").slice(0, 10);
      if (!name || !CODE_RE.test(code)) return json({ error: "invalid payload" }, 400);

      const now = new Date().toISOString();
      let count = 1, firstIssued = now;
      try {
        const e = await tc.getEntity(PK, code);
        count = Number(e.count || 0) + 1;
        firstIssued = e.firstIssued || now;
      } catch (err) {
        if (err.statusCode !== 404) throw err;
      }
      await tc.upsertEntity(
        { partitionKey: PK, rowKey: code, name, course, courseDate, firstIssued, lastIssued: now, count },
        "Replace"
      );
      return json({ ok: true });
    } catch (err) {
      context.error("certificate registry failed:", err.message);
      return json({ error: "registry unavailable" }, 500);
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
