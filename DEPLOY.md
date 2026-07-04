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
