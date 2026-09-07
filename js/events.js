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
    title: "Microsoft University, Azure Architect (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-07", end: "2026-09-11",
    title: "Microsoft University, Azure Architect (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
  },
  {
    date: "2026-09-14", end: "2026-09-18",
    title: "Microsoft University, Azure Architect (internal)",
    type: "Event",
    city: "Oslo, NO",
    venue: "Glasspaper",
    soldout: true,
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
    date: "2026-11-15", end: "2026-11-20",
    title: "Live! 360 Tech Con 2026",
    type: "Conference",
    city: "Orlando, FL, USA",
    venue: "Royal Pacific Resort — Universal Orlando",
    url: "https://na.eventscloud.com/ereg/newreg.php?eventid=838133",
  },
];
