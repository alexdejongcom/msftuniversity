# Deploy: GitHub → Azure Static Web Apps

The site folder is already a git repo with one commit on `main`. The `staticwebapp.config.json` is included (404 page, security headers).

## 1. Push to GitHub

From this folder (`msftuniversity-new`), with GitHub CLI:

```bash
gh repo create msftuniversity --public --source . --push
```

Or manually:

```bash
git remote add origin https://github.com/<your-username>/msftuniversity.git
git push -u origin main
```

## 2. Create the Static Web App

1. portal.azure.com → **Create a resource** → **Static Web App**
2. Subscription + resource group (e.g. `rg-msftuniversity`)
3. Name: `msftuniversity` · Plan: **Free** · Region: West Europe
4. Source: **GitHub** → sign in → pick your repo `msftuniversity`, branch `main`
5. Build presets: **Custom**
   - App location: `/`
   - Api location: *(empty)*
   - Output location: *(empty)*
6. **Review + create** → **Create**

Azure commits a GitHub Actions workflow to your repo and runs the first deployment (~2 min). Your site is live at `https://<generated-name>.azurestaticapps.net`.

Then run `git pull` locally to fetch the workflow file Azure added.

## 3. Custom domain (msftuniversity.com)

In the Static Web App → **Custom domains**:

1. **+ Add** → Custom domain on other DNS
2. For `www.msftuniversity.com`: add a **CNAME** at your DNS provider pointing `www` → `<generated-name>.azurestaticapps.net`, then validate.
3. For the apex `msftuniversity.com`: choose **TXT** validation, add the TXT record shown, then add an **ALIAS/ANAME** record (or A record via your provider's flattening) pointing to the same host. Set one of the two as the default domain with redirect.

SSL certificates are issued automatically — free.

## 4. Updating the site

```bash
git add -A
git commit -m "update"
git push
```

Every push to `main` auto-deploys via GitHub Actions.

## Don't forget

- Your old WordPress site currently serves msftuniversity.com — switch DNS only when you're happy with the new site.
- The About page still hotlinks your photo from the old WordPress site. Before killing WordPress: save the photo as `assets/alex.jpg`, update the `<img src>` in `about.html`, commit, push.

## Newsletter — The Briefing

Self-hosted on Azure: subscribers in Table Storage (same `COUNTER_STORAGE` account), mail through
Azure Communication Services (ACS), editor at `/newsletter-admin.html`, scheduler in GitHub Actions.
Do these once, in order. You paste every key/connection string yourself — never share them.

### 1. Email sending (Azure portal)
1. Create an **Email Communication Services** resource (data location: Europe).
2. In it: **Provision domains → Add domain → Custom domain** → `msftuniversity.com`.
3. At your DNS provider add the records Azure shows: the **TXT** (domain verification), **SPF** (TXT) and
   the two **DKIM** CNAMEs. Click *Verify* for each until all show *Verified*.
   Also add a DMARC record to start monitoring: `_dmarc` TXT `v=DMARC1; p=none; rua=mailto:alex@alexdejong.com`.
4. In the domain: **MailFrom addresses → Add** → username `newsletter`, display name
   `The Briefing · Microsoft University`.
5. Create a **Communication Services** resource (same region), then **Email → Domains → Connect domain**
   and connect `msftuniversity.com`.
6. Communication Services → **Keys** → copy the *Connection string*.

### 2. App settings (Static Web App → Settings → Environment variables)
| Name | Value |
|---|---|
| `ACS_CONNECTION_STRING` | the connection string from step 1.6 |
| `NL_FROM` | `newsletter@msftuniversity.com` |
| `NL_ADMIN_EMAIL` | `alex@alexdejong.com` (gets test mails and the "draft ready" reminder) |
| `NL_CRON_KEY` | a long random string — e.g. run `openssl rand -hex 24` |
| `NL_SITE_URL` | `https://msftuniversity.com` (optional, this is the default) |

`COUNTER_STORAGE` is already there. Optional later: `NL_RATE_MINUTE` / `NL_RATE_HOUR` (default 30 / 100 —
Azure's starting limits for a custom domain).

### 3. Editor access
Static Web App → **Role management → Invite**: provider *Microsoft Entra ID*, your email, domain
`msftuniversity.com`, role **`newsletter-admin`**. Open the invite link and sign in. The editor and its API
only work for that role.

### 4. Scheduler
GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**: `NL_CRON_KEY` with the
**same value** as the app setting. The *Newsletter scheduler* workflow then runs hourly.

### 5. First run
1. Subscribe yourself on `/newsletter.html` and click the confirmation link.
2. Open `/newsletter-admin.html` → **Build a new draft** → tick items, add your take → **Send me a test**.
3. Happy? **Send to N subscribers.**

### Growing the list
Azure starts every custom domain at **30 mails/minute and 100/hour**. Bigger lists are sent in batches
automatically (keep the editor open to speed it up, the hourly scheduler finishes it otherwise). Once the domain
has a few weeks of clean sending, request a quota increase (ACS docs: *Quota increase for email domains*) and
raise `NL_RATE_MINUTE` / `NL_RATE_HOUR` to match.
