# -*- coding: utf-8 -*-
"""
Exam data for the prep hub.

`url`, `title` and `study_guide` were read from Microsoft Learn (the exam
URLs resolve through learn.microsoft.com/credentials/certifications/...),
so links stay correct. `blurb`, `who` and `tip` are our own words — we do
not copy Microsoft's exam descriptions or their skills-measured lists;
those live behind the official links on every page.

`pa` = a free official practice assessment exists for this exam.

Optional richer fields, added per exam as we work through the catalog.
Every one is optional — pages render fine without them:

    overview    2-3 sentence course description, our own words
    duration    length of the instructor-led course, e.g. "3 days"
    course      the Microsoft course code behind it, e.g. "AB-650T00"
    exam_time   how long the exam itself runs, e.g. "120 minutes"
    prereq      what you are assumed to already know, one line
    challenges  list of 5 real problems the course answers. OUR framing of
                why someone sits this exam — not Microsoft's objectives
    labs        dict(count=, paths=[...], repo=, guide=, summary=)
                `repo` is the official MicrosoftLearning lab repository
                where one exists; omit the whole dict when there are no labs
    retired     date Microsoft withdrew the exam, e.g. "31 August 2026".
                Set this and the page leads with a retirement notice; leave
                `selling` off entirely, since there is nothing left to sell.
    selling     dict(pitch=, triggers=[...], buyer=, attendees=,
                     objections=[(question, answer), ...], next=[...])
                Enablement for the partners who resell our courses:
                the one-liner, when to raise it, who signs, the pushbacks
                they will hear, and what to sell after it.
"""

FAMILIES = [
    ("ai", "AI &amp; Business Value", "AB and AI exams — Copilot, agents and the business case for AI."),
    ("azure", "Azure &amp; Infrastructure", "The AZ track, from cloud fundamentals to architect level."),
    ("data", "Data, Fabric &amp; Analytics", "The DP track — databases, Fabric and analytics."),
    ("github", "GitHub", "The GH track — GitHub itself, Actions, Copilot and Advanced Security."),
    ("dynamics", "Dynamics 365", "The MB track — functional consultant and developer paths."),
    ("m365", "Microsoft 365 &amp; Teams", "The MS and MD track — tenant, endpoints and Teams."),
    ("power", "Power Platform", "The PL track — from fundamentals to developer."),
    ("security", "Security", "The SC track — the fastest-growing corner of the catalog."),
]

