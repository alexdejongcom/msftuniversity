/* Course evaluation — Azure Function (SWA managed) + Azure Table Storage.
 *
 * POST /api/evaluation → stores one anonymous course evaluation:
 *   ratings (1–5) for content, instructor and overall, a pace choice
 *   (slow / right / fast) and an optional free-text comment.
 *
 * Reuses the COUNTER_STORAGE connection string (same storage account as the
 * visitor counter and certificate registry). Table "evaluations",
 * PartitionKey=<courseDate>, RowKey=<timestamp>-<random> — so the Storage
 * browser groups responses per course automatically.
 */
const { app } = require("@azure/functions");
const { TableClient } = require("@azure/data-tables");

const TABLE = "evaluations";
const PACES = ["slow", "right", "fast"];

function client() {
  const conn = process.env.COUNTER_STORAGE;
  if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
  return TableClient.fromConnectionString(conn, TABLE);
}

function rating(v) {
  const n = Math.round(Number(v));
  return n >= 1 && n <= 5 ? n : null;
}

app.http("evaluation", {
  methods: ["POST"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const body = await request.json().catch(() => ({}));

      const course = String(body.course || "").slice(0, 300);
      const courseDate = String(body.date || "").slice(0, 10);
      const content = rating(body.content);
      const instructor = rating(body.instructor);
      const overall = rating(body.overall);
      const pace = PACES.includes(body.pace) ? body.pace : null;
      const comment = String(body.comment || "").trim().slice(0, 2000);

      if (!/^\d{4}-\d{2}-\d{2}$/.test(courseDate) || !content || !instructor || !overall || !pace) {
        return json({ error: "invalid payload" }, 400);
      }

      const tc = client();
      await tc.createTable(); // no-op if it already exists

      const now = new Date();
      const rowKey =
        now.toISOString().replace(/[:.]/g, "-") +
        "-" + Math.random().toString(36).slice(2, 8);

      await tc.createEntity({
        partitionKey: courseDate,
        rowKey,
        course,
        courseDate,
        content,
        instructor,
        overall,
        pace,
        comment,
        submitted: now.toISOString(),
      });

      return json({ ok: true });
    } catch (err) {
      context.error("evaluation submit failed:", err.message);
      return json({ error: "evaluation unavailable" }, 500);
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
