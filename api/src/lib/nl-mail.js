/* Newsletter mail — Azure Communication Services Email + rate limiting.
 *
 * App settings:
 *   ACS_CONNECTION_STRING  Communication Services resource connection string
 *   NL_FROM                sender, e.g. newsletter@msftuniversity.com
 *   NL_RATE_MINUTE / NL_RATE_HOUR  send limits (default 30 / 100 — the ACS
 *                          defaults for a custom domain; raise both after
 *                          Microsoft approves a quota increase)
 */
const store = require("./nl-store");

let _client = null;
function client() {
  if (_client) return _client;
  const conn = process.env.ACS_CONNECTION_STRING;
  if (!conn) throw new Error("ACS_CONNECTION_STRING app setting is not configured");
  const { EmailClient } = require("@azure/communication-email");
  _client = new EmailClient(conn);
  return _client;
}
function _setClient(c) { _client = c; } // tests

const LIMIT_MIN = () => +process.env.NL_RATE_MINUTE || 30;
const LIMIT_HOUR = () => +process.env.NL_RATE_HOUR || 100;

/* How many mails may we send right now? Fixed windows, stored in meta/rate. */
async function budget() {
  const now = Date.now();
  const r = (await store.get("meta", "rate")) || { minStart: 0, minCount: 0, hourStart: 0, hourCount: 0 };
  const minCount = now - r.minStart < 60e3 ? r.minCount : 0;
  const hourCount = now - r.hourStart < 3600e3 ? r.hourCount : 0;
  return {
    left: Math.max(0, Math.min(LIMIT_MIN() - minCount, LIMIT_HOUR() - hourCount)),
    waitSeconds: hourCount >= LIMIT_HOUR() ? Math.ceil((r.hourStart + 3600e3 - now) / 1000) : minCount >= LIMIT_MIN() ? Math.ceil((r.minStart + 60e3 - now) / 1000) : 0,
  };
}
async function record(n) {
  if (!n) return;
  const now = Date.now();
  const r = (await store.get("meta", "rate")) || { minStart: 0, minCount: 0, hourStart: 0, hourCount: 0 };
  const fresh = (start, ms) => now - start >= ms;
  await store.upsert({
    partitionKey: "meta", rowKey: "rate",
    minStart: fresh(r.minStart, 60e3) ? now : r.minStart,
    minCount: (fresh(r.minStart, 60e3) ? 0 : r.minCount) + n,
    hourStart: fresh(r.hourStart, 3600e3) ? now : r.hourStart,
    hourCount: (fresh(r.hourStart, 3600e3) ? 0 : r.hourCount) + n,
  });
}

/* Send one message. Doesn't wait for delivery — ACS accepts and queues it. */
async function send({ to, subject, html, text, unsubscribeUrl }) {
  const from = process.env.NL_FROM;
  if (!from) throw new Error("NL_FROM app setting is not configured");
  const message = {
    senderAddress: from,
    content: { subject, html, plainText: text },
    recipients: { to: [{ address: to }] },
    disableUserEngagementTracking: true, // no tracking pixels, no rewritten links
  };
  if (unsubscribeUrl) {
    message.headers = { "List-Unsubscribe": "<" + unsubscribeUrl + ">", "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" };
  }
  try {
    await client().beginSend(message);
  } catch (e) {
    // If the service ever rejects the custom headers, send without them
    // rather than not at all — the footer link still works.
    if (message.headers && e.statusCode === 400 && /header/i.test(e.message || "")) {
      delete message.headers;
      await client().beginSend(message);
    } else throw e;
  }
}

module.exports = { send, budget, record, _setClient };