EXAMS = {
"AB-100": dict(fam="ai", level="Advanced", title="Agentic AI Business Solutions Architect",
    url="https://learn.microsoft.com/credentials/certifications/exams/ab-100/",
    sg="https://aka.ms/AB100-StudyGuide", pa=False,
    blurb="The architect-level exam for designing agentic AI solutions across Copilot Studio, Foundry and the Dynamics 365 and Power Platform stack.",
    who="Solution architects who already hold an associate-level Dynamics 365, Power Platform or Azure AI certification — it has prerequisites, so check before you book.",
    overview=(
        "The architect exam of the AB track, and the only one that is mostly about deciding "
        "rather than doing. Which process actually deserves an agent, what it may touch, how the "
        "design spans Copilot Studio, Foundry, Dynamics 365 and Power Platform, and what happens "
        "when it meets production. Planning and design carry about two thirds of the weighting — "
        "the build is assumed to be somebody else's job."),
    duration="3 days", course="AB-100T00",
    prereq=("An associate-level certification is a formal prerequisite — Dynamics 365, Power "
            "Platform or Azure AI. Check your candidates qualify before booking the exam."),
    challenges=[
        "Deciding which processes justify an agent and which are better served by a form and a flow.",
        "Designing across products rather than inside one, when Copilot Studio, Foundry, Dynamics "
        "365 and Power Platform each own part of the same workflow.",
        "Agreeing what an agent may decide on its own and where a human stays in the loop.",
        "Putting a defensible cost on an agentic solution before it is built, when usage rather "
        "than seat count drives the bill.",
        "Taking the prototype that impressed a steering group and making it survive production.",
    ],
    selling=dict(
        pitch=("Their agent pilot worked. This is the course that tells them whether it should "
               "become a platform."),
        triggers=[
            "Several agent pilots have succeeded separately and nobody owns the overall design.",
            "A steering group has asked what agentic AI will cost them over three years.",
            "They keep changing their mind between Copilot Studio, Foundry and custom code.",
            "An agent is about to touch a system of record and risk has woken up.",
            "They have plenty of associate-level people and no architect.",
        ],
        buyer="Enterprise architecture lead, CTO or transformation director — often funded from a programme budget rather than a training one.",
        attendees="Solution architects and senior consultants who already hold an associate certification. Verify that first; the exam is gated on it.",
        objections=[
            ("Our architects already design on Power Platform.",
             "Agentic design breaks some Power Platform habits: behaviour that is not "
             "deterministic, identity for a non-human actor, and cost that moves with usage "
             "instead of seats."),
            ("It has prerequisites and our people are not certified yet.",
             "True, and worth checking before you quote. The course still teaches them the job — "
             "only the exam is gated, and the associate cert can follow."),
            ("Can't the makers work the architecture out as they go?",
             "That is how an organisation ends up with nine agents doing the same job against "
             "four different copies of the data."),
            ("Three days feels long for an architecture course.",
             "Two of them are planning and design, which is where the weighting sits and where "
             "the expensive mistakes get made."),
        ],
        next=[
            "AB-620 for the people who will build what the architect designed",
            "AB-650 for the admins who will have to govern the result",
            "SC-401 once the design starts touching regulated data",
            "A design workshop on one of their real processes instead of a second course",
        ])),
"AB-210": dict(fam="ai", level="Intermediate", title="Accelerating Sales Pipelines with AI in Dynamics 365",
    url="https://learn.microsoft.com/credentials/certifications/d365-sales-ai-consultant-associate/",
    sg="https://aka.ms/AB210-StudyGuide", pa=False,
    blurb="Putting AI to work in the sales cycle — scoring and prioritising pipeline, drafting the follow-up, and keeping the CRM honest without manual data entry.",
    who="Dynamics 365 Sales consultants and functional consultants adding the AI layer to an existing sales implementation."),
"AB-250": dict(fam="ai", level="Intermediate", title="Transforming Contact Center Experiences with AI in Dynamics 365",
    url="https://learn.microsoft.com/credentials/certifications/d365-contact-center-ai-engineer-associate/",
    sg="https://aka.ms/AB250-StudyGuide", pa=False,
    blurb="Designing the AI side of a contact centre: routing, self-service agents, live agent assistance and the handover between them.",
    who="Engineers and consultants building on Dynamics 365 Contact Center who now own the conversational AI as well."),
"AB-400": dict(fam="ai", level="Intermediate", title="Extending Microsoft Power Platform Solutions with Code and AI",
    url="https://learn.microsoft.com/credentials/certifications/exams/ab-400/",
    sg="https://aka.ms/AB400-StudyGuide", pa=False,
    blurb="Where low-code runs out: custom code, APIs and AI services layered onto Power Platform solutions that have outgrown the designer.",
    who="Power Platform developers who write code as well as configure, and want the developer credential on the AB track."),
"AB-410": dict(fam="ai", level="Intermediate", title="Building Intelligent Applications",
    url="https://learn.microsoft.com/credentials/certifications/intelligent-applications-builder-associate/",
    sg="https://aka.ms/AB410-StudyGuide", pa=False,
    blurb="Building applications with AI at the centre rather than bolted on — models, grounding data, and the plumbing that makes them behave in production.",
    who="Developers building AI-first applications on Microsoft's stack. Earns the Intelligent Applications Builder Associate certification."),
"AB-620": dict(fam="ai", level="Intermediate", title="Designing and Building Integrated AI Agent Solutions in Copilot Studio",
    url="https://learn.microsoft.com/credentials/certifications/ai-agent-builder-associate/",
    sg="https://aka.ms/AB620-StudyGuide", pa=False,
    blurb="Agents that do real work in Copilot Studio: topics and triggers, connecting them to live systems, and testing them before anyone else does.",
    who="Makers and consultants building agents for the business. The natural next step after the Copilot Studio courses.",
    overview=(
        "The builder's exam for Copilot Studio. It starts with planning and configuring an agent, "
        "then spends its largest share on the part that separates a demo from a tool — wiring an "
        "agent into real systems with knowledge, tools and workflows, and getting several agents "
        "to cooperate. The closing fifth is testing, publishing and managing them, which is "
        "exactly where most first agents come apart."),
    duration="3 days", course="AB-620T00",
    prereq="Comfortable in Microsoft 365 and Power Platform. No Copilot Studio experience assumed.",
    challenges=[
        "Getting an agent past the demo — answering from live data instead of something typed in.",
        "Choosing between knowledge, tools and workflows for a given job, rather than reaching "
        "for whichever one was learned first.",
        "Making several agents cooperate without quietly duplicating each other's work.",
        "Testing something non-deterministic well enough to put it in front of a customer.",
        "Owning it after launch: versions, changed source data, and the questions it has started "
        "getting wrong.",
    ],
    labs=dict(
        count=5,
        repo="https://github.com/MicrosoftLearning/AB-620T00_build_integrated_ai_agents_in_copilot_studio",
        guide="https://microsoftlearning.github.io/AB-620T00_build_integrated_ai_agents_in_copilot_studio/",
        summary=("Five labs that build one agent up in stages, plus an environment setup. Design "
                 "and configure it, add workflows, integrate knowledge and tools, extend it into "
                 "a multi-agent solution, then evaluate, publish and manage it.")),
    selling=dict(
        pitch=("Copilot Studio is already in their licence. This is the course that turns it from "
               "a chatbot into something that does the work."),
        triggers=[
            "Makers have built agents that answer questions but cannot actually do anything.",
            "Every department wants its own agent and IT can see the sprawl coming.",
            "Their first agent is live and already giving answers somebody had to correct.",
            "They are carrying Power Virtual Agents habits into Copilot Studio.",
            "An architect has produced an agent design and nobody can build it.",
        ],
        buyer="Head of Power Platform or the automation lead; sometimes the business unit that owns the process being automated.",
        attendees="Power Platform makers, app makers, and developers extending Copilot. Low-code people, not necessarily developers.",
        objections=[
            ("Copilot Studio is low-code — our people will pick it up.",
             "They will pick up topics in an afternoon. Tools, connectors, multi-agent design and "
             "evaluation are where self-taught makers stall, and those are three fifths of this exam."),
            ("We would rather wait until the product settles.",
             "It is not going to settle. The skills that carry over regardless — grounding, tools, "
             "evaluation — are the ones this course is built on."),
            ("Can they not just watch the Learn modules?",
             "The five labs are the course: build an agent, connect it, break it, publish it. "
             "Watching somebody else do that does not transfer."),
            ("Our agents only need to answer HR questions.",
             "That is the first lab. The value is in the four that follow it."),
        ],
        next=[
            "AB-650 for whoever governs the agents once there are twenty of them",
            "AB-100 if they need the architecture layer above the build",
            "PL-7008 as a fast Applied Skills win for the same people",
            "A build day on one of their real processes",
        ])),
"AB-650": dict(fam="ai", level="Intermediate", title="Administering Microsoft 365 and AI Services",
    url="https://learn.microsoft.com/credentials/certifications/exams/ab-650/",
    sg="https://learn.microsoft.com/credentials/certifications/resources/study-guides/ab-650", pa=False,
    blurb="Running Microsoft 365 once AI is part of it — provisioning and governing Copilot and agents alongside the tenant administration you already do.",
    who="Microsoft 365 administrators whose job grew an AI half. Currently in beta, so expect the objectives to move.",
    overview=(
        "The administrator exam for a tenant that now has AI in it. The first quarter is the "
        "familiar ground — tenants, domains, licensing, mailboxes, Teams and SharePoint. The rest "
        "is what changes once Copilot, Cowork and agents are switched on: who can reach what, "
        "which content surfaces in a Copilot answer, and how a non-human identity is governed "
        "through its life. Roughly three quarters of the exam is about securing and governing "
        "the estate rather than building it, which tells you where the job has moved."),
    duration="3 days", course="AB-650T00", exam_time="120 minutes",
    prereq=("Hands-on with Microsoft 365 workloads and Microsoft Entra ID, a working "
            "understanding of Defender XDR, and some Microsoft Graph PowerShell."),
    challenges=[
        "Copilot surfacing content people could always technically open but never actually found — "
        "oversharing that was invisible until search got good.",
        "Agents arriving as a new class of identity: who owns one, what it may reach, and how it "
        "is retired when the project ends.",
        "Proving to an auditor what an AI service did — DLP, retention and activity evidence that "
        "covers prompts and responses, not just files.",
        "Licensing spread across Microsoft 365 Copilot, Agent 365 and Copilot Studio, with "
        "self-service purchases quietly appearing alongside them.",
        "Keeping conditional access, sign-in protection and privileged access coherent once "
        "both people and agents are in scope.",
    ],
    labs=dict(
        count=7, paths=3,
        repo="https://github.com/MicrosoftLearning/AB-650T00_administer_microsoft_365_and_ai_services",
        guide="https://microsoftlearning.github.io/AB-650T00_administer_microsoft_365_and_ai_services/",
        summary=("Seven hands-on labs across three learning paths. The first pair covers operating "
                 "the tenant and governing collaboration content. The middle three are the identity "
                 "and protection block — delegated access, sign-in controls and information "
                 "protection. The last two are the AI half: rolling out Copilot Cowork, then "
                 "governing agents and running AI services day to day.")),
    selling=dict(
        pitch=("The customer has already paid for Copilot. This is the course that keeps the "
               "rollout from becoming a security incident."),
        triggers=[
            "They bought Microsoft 365 Copilot or Agent 365 licences and usage has flattened.",
            "Security or legal has paused a Copilot rollout over what it might surface.",
            "Agents are turning up in the tenant that nobody formally approved.",
            "An audit, NIS2 or ISO review has asked who can see what, and nobody can answer quickly.",
            "Their Microsoft 365 admins have not been retrained since Copilot arrived.",
        ],
        buyer="IT manager or head of infrastructure holds the budget; the CISO signs off the governance half.",
        attendees="Microsoft 365 administrators, Entra and identity admins, and service desk leads moving up into tenant work.",
        objections=[
            ("Our admins already know Microsoft 365.",
             "About a fifth of this is revision. The rest is new ground: agent identities, "
             "Copilot-aware DLP, data security posture management, and the Copilot readiness work "
             "that has no equivalent in the old MS-102 world."),
            ("Let's wait until it is out of beta.",
             "Beta applies to the exam, not the product. The tenant work is live now, and the "
             "oversharing problem is live with it. Train now, certify when it goes GA."),
            ("Can't they just use Microsoft Learn?",
             "They can, and they should. The difference is seven labs on a tenant that is not "
             "production, plus somebody in the room who has done the rollout before."),
            ("We only have a few Copilot users so far.",
             "Oversharing scales with how much content you have, not how many licences. A pilot "
             "of twenty people can surface a decade of badly permissioned SharePoint."),
            ("Three days is a lot of time out.",
             "It is one day of admin refresh and two days of the governance and AI work their "
             "security team is already asking them about."),
        ],
        next=[
            "SC-401 for the Purview depth behind the information-protection day",
            "SC-300 for teams that need the identity side properly",
            "AB-620 for the makers who will actually build the agents",
            "A follow-up Agent 365 workshop once their estate has grown",
        ])),
"AB-730": dict(fam="ai", level="Beginner", title="AI Business Professional",
    url="https://learn.microsoft.com/credentials/certifications/ai-business-professional/",
    sg="https://aka.ms/ab730-StudyGuide", pa=True,
    blurb="AI skills for people who work with the business rather than the platform: where AI creates value, and how to use it responsibly day to day.",
    who="Business professionals, consultants and managers who need fluency without going deep into the technology.",
    overview=(
        "The non-technical end of the AB track, and the one most people in an organisation "
        "should actually sit. A day on what generative AI is doing under the surface, how to "
        "prompt it as a skill rather than a trick, how Copilot behaves across the documents, "
        "spreadsheets and meetings they already live in, and where agents start to earn their "
        "keep. No administration, no building."),
    duration="1 day", course="AB-730T00",
    prereq="None. Day-to-day familiarity with Microsoft 365 is enough.",
    challenges=[
        "Licences bought, Copilot opened twice, and nobody changed how they work.",
        "Prompting treated as a magic phrase rather than a skill, so results vary and trust drops.",
        "People not knowing which parts of their own week are worth handing over.",
        "Output either taken at face value or rejected outright — neither of which is use.",
        "The gap between the handful of enthusiasts and everyone else widening until adoption stalls.",
    ],
    labs=dict(
        count=4,
        repo="https://github.com/MicrosoftLearning/AB-730-AI-business-professional",
        guide="https://microsoftlearning.github.io/AB-730-AI-business-professional/",
        summary=("Four labs shaped like an ordinary working week rather than a product tour: "
                 "planning a client summit with Copilot Chat, drafting and refining business "
                 "content, analysing and visualising data, then running meetings and "
                 "collaboration.")),
    selling=dict(
        pitch=("This is the course that makes the Copilot licences they already bought show up "
               "in the usage report."),
        triggers=[
            "A Copilot rollout where active use is far below the licence count.",
            "A department asking for AI training and nobody knowing what to put in front of them.",
            "Leadership asking for an AI-literacy baseline across the whole business.",
            "A cohort of new starters, or a team who have never used Copilot seriously.",
            "An adoption programme that needs a formal, certifiable component attached to it.",
        ],
        buyer="HR or L&D, or the adoption lead on the Copilot programme. Rarely IT, which is worth knowing before you call.",
        attendees="Anyone who uses Microsoft 365 daily. Non-technical by design, and it scales to large cohorts.",
        objections=[
            ("Our people can work Copilot out for themselves.",
             "Some will. The usage reports from organisations that assumed everyone would are "
             "the whole argument for this course."),
            ("One day — is that really enough?",
             "For this audience one day is the ceiling you will get signed off, and the course "
             "is scoped to fit it rather than pretending otherwise."),
            ("We want something tailored, not a Microsoft course.",
             "The four labs are ordinary work: an event plan, a document, a spreadsheet, a "
             "meeting. Tailoring it is mostly swapping the scenario for one of theirs."),
            ("Is there a certification at the end?",
             "Yes, and a free official practice assessment, which matters to the people who "
             "want a finish line."),
        ],
        next=[
            "AB-731 for the leaders who sponsored the programme",
            "AB-900 for whoever ends up administering it",
            "Sell this one per department rather than per person — it is the volume course",
            "A prompting clinic six weeks later, once they have hit real friction",
        ])),
"AB-731": dict(fam="ai", level="Intermediate", title="AI Transformation Leader",
    url="https://learn.microsoft.com/credentials/certifications/ai-transformation-leader/",
    sg="https://aka.ms/ab731-StudyGuide", pa=True,
    blurb="Leading an organisation through AI adoption — strategy, governance, change and measuring whether any of it actually worked.",
    who="Leaders and programme owners driving AI transformation, not the engineers implementing it.",
    overview=(
        "The leadership day. Where generative AI creates value and, just as usefully, where it "
        "does not; what is actually inside Microsoft's AI portfolio; and how an organisation "
        "gets from a successful pilot to something it runs. About three quarters of it is value "
        "and capability, with the last quarter on implementation and adoption. No building, no "
        "administration, no labs."),
    duration="1 day", course="AB-731T00",
    prereq="None technical. It assumes you own or influence a budget and a change programme.",
    challenges=[
        "A board asking for an AI strategy when what exists is three enthusiastic pilots.",
        "Separating genuine value from vendor narrative across a portfolio that changes quarterly.",
        "Choosing where to start when every department is certain it should be first.",
        "Measuring whether any of it worked, in terms the finance director will accept.",
        "Carrying the whole organisation rather than the early adopters — a change problem "
        "wearing a technology costume.",
    ],
    selling=dict(
        pitch=("Their pilots worked and no strategy followed. This is the day that closes "
               "that gap."),
        triggers=[
            "A board or exec team has asked for an AI plan with a date attached.",
            "Pilots succeeded and nothing scaled, and nobody can say why.",
            "Several vendors are selling them AI and they cannot compare the offers.",
            "A transformation programme is running with no AI workstream in it.",
            "They sent the technical people on Copilot training and leadership got left behind.",
        ],
        buyer="CIO, CDO or transformation director. Frequently sold alongside a strategy engagement rather than as training.",
        attendees="Executives, programme owners and senior managers. Deliberately not the engineers.",
        objections=[
            ("Our leadership does not do training.",
             "Then call it a briefing. One day, no labs, and they leave with an adoption plan "
             "rather than a certificate they will never mention."),
            ("We already have an AI strategy.",
             "Good — this is the day it gets pressure-tested against what the platform can "
             "actually do today, which is usually where strategies move."),
            ("Is this not just marketing content?",
             "A third of the exam is identifying business value, and that includes identifying "
             "where there is none. It is a filter as much as a pitch."),
            ("Our people need hands-on, not theory.",
             "Different audience entirely. Sell AB-730 to them and this to the people funding them."),
        ],
        next=[
            "AB-730 for the workforce the leader is about to mobilise",
            "AB-650 for the administrators who inherit the rollout",
            "AB-100 if the ambition turns out to be genuinely agentic",
            "A strategy workshop on their own portfolio rather than a second course",
        ])),
"AB-900": dict(fam="ai", level="Beginner", title="Microsoft 365 Copilot and Agent Administration Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/copilot-and-agent-administration-fundamentals/",
    sg="https://aka.ms/ab900-StudyGuide", pa=True,
    blurb="The fundamentals of administering Microsoft 365 Copilot and agents: rollout, permissions, governance and the guardrails around them.",
    who="Administrators taking their first structured look at running Copilot and agents in a tenant.",
    overview=(
        "The fundamentals day for running Microsoft 365 once Copilot is in it. A tour of the "
        "services and objects an administrator touches, then the larger share: what data "
        "protection and governance mean when Copilot can surface anything a user could already "
        "reach, and the basic administrative tasks for Copilot and agents. Think of it as the "
        "gentle version of AB-650 — same territory, none of the depth, and no labs."),
    duration="1 day", course="AB-900T00",
    prereq="None. General familiarity with Microsoft 365 as a user is plenty.",
    challenges=[
        "A service desk being handed Copilot questions that nobody prepared them for.",
        "Not knowing which admin centre owns which setting now that AI is in the picture.",
        "Governance arriving as a policy document rather than as things somebody actually clicks.",
        "Nobody able to explain to a user, in one sentence, why Copilot can see a given file.",
        "Needing a shared vocabulary across a mixed team before a serious AB-650 conversation "
        "is even possible.",
    ],
    selling=dict(
        pitch=("The one-day version, for the people who will be asked Copilot questions long "
               "before anyone trains them."),
        triggers=[
            "A Copilot rollout where the service desk found out last.",
            "A mixed team in which exactly one person really understands the tenant.",
            "Junior admins or new starters who need a baseline quickly.",
            "A customer who balked at three days for AB-650 and needs a step before it.",
            "Pre-work ahead of a larger security or governance engagement.",
        ],
        buyer="IT manager, or whoever owns the service desk. Small enough to approve without a business case.",
        attendees="Service desk staff, junior administrators, and non-specialists who have inherited a corner of the tenant.",
        objections=[
            ("Fundamentals courses are a wasted day.",
             "For a specialist, yes. This is for the people who receive the ticket, not the "
             "people who write the policy."),
            ("Why not just send them on AB-650?",
             "Three days, and it assumes experience they do not have yet. This is the step that "
             "makes AB-650 land properly six months later."),
            ("There are no labs?",
             "Correct, and say so up front. It is a knowledge day. If they want hands-on from "
             "the start, sell AB-650 instead and skip this."),
            ("Is it worth certifying at this level?",
             "The certificate matters less than the shared vocabulary. The free practice "
             "assessment is a useful nudge to make people actually finish it."),
        ],
        next=[
            "AB-650 as the natural follow-on for whoever shows aptitude",
            "AB-730 for the end users those administrators support",
            "SC-900 if their questions keep turning out to be security questions",
            "A tenant review delivered alongside, so the training lands on their own estate",
        ])),
"AI-900": dict(fam="ai", level="Beginner", title="Microsoft Azure AI Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/exams/ai-900/",
    sg="https://aka.ms/AI900-StudyGuide", pa=True,
    blurb="The entry point to AI on Azure — core machine learning concepts, the Azure AI services, generative AI and responsible AI.",
    who="Anyone starting out with AI on Azure. No coding or data-science background needed."),

"AZ-104": dict(fam="azure", level="Intermediate", title="Microsoft Azure Administrator",
    url="https://learn.microsoft.com/credentials/certifications/azure-administrator/",
    sg="https://aka.ms/AZ104-StudyGuide", pa=True,
    blurb="The workhorse Azure exam: identity, governance, storage, compute, virtual networking and monitoring — the things you touch every day.",
    who="Administrators with six months of hands-on Azure. The most common first role-based Azure certification.",
    overview=(
        "The workhorse Azure exam, and the one most Azure careers are built on. Five areas, "
        "none of them optional: identity and governance, storage, compute, virtual networking, "
        "and the monitoring that tells you when any of it breaks. It is deliberately broad "
        "rather than deep — the point is that an administrator can be handed any part of a "
        "subscription and not be lost."),
    duration="4 days", course="AZ-104T00", exam_time="100 minutes",
    prereq="Around six months of hands-on Azure, plus comfort with networking, identity and PowerShell or CLI.",
    challenges=[
        "A subscription grown by project teams, where nobody can say who owns which resource group.",
        "Cost that arrives as a surprise every month because nothing was tagged or budgeted.",
        "Storage and backup configured once at build time and never reviewed since.",
        "Virtual networks designed by whoever needed one first, now needing to talk to each other.",
        "Admins who can click through the portal but cannot script the same job twice.",
    ],
    labs=dict(
        count=14,
        repo="https://github.com/MicrosoftLearning/AZ-104-MicrosoftAzureAdministrator",
        guide="https://microsoftlearning.github.io/AZ-104-MicrosoftAzureAdministrator/",
        summary=("Fourteen labs covering the whole administrator surface — Entra ID identities, "
                 "governance, storage, virtual machines, networking and monitoring. The repo is "
                 "actively maintained, which matters on a platform that changes monthly.")),
    selling=dict(
        pitch=("This is the baseline. If their people run anything in Azure and have not done "
               "AZ-104, this is the gap you are selling into."),
        triggers=[
            "They are migrating to Azure and the team are learning it from blog posts.",
            "An unexpected Azure bill has made someone ask who is managing this.",
            "They are hiring Azure admins and need a common standard to interview against.",
            "A managed service provider is handing the estate back to them.",
            "Any Azure project where the operate phase has no named owner.",
        ],
        buyer="IT manager or head of infrastructure. The easiest Azure training to get approved, because the role is obvious.",
        attendees="Infrastructure administrators moving to Azure, and cloud engineers who learned it piecemeal.",
        objections=[
            ("Our people already work in Azure every day.",
             "Then they know the two or three services their projects used. AZ-104 is the other "
             "two thirds, which is where the cost and governance problems live."),
            ("Four days is a lot for an administrator course.",
             "It is the broadest exam in the track — five weighted areas. Cutting it short just "
             "moves the gap somewhere less visible."),
            ("Can they not do AZ-900 first and see?",
             "AZ-900 is a good primer for non-technical people. For working administrators it "
             "is a day they will find slow."),
            ("We are mostly on-premises still.",
             "Then AZ-800 and AZ-801 may fit better. Worth asking before you quote this one."),
        ],
        next=[
            "AZ-305 for the ones ready to design rather than operate",
            "AZ-700 when the networking turns out to be the hard part",
            "SC-300 because most Azure problems become identity problems",
            "AZ-800 and AZ-801 if the estate is genuinely hybrid",
        ]),
    ),
"AZ-140": dict(fam="azure", level="Intermediate", title="Configuring and Operating Microsoft Azure Virtual Desktop",
    url="https://learn.microsoft.com/credentials/certifications/azure-virtual-desktop-specialty/",
    sg="https://aka.ms/AZ140-StudyGuide", pa=True,
    blurb="Planning, deploying and operating Azure Virtual Desktop — host pools, images, FSLogix profiles, access and the performance tuning that follows.",
    who="Desktop and infrastructure specialists running virtual desktops on Azure.",
    overview=(
        "A specialist exam with an unusually clear job behind it. Nearly half of it is planning "
        "and implementing the Azure Virtual Desktop infrastructure itself — host pools, images, "
        "session hosts, storage for profiles. The rest covers identity and security for those "
        "desktops, the user environment and application delivery, and keeping the whole thing "
        "monitored once real people depend on it."),
    duration="4 days", course="AZ-140T00", exam_time="100 minutes",
    prereq="Solid Azure administration (AZ-104 level) plus Windows desktop and identity experience.",
    challenges=[
        "A virtual desktop pilot that was fast for ten people and crawls for two hundred.",
        "Profile storage chosen without understanding FSLogix, and logon times paying for it.",
        "Golden images maintained by hand, so every update is a day nobody wants.",
        "Licensing and sizing guessed at, and the monthly bill reflecting that.",
        "Remote or contract staff needing access from unmanaged devices, securely.",
    ],
    labs=dict(
        repo="https://github.com/MicrosoftLearning/AZ-140-Configuring-and-Operating-Microsoft-Azure-Virtual-Desktop",
        summary=("The official lab repository for the course, maintained by Microsoft Learning. "
                 "The exercises build a working Azure Virtual Desktop environment rather than "
                 "demonstrating features in isolation.")),
    selling=dict(
        pitch=("Virtual desktops are easy to pilot and hard to run. This is the course that "
               "covers the second part."),
        triggers=[
            "A virtual desktop pilot that worked and is now struggling to scale.",
            "An office move, acquisition or hybrid-working policy that needs desktops anywhere.",
            "Logon times or application performance generating daily complaints.",
            "Contractors or third parties needing access without managed laptops.",
            "A Citrix or VMware renewal prompting a look at what Azure can do instead.",
        ],
        buyer="Head of end-user computing or infrastructure manager. Often funded from a workplace programme.",
        attendees="Desktop and infrastructure specialists who already know Azure basics.",
        objections=[
            ("We only have a small virtual desktop estate.",
             "Small estates are where the sizing and profile mistakes are cheapest to fix. "
             "After two hundred users they are expensive."),
            ("Our team already built it.",
             "Building it is the pilot. This course is about operating it — images, profiles, "
             "scaling and monitoring, which is where the complaints come from."),
            ("Is this not just AZ-104 with desktops?",
             "AZ-104 does not touch host pools, FSLogix or application delivery. There is "
             "almost no overlap beyond the Azure fundamentals."),
            ("We are considering Windows 365 instead.",
             "Worth having that conversation first. The course is still relevant, but the "
             "sizing and cost arguments change."),
        ],
        next=[
            "AZ-104 first if they have not done it — this course assumes it",
            "AZ-700 when the networking behind the desktops gets complicated",
            "SC-300 for conditional access on unmanaged devices",
            "An AVD design review on their own estate",
        ]),
    ),
"AZ-204": dict(fam="azure", level="Intermediate", title="Developing Solutions for Microsoft Azure",
    url="https://learn.microsoft.com/credentials/certifications/azure-developer/",
    sg="https://aka.ms/AZ204-StudyGuide", pa=True,
    blurb="Building on Azure: compute options, storage, security, integration and the monitoring and troubleshooting that comes with shipping to production.",
    who="Developers with a year or two of professional development and real Azure SDK experience.",
    overview=(
        "The developer exam. Compute carries the biggest share — App Service, Functions, "
        "containers — then storage, then implementing security properly rather than putting "
        "secrets in config. The last part is about connecting things: consuming Azure and "
        "third-party services through messaging, events and API Management. It assumes you "
        "can already write code; it tests whether you can write code that runs well on Azure."),
    course="AZ-204T00",
    prereq="A year or two of professional development, and real Azure experience. Fluency in at least one supported language.",
    challenges=[
        "Applications lifted into Azure unchanged, then surprising everyone with the bill.",
        "Secrets and connection strings living in configuration files and repositories.",
        "Services wired together synchronously, so one slow dependency takes everything down.",
        "No instrumentation, so production problems are diagnosed by guesswork.",
        "Developers choosing a compute option by familiarity rather than by fit.",
    ],
    labs=dict(
        count=11,
        repo="https://github.com/MicrosoftLearning/AZ-204-DevelopingSolutionsforMicrosoftAzure",
        guide="https://microsoftlearning.github.io/AZ-204-DevelopingSolutionsforMicrosoftAzure/",
        summary=("Eleven hands-on labs that build and deploy real Azure services rather than "
                 "walking through the portal — App Service, Functions, storage, Key Vault, "
                 "messaging and API Management.")),
    selling=dict(
        pitch=("Their developers can write the application. This is what makes it run properly "
               "on Azure instead of just running."),
        triggers=[
            "A lift-and-shift migration where cloud costs did not fall as promised.",
            "A development team told to go cloud-native with no one to show them how.",
            "Secrets found in a repository during a security review.",
            "Production incidents that take too long to diagnose because nothing is instrumented.",
            "A platform team standing up Azure and needing the developers to meet them halfway.",
        ],
        buyer="Development manager or head of engineering. A different budget from infrastructure training, and worth knowing that.",
        attendees="Professional developers with real Azure exposure. Not a beginner course.",
        objections=[
            ("Our developers learn from documentation.",
             "They learn the service they are using today. The value here is knowing which of "
             "five compute options fits, before committing to one."),
            ("We use GitHub Actions and not Azure DevOps.",
             "This exam is about building on Azure, not the pipeline. AZ-400 is the one with "
             "the pipeline question in it."),
            ("Certification does not matter for developers.",
             "Often true. Sell the labs and the architecture judgement; treat the certificate "
             "as a bonus for the ones who want it."),
            ("Our stack is mostly containers.",
             "Containers are in here, but if that is the whole story, look at the AKS-focused "
             "material instead and save them the rest."),
        ],
        next=[
            "AZ-400 for the pipeline and release side",
            "AZ-305 for the developer becoming an architect",
            "SC-500 when the application security questions get serious",
            "A code-level architecture review on their own workload",
        ]),
    ),
"AZ-305": dict(fam="azure", level="Advanced", title="Designing Microsoft Azure Infrastructure Solutions",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-305/",
    sg="https://aka.ms/AZ305-StudyGuide", pa=True,
    blurb="The architect exam. Designing identity, governance, data storage, business continuity and infrastructure — trade-offs rather than button-clicking.",
    who="Architects who already know Azure operations well. Case-study heavy; experience matters more than memorisation.",
    overview=(
        "The Azure architect exam, and the step up from operating to designing. Infrastructure "
        "design carries the largest share, followed by identity, governance and monitoring, "
        "then data storage and business continuity. It is case-study heavy by design: the "
        "questions give you requirements and constraints and ask what you would build, which "
        "is a different skill from knowing what the services do."),
    duration="4 days", course="AZ-305T00",
    prereq="AZ-104 level Azure operations experience. This exam assumes you have run the platform before designing on it.",
    challenges=[
        "Designs that work technically and fail on cost, or the reverse.",
        "Business continuity promised in a contract and never actually tested.",
        "Identity and governance bolted on after the architecture was agreed.",
        "Data storage chosen for familiarity rather than access pattern, then regretted at scale.",
        "An architect who can describe services but cannot defend a design under questioning.",
    ],
    labs=dict(
        repo="https://github.com/MicrosoftLearning/AZ-305-DesigningMicrosoftAzureInfrastructureSolutions",
        summary=("The official course repository. This one is case-study driven rather than "
                 "click-through — the work is design decisions against requirements, which is "
                 "exactly how the exam is written.")),
    selling=dict(
        pitch=("They have people who can build anything in Azure and nobody who decides what "
               "to build. That is the gap this fills."),
        triggers=[
            "Cloud spend rising without a corresponding design authority.",
            "A migration programme about to start with no target architecture.",
            "Their best AZ-104 people are ready for the next step.",
            "A failed or painful disaster recovery test.",
            "A customer or regulator asking for an architecture document they do not have.",
        ],
        buyer="Head of architecture, CTO, or the programme funding a migration.",
        attendees="Azure administrators and engineers moving into architecture, and architects new to Azure.",
        objections=[
            ("Our architects already design on Azure.",
             "Then this is validation and vocabulary, which matters if they are presenting "
             "designs to customers or auditors. If not, spend the money elsewhere."),
            ("It is the same material as AZ-104.",
             "The services overlap, the skill does not. AZ-104 asks how to configure it; "
             "AZ-305 asks whether you should."),
            ("Case studies feel academic.",
             "They are the closest thing to the actual job. Most architecture failures are "
             "requirement failures, not technical ones."),
            ("We use a lot of third-party tooling.",
             "Fine — the design principles carry. Just set expectations that the reference "
             "architectures are Microsoft's."),
        ],
        next=[
            "AZ-104 first for anyone without the operations grounding",
            "SC-100 for the security architecture counterpart",
            "AZ-700 and AZ-400 to deepen specific parts of the design",
            "An architecture review engagement, which often follows naturally",
        ]),
    ),
"AZ-400": dict(fam="azure", level="Advanced", title="Designing and Implementing Microsoft DevOps Solutions",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-400/",
    sg="https://aka.ms/AZ400-StudyGuide", pa=True,
    blurb="DevOps end to end: source control, CI/CD pipelines, infrastructure as code, secrets, dependencies and feedback loops.",
    who="Engineers who live in pipelines. Expect both Azure DevOps and GitHub across the exam.",
    overview=(
        "The DevOps exam, and an unusually lopsided one: build and release pipelines carry more "
        "than half the weighting on their own. Around that sit process and communication, "
        "source control strategy, security and compliance in the pipeline, and instrumentation. "
        "It covers both Azure DevOps and GitHub, which is realistic — most organisations are "
        "running some of each."),
    duration="4 days", course="AZ-400T00",
    prereq="Experience with both Azure administration and development, plus day-to-day work in a pipeline.",
    challenges=[
        "Releases that need a person, a runbook and a quiet Friday evening.",
        "Half the teams on Azure DevOps and half on GitHub, with no agreed direction.",
        "Security scanning bolted on at the end, so findings arrive too late to act on.",
        "Branching strategies inherited from a previous team and never revisited.",
        "No usable telemetry, so nobody can say whether a release improved anything.",
    ],
    labs=dict(
        count=16,
        repo="https://github.com/MicrosoftLearning/AZ400-DesigningandImplementingMicrosoftDevOpsSolutions",
        guide="https://microsoftlearning.github.io/AZ400-DesigningandImplementingMicrosoftDevOpsSolutions/",
        summary=("Sixteen labs, starting with validating the lab environment and then building "
                 "up real pipelines across Azure DevOps and GitHub — source control, builds, "
                 "releases, security scanning and monitoring.")),
    selling=dict(
        pitch=("Their deployments need a human and a weekend. This is the course that changes "
               "that, and it covers GitHub as well as Azure DevOps."),
        triggers=[
            "Release nights. If they still have them, this is the conversation.",
            "A GitHub migration, or a split estate with no agreed direction.",
            "A security review that asked where scanning happens in the pipeline.",
            "Teams delivering at very different speeds with no shared practice.",
            "A platform engineering initiative that needs a common baseline.",
        ],
        buyer="Head of engineering, platform lead, or the DevOps capability owner.",
        attendees="Engineers who already work in pipelines — developers and infrastructure people both.",
        objections=[
            ("We already do CI/CD.",
             "Most do, in one team. This is about the other seven teams, and the security and "
             "instrumentation that usually get skipped."),
            ("We are moving to GitHub, so a Microsoft DevOps course seems wrong.",
             "The exam covers both deliberately. That is precisely why it suits an organisation "
             "mid-migration."),
            ("DevOps is culture, not tooling.",
             "Agreed, and the first tenth of the exam is process and communication. The other "
             "ninety percent is the tooling that makes the culture possible."),
            ("Four days away from delivery is hard to justify.",
             "Count the hours currently spent on manual releases over a quarter and compare."),
        ],
        next=[
            "AZ-204 for developers who need the Azure side strengthened",
            "GH-200 and the GitHub track if they are standardising there",
            "SC-500 for pipeline and workload security",
            "A pipeline review on one of their real repositories",
        ]),
    ),
"AZ-500": dict(fam="azure", level="Intermediate", title="Microsoft Azure Security Technologies",
    url="https://learn.microsoft.com/credentials/certifications/azure-security-engineer/",
    sg="https://aka.ms/AZ500-StudyGuide", pa=True,
    blurb="Securing Azure: identity and access, platform protection, data and application security, and security operations.",
    who="Security engineers working in Azure. Pairs naturally with SC-300 on the identity side.",
    retired="31 August 2026",
    overview=(
        "Retired by Microsoft on 31 August 2026, along with its renewal assessments. It is "
        "listed here because a lot of people hold it and still need the context: the material "
        "covered securing identity and access, networking, compute, storage and databases in "
        "Azure, with a large final block on Defender for Cloud and Sentinel. Its replacement "
        "is SC-500, which keeps that ground and adds AI workloads."),
    prereq="Historical entry — the exam can no longer be taken.",
    challenges=[
        "Holders asking what happens to a certification that can no longer be renewed.",
        "Job descriptions and procurement documents that still ask for AZ-500 by name.",
        "Teams part-way through AZ-500 study when it was withdrawn.",
        "Training plans and budgets written around a course that no longer leads anywhere.",
        "Deciding whether existing holders go to SC-500 or elsewhere.",
    ],
    ),
"AZ-700": dict(fam="azure", level="Intermediate", title="Designing and Implementing Microsoft Azure Networking Solutions",
    url="https://learn.microsoft.com/credentials/certifications/azure-network-engineer-associate/",
    sg="https://aka.ms/az700-StudyGuide", pa=True,
    blurb="Azure networking in depth — hybrid connectivity, routing, load balancing, private access to services and network security.",
    who="Network engineers moving into Azure, and Azure admins who want the networking layer properly nailed down.",
    overview=(
        "The networking specialist exam, and the one that rescues most Azure projects that have "
        "quietly gone wrong. Core network infrastructure carries the largest share, then "
        "connectivity services — VPN, ExpressRoute, Virtual WAN — followed by application "
        "delivery, private access to Azure services, and network security. It is the deepest "
        "treatment of Azure networking Microsoft publishes."),
    duration="3 days", course="AZ-700T00", exam_time="100 minutes",
    prereq="AZ-104 level Azure experience plus real networking knowledge — routing, VPN and DNS.",
    challenges=[
        "Virtual networks created per project, now needing to reach each other and the data centre.",
        "Hub-and-spoke drawn on a whiteboard and implemented three different ways.",
        "Private endpoints and DNS resolution, which defeat more teams than anything else in Azure.",
        "ExpressRoute bought and underused because nobody designed around it.",
        "Traffic leaving Azure and coming back in because the routing was never thought through.",
    ],
    labs=dict(
        count=17,
        repo="https://github.com/MicrosoftLearning/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions",
        summary=("Seventeen exercises that build the network rather than describe it — virtual "
                 "networks, peering and routing, VPN and ExpressRoute connectivity, load "
                 "balancing and application delivery, private access and network security.")),
    selling=dict(
        pitch=("Most stalled Azure projects are networking problems wearing another costume. "
               "This is the three days that unblocks them."),
        triggers=[
            "A hybrid connectivity project that is late.",
            "Private endpoint or DNS resolution problems nobody can resolve.",
            "An ExpressRoute circuit that is paid for and underused.",
            "A landing zone design that needs implementing properly.",
            "Network engineers being asked to own Azure without Azure training.",
        ],
        buyer="Head of network or infrastructure. Sometimes the cloud programme, when connectivity is on the critical path.",
        attendees="Network engineers moving into Azure, and Azure administrators who have hit the networking ceiling.",
        objections=[
            ("Our network team knows networking.",
             "They do. Azure routing, private endpoints and DNS behave differently enough that "
             "traditional expertise can actively mislead."),
            ("It is only three days.",
             "It is the shortest specialist course here and the one with the highest hit rate "
             "on real, current problems."),
            ("AZ-104 covers networking already.",
             "At an introductory level. Everything hard — Virtual WAN, ExpressRoute, private "
             "DNS at scale — is in AZ-700."),
            ("We outsource our network.",
             "Then sell it to the partner, or to the person who has to review what the partner "
             "designed."),
        ],
        next=[
            "AZ-305 for the broader architecture around the network",
            "AZ-104 first if they lack the Azure grounding",
            "SC-500 for the network security side",
            "A landing zone review, which this course tends to generate demand for",
        ]),
    ),
"AZ-800": dict(fam="azure", level="Intermediate", title="Administering Windows Server Hybrid Core Infrastructure",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-800/",
    sg="https://aka.ms/AZ800-StudyGuide", pa=True,
    blurb="Windows Server where most of it actually lives: hybrid. Identity, compute, network infrastructure and storage across on-premises and Azure.",
    who="Windows Server administrators. Half of a pair — AZ-801 completes the hybrid administrator certification.",
    overview=(
        "Windows Server as it actually exists in most organisations: on-premises, connected to "
        "Azure, and not going away. Active Directory Domain Services across both worlds carries "
        "the biggest share, then managing servers and workloads in a hybrid setup, virtual "
        "machines and containers, hybrid networking, and storage and file services. It is the "
        "first half of a pair with AZ-801."),
    course="AZ-800T00",
    prereq="Real Windows Server administration experience, plus familiarity with Azure fundamentals.",
    challenges=[
        "A domain built in 2008 that everything depends on and nobody wants to touch.",
        "Hybrid identity working by accident, with no one certain how.",
        "File servers nobody has reviewed since the last migration.",
        "Azure adopted alongside a data centre that is staying, with no plan to connect them properly.",
        "Windows Server skills that stopped being refreshed around 2016.",
    ],
    labs=dict(
        count=21,
        repo="https://github.com/MicrosoftLearning/AZ-800-Administering-Windows-Server-Hybrid-Core-Infrastructure",
        guide="https://microsoftlearning.github.io/AZ-800-Administering-Windows-Server-Hybrid-Core-Infrastructure/",
        summary=("Twenty-one labs, the most in the AZ track. Identity services first, then "
                 "hybrid management, virtual machines and containers, networking, and storage "
                 "and file services.")),
    selling=dict(
        pitch=("Their data centre is not closing. This is the course for the half of the estate "
               "everyone stopped training for."),
        triggers=[
            "A hybrid estate with no plan to be fully cloud any time soon.",
            "An Active Directory nobody wants to modify.",
            "A Windows Server end-of-support date approaching.",
            "A team whose Windows Server training stopped several versions ago.",
            "Azure adoption that needs the on-premises side connected properly.",
        ],
        buyer="Infrastructure manager. Usually an easy sell, because the pain is long-standing and visible.",
        attendees="Windows Server administrators, including those who have been doing it for years without formal training.",
        objections=[
            ("We are moving to the cloud, Windows Server is legacy.",
             "Almost nobody finishes that journey. The hybrid period lasts years, and this is "
             "the course about managing it rather than wishing it away."),
            ("Our admins have run Windows Server for a decade.",
             "Then the gap is the hybrid half — Azure Arc, hybrid identity, cloud storage "
             "integration — which did not exist when they learned it."),
            ("Should we do AZ-800 or AZ-801?",
             "AZ-800 first, always. AZ-801 assumes it."),
            ("Is there still demand for Windows Server skills?",
             "Look at their own server list before answering that. Usually it answers itself."),
        ],
        next=[
            "AZ-801 as the second half — most customers buy both",
            "AZ-104 for the Azure side of the hybrid estate",
            "AZ-700 when the site-to-site connectivity is the problem",
            "An Active Directory health check, which pairs naturally",
        ]),
    ),
"AZ-801": dict(fam="azure", level="Advanced", title="Configuring Windows Server Hybrid Advanced Services",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-801/",
    sg="https://aka.ms/AZ801-StudyGuide", pa=True,
    blurb="The advanced half of the hybrid server track: security, high availability, disaster recovery, migration and troubleshooting.",
    who="Experienced Windows Server administrators. Take AZ-800 first.",
    overview=(
        "The second half of the Windows Server hybrid pair, and the more interesting one. "
        "Securing Windows Server on-premises and in hybrid, high availability, disaster "
        "recovery, migrating servers and workloads, and troubleshooting when it all goes wrong. "
        "Where AZ-800 is about running the estate, this is about hardening it, moving it and "
        "recovering it."),
    course="AZ-801T00",
    prereq="AZ-800 or equivalent. This one genuinely assumes the first half.",
    challenges=[
        "A disaster recovery plan that exists as a document and has never been tested.",
        "Servers overdue for migration, with nobody confident enough to move them.",
        "Windows Server hardening left at whatever the default was on install.",
        "Clustering and high availability configured once by someone who has since left.",
        "Troubleshooting by restart, because nobody has the diagnostic skills.",
    ],
    labs=dict(
        count=14,
        repo="https://github.com/MicrosoftLearning/AZ-801-Configuring-Windows-Server-Hybrid-Advanced-Services",
        guide="https://microsoftlearning.github.io/AZ-801-Configuring-Windows-Server-Hybrid-Advanced-Services/",
        summary=("Fourteen labs starting with securing Windows Server and moving through high "
                 "availability, disaster recovery, migration and troubleshooting — the work you "
                 "only want to do for the first time in a lab.")),
    selling=dict(
        pitch=("The disaster recovery plan they have never tested, and the migration they keep "
               "postponing. Both are in here."),
        triggers=[
            "A disaster recovery test that failed, or one that has never happened.",
            "A server migration that has slipped more than once.",
            "A security review flagging unhardened Windows Server estate.",
            "An end-of-support deadline forcing movement.",
            "They have already done AZ-800 — this is the natural follow-on.",
        ],
        buyer="Infrastructure manager, often with security or risk co-signing because of the recovery angle.",
        attendees="Experienced Windows Server administrators who have completed AZ-800 or equivalent.",
        objections=[
            ("We have backups, so disaster recovery is covered.",
             "Backups are not recovery until somebody has restored from them under time "
             "pressure. That distinction is most of this course."),
            ("Can we skip AZ-800 and come straight here?",
             "Not really. This one assumes the first half, and the room will split if half "
             "have it and half do not."),
            ("Migration is a one-off project, not a skill.",
             "They said that about the last three. Most estates migrate something every year."),
            ("Our hardening is handled by a managed service.",
             "Then someone still has to review what the provider did. This is the course that "
             "makes that review meaningful."),
        ],
        next=[
            "AZ-800 first if they have not done it",
            "SC-500 for the broader cloud security picture",
            "AZ-104 for the Azure half of the hybrid estate",
            "A disaster recovery test run as a workshop, which sells well after this",
        ]),
    ),
"AZ-900": dict(fam="azure", level="Beginner", title="Microsoft Azure Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/azure-fundamentals/",
    sg="https://aka.ms/AZ900-StudyGuide", pa=True,
    blurb="Cloud concepts, Azure architecture and services, and how management and governance work — plus pricing and support.",
    who="Anyone, technical or not, who needs a credible foundation in Azure. The most-taken Microsoft exam for a reason.",
    overview=(
        "The entry point, and the one most people in an organisation should sit before anything "
        "else. Cloud concepts first, then the largest block on Azure architecture and services, "
        "and finally management and governance — cost, policy and compliance. Nothing is built "
        "here. The purpose is that afterwards a mixed room can discuss an Azure project without "
        "talking past each other."),
    duration="1 day", course="AZ-900T00", exam_time="45 minutes",
    prereq="None whatsoever. It is written for people with no technical background.",
    challenges=[
        "A cloud migration being approved by people who cannot evaluate what they are approving.",
        "Procurement and finance teams facing consumption billing for the first time.",
        "Project managers running Azure work without the vocabulary for it.",
        "Technical staff from other platforms needing the map before the detail.",
        "A business case argued on assumptions nobody in the room can check.",
    ],
    labs=dict(
        count=5,
        repo="https://github.com/MicrosoftLearning/AZ-900-Microsoft-Azure-Fundamentals",
        guide="https://microsoftlearning.github.io/AZ-900-Microsoft-Azure-Fundamentals/",
        summary=("Five short guided exercises — creating a resource, and working through the "
                 "cost and governance tooling. Enough to make the portal real without turning "
                 "the day into an administration course.")),
    selling=dict(
        pitch=("One day that makes every later Azure conversation cheaper, because the whole "
               "room finally means the same thing by the same words."),
        triggers=[
            "A cloud programme about to start with a mixed audience.",
            "Finance or procurement meeting consumption-based billing for the first time.",
            "New joiners, or staff moving across from another platform.",
            "Sales and account teams who need to talk credibly about Azure.",
            "Pre-work bundled ahead of AZ-104 or AZ-305.",
        ],
        buyer="L&D, or the cloud programme manager. Cheap enough to approve without a business case.",
        attendees="Anyone — business stakeholders, project managers, finance, sales, and technical people wanting the map first.",
        objections=[
            ("Fundamentals is beneath our technical team.",
             "It is. Sell it for everyone around them, which is usually where the "
             "misunderstandings actually originate."),
            ("A 45-minute exam cannot be worth much.",
             "As a credential, modestly. As a shared vocabulary before a four-day course, it "
             "saves more time than it costs."),
            ("They can watch the free Learn modules.",
             "They can, and most will not. A booked day with five exercises is the difference "
             "between intending to and having done it."),
            ("We would rather go straight to AZ-104.",
             "If everyone has the background, do. If half the room does not, they will be lost "
             "by lunchtime on day one and will not say so."),
        ],
        next=[
            "AZ-104 as the standard next step for technical staff",
            "AZ-305 for the architecture-minded",
            "SC-900 for the same audience on the security side",
            "Sell per cohort rather than per person — this is the volume course",
        ]),
    ),

"DP-300": dict(fam="data", level="Intermediate", title="Administering Microsoft Azure SQL Solutions",
    url="https://learn.microsoft.com/credentials/certifications/azure-database-administrator-associate/",
    sg="https://aka.ms/dp300-StudyGuide", pa=True,
    blurb="Running SQL on Azure: planning and deploying, securing, monitoring, optimising performance and automating the routine work.",
    who="Database administrators bringing SQL Server skills onto the Azure platform."),
"DP-420": dict(fam="data", level="Advanced", title="Azure Cosmos DB Developer Specialty",
    url="https://learn.microsoft.com/credentials/certifications/azure-cosmos-db-developer-specialty/",
    sg="https://aka.ms/dp420-StudyGuide", pa=True,
    blurb="Designing and building cloud-native applications on Azure Cosmos DB — data modelling, partitioning, querying and tuning throughput.",
    who="Developers building on Cosmos DB. Genuinely specialised; partitioning design is where people come unstuck."),
"DP-600": dict(fam="data", level="Intermediate", title="Implementing Analytics Solutions Using Microsoft Fabric",
    url="https://learn.microsoft.com/credentials/certifications/fabric-analytics-engineer-associate/",
    sg="https://aka.ms/dp600-StudyGuide", pa=True,
    blurb="Designing and building analytics in Microsoft Fabric — preparing and modelling data, then delivering it so people can actually use it.",
    who="Analytics engineers and BI professionals. The natural step up from PL-300."),
"DP-700": dict(fam="data", level="Intermediate", title="Implementing Data Engineering Solutions Using Microsoft Fabric",
    url="https://learn.microsoft.com/credentials/certifications/fabric-data-engineer-associate/",
    sg="https://aka.ms/DP700-StudyGuide", pa=True,
    blurb="Data engineering in Fabric: ingesting and transforming at scale, managing the analytics lifecycle, and monitoring and optimising what you built.",
    who="Data engineers working in Fabric, comfortable with SQL, PySpark or KQL."),
"DP-900": dict(fam="data", level="Beginner", title="Microsoft Azure Data Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/azure-data-fundamentals/",
    sg="https://aka.ms/dp900-StudyGuide", pa=True,
    blurb="Core data concepts and how relational, non-relational and analytics workloads work on Azure.",
    who="Anyone starting in data. A sensible first step before DP-300, DP-600 or DP-700."),

"GH-100": dict(fam="github", level="Intermediate", title="GitHub Administration",
    url="https://learn.microsoft.com/credentials/certifications/github-administration/",
    sg="https://aka.ms/GH100-StudyGuide", pa=True,
    blurb="Administering GitHub at organisation and enterprise scale — authentication, permissions, policies, and keeping a large estate healthy.",
    who="Administrators responsible for a GitHub organisation or enterprise."),
"GH-200": dict(fam="github", level="Intermediate", title="GitHub Actions",
    url="https://learn.microsoft.com/credentials/certifications/github-actions/",
    sg="https://aka.ms/GH200-StudyGuide", pa=True,
    blurb="Automating with GitHub Actions: building workflows, managing secrets and runners, and packaging what you build so others can reuse it.",
    who="Developers and DevOps engineers automating their delivery pipeline in GitHub."),
"GH-300": dict(fam="github", level="Intermediate", title="GitHub Copilot",
    url="https://learn.microsoft.com/credentials/certifications/github-copilot/",
    sg="https://aka.ms/GH300-StudyGuide", pa=True,
    blurb="Using GitHub Copilot well — prompt and context craft, the features across plans, plus privacy, content exclusions and responsible use.",
    who="Developers and technology managers rolling Copilot out to a team."),
"GH-500": dict(fam="github", level="Intermediate", title="GitHub Advanced Security",
    url="https://learn.microsoft.com/credentials/certifications/github-advanced-security/",
    sg="https://aka.ms/GH500-StudyGuide", pa=True,
    blurb="Securing the software supply chain with code scanning, secret scanning and dependency review — configuring them and acting on what they find.",
    who="Security-minded engineers and AppSec teams working in GitHub."),
"GH-900": dict(fam="github", level="Beginner", title="GitHub Foundations",
    url="https://learn.microsoft.com/credentials/certifications/github-foundations/",
    sg="https://aka.ms/GH900-StudyGuide", pa=True,
    blurb="The fundamentals of GitHub: repositories, collaboration through issues and pull requests, and how the platform fits together.",
    who="Anyone new to GitHub. The right starting point before GH-100, GH-200, GH-300 or GH-500."),

"MB-230": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Customer Service Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/exams/mb-230/",
    sg="https://aka.ms/MB230-StudyGuide", pa=True,
    blurb="Configuring Dynamics 365 Customer Service — cases, queues, entitlements, SLAs, knowledge management and the analytics on top.",
    who="Functional consultants implementing customer service solutions."),
