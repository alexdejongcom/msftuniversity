/* ============================================================
   TRAINER TOOLBOX — your private link vault
   ============================================================
   These are the permanent links. They live in git, so they are
   the same on every machine you open toolbox.html on.

   To add one, copy a line into the right group:
     { name: "What it is", url: "https://...", note: "optional hint" }

   To add a whole new group, copy a group block. Order here is
   the order on the page.

   You can also add links straight from the page with the
   "Add link" button — but those are stored in that one browser
   only. Anything you want to keep forever belongs in this file.
   ============================================================ */

const TOOLBOX = [

  {
    group: "Demo tenants & environments",
    icon: "cloud",
    links: [
      { name: "Microsoft Demos", url: "https://demos.microsoft.com", note: "The demo portal" },
      { name: "Microsoft Demo eXperiences (CDX)", url: "https://cdx.transform.microsoft.com", note: "Tenant provisioning" },
      { name: "Microsoft 365 admin center", url: "https://admin.microsoft.com" },
      { name: "Azure portal", url: "https://portal.azure.com" },
      { name: "Entra admin center", url: "https://entra.microsoft.com" },
      { name: "Intune admin center", url: "https://intune.microsoft.com" },
      { name: "Microsoft Purview portal", url: "https://purview.microsoft.com" },
      { name: "Microsoft Defender portal", url: "https://security.microsoft.com" },
      { name: "Power Platform admin center", url: "https://admin.powerplatform.microsoft.com" },
      { name: "Copilot Studio", url: "https://copilotstudio.microsoft.com" },
    ],
  },

  {
    group: "In the classroom",
    icon: "board",
    links: [
      { name: "The whiteboards", url: "https://dejongms-my.sharepoint.com/:f:/g/personal/alex_alexdejong_com/EsVGJ2WLoU9Fowhg_7Czz9cBtJwC65C3fGvZNu5Yx0l31Q?e=evenrn", note: "Shared OneDrive folder" },
      { name: "My Course Today", url: "course-today.html", note: "The page you put on the projector" },
      { name: "Exam Prep Hub", url: "exams.html", note: "All 46 exams" },
      { name: "Study Engine", url: "https://www.pdsmm.xyz/", note: "Practice questions" },
      { name: "Certificate verification", url: "verify.html" },
      { name: "Service Health (parody)", url: "status.html", note: "Good for a laugh at 09:05" },
    ],
  },

  {
    group: "Learning & certification",
    icon: "book",
    links: [
      { name: "Microsoft Learn", url: "https://learn.microsoft.com" },
      { name: "Learn catalog — all certifications", url: "https://learn.microsoft.com/credentials/browse/" },
      { name: "My Certifications Dashboard", url: "https://aka.ms/certdashboard" },
      { name: "Microsoft Trainer Portal (MCT)", url: "https://aka.ms/mctportal" },
      { name: "MCT Lounge", url: "https://prod.mct.pvue2.com/#/tech-communities", note: "Tech communities" },
      { name: "Microsoft Learning Download Center", url: "https://prod.mct.pvue2.com/#/courseware", note: "Courseware downloads" },
      { name: "MCT Lab Access", url: "https://prod.mct.pvue2.com/#/extreme-labs", note: "Extreme Labs" },
      { name: "Godeploy Labs", url: "https://lms.godeploy.it", note: "Lab environment" },
      { name: "MCT Program forums", url: "https://aka.ms/mctcommunity" },
      { name: "Pearson VUE profile", url: "https://wsr.pearsonvue.com/testtaker/registration/Dashboard/MICROSOFT", note: "Exam registration" },
      { name: "MeasureUp locker", url: "https://www.measureup.com/customer/account/", note: "Practice tests" },
      { name: "Skillable / Learn on Demand", url: "https://labondemand.com", note: "Lab hosting" },
    ],
  },

  {
    group: "Docs I open every day",
    icon: "doc",
    links: [
      { name: "Microsoft 365 Roadmap", url: "https://www.microsoft.com/microsoft-365/roadmap" },
      { name: "Azure Updates", url: "https://azure.microsoft.com/updates/" },
      { name: "Message center (M365)", url: "https://admin.microsoft.com/Adminportal/Home#/MessageCenter" },
      { name: "Microsoft 365 service health", url: "https://portal.office.com/servicestatus" },
      { name: "Azure status", url: "https://azure.status.microsoft/status" },
      { name: "Licensing: M365 plan comparison", url: "https://m365maps.com", note: "m365maps.com — the licence map" },
      { name: "Copilot adoption hub", url: "https://adoption.microsoft.com/copilot/" },
      { name: "Security Copilot docs", url: "https://learn.microsoft.com/copilot/security/" },
    ],
  },

  {
    group: "Business",
    icon: "briefcase",
    links: [
      { name: "Partner Center dashboard", url: "https://partner.microsoft.com/dashboard/home" },
      { name: "Glasspaper course pages", url: "https://www.glasspaper.no" },
      { name: "DSD Europe webinars", url: "https://www.dsdeurope.nl/webinars" },
      { name: "Fast Lane NL", url: "https://www.flane.nl" },
      { name: "Skilling Hub", url: "https://www.skilling-hub.com" },
      { name: "This site on GitHub", url: "https://github.com/alexdejongcom" },
    ],
  },

];
