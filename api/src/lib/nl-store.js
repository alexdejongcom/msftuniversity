/* Newsletter storage — Azure Table Storage (reuses COUNTER_STORAGE).
 *
 * One table, "newsletter", several partitions:
 *   sub        RowKey = first 32 hex of sha256(lower-case email)
 *              { email, status: pending|active, secret, createdAt, confirmedAt, lastMailAt }
 *              Unsubscribing DELETES the row — we keep nothing about people
 *              who left. Unconfirmed sign-ups are purged after 7 days.
 *   issue      RowKey = issue id (ms timestamp)
 *              { status: draft|sending|sent, subject, intro, outro, items(JSON),
 *                events(JSON), createdAt, updatedAt, sentAt, total, sent, failed }
 *   q-<issue>  RowKey = sub RowKey — the send queue for one issue
 *              { email, status: queued|sent|failed, error }
 *   meta       "rate"   rolling send counters (ACS rate limits)
 *              "remind" which cycle the admin was last reminded about
 */
const crypto = require("crypto");
const { TableClient, TableTransaction } = require("@azure/data-tables");

const TABLE = "newsletter";
let _client = null, _created = false;

async function table() {
  if (!_client) {
    const conn = process.env.COUNTER_STORAGE;
    if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
    _client = TableClient.fromConnectionString(conn, TABLE);
  }
  if (!_created) { await _client.createTable(); _created = true; }
  return _client;
}
function _setClient(c) { _client = c; _created = true; } // tests

async function get(pk, rk) {
  try { return await (await table()).getEntity(pk, rk); }
  catch (e) { if (e.statusCode === 404) return null; throw e; }
}
async function upsert(entity) { return (await table()).upsertEntity(entity, "Replace"); }
async function merge(entity) { return (await table()).updateEntity(entity, "Merge"); }
async function remove(pk, rk) {
  try { await (await table()).deleteEntity(pk, rk); }
  catch (e) { if (e.statusCode !== 404) throw e; }
}
async function list(filter, select, max = 5000) {
  const out = [];
  const iter = (await table()).listEntities({ queryOptions: { filter, select } });
  for await (const e of iter) { out.push(e); if (out.length >= max) break; }
  return out;
}
async function batchInsert(pk, rows) {
  const t = await table();
  for (let i = 0; i < rows.length; i += 100) {
    const tx = new TableTransaction();
    rows.slice(i, i + 100).forEach((r) => tx.upsertEntity({ partitionKey: pk, ...r }, "Replace"));
    await t.submitTransaction(tx.actions);
  }
}

const subKey = (email) => crypto.createHash("sha256").update(email.trim().toLowerCase()).digest("hex").slice(0, 32);
const newSecret = () => crypto.randomBytes(16).toString("hex");
const tokenOf = (sub) => sub.rowKey + "." + sub.secret;

async function subByToken(token) {
  const m = /^([0-9a-f]{32})\.([0-9a-f]{32})$/.exec(String(token || ""));
  if (!m) return null;
  const sub = await get("sub", m[1]);
  if (!sub || !sub.secret) return null;
  const a = Buffer.from(sub.secret), b = Buffer.from(m[2]);
  return a.length === b.length && crypto.timingSafeEqual(a, b) ? sub : null;
}

const esc = (s) => String(s).replace(/'/g, "''"); // OData string literal

module.exports = { table, _setClient, get, upsert, merge, remove, list, batchInsert, subKey, newSecret, tokenOf, subByToken, esc };