"MB-240": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Field Service Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/exams/mb-240/",
    sg="https://aka.ms/MB240-StudyGuide", pa=True,
    blurb="Field Service end to end: work orders, scheduling and dispatch, inventory, assets and the mobile experience technicians actually use.",
    who="Functional consultants delivering field service implementations."),
"MB-280": dict(fam="dynamics", level="Intermediate", title="Dynamics 365 Customer Experience Analyst",
    url="https://learn.microsoft.com/credentials/certifications/d365-customer-experience-analyst-associate/",
    sg="https://aka.ms/MB280-StudyGuide", pa=True,
    blurb="Configuring the customer experience apps — sales, customer insights and the journeys that connect marketing to selling.",
    who="Consultants and analysts working across Dynamics 365 Sales and Customer Insights."),
"MB-310": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Finance Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/d365-functional-consultant-financials/",
    sg="https://aka.ms/mb310-StudyGuide", pa=True,
    blurb="Implementing Dynamics 365 Finance: ledgers, receivables and payables, budgeting, fixed assets and financial close.",
    who="Functional consultants with a finance background."),
"MB-330": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Supply Chain Management Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/d365-functional-consultant-supply-chain-management/",
    sg="https://aka.ms/mb330-StudyGuide", pa=True,
    blurb="Supply chain in Dynamics 365 — products and inventory, procurement, sales, warehousing and manufacturing.",
    who="Functional consultants implementing supply chain and manufacturing processes."),
