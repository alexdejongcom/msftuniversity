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
    who="Administrators with six months of hands-on Azure. The most common first role-based Azure certification."),
"AZ-140": dict(fam="azure", level="Intermediate", title="Configuring and Operating Microsoft Azure Virtual Desktop",
    url="https://learn.microsoft.com/credentials/certifications/azure-virtual-desktop-specialty/",
    sg="https://aka.ms/AZ140-StudyGuide", pa=True,
    blurb="Planning, deploying and operating Azure Virtual Desktop — host pools, images, FSLogix profiles, access and the performance tuning that follows.",
    who="Desktop and infrastructure specialists running virtual desktops on Azure."),
"AZ-204": dict(fam="azure", level="Intermediate", title="Developing Solutions for Microsoft Azure",
    url="https://learn.microsoft.com/credentials/certifications/azure-developer/",
    sg="https://aka.ms/AZ204-StudyGuide", pa=True,
    blurb="Building on Azure: compute options, storage, security, integration and the monitoring and troubleshooting that comes with shipping to production.",
    who="Developers with a year or two of professional development and real Azure SDK experience."),
"AZ-305": dict(fam="azure", level="Advanced", title="Designing Microsoft Azure Infrastructure Solutions",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-305/",
    sg="https://aka.ms/AZ305-StudyGuide", pa=True,
    blurb="The architect exam. Designing identity, governance, data storage, business continuity and infrastructure — trade-offs rather than button-clicking.",
    who="Architects who already know Azure operations well. Case-study heavy; experience matters more than memorisation."),
"AZ-400": dict(fam="azure", level="Advanced", title="Designing and Implementing Microsoft DevOps Solutions",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-400/",
    sg="https://aka.ms/AZ400-StudyGuide", pa=True,
    blurb="DevOps end to end: source control, CI/CD pipelines, infrastructure as code, secrets, dependencies and feedback loops.",
    who="Engineers who live in pipelines. Expect both Azure DevOps and GitHub across the exam."),
"AZ-500": dict(fam="azure", level="Intermediate", title="Microsoft Azure Security Technologies",
    url="https://learn.microsoft.com/credentials/certifications/azure-security-engineer/",
    sg="https://aka.ms/AZ500-StudyGuide", pa=True,
    blurb="Securing Azure: identity and access, platform protection, data and application security, and security operations.",
    who="Security engineers working in Azure. Pairs naturally with SC-300 on the identity side."),
"AZ-700": dict(fam="azure", level="Intermediate", title="Designing and Implementing Microsoft Azure Networking Solutions",
    url="https://learn.microsoft.com/credentials/certifications/azure-network-engineer-associate/",
    sg="https://aka.ms/az700-StudyGuide", pa=True,
    blurb="Azure networking in depth — hybrid connectivity, routing, load balancing, private access to services and network security.",
    who="Network engineers moving into Azure, and Azure admins who want the networking layer properly nailed down."),
"AZ-800": dict(fam="azure", level="Intermediate", title="Administering Windows Server Hybrid Core Infrastructure",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-800/",
    sg="https://aka.ms/AZ800-StudyGuide", pa=True,
    blurb="Windows Server where most of it actually lives: hybrid. Identity, compute, network infrastructure and storage across on-premises and Azure.",
    who="Windows Server administrators. Half of a pair — AZ-801 completes the hybrid administrator certification."),
"AZ-801": dict(fam="azure", level="Advanced", title="Configuring Windows Server Hybrid Advanced Services",
    url="https://learn.microsoft.com/credentials/certifications/exams/az-801/",
    sg="https://aka.ms/AZ801-StudyGuide", pa=True,
    blurb="The advanced half of the hybrid server track: security, high availability, disaster recovery, migration and troubleshooting.",
    who="Experienced Windows Server administrators. Take AZ-800 first."),
"AZ-900": dict(fam="azure", level="Beginner", title="Microsoft Azure Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/azure-fundamentals/",
    sg="https://aka.ms/AZ900-StudyGuide", pa=True,
    blurb="Cloud concepts, Azure architecture and services, and how management and governance work — plus pricing and support.",
    who="Anyone, technical or not, who needs a credible foundation in Azure. The most-taken Microsoft exam for a reason."),

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

