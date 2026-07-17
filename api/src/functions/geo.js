/* Visitor geography — Azure Function (SWA managed) + Azure Table Storage.
 *
 * POST /api/geo {tz} → maps the browser's IANA timezone to a country and
 *                      increments that country's counter. No IP addresses,
 *                      no cookies, no per-visitor rows — one aggregate
 *                      count per country, nothing else. GDPR's easiest day.
 * GET  /api/geo      → [{ country: "NL", count: 42 }, ...] sorted desc.
 *
 * Reuses COUNTER_STORAGE. Table "geo", PartitionKey="geo", RowKey=<ISO2>.
 * ETag retry like the visitor counter, so concurrent visitors don't lose
 * counts.
 */
const { app } = require("@azure/functions");
const { TableClient } = require("@azure/data-tables");

const TABLE = "geo";
const PK = "geo";

/* IANA timezone → ISO 3166-1 alpha-2. Major zones; unknown zones are
 * simply not counted (shown as nothing rather than guessed wrong). */
const TZ = {
  "Europe/Amsterdam":"NL","Europe/Brussels":"BE","Europe/Luxembourg":"LU","Europe/Paris":"FR",
  "Europe/Berlin":"DE","Europe/Busingen":"DE","Europe/Zurich":"CH","Europe/Vienna":"AT",
  "Europe/London":"GB","Europe/Dublin":"IE","Europe/Lisbon":"PT","Europe/Madrid":"ES",
  "Europe/Rome":"IT","Europe/Vatican":"VA","Europe/Malta":"MT","Europe/Monaco":"MC",
  "Europe/Oslo":"NO","Europe/Stockholm":"SE","Europe/Copenhagen":"DK","Europe/Helsinki":"FI",
  "Europe/Reykjavik":"IS","Europe/Tallinn":"EE","Europe/Riga":"LV","Europe/Vilnius":"LT",
  "Europe/Warsaw":"PL","Europe/Prague":"CZ","Europe/Bratislava":"SK","Europe/Budapest":"HU",
  "Europe/Ljubljana":"SI","Europe/Zagreb":"HR","Europe/Sarajevo":"BA","Europe/Belgrade":"RS",
  "Europe/Podgorica":"ME","Europe/Skopje":"MK","Europe/Tirane":"AL","Europe/Athens":"GR",
  "Europe/Sofia":"BG","Europe/Bucharest":"RO","Europe/Chisinau":"MD","Europe/Kyiv":"UA",
  "Europe/Kiev":"UA","Europe/Minsk":"BY","Europe/Moscow":"RU","Europe/Kaliningrad":"RU",
  "Europe/Samara":"RU","Europe/Volgograd":"RU","Europe/Istanbul":"TR","Europe/Andorra":"AD",
  "Europe/Gibraltar":"GI","Europe/Guernsey":"GG","Europe/Jersey":"JE","Europe/Isle_of_Man":"IM",
  "Atlantic/Reykjavik":"IS","Atlantic/Azores":"PT","Atlantic/Madeira":"PT","Atlantic/Canary":"ES",
  "Atlantic/Faroe":"FO","Atlantic/Bermuda":"BM","Atlantic/Cape_Verde":"CV",
  "America/New_York":"US","America/Detroit":"US","America/Chicago":"US","America/Denver":"US",
  "America/Phoenix":"US","America/Los_Angeles":"US","America/Anchorage":"US","America/Adak":"US",
  "America/Boise":"US","America/Indiana/Indianapolis":"US","America/Indianapolis":"US",
  "America/Kentucky/Louisville":"US","America/Juneau":"US","Pacific/Honolulu":"US",
  "America/Toronto":"CA","America/Vancouver":"CA","America/Edmonton":"CA","America/Winnipeg":"CA",
  "America/Halifax":"CA","America/St_Johns":"CA","America/Regina":"CA","America/Montreal":"CA",
  "America/Mexico_City":"MX","America/Tijuana":"MX","America/Monterrey":"MX","America/Cancun":"MX",
  "America/Guatemala":"GT","America/Belize":"BZ","America/El_Salvador":"SV","America/Tegucigalpa":"HN",
  "America/Managua":"NI","America/Costa_Rica":"CR","America/Panama":"PA","America/Havana":"CU",
  "America/Jamaica":"JM","America/Port-au-Prince":"HT","America/Santo_Domingo":"DO",
  "America/Puerto_Rico":"PR","America/Barbados":"BB","America/Trinidad":"TT","America/Curacao":"CW",
  "America/Aruba":"AW","America/Bogota":"CO","America/Caracas":"VE","America/Guyana":"GY",
  "America/Paramaribo":"SR","America/Lima":"PE","America/Guayaquil":"EC","America/La_Paz":"BO",
  "America/Asuncion":"PY","America/Montevideo":"UY","America/Santiago":"CL",
  "America/Argentina/Buenos_Aires":"AR","America/Buenos_Aires":"AR","America/Cordoba":"AR",
  "America/Sao_Paulo":"BR","America/Rio_Branco":"BR","America/Manaus":"BR","America/Fortaleza":"BR",
  "America/Recife":"BR","America/Bahia":"BR","America/Belem":"BR","America/Cuiaba":"BR",
  "Africa/Cairo":"EG","Africa/Tripoli":"LY","Africa/Tunis":"TN","Africa/Algiers":"DZ",
  "Africa/Casablanca":"MA","Africa/Lagos":"NG","Africa/Accra":"GH","Africa/Abidjan":"CI",
  "Africa/Dakar":"SN","Africa/Bamako":"ML","Africa/Nairobi":"KE","Africa/Kampala":"UG",
  "Africa/Dar_es_Salaam":"TZ","Africa/Addis_Ababa":"ET","Africa/Khartoum":"SD",
  "Africa/Kinshasa":"CD","Africa/Luanda":"AO","Africa/Douala":"CM","Africa/Johannesburg":"ZA",
  "Africa/Windhoek":"NA","Africa/Gaborone":"BW","Africa/Harare":"ZW","Africa/Lusaka":"ZM",
  "Africa/Maputo":"MZ","Indian/Mauritius":"MU","Indian/Antananarivo":"MG",
  "Asia/Jerusalem":"IL","Asia/Tel_Aviv":"IL","Asia/Beirut":"LB","Asia/Damascus":"SY",
  "Asia/Amman":"JO","Asia/Baghdad":"IQ","Asia/Kuwait":"KW","Asia/Riyadh":"SA","Asia/Bahrain":"BH",
  "Asia/Qatar":"QA","Asia/Dubai":"AE","Asia/Muscat":"OM","Asia/Aden":"YE","Asia/Tehran":"IR",
  "Asia/Baku":"AZ","Asia/Yerevan":"AM","Asia/Tbilisi":"GE","Asia/Kabul":"AF","Asia/Karachi":"PK",
  "Asia/Kolkata":"IN","Asia/Calcutta":"IN","Asia/Colombo":"LK","Asia/Dhaka":"BD",
  "Asia/Kathmandu":"NP","Asia/Thimphu":"BT","Asia/Yangon":"MM","Asia/Bangkok":"TH",
  "Asia/Vientiane":"LA","Asia/Phnom_Penh":"KH","Asia/Ho_Chi_Minh":"VN","Asia/Saigon":"VN",
  "Asia/Kuala_Lumpur":"MY","Asia/Singapore":"SG","Asia/Jakarta":"ID","Asia/Makassar":"ID",
  "Asia/Jayapura":"ID","Asia/Manila":"PH","Asia/Brunei":"BN","Asia/Hong_Kong":"HK",
  "Asia/Macau":"MO","Asia/Taipei":"TW","Asia/Shanghai":"CN","Asia/Chongqing":"CN",
  "Asia/Urumqi":"CN","Asia/Seoul":"KR","Asia/Pyongyang":"KP","Asia/Tokyo":"JP",
  "Asia/Ulaanbaatar":"MN","Asia/Almaty":"KZ","Asia/Tashkent":"UZ","Asia/Bishkek":"KG",
  "Asia/Dushanbe":"TJ","Asia/Ashgabat":"TM","Asia/Novosibirsk":"RU","Asia/Yekaterinburg":"RU",
  "Asia/Krasnoyarsk":"RU","Asia/Irkutsk":"RU","Asia/Vladivostok":"RU","Asia/Nicosia":"CY",
  "Australia/Sydney":"AU","Australia/Melbourne":"AU","Australia/Brisbane":"AU",
  "Australia/Perth":"AU","Australia/Adelaide":"AU","Australia/Darwin":"AU","Australia/Hobart":"AU",
  "Pacific/Auckland":"NZ","Pacific/Chatham":"NZ","Pacific/Fiji":"FJ","Pacific/Guam":"GU",
  "Pacific/Port_Moresby":"PG","Pacific/Noumea":"NC","Pacific/Tahiti":"PF","Pacific/Apia":"WS",
  "Pacific/Tongatapu":"TO",
};