"MB-500": dict(fam="dynamics", level="Intermediate", title="Dynamics 365: Finance and Operations Apps Developer",
    url="https://learn.microsoft.com/credentials/certifications/d365-finance-and-operations-apps-developer-associate/",
    sg="https://aka.ms/mb500-StudyGuide", pa=True,
    blurb="Extending the finance and operations apps — X++ development, data models, integrations and the application lifecycle around them.",
    who="Developers customising Dynamics 365 Finance and Operations."),
"MB-800": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Business Central Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/d365-business-central-functional-consultant-associate/",
    sg="https://aka.ms/MB800-StudyGuide", pa=True,
    blurb="Setting up and configuring Business Central — company setup, financials, purchasing, sales and inventory for smaller organisations.",
    who="Functional consultants delivering Business Central to SMB customers."),
"MB-820": dict(fam="dynamics", level="Intermediate", title="Microsoft Dynamics 365 Business Central Developer",
    url="https://learn.microsoft.com/credentials/certifications/d365-business-central-developer-associate/",
    sg="https://aka.ms/mb820-StudyGuide", pa=True,
    blurb="Building extensions for Business Central in AL — data and interface objects, integrations, testing and deployment.",
    who="Developers extending Business Central. MB-800 knowledge helps a great deal."),

"MD-102": dict(fam="m365", level="Intermediate", title="Managing and Securing Microsoft 365 Endpoints by using Intune",
    url="https://learn.microsoft.com/credentials/certifications/modern-desktop/",
    sg="https://aka.ms/md102-StudyGuide", pa=True,
    blurb="Managing and securing endpoints with Intune — deployment, identity and compliance, applications, and protecting the device fleet.",
    who="Endpoint and desktop administrators. The Intune exam, in practice.",
    overview=(
        "The Intune exam, and the one that has changed name to match what it actually is — "
        "Microsoft renamed it to 'Managing and Securing Microsoft 365 Endpoints by using "
        "Intune'. Preparing the infrastructure first, then the bulk of it: enrolling, managing "
        "and maintaining devices, protecting them, and managing the applications on them. The "
        "last tenth is automation, monitoring and reporting, which is what separates an estate "
        "that runs itself from one that needs a person."),
    duration="5 days", course="MD-102T00", exam_time="100 minutes",
    prereq="Microsoft 365 administration experience and real-world device management background.",
    challenges=[
        "A device estate half in Configuration Manager and half in Intune, with no agreed "
        "finishing line for the migration.",
        "Enrolment that works for corporate laptops and falls apart for anything personal.",
        "Compliance policies written once, never reviewed, and now blocking people silently.",
        "Application packaging and deployment that still depends on one person's knowledge.",
        "No reporting anyone trusts, so nobody can say how many devices are actually healthy.",
    ],
    labs=dict(
        count=7,
        repo="https://github.com/MicrosoftLearning/MD-102T00-Microsoft-365-Endpoint-Administrator",
        summary=("Seven labs including the environment setup, working through enrolment, "
                 "configuration and compliance policies, protection and application "
                 "management on a tenant that is not production.")),
    selling=dict(
        pitch=("Everyone has Intune in the licence. This is the course that gets them off "
               "Configuration Manager and onto it properly."),
        triggers=[
            "A Configuration Manager to Intune migration that has stalled halfway.",
            "Windows Autopilot being considered, or attempted and abandoned.",
            "A move to hybrid or remote working that has exposed device management gaps.",
            "BYOD or contractor devices needing access without full management.",
            "An endpoint security review that found inconsistent compliance policies.",
        ],
        buyer="Head of end-user computing or IT operations manager. Device management budgets are usually easy to locate.",
        attendees="Endpoint and desktop administrators, and infrastructure people inheriting Intune.",
        objections=[
            ("We already use Intune.",
             "Most organisations use about a third of it. Autopilot, application protection "
             "and the reporting side are where the gaps usually are."),
            ("Five days is long for a device course.",
             "It is the broadest exam in the M365 track. If the estate is small, the first "
             "three days carry most of the value — worth discussing."),
            ("Our Configuration Manager works fine.",
             "Then co-management is the conversation, and it is covered. Nobody is asking "
             "them to switch everything off on a Friday."),
            ("Is this not the same as MS-102?",
             "No overlap worth worrying about. MS-102 is the tenant; MD-102 is the devices on it."),
        ],
        next=[
            "MS-102 for the tenant layer above the devices",
            "SC-300 when conditional access becomes the sticking point",
            "AB-650 once Copilot reaches those managed endpoints",
            "An Autopilot pilot run as a workshop on their own hardware",
        ]),
    ),
