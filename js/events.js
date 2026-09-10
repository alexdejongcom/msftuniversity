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

   See also DELIVERED at the bottom of this file: the archive of
   courses already given, kept at month precision.
   ============================================================ */

const EVENTS = [
  {
    date: "2026-07-10",
    title: "DSD Cloud Academy — Microsoft AI Security with Purview & Defender",
    type: "Webinar",
    city: "Online",
    venue: "DSD Europe",
    url: "https://dsdeurope.webinargeek.com/dsd-cloud-academy-microsoft-ai-security-met-purview-defender",
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
    date: "2026-07-15",
    title: "Enhance Endpoint Security with Intune & Security Copilot (MD-4011)",
    type: "Training",
    city: "Eindhoven, NL",
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
    date: "2026-08-11",
    title: "An Essential Guide to SMB Selling with Microsoft 365 & Copilot Business (internal)",
    type: "Webinar",
    city: "Online",
    venue: "Microsoft Partner Skilling",
    soldout: true,
  },
  {
    date: "2026-08-18",
    title: "Position Microsoft 365 E7 for Customers to Realize Frontier Firm Potential (internal)",
    type: "Webinar",
    city: "Online",
    venue: "Microsoft Partner Skilling",
    soldout: true,
  },
  {
    date: "2026-08-24", end: "2026-08-28",
    title: "Security Course (internal)",
    type: "Training",
    city: "Gjøvik, NO",
    soldout: true,
  },
  {
    date: "2026-08-25",
    title: "Accelerate Your AI Transformation with Microsoft 365 Copilot + Agents (internal)",
    type: "Webinar",
    city: "Online",
    venue: "Microsoft Partner Skilling",
    soldout: true,
  },
  {
    date: "2026-08-31", end: "2026-09-04",
    title: "Microsoft University, Azure Architect",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-07", end: "2026-09-11",
    title: "Microsoft University, Azure Architect",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-14", end: "2026-09-16",
    title: "Azure Infrastructure (internal)",
    type: "Training",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-15",
    title: "Copilot Week: Day 1 — Getting Started with Copilot",
    type: "Webinar",
    city: "Online",
    venue: "DSD Europe",
    url: "https://www.dsdeurope.nl/webinars/webinar-week-dag-1-slim-starten-met-copilot",
  },
  {
    date: "2026-09-16",
    title: "Copilot Week: Day 2 — Working More Productively with Copilot in Outlook, Teams & Word",
    type: "Webinar",
    city: "Online",
    venue: "DSD Europe",
    url: "https://www.dsdeurope.nl/webinars/copilot-week-dag-2-productiever-werken-met-copilot-in-outlook-teams-word",
  },
  {
    date: "2026-09-17",
    title: "Copilot Week: Day 3 — Insight and Decision-Making with Copilot in Excel & OneDrive",
    type: "Webinar",
    city: "Online",
    venue: "DSD Europe",
    url: "https://www.dsdeurope.nl/webinars/copilot-week-dag-3-inzicht-en-besluitvorming-met-copilot-in-excel-onedrive",
  },
  {
    date: "2026-09-18",
    title: "Copilot Week: Day 4 — Making Copilot Part of Your Working Day",
    type: "Webinar",
    city: "Online",
    venue: "DSD Europe",
    url: "https://www.dsdeurope.nl/webinars/copilot-week-dag-4-dagelijks-waarde-halen-uit-copilot",
  },
  {
    date: "2026-09-22",
    title: "Implement Agent 365 to Secure AI Apps, Copilot & Agents — Project Ready",
    type: "Workshop",
    city: "Athens, GR",
    venue: "Microsoft Office Athens",
    url: "https://www.skilling-hub.com/en-US/listing/implement-agent-365-secure-al-apps-copilot-agents::athens::pr",
  },
  {
    date: "2026-09-30", end: "2026-10-02",
    title: "DSD Cloud University — Microsoft 365 Copilot and Agents",
    type: "Training",
    city: "Rosmalen, NL",
    venue: "DSD Europe",
    url: "https://www.dsdeurope.nl/dsd-cloud-university-microsoft-365-copilot-agents",
  },
  {
    date: "2026-10-05",
    title: "Implement Agent 365 to Secure AI Apps, Copilot & Agents — Project Ready",
    type: "Workshop",
    city: "Zurich, CH",
    venue: "Microsoft Office Zurich — The Circle",
    url: "https://www.skilling-hub.com/en-US/listing/implement-agent-365-secure-al-apps-copilot-agents::zurich::pr",
  },
  {
    date: "2026-10-06",
    title: "Drive Agentic AI Conversations with Copilot Cowork & Copilot Studio — Project Ready",
    type: "Workshop",
    city: "Zurich, CH",
    venue: "Microsoft Office Zurich — The Circle",
    url: "https://www.skilling-hub.com/en-US/listing/drive-agentic-ai-conversations-m365-copilot-copilotstudio-zurich-pr",
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
    date: "2026-10-19", end: "2026-10-22",
    title: "Information Security Administrator (SC-401)",
    type: "Training",
    city: "Oslo, NO",
    venue: "Glasspaper",
    url: "https://www.glasspaper.no/kurs/sc-401-information-security-administrator/",
  },
  {
    date: "2026-10-26", end: "2026-10-29",
    title: "Microsoft Identity and Access Administrator (SC-300)",
    type: "Training",
    city: "Oslo, NO",
    venue: "Glasspaper",
    url: "https://www.glasspaper.no/kurs/sc-300-microsoft-identity-and-access-administrator/",
  },
  {
    date: "2026-10-30",
    title: "Implement Information Protection and Data Loss Prevention with Microsoft Purview (SC-5003)",
    type: "Training",
    city: "Online",
    venue: "Fast Lane",
    url: "https://www.flane.nl/addbooking?eventid=2194718",
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

/* ============================================================
   DELIVERED — the archive
   ============================================================
   Courses already given, kept at MONTH precision because that is
   how they were recorded. There is deliberately no `date` field:
   these must never surface as "upcoming" anywhere.

   Only the About page reads this list, for the "In the classroom"
   counters. The events page, the globe, the terminal and the
   certificate generator all ignore it.

   Fields:
     month  "YYYY-MM"  the month it ran (required)
     title  course name
     type   "Training" | "Event" | "Webinar" | "Workshop" | "Conference" | "Keynote"
     city   "City, Country" or "Online"
     venue  organiser (optional)

   If exact dates ever turn up, move an entry into EVENTS above
   with a real `date` (and `end`) and delete it from here.
   ============================================================ */

/* How long each course runs, for archive entries that have no dates.
   Anything not listed here counts as a single day.

   Matching order: a course code in the title decides it outright — if the
   code is not listed below, the course is one day and the name table is
   never consulted. Only titles with no code fall through to `names`.
   So "Getting Started with Copilot Studio (PL-7008)" is one day via its
   code, while the uncoded "Copilot Studio" course is three.

   Dated entries in EVENTS above ignore this entirely — they already know
   their own start and end. */
const COURSE_DAYS = {
  codes: {
    "SC-100": 4,
    "SC-200": 4,
    "SC-300": 4,
    "SC-401": 4,
    "AZ-104": 5,
    "AZ-140": 4,
    "AZ-305": 4,
  },
  names: {
    "device management masterclass": 3,
    "copilot studio": 3,
    "cloud university": 3,
    "ai transformation": 3,
  },
  default: 1,
};

const DELIVERED = [
  { month: "2026-01", title: "Getting Started with Copilot Studio (PL-7008)", type: "Training", city: "Bergen, NO" },
  { month: "2026-01", title: "Configuring and Operating Microsoft Azure Virtual Desktop (AZ-140)", type: "Training", city: "Online" },
  { month: "2026-01", title: "Microsoft 365 Endpoint Administrator (MD-102)", type: "Training", city: "Den Bosch, NL", venue: "DSD Europe" },

  { month: "2026-02", title: "Microsoft Device Management Masterclass", type: "Training", city: "Oslo, NO" },
  { month: "2026-02", title: "Microsoft 365 Fundamentals (MS-900)", type: "Training", city: "Bergen, NO" },
  { month: "2026-02", title: "Microsoft Cybersecurity Architect (SC-100)", type: "Training", city: "Lillehammer, NO" },
  { month: "2026-02", title: "Microsoft Device Management Masterclass", type: "Training", city: "Bergen, NO" },
  { month: "2026-02", title: "Microsoft Copilot", type: "Training", city: "Utrecht, NL", venue: "Ictivity" },
  { month: "2026-02", title: "DSD Cloud Academy", type: "Webinar", city: "Online", venue: "DSD Europe" },
  { month: "2026-02", title: "Microsoft Copilot", type: "Webinar", city: "Online", venue: "Microsoft" },
  { month: "2026-02", title: "DSD Cloud University", type: "Training", city: "Den Bosch, NL", venue: "DSD Europe" },
  { month: "2026-02", title: "MS-4007", type: "Training", city: "Nieuwegein, NL", venue: "Global Knowledge" },

  { month: "2026-03", title: "Microsoft CSP — Copilot", type: "Event", city: "Brussels, BE", venue: "Microsoft" },
  { month: "2026-03", title: "Agentic AI Roadshow", type: "Event", city: "Johannesburg, ZA", venue: "Microsoft" },
  { month: "2026-03", title: "Microsoft CSP — Agentic AI", type: "Event", city: "Brussels, BE", venue: "Microsoft" },
  { month: "2026-03", title: "Azure AI Fundamentals (AI-900)", type: "Training", city: "Oslo, NO" },
  { month: "2026-03", title: "Azure Fundamentals (AZ-900)", type: "Training", city: "Lillehammer, NO" },
  { month: "2026-03", title: "Microsoft Sentinel", type: "Training", city: "Zurich, CH" },
  { month: "2026-03", title: "Copilot Studio", type: "Training", city: "Utrecht, NL", venue: "Ictivity" },
  { month: "2026-03", title: "AI Transformation", type: "Training", city: "Online", venue: "Microsoft" },
  { month: "2026-03", title: "Azure Fundamentals (AZ-900)", type: "Training", city: "Den Bosch, NL", venue: "Ictivity" },
  { month: "2026-03", title: "Azure Fundamentals (AZ-900)", type: "Training", city: "Den Bosch, NL", venue: "Ictivity" },
  { month: "2026-03", title: "DSD Cloud University — Copilot Studio", type: "Training", city: "Den Bosch, NL", venue: "DSD Europe" },

  { month: "2026-04", title: "Microsoft Copilot", type: "Training", city: "Zurich, CH" },
  { month: "2026-04", title: "Microsoft Device Management Masterclass", type: "Training", city: "Oslo, NO" },
  { month: "2026-04", title: "Security Operations Analyst (SC-200)", type: "Training", city: "Oslo, NO" },
  { month: "2026-04", title: "Configuring and Operating Microsoft Azure Virtual Desktop (AZ-140)", type: "Training", city: "Online", venue: "Glasspaper" },
  { month: "2026-04", title: "Microsoft Identity and Access Administrator (SC-300)", type: "Training", city: "Venlo, NL", venue: "Ictivity" },
  { month: "2026-04", title: "SC-3025", type: "Training", city: "Online", venue: "Fast Lane" },
  { month: "2026-04", title: "SC-3025", type: "Training", city: "Online", venue: "Fast Lane" },
  { month: "2026-04", title: "AB-730", type: "Training", city: "Utrecht, NL", venue: "Ictivity" },

  { month: "2026-05", title: "Copilot Studio", type: "Training", city: "Ålesund, NO" },
  { month: "2026-05", title: "Agentic AI", type: "Training", city: "Ålesund, NO" },
  { month: "2026-05", title: "Azure Fundamentals (AZ-900)", type: "Training", city: "Den Bosch, NL", venue: "Ictivity" },
  { month: "2026-05", title: "Keynote", type: "Keynote", city: "Den Bosch, NL", venue: "DSD Europe" },

  { month: "2026-06", title: "Security, Compliance and Identity Fundamentals (SC-900)", type: "Training", city: "Trondheim, NO" },
  { month: "2026-06", title: "Security", type: "Training", city: "Dilbeek, BE", venue: "Copaco" },
  { month: "2026-06", title: "Azure Administrator (AZ-104)", type: "Training", city: "Oslo, NO" },
  { month: "2026-06", title: "Microsoft Copilot", type: "Training", city: "London, UK" },
  { month: "2026-06", title: "Designing Microsoft Azure Infrastructure Solutions (AZ-305)", type: "Training", city: "Oslo, NO" },
  { month: "2026-06", title: "Azure AI Fundamentals (AI-900)", type: "Training", city: "Almere, NL" },
  { month: "2026-06", title: "Security, Compliance and Identity Fundamentals (SC-900)", type: "Training", city: "Almere, NL" },
  { month: "2026-06", title: "Azure Fundamentals (AZ-900)", type: "Training", city: "Almere, NL" },
  { month: "2026-06", title: "Microsoft 365 E7 Event", type: "Event", city: "London, UK", venue: "Ingram Micro" },

  { month: "2026-07", title: "Microsoft Purview", type: "Training", city: "London, UK", venue: "Ingram Micro" },
];
