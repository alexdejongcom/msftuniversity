# MSFT University — new website

Modern static site (5 pages, Microsoft Fluent-inspired design). No build step, no dependencies.

## Files

- `index.html` — Home
- `training.html` — Training & Services (courses, speaking, CTO as a Service)
- `resources.html` — Learning Resources (all links migrated from the old site)
- `about.html` — About Alex de Jong
- `contact.html` — Contact / booking
- `css/style.css` — the entire design

## Before going live

1. **Your photo**: `about.html` currently loads your photo from the old WordPress site. Save your photo as `assets/alex.jpg` and change the `<img src>` in `about.html` to `assets/alex.jpg`.
2. Review the course/speaking descriptions — I wrote them from your current site content; adjust wording as you like.

## Deploying (options)

**Azure Static Web Apps (recommended, free tier)**
1. Push this folder to a GitHub repo.
2. Azure Portal → Create Static Web App → link the repo, app location `/`.
3. Add custom domain `msftuniversity.com` under Custom domains, update DNS (CNAME) at your registrar.

**Any other host**: it's plain HTML/CSS — upload the folder to Azure Storage static hosting, GitHub Pages, Netlify, or your current hosting.

## Editing

Everything is plain HTML. Colors and fonts live in the `:root` block at the top of `css/style.css`. Nav and footer are repeated in each file — edit them in all 5 pages when you change a menu item.

## Extras added later

- `404.html` — BSOD-style not-found page (configure your host to serve it for 404s; on Azure Static Web Apps add a `staticwebapp.config.json` responseOverride).
- `robots.txt` + `sitemap.xml` — SEO basics.
- `js/site.js` — nav behavior + three easter eggs: browser console message, Konami code (↑↑↓↓←→←→BA) triggers a friendly BSOD, and clicking the logo squares 5× summons Clippy.

## Events workflow

Events live in `js/events.js`. The events page sorts by date automatically and hides any event whose start date has passed. To add one: copy a block in that file, fill in date/title/city/url, commit, push. Or tell Claude: "new event <booking-url>" — it fetches the details (translated to English) and adds the entry.

## Visitor counter (Azure Functions + Table Storage)

The odometer in the footer is served by `/api/counter` (`api/src/functions/counter.js`), a managed
Azure Function that increments a counter in Azure Table Storage. One-time setup:

1. Create a Storage Account (any cheap LRS one, e.g. `stmsftuniversity`).
2. Copy its connection string (Access keys blade).
3. Static Web App → Environment variables → add `COUNTER_STORAGE` = that connection string.
4. Push — the workflow deploys the `api/` folder automatically (api_location is set to "api").

GET /api/counter returns the count; POST increments (once per visitor session, handled client-side).
The widget hides itself if the API is unavailable.