"MS-102": dict(fam="m365", level="Intermediate", title="Microsoft 365 Administrator",
    url="https://learn.microsoft.com/credentials/certifications/exams/ms-102/",
    sg="https://aka.ms/MS102-StudyGuide", pa=True,
    blurb="Running a Microsoft 365 tenant: deployment, identity and access with Microsoft Entra, threat protection and compliance.",
    who="Microsoft 365 administrators. The backbone certification for the M365 platform.",
    overview=(
        "The backbone certification for anyone running Microsoft 365. It splits almost evenly "
        "across four areas: deploying and managing the tenant, Entra identity and access, "
        "security and threat management with Defender XDR — which carries the biggest single "
        "share — and compliance with Purview. It is the exam that proves somebody can be "
        "handed a tenant and keep it running safely."),
    duration="5 days", course="MS-102T00",
    prereq="Working knowledge of Microsoft 365 workloads, DNS, and general networking and identity concepts.",
    challenges=[
        "A tenant configured during a migration years ago and never reviewed since.",
        "Security defaults left wherever they landed, because nobody owns them.",
        "Defender XDR licensed and largely unused, so alerts go to an inbox nobody reads.",
        "Compliance obligations acknowledged in a policy document and nowhere in the tenant.",
        "One person who understands the tenant, and a succession problem nobody has named.",
    ],
    labs=dict(
        count=25,
        repo="https://github.com/MicrosoftLearning/MS-102T00-Microsoft-365-Administrator-Essentials",
        summary=("Twenty-five lab exercises starting from initialising a tenant and building "
                 "out through identity, Defender XDR and Purview — the most thorough lab set "
                 "in the Microsoft 365 track.")),
    selling=dict(
        pitch=("If one person in their organisation understands the tenant, this is the "
               "course that fixes the bus-factor problem."),
        triggers=[
            "A tenant inherited from a migration partner with no handover.",
            "One administrator who holds all the Microsoft 365 knowledge.",
            "An E5 or Defender investment that is barely used.",
            "A compliance or insurance questionnaire they struggled to answer.",
            "New administrators joining who need a common grounding.",
        ],
        buyer="IT manager or head of IT operations. Straightforward to approve — the role is unambiguous.",
        attendees="Microsoft 365 administrators, and infrastructure staff taking on tenant responsibility.",
        objections=[
            ("Our admins run Microsoft 365 every day.",
             "They run the parts their tickets touch. The Defender XDR third and the Purview "
             "tenth are usually where the unexamined risk sits."),
            ("Five days is a long time.",
             "Four areas, all weighted. It is genuinely a week's worth, and splitting it "
             "across two blocks works well for small teams."),
            ("We have a managed service provider for this.",
             "Then someone internal still needs to review what the provider does. This is the "
             "course that makes that review meaningful rather than ceremonial."),
            ("Is MS-102 still current?",
             "Yes, and the lab repository was updated this month. Worth saying, because people "
             "remember the retired MS-100 and MS-101 pair."),
        ],
        next=[
            "MD-102 for the device layer",
            "SC-300 for identity in proper depth",
            "SC-401 for the compliance half taken seriously",
            "AB-650 once Copilot and agents land in that tenant",
        ]),
    ),
