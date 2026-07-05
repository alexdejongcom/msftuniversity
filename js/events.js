/* ============================================================
   UPCOMING EVENTS — the "tour dates"
   ============================================================
   To add an event, copy a block and fill it in. That's all.
   The page sorts by date automatically and hides events
   whose start date has passed.

   Fields:
     date     "YYYY-MM-DD"  first day (required)
     end      "YYYY-MM-DD"  last day (optional, for multi-day courses)
     title    course/keynote name
     type     "Training" | "Keynote" | "Workshop" | "Conference"
     city     "City, Country" or "Online"
     venue    training partner or event name (optional)
     url      booking link (omit or "" = no button)
     soldout  true = show SOLD OUT instead of the button
   ============================================================ */

const EVENTS = [
  {
    date: "2026-07-10",
    title: "DSD Cloud Academy",
    type: "Training",
    city: "Online",
    soldout: true,
  },
  {
    date: "2026-07-14",
    title: "Microsoft 365 E7 Event",
    type: "Event",
    city: "London, UK",
    venue: "Ingram Micro",
    soldout: true,
  },
  {
    date: "2026-08-04", end: "2026-08-05",
    title: "TechMentor & Cybersecurity Live! @ Microsoft HQ",
    type: "Conference",
    city: "Redmond, WA, USA",
    venue: "Microsoft Headquarters",
    url: "https://techmentorevents.com/re2026reg",
  },
  {
    date: "2026-08-10",
    title: "Getting Started with Copilot Studio (PL-7008 / MS-4009)",
    type: "Training",
    city: "Oslo, NO",
    venue: "Glasspaper",
    url: "https://www.glasspaper.no/kurs/kom-i-gang-med-copilot-studio/orderform?dId=12973435",
  },
  {
    date: "2026-08-24", end: "2026-08-28",
    title: "Security Course (internal)",
    type: "Training",
    city: "Gjøvik, NO",
    soldout: true,
  },
  {
    date: "2026-08-31", end: "2026-09-04",
    title: "Microsoft University (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-07", end: "2026-09-11",
    title: "Microsoft University (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-14", end: "2026-09-18",
    title: "Microsoft University (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-21",
    title: "Mastering Microsoft Device Management",
    type: "Training",
    city: "Oslo, NO",
    venue: "Glasspaper",
    url: "https://www.glasspaper.no/kurs/mastering-microsoft-device-management/orderform?dId=12976592",
  },
  {
    date: "2026-09-30", end: "2026-10-02",
    title: "DSD Cloud University — Copilot and Agents",
    type: "Training",
    city: "Rosmalen, NL",
    venue: "DSD Europe",
  },
  {
    date: "2026-10-13", end: "2026-10-15",
    title: "NIC 2026 — Nordic Infrastructure Conference",
    type: "Conference",
    city: "Oslo, NO",
    venue: "Oslo Spektrum",
    url: "https://nicconf.com/tickets",
  },
  {
    date: "2026-10-20", end: "2026-10-22",
    title: "In-company Training (internal)",
    type: "Training",
    city: "Eindhoven, NL",
    venue: "Ictivity",
    soldout: true,
  },
  {
    date: "2026-11-15", end: "2026-11-20",
    title: "Live! 360 Tech Con 2026",
    type: "Conference",
    city: "Orlando, FL, USA",
    venue: "Royal Pacific Resort — Universal Orlando",
    url: "https://na.eventscloud.com/ereg/newreg.php?eventid=838133",
  },
];
