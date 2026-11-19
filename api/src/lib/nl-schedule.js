/* The Redmond Report — fixed rhythm.
 *
 * Every other Thursday at 09:30 Amsterdam time ("slots"), counted from
 * NL_FIRST_SEND (a Thursday, YYYY-MM-DD; default 2026-11-26). The draft
 * reminder goes out on the Tuesday before a slot, from 08:00 Amsterdam time.
 * Handles CET/CEST without a timezone library.
 */
const TZ = "Europe/Amsterdam";
const DAY = 86400e3;
const SEND_H = 9, SEND_M = 30, REMIND_H = 8;

const anchor = () => (/^\d{4}-\d{2}-\d{2}$/.test(process.env.NL_FIRST_SEND || "") ? process.env.NL_FIRST_SEND : "2026-11-26");

// Offset of Amsterdam from UTC (minutes) at a given instant
function offsetMin(ts) {
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" })
    .formatToParts(new Date(ts)).map((x) => [x.type, x.value]));
  const asUtc = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute);
  return Math.round((asUtc - Math.floor(ts / 60e3) * 60e3) / 60e3);
}
// Wall-clock time in Amsterdam → UTC epoch ms
function amsterdam(dateStr, h, m) {
  const [y, mo, d] = dateStr.split("-").map(Number);
  const guess = Date.UTC(y, mo - 1, d, h, m);
  let ts = guess - offsetMin(guess) * 60e3;
  ts = guess - offsetMin(ts) * 60e3; // second pass settles DST edges
  return ts;
}
const addDays = (dateStr, n) => new Date(Date.parse(dateStr + "T00:00:00Z") + n * DAY).toISOString().slice(0, 10);

/* The first slot whose send time is after `after` (epoch ms). */
function nextSlot(after = Date.now()) {
  const a = anchor();
  let k = Math.max(0, Math.floor((after - Date.parse(a + "T00:00:00Z")) / (14 * DAY)) - 1);
  for (;; k++) {
    const date = addDays(a, 14 * k);
    const sendAt = amsterdam(date, SEND_H, SEND_M);
    if (sendAt > after) return { date, sendAt, remindAt: amsterdam(addDays(date, -2), REMIND_H, 0) };
  }
}

const MON = ["January","February","March","April","May","June","July","August","September","October","November","December"];
function label(slot) {
  const d = new Date(slot.date + "T12:00:00Z");
  return "Thursday " + d.getUTCDate() + " " + MON[d.getUTCMonth()] + ", 09:30";
}

module.exports = { nextSlot, label, amsterdam, offsetMin };