"MS-700": dict(fam="m365", level="Intermediate", title="Managing Microsoft Teams",
    url="https://learn.microsoft.com/credentials/certifications/m365-teams-administrator-associate/",
    sg="https://aka.ms/ms700-StudyGuide", pa=True,
    blurb="Planning and configuring Teams — governance and lifecycle, chat and collaboration, meetings and the settings that keep it manageable.",
    who="Teams administrators and M365 admins who own collaboration.",
    overview=(
        "Running Teams as a platform rather than using it as an app. Configuring and managing "
        "the Teams environment is nearly half the exam on its own, then governance of teams, "
        "channels, chats and apps, then meetings and calling, and finally monitoring and "
        "troubleshooting. Voice gets a look here; MS-721 is where it is covered properly."),
    duration="4 days", course="MS-700T00", exam_time="100 minutes",
    prereq="Microsoft 365 administration experience, and familiarity with how Teams sits on top of it.",
    challenges=[
        "Teams sprawl — thousands of teams, no naming standard, no lifecycle, nobody deleting.",
        "Guest and external access configured by whoever needed it most urgently.",
        "Meeting policies applied tenant-wide because per-group policy was never set up.",
        "Call quality complaints that nobody can actually investigate.",
        "Apps installed by users with no governance over what they can reach.",
    ],
    labs=dict(
        count=4,
        repo="https://github.com/MicrosoftLearning/MS-700-Managing-Microsoft-Teams",
        summary=("Four substantial labs covering the Teams environment, governance of teams "
                 "and channels, policy management, and the monitoring and troubleshooting "
                 "tooling.")),
    selling=dict(
        pitch=("Teams got deployed in a hurry and nobody has governed it since. That is the "
               "conversation."),
        triggers=[
            "Teams sprawl with no lifecycle policy and a growing storage bill.",
            "Guest access questions from security that nobody can answer confidently.",
            "Call or meeting quality complaints with no diagnostic process.",
            "A Teams Premium or Copilot rollout that assumes the basics are in order.",
            "Compliance asking about retention on chats and channels.",
        ],
        buyer="Collaboration lead, or the Microsoft 365 owner. Sometimes funded from a workplace experience programme.",
        attendees="Teams administrators and Microsoft 365 admins who have inherited collaboration.",
        objections=[
            ("Teams manages itself.",
             "Until the first legal hold, the first guest-access audit, or the first storage "
             "bill nobody budgeted for."),
            ("We only need the voice part.",
             "Then MS-721 is the better fit and will save them a day. Worth asking before "
             "quoting this one."),
            ("Our users are happy with Teams.",
             "Good — this is not a user course. It is for the person who has to answer "
             "security and compliance about it."),
            ("Four days for one application?",
             "Teams is not one application. It is SharePoint, Exchange, Entra groups and a "
             "voice platform wearing a single icon."),
        ],
        next=[
            "MS-721 for the voice and meeting room depth",
            "MS-102 for the tenant underneath it",
            "SC-401 when retention and eDiscovery come up",
            "A Teams governance review on their own tenant",
        ]),
    ),