function client() {
  const conn = process.env.COUNTER_STORAGE;
  if (!conn) throw new Error("COUNTER_STORAGE app setting is not configured");
  return TableClient.fromConnectionString(conn, TABLE);
}

app.http("geo", {
  methods: ["GET", "POST"],
  authLevel: "anonymous",
  handler: async (request, context) => {
    try {
      const tc = client();
      await tc.createTable(); // no-op if it already exists

      if (request.method === "GET") {
        const out = [];
        for await (const e of tc.listEntities()) {
          out.push({ country: e.rowKey, count: Number(e.count) || 0 });
        }
        out.sort((a, b) => b.count - a.count);
        return json(out);
      }

      // POST → count one visit for the timezone's country
      const body = await request.json().catch(() => ({}));
      const tz = String(body.tz || "").slice(0, 40);
      const country = TZ[tz];
      if (!country) return json({ ok: true, counted: false }); // unknown zone: not counted

      for (let attempt = 0; attempt < 5; attempt++) {
        let e = null;
        try {
          e = await tc.getEntity(PK, country);
        } catch (err) {
          if (err.statusCode !== 404) throw err;
        }
        try {
          if (!e) {
            await tc.createEntity({ partitionKey: PK, rowKey: country, count: 1 });
            return json({ ok: true, counted: true });
          }
          await tc.updateEntity(
            { partitionKey: PK, rowKey: country, count: Number(e.count) + 1 },
            "Replace",
            { etag: e.etag }
          );
          return json({ ok: true, counted: true });
        } catch (err) {
          if (err.statusCode !== 412 && err.statusCode !== 409) throw err; // race → retry
        }
      }
      return json({ ok: false }, 503);
    } catch (err) {
      context.error("geo failed:", err.message);
      return json({ error: "geo unavailable" }, 500);
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