"MD-102": dict(fam="m365", level="Intermediate", title="Endpoint Administrator",
    url="https://learn.microsoft.com/credentials/certifications/modern-desktop/",
    sg="https://aka.ms/md102-StudyGuide", pa=True,
    blurb="Managing and securing endpoints with Intune — deployment, identity and compliance, applications, and protecting the device fleet.",
    who="Endpoint and desktop administrators. The Intune exam, in practice."),
"MS-102": dict(fam="m365", level="Intermediate", title="Microsoft 365 Administrator",
    url="https://learn.microsoft.com/credentials/certifications/exams/ms-102/",
    sg="https://aka.ms/MS102-StudyGuide", pa=True,
    blurb="Running a Microsoft 365 tenant: deployment, identity and access with Microsoft Entra, threat protection and compliance.",
    who="Microsoft 365 administrators. The backbone certification for the M365 platform."),
"MS-700": dict(fam="m365", level="Intermediate", title="Managing Microsoft Teams",
    url="https://learn.microsoft.com/credentials/certifications/m365-teams-administrator-associate/",
    sg="https://aka.ms/ms700-StudyGuide", pa=True,
    blurb="Planning and configuring Teams — governance and lifecycle, chat and collaboration, meetings and the settings that keep it manageable.",
    who="Teams administrators and M365 admins who own collaboration."),
"MS-721": dict(fam="m365", level="Advanced", title="Collaboration Communications Systems Engineer",
    url="https://learn.microsoft.com/credentials/certifications/m365-collaboration-communications-systems-engineer/",
    sg="https://aka.ms/MS721-StudyGuide", pa=True,
    blurb="Teams Phone, meetings and meeting rooms — voice routing, certified devices, and troubleshooting call quality when it goes wrong.",
    who="Engineers responsible for voice and meeting rooms. Telephony experience is a real advantage."),

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
    who="Security architects. Expect one of SC-200, SC-300, AZ-500 or MS-102 behind you; this exam assumes that ground is covered."),
"SC-200": dict(fam="security", level="Intermediate", title="Microsoft Security Operations Analyst",
    url="https://learn.microsoft.com/credentials/certifications/security-operations-analyst/",
    sg="https://aka.ms/SC200-StudyGuide", pa=True,
    blurb="Threat detection and response with Defender XDR and Microsoft Sentinel — mitigating threats and hunting for what the alerts missed.",
    who="SOC analysts and security engineers. KQL is worth practising before you sit it."),
"SC-300": dict(fam="security", level="Intermediate", title="Microsoft Identity and Access Administrator",
    url="https://learn.microsoft.com/credentials/certifications/identity-and-access-administrator/",
    sg="https://aka.ms/sc300-StudyGuide", pa=True,
    blurb="Microsoft Entra in depth — identity lifecycle, authentication and conditional access, application access and identity governance.",
    who="Identity administrators. Identity is the control plane, which makes this one of the highest-leverage certifications here."),
"SC-401": dict(fam="security", level="Intermediate", title="Information Security Administrator",
    url="https://learn.microsoft.com/credentials/certifications/information-security-administrator/",
    sg="https://aka.ms/SC401-StudyGuide", pa=True,
    blurb="Protecting data with Microsoft Purview — information protection, data loss prevention, insider risk and retention.",
    who="Administrators who own data protection and compliance. The successor to the old SC-400."),
"SC-500": dict(fam="security", level="Intermediate", title="Implementing End-to-End Security Controls for Cloud and AI Workloads",
    url="https://learn.microsoft.com/credentials/certifications/cloud-and-ai-security-engineer-associate/",
    sg="https://aka.ms/SC500-StudyGuide", pa=False,
    blurb="Security across the whole estate rather than one product: identity and governance, storage, databases and networking, compute, and the platforms AI workloads actually run on.",
    who="Security engineers working across Azure and Microsoft 365 who now have AI workloads to protect as well. Earns the Cloud and AI Security Engineer Associate certification."),
"SC-900": dict(fam="security", level="Beginner", title="Microsoft Security, Compliance, and Identity Fundamentals",
    url="https://learn.microsoft.com/credentials/certifications/security-compliance-and-identity-fundamentals/",
    sg="https://aka.ms/sc900-StudyGuide", pa=True,
    blurb="The vocabulary and the map: security and compliance concepts, and what each Microsoft security, identity and compliance capability is for.",
    who="Anyone before starting the SC track — and business stakeholders who need to follow the conversation."),
}