"MS-721": dict(fam="m365", level="Advanced", title="Collaboration Communications Systems Engineer",
    url="https://learn.microsoft.com/credentials/certifications/m365-collaboration-communications-systems-engineer/",
    sg="https://aka.ms/MS721-StudyGuide", pa=True,
    blurb="Teams Phone, meetings and meeting rooms — voice routing, certified devices, and troubleshooting call quality when it goes wrong.",
    who="Engineers responsible for voice and meeting rooms. Telephony experience is a real advantage.",
    overview=(
        "The voice and meeting rooms specialism, and the most niche exam we teach. Teams Phone "
        "carries the largest share, then planning and designing the overall system, then "
        "Teams Rooms and devices, and meetings, webinars and town halls. It assumes real "
        "telephony background — this is not a Teams administration course with a phone chapter "
        "bolted on."),
    duration="5 days", course="MS-721T00", exam_time="100 minutes",
    prereq="Telephony experience is close to essential, plus Teams administration (MS-700 level).",
    challenges=[
        "A PSTN migration where the old PBX contract ends before the new system is ready.",
        "Direct Routing, Operator Connect or Calling Plans — a decision with long consequences "
        "made on incomplete information.",
        "Meeting rooms bought per office, each configured differently, none monitored.",
        "Emergency calling and location requirements that nobody has properly read.",
        "Call quality problems that turn out to be network problems, and vice versa.",
    ],
    labs=dict(
        count=7,
        repo="https://github.com/MicrosoftLearning/MS-721T00-Collaboration-Communications-Systems-Engineer",
        summary=("Seven labs including setup, covering Teams Phone configuration, call "
                 "routing, meeting and event management, and the Teams Rooms device estate.")),
    selling=dict(
        pitch=("Their PBX contract is ending and somebody has to make Teams Phone work. "
               "Very few people can."),
        triggers=[
            "A PBX or telephony contract approaching renewal.",
            "An office refit or move that includes meeting rooms.",
            "Teams Phone bought and only partly rolled out.",
            "Emergency calling or regulatory requirements raised by legal.",
            "Persistent call quality complaints with no owner.",
        ],
        buyer="Head of unified communications or infrastructure. Often attached to a telephony project budget rather than training.",
        attendees="Engineers responsible for voice and meeting rooms. Telephony background strongly assumed.",
        objections=[
            ("Our telephony is outsourced.",
             "Then sell it to the provider, or to whoever has to specify and review their "
             "work. Someone internal still signs off the design."),
            ("MS-700 covers calling already.",
             "It touches it. Teams Phone alone is a third of MS-721, and Direct Routing is "
             "barely visible in MS-700."),
            ("This is very specialised for five days.",
             "It is, and that is the point — the specialists are rare and the projects are "
             "expensive to get wrong."),
            ("We are not ready to move off our PBX.",
             "Then the planning and design content is exactly the right preparation. Better "
             "trained before the decision than after."),
        ],
        next=[
            "MS-700 first if the Teams administration grounding is missing",
            "AZ-700 when the call quality problems turn out to be the network",
            "MS-102 for the tenant underneath",
            "A Teams Phone design workshop ahead of their migration",
        ]),
    ),

"PL-200": dict(fam="power", level="Intermediate", title="Microsoft Power Platform Functional Consultant",
    url="https://learn.microsoft.com/credentials/certifications/exams/pl-200/",
    sg="https://aka.ms/PL200-StudyGuide", pa=True,
    blurb="Configuring Dataverse, building apps and automations, and delivering a working Power Platform solution end to end.",
    who="Functional consultants and makers who configure more than they code."),
"PL-300": dict(fam="power", level="Intermediate", title="Microsoft Power BI Data Analyst",
    url="https://learn.microsoft.com/credentials/certifications/data-analyst-associate/",
    sg="https://aka.ms/pl300-StudyGuide", pa=True,
    blurb="Preparing, modelling and visualising data in Power BI — including the DAX and the model design that separate a report from a good report.",
    who="Analysts working in Power BI. One of the most useful certifications on this list for everyday work."),
"PL-400": dict(fam="power", level="Intermediate", title="Microsoft Power Platform Developer",
    url="https://learn.microsoft.com/credentials/certifications/power-platform-developer-associate/",
    sg="https://aka.ms/PL400-StudyGuide", pa=True,
    blurb="Extending Power Platform with code — plug-ins, custom connectors, client scripting and integrations beyond what configuration reaches.",
    who="Developers working alongside functional consultants on Power Platform projects."),
"PL-900": dict(fam="power", level="Beginner", title="Microsoft Power Platform Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/power-platform-fundamentals/",
    sg="https://aka.ms/PL900-StudyGuide", pa=True,
    blurb="What Power Platform is and what each part does — Power Apps, Power Automate, Power BI, Power Pages and Copilot Studio.",
    who="Anyone starting with Power Platform, including business users who will build their first app."),

"SC-100": dict(fam="security", level="Advanced", title="Microsoft Cybersecurity Architect",
    url="https://learn.microsoft.com/credentials/certifications/exams/sc-100/",
    sg="https://aka.ms/SC100-StudyGuide", pa=True,
    blurb="Designing a Zero Trust security strategy — architecture across identity, data, applications and infrastructure, and the governance around it.",
    who="Security architects. Expect one of SC-200, SC-300, AZ-500 or MS-102 behind you; this exam assumes that ground is covered.",
    overview=(
        "The architect exam of the SC track. It is not about configuring anything — it is about "
        "deciding what an organisation should do, and defending that in front of the people who "
        "have to fund it. Strategy and Zero Trust framing first, then designs for security "
        "operations, identity and compliance, for infrastructure, and for applications and data. "
        "The four areas are weighted almost evenly, so there is nowhere to hide."),
    duration="4 days", course="SC-100T00",
    prereq=("An associate-level security certification first — SC-200, SC-300, AZ-500 or "
            "equivalent experience. This exam assumes you have already done the implementing."),
    challenges=[
        "A board that has bought Zero Trust as a phrase and needs it turned into a sequence of "
        "funded projects.",
        "Security tooling bought department by department, now overlapping in places and "
        "leaving gaps nobody owns.",
        "Designing for an estate that will still be hybrid in five years, rather than the "
        "cloud-only diagram everyone draws.",
        "Turning a regulatory obligation into technical controls somebody can actually build "
        "and evidence.",
        "Being the person who has to say out loud which risks the organisation is choosing "
        "to accept.",
    ],
    labs=dict(
        count=12,
        repo="https://github.com/MicrosoftLearning/SC-100-Microsoft-Cybersecurity-Architect",
        guide="https://microsoftlearning.github.io/SC-100-Microsoft-Cybersecurity-Architect/",
        summary=("Twelve lab exercises — lighter on clicking than the associate courses, because "
                 "this is a design exam. They cover compliance assessment, Entra ID policy and "
                 "conditional access, B2B collaboration and the rest of the estate.")),
    selling=dict(
        pitch=("Their security team can build anything. This is for the person who has to "
               "decide what gets built, and in what order."),
        triggers=[
            "A Zero Trust programme that exists on a slide and nowhere else.",
            "Overlapping security products bought over three years, with no one able to say "
            "which owns what.",
            "A regulator, insurer or major customer has asked to see a security architecture.",
            "Their best SC-200 and SC-300 people are ready for the next step and will leave if "
            "they do not get it.",
            "A breach or near miss has the board asking who is actually designing this.",
        ],
        buyer="CISO or head of security architecture. Budget usually sits with security rather than IT training.",
        attendees="Security architects and senior engineers moving up. Check the prerequisite certification before booking the exam.",
        objections=[
            ("Our architects do not need a Microsoft course.",
             "Fair if their estate is not Microsoft. If it is, this is the only place the "
             "reference architectures and the licensing reality get taught together."),
            ("Four days of theory is a lot.",
             "It is four days of design decisions with twelve labs attached. The judgement is "
             "the product here — architects are not paid for clicks."),
            ("Could they not just repeat SC-200 or SC-300?",
             "Those teach implementing. If the gap is that nobody owns the overall design, "
             "another associate course will not close it."),
            ("Can one person really architect all of this?",
             "No, and the course says as much. What it gives them is a shared frame, so the "
             "identity, SecOps and data people are designing the same system."),
        ],
        next=[
            "SC-200 and SC-300 for the team who will implement the design",
            "SC-500 once the design reaches Azure workloads and AI",
            "SC-401 for the data protection half of it",
            "A design review on their own architecture — usually an easier sell than a second course",
        ])),
"SC-200": dict(fam="security", level="Intermediate", title="Microsoft Security Operations Analyst",
    url="https://learn.microsoft.com/credentials/certifications/security-operations-analyst/",
    sg="https://aka.ms/SC200-StudyGuide", pa=True,
    blurb="Threat detection and response with Defender XDR and Microsoft Sentinel — mitigating threats and hunting for what the alerts missed.",
    who="SOC analysts and security engineers. KQL is worth practising before you sit it.",
    overview=(
        "The day job of a security operations analyst, in exam form. Running the environment "
        "carries the largest share — Defender XDR, Sentinel, the connectors and the rules that "
        "decide what you ever get told about. Then responding to incidents across identity, "
        "endpoint, email and cloud, and finally proactive hunting for the things no rule "
        "caught. KQL runs underneath all three."),
    duration="4 days", course="SC-200T00", exam_time="100 minutes",
    prereq=("Comfortable with Microsoft 365 and Azure, and willing to write KQL. Do not send "
            "somebody who has never queried anything."),
    challenges=[
        "An alert queue nobody can get to the bottom of, so the real incident waits behind "
        "forty false positives.",
        "Sentinel deployed, ingesting expensively, and tuned by nobody since go-live.",
        "An incident that crosses identity, endpoint and email, handled by three people who "
        "each see a third of it.",
        "Analysts who can read a dashboard but cannot write the query that answers the actual "
        "question.",
        "No hunting at all — a SOC that is entirely reactive and only finds what the vendor "
        "wrote a rule for.",
    ],
    labs=dict(
        count=25,
        repo="https://github.com/MicrosoftLearning/SC-200T00A-Microsoft-Security-Operations-Analyst",
        summary=("Twenty-five lab exercises, the most hands-on course in the SC track. They "
                 "run from exploring Defender XDR and Security Copilot, through deploying "
                 "Defender for Endpoint and Purview Audit, into Sentinel and the hunting work.")),
    selling=dict(
        pitch=("They are paying for Sentinel and Defender already. This is the course that "
               "makes the SOC actually use them."),
        triggers=[
            "Sentinel costs are rising and nobody can explain what the ingestion is buying.",
            "An incident took days longer than it should have, and the review blamed tooling.",
            "They are building a SOC in-house, or taking one back from an MSSP.",
            "Analysts are reading dashboards because they cannot write KQL.",
            "Security Copilot has arrived and the team do not know where it fits.",
        ],
        buyer="SOC manager or head of security operations; sometimes the MSSP running the service on their behalf.",
        attendees="SOC analysts at tiers one and two, security engineers, and incident responders.",
        objections=[
            ("Our analysts learn on the job.",
             "They learn the alerts they happen to see. The twenty-five labs cover the "
             "incidents they have not had yet, which is the point of training."),
            ("We use a different SIEM.",
             "Then the Sentinel days are less relevant, but Defender XDR is where the signal "
             "originates either way. Worth checking which half they actually need."),
            ("Four days off the rota is impossible.",
             "That is the real objection, and it is why this one sells as two blocks of two "
             "days more often than as a solid week."),
            ("KQL looks intimidating for our tier one.",
             "It is taught from scratch here, and it is the single skill that most changes "
             "what a tier one analyst can do unaided."),
        ],
        next=[
            "SC-100 for the analyst ready to move into architecture",
            "SC-300 when the incidents keep turning out to be identity incidents",
            "SC-500 for the Azure workload side of the estate",
            "A KQL day, which sells well on its own to the same team",
        ])),
"SC-300": dict(fam="security", level="Intermediate", title="Microsoft Identity and Access Administrator",
    url="https://learn.microsoft.com/credentials/certifications/identity-and-access-administrator/",
    sg="https://aka.ms/sc300-StudyGuide", pa=True,
    blurb="Microsoft Entra in depth — identity lifecycle, authentication and conditional access, application access and identity governance.",
    who="Identity administrators. Identity is the control plane, which makes this one of the highest-leverage certifications here.",
    overview=(
        "Microsoft Entra, properly. The identity lifecycle and how accounts actually get "
        "created and removed, then authentication and conditional access — the largest single "
        "block. After that two areas people routinely underestimate: workload identities, now "
        "that applications and agents need identities of their own, and identity governance, "
        "which is where access reviews and entitlement management live. Four areas, evenly "
        "weighted."),
    duration="4 days", course="SC-300T00", exam_time="100 minutes",
    prereq="Working knowledge of Microsoft 365 and Azure administration, and of directory concepts.",
    challenges=[
        "Leavers who still have access months later, because joining is automated and leaving "
        "is an email.",
        "Conditional access grown one exception at a time, until nobody dares change a policy.",
        "Service principals and app registrations created years ago by people who have left, "
        "holding permissions nobody has reviewed.",
        "An auditor asking who approved a given person's access, and the answer taking a week "
        "to assemble.",
        "Privileged accounts standing permanently, because just-in-time access was always "
        "next quarter's project.",
    ],
    labs=dict(
        count=29,
        repo="https://github.com/MicrosoftLearning/SC-300-Identity-and-Access-Administrator",
        summary=("Twenty-nine lab exercises including environment setup — the most thorough "
                 "lab set in the track. Roles and tenant properties, group-based licensing, "
                 "authentication methods, conditional access, application access and the "
                 "governance features on top.")),
    selling=dict(
        pitch=("Identity is the control plane. This is the course that stops it being the "
               "weakest part of their security."),
        triggers=[
            "An audit or penetration test has flagged standing privileged access.",
            "A joiner-mover-leaver process that works on the way in and not on the way out.",
            "Conditional access policies nobody wants to touch in case something breaks.",
            "They have bought Entra ID P2 and use almost none of it.",
            "Agents and workload identities are arriving and the identity team has no plan.",
        ],
        buyer="Head of identity, IAM lead, or the IT manager who owns Entra. Security often co-funds it.",
        attendees="Identity and access administrators, Microsoft 365 administrators who own Entra, and security engineers on the identity side.",
        objections=[
            ("We already do identity — our admins create accounts every day.",
             "Creating accounts is the first fifth. Workload identities and governance are "
             "where the audit findings come from, and those are half this exam."),
            ("Entra changes constantly.",
             "It does, which is why the structure matters more than the screenshots. The lab "
             "repo is maintained and was updated this month."),
            ("Our identity is still mostly on-premises.",
             "Then hybrid identity is exactly the conversation, and it is covered. The course "
             "does not assume they are cloud-only."),
            ("Is this not just AZ-104 again?",
             "AZ-104 touches Entra. This one spends four days inside it, including the "
             "governance that AZ-104 never reaches."),
        ],
        next=[
            "SC-100 for the architect-level view above it",
            "SC-401 when the conversation turns to what those identities can reach",
            "AB-650 once agents need identities and lifecycle of their own",
            "An access review workshop on their own tenant",
        ])),
"SC-401": dict(fam="security", level="Intermediate", title="Information Security Administrator",
    url="https://learn.microsoft.com/credentials/certifications/information-security-administrator/",
    sg="https://aka.ms/SC401-StudyGuide", pa=True,
    blurb="Protecting data with Microsoft Purview — information protection, data loss prevention, insider risk and retention.",
    who="Administrators who own data protection and compliance. The successor to the old SC-400.",
    overview=(
        "Microsoft Purview, in the era where Copilot can read everything a user can. Three "
        "evenly weighted blocks: classifying and labelling information, stopping it leaving "
        "and deciding how long it is kept, and then the detection side — insider risk, alerts "
        "and activity. The official course title now says 'in the AI era', which is an honest "
        "description of why this exam has got busier."),
    duration="4 days", course="SC-401T00", exam_time="100 minutes",
    prereq="Microsoft 365 administration experience and a working grasp of compliance concepts.",
    challenges=[
        "Sensitive data nobody can locate, in a tenant that has been accumulating since 2016.",
        "A labelling scheme designed by committee that users bypass within a week.",
        "DLP policies in audit mode for two years because nobody dares turn enforcement on.",
        "Retention obligations that conflict — legal wants it kept, privacy wants it gone.",
        "Copilot turning a decade of quiet oversharing into answers somebody can read today.",
    ],
    labs=dict(
        count=14,
        repo="https://github.com/MicrosoftLearning/SC-401T00-Information-Security-Administrator",
        summary=("Fourteen lab exercises including setup. Compliance roles first, then "
                 "sensitive information types and sensitivity labels, and on into data loss "
                 "prevention, retention and the risk and alerting work.")),
    selling=dict(
        pitch=("Copilot has made their oversharing visible. This is the course that gives "
               "somebody the tools to fix it."),
        triggers=[
            "A Copilot rollout paused or slowed over what it might surface.",
            "An audit, NIS2 or ISO review asking where sensitive data actually lives.",
            "DLP sitting in audit mode indefinitely because the false positives were never tuned.",
            "A near miss — data shared externally that should not have been.",
            "They bought E5 or a compliance add-on and use a fraction of Purview.",
        ],
        buyer="Compliance lead, data protection officer, or the CISO. Legal sometimes has a view and occasionally the budget.",
        attendees="Microsoft 365 and compliance administrators, and the security people who have inherited Purview.",
        objections=[
            ("We have DLP already.",
             "Most organisations have DLP in audit mode. The gap is usually tuning and "
             "enforcement, which is a third of this exam."),
            ("Purview is enormous — can four days cover it?",
             "It covers the three areas the exam weights evenly. eDiscovery and the deeper "
             "records management are a separate conversation, and worth saying so."),
            ("Our data is a mess, training will not fix that.",
             "True. The course gives them the classification and labelling approach to work "
             "through it — and the honest answer is that it is a programme, not a week."),
            ("Can the security team not pick this up?",
             "They can, but it is usually a different person. Purview rewards someone who "
             "will own it continuously rather than visit it after an incident."),
        ],
        next=[
            "SC-500 for the Azure and AI workload security around it",
            "SC-300 when the findings turn out to be access problems",
            "AB-650 for the Copilot administration side",
            "A data discovery exercise on their own tenant, which often funds the training",
        ])),
"SC-500": dict(fam="security", level="Intermediate", title="Implementing End-to-End Security Controls for Cloud and AI Workloads",
    url="https://learn.microsoft.com/credentials/certifications/cloud-and-ai-security-engineer-associate/",
    sg="https://aka.ms/SC500-StudyGuide", pa=False,
    blurb="Security across the whole estate rather than one product: identity and governance, storage, databases and networking, compute, and the platforms AI workloads actually run on.",
    who="Security engineers working across Azure and Microsoft 365 who now have AI workloads to protect as well. Earns the Cloud and AI Security Engineer Associate certification.",
    overview=(
        "The successor to AZ-500, widened to take in AI workloads. Four evenly weighted areas: "
        "identity, access and governance; securing storage, databases and networking; securing "
        "compute; and managing security posture across the lot. The AI part is not a bolt-on "
        "module — it runs through the whole thing, because the platforms AI runs on are the "
        "same platforms you were already securing."),
    duration="4 days", course="SC-500T00", exam_time="120 minutes",
    prereq=("Hands-on administration of Azure and hybrid environments — compute, network and "
            "storage — plus strong Microsoft Entra ID and some Microsoft 365."),
    challenges=[
        "An Azure estate grown by project teams, where nobody can say what is exposed today.",
        "AI workloads deployed by developers into subscriptions the security team does not watch.",
        "Posture tools producing hundreds of recommendations and no agreed order to fix them.",
        "Network and storage controls configured once at build time and never revisited.",
        "AZ-500 holders whose certification is retiring, and who need the path forward.",
    ],
    selling=dict(
        pitch=("AZ-500 is going away and their Azure estate now runs AI. This is the "
               "replacement, and it covers both."),
        triggers=[
            "They hold AZ-500 certifications and have heard it is being retired.",
            "AI or Foundry workloads have appeared in Azure and security was not consulted.",
            "A cloud security posture review produced a backlog nobody has prioritised.",
            "They are hiring Azure security engineers and need a common standard.",
            "An SC-100 architecture has been signed off and now needs implementing in Azure.",
        ],
        buyer="Head of cloud or cloud security lead. Often funded from the cloud programme rather than training.",
        attendees="Azure security engineers, cloud engineers taking on security, and AZ-500 holders moving across.",
        objections=[
            ("We will wait, it is still in beta.",
             "Beta applies to the exam, not the controls. Train now and certify when it goes "
             "generally available — the Azure work is live either way."),
            ("Our people already hold AZ-500.",
             "Then this is the natural transition, and the AI and posture material is new "
             "ground rather than revision."),
            ("There is no practice assessment yet.",
             "Correct, and worth saying up front. Microsoft usually publishes one within a "
             "couple of months of an exam leaving beta."),
            ("We do not have AI workloads yet.",
             "Three quarters of it is Azure security you need regardless. The AI content is "
             "the part that stops this being out of date in a year."),
        ],
        next=[
            "SC-100 for the architecture layer above it",
            "SC-401 when the data inside those workloads needs protecting",
            "SC-200 for the team who will respond to what the posture tooling finds",
            "An Azure security posture review delivered alongside the course",
        ])),
"SC-900": dict(fam="security", level="Beginner", title="Microsoft Security, Compliance, and Identity Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/security-compliance-and-identity-fundamentals/",
    sg="https://aka.ms/sc900-StudyGuide", pa=True,
    blurb="The vocabulary and the map: security and compliance concepts, and what each Microsoft security, identity and compliance capability is for.",
    who="Anyone before starting the SC track — and business stakeholders who need to follow the conversation.",
    overview=(
        "The map of the territory, in a day. Core security, compliance and identity concepts, "
        "then what each part of the Microsoft portfolio is actually for — Entra, the Defender "
        "family, and the compliance side. The security capabilities carry the biggest share. "
        "Nobody configures anything here; the point is that afterwards a mixed room can have "
        "the same conversation using the same words."),
    duration="1 day", course="SC-900T00", exam_time="45 minutes",
    prereq="None. It is written for people with no security background at all.",
    challenges=[
        "A project where the security people and everyone else are plainly not describing the "
        "same system.",
        "Product names used interchangeably until nobody is sure which tool does what.",
        "Decisions about security budget taken by people who cannot evaluate the options.",
        "New joiners needing a baseline before any of the deeper SC courses will land.",
        "Business stakeholders who nod through security reviews they do not actually follow.",
    ],
    labs=dict(
        count=16,
        repo="https://github.com/MicrosoftLearning/SC-900-Microsoft-Security-Compliance-and-Identity-Fundamentals",
        guide="https://microsoftlearning.github.io/SC-900-Microsoft-Security-Compliance-and-Identity-Fundamentals/",
        summary=("Sixteen short guided explorations including setup — Entra ID, self-service "
                 "password reset, conditional access and onward through the Defender and "
                 "Purview portals. Looking rather than building, which suits the audience.")),
    selling=dict(
        pitch=("One day that makes every later security conversation cheaper, because "
               "everyone finally means the same thing by the same words."),
        triggers=[
            "A security programme about to start with a mixed technical and business audience.",
            "New joiners or a team moving into security-adjacent work.",
            "A customer who wants the SC track but has nobody ready for the associate level.",
            "Sales or account teams who need to talk credibly about the security portfolio.",
            "Pre-work bundled ahead of SC-200, SC-300 or SC-401.",
        ],
        buyer="L&D, or the programme manager running a security initiative. Low cost, easy to approve.",
        attendees="Anyone — business stakeholders, new starters, project managers, salespeople, and technical people who want the map before the detail.",
        objections=[
            ("Fundamentals is too basic for our team.",
             "For the security team, yes. This is for everyone they have to work with, which "
             "is usually where the friction actually is."),
            ("It is only 45 minutes of exam — is it worth anything?",
             "As a credential, modestly. As a shared vocabulary before a four-day course, it "
             "saves more time than it costs."),
            ("Can they not read about this?",
             "They can, and most do not. A scheduled day with sixteen guided explorations is "
             "the difference between intending to and having done it."),
            ("We would rather go straight to SC-200.",
             "If they have the background, do. If half the room does not, SC-200 will lose "
             "them on day one and they will not say so."),
        ],
        next=[
            "SC-300 or SC-200 as the usual next step, depending on where they sit",
            "SC-401 for the compliance-minded ones",
            "Sell it per cohort rather than per person — it is a volume course",
            "AB-730 for the same audience on the AI side",
        ])),
}
