# GardenCalc — automated SEO calculator site

**Live site: <https://huzaifamasood30.github.io/gardencalc/>**

A fully automated static site of home and garden calculators. A scheduled pipeline
discovers keywords, generates and gates articles, builds the site, and deploys it to
GitHub Pages. The only manual steps are account-level actions (search console, ads),
which the build cannot do for you.

## How it works

```
keywords -> clusters -> generate -> internal links -> quality gates
        -> static build -> health verify -> adsense check -> monitor -> dashboard
```

Every stage writes a JSON artifact under `data/` and a human report under `reports/`,
so a run is auditable after the fact.

## Quick start

```bash
pip install -r requirements.txt
python scripts/run_all.py --limit 3     # full pipeline
python -m http.server -d site 8000      # preview at http://localhost:8000
```

## Scripts

| Script | Purpose |
| --- | --- |
| `run_all.py` | Full pipeline in one command (used by CI) |
| `keywords.py` | Live Google + Bing autosuggest expansion, filtered for relevance |
| `cluster.py` | Topic clusters and the article plan |
| `generate.py` | Article generation (LLM when configured, deterministic template otherwise) |
| `calculators.py` | Calculator formulas — the single source of truth for the numbers |
| `quality.py` | 12 content gates; nothing thin or spammy reaches the site |
| `interlink.py` | Internal link graph, contextual links, orphan detection |
| `build.py` | Static site generator |
| `seo.py` | Schema.org, sitemap, robots, RSS, per-page SEO score |
| `verify.py` | Health checks: broken links, duplicate meta, orphans, sitemap |
| `adsense.py` | AdSense readiness audit |
| `monitor.py` | Score snapshots and regression detection |
| `dashboard.py` | Single-file HTML dashboard |
| `distribution.py` | Ready-to-paste off-site promotion copy and a tracked checklist |
| `promotion.py` | Curated no-login backlink targets with exact post text, anchor and link type; dedupe log |

## Configuration

`config/site.json` — name, URL, analytics ID, AdSense client, verification tags.
`config/seo.json` — limits and which quality gates are enabled.
`config/topics.json` — seed topics, clusters, and calculator definitions.

## Going live on GitHub Pages (free)

1. **Create the repository.** On github.com, create a new repository (e.g. `gardencalc`).
   Public is required for free GitHub Pages. Do **not** add a README or .gitignore.
2. **Push this project.**
   ```bash
   cd seo-autoblog
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
   git push -u origin main
   ```
3. **Enable Pages.** Repo → Settings → Pages → *Build and deployment* → Source:
   **GitHub Actions**. Do not choose a branch.
4. **Run the workflow once.** Actions tab → *SEO pipeline* → *Run workflow*.
   The first run generates content, builds, and deploys. The workflow derives the site's
   base URL from the repository automatically, so no config edit is needed.
5. **Your live URL** is `https://<YOUR_USERNAME>.github.io/<YOUR_REPO>/`.
   (If the repository is named `<YOUR_USERNAME>.github.io`, the URL is the bare
   `https://<YOUR_USERNAME>.github.io/`.)

After that the pipeline runs daily at 06:17 UTC and the health check at 07:43 UTC.

### Search Console / Bing verification (manual, account-level — cannot be automated)

Verification proves you own the domain, so it must be done by you:

1. Go to <https://search.google.com/search-console> → *Add property* → **URL prefix** →
   paste your live URL. Choose the **HTML tag** method and copy the `content="..."` value.
2. In your repository, set the verification token so the build emits the meta tag:
   - Repository → Settings → Secrets and variables → Actions → **Variables**.
   - Add a variable `GOOGLE_SITE_VERIFICATION` with the token value.
   - Re-run the *SEO pipeline* workflow. *(Alternatively, paste it into
     `google_site_verification` in `config/site.json` and commit.)*
3. Back in Search Console, click *Verify*.
4. Submit the sitemap: Search Console → *Sitemaps* → enter `sitemap.xml`.
5. Bing: <https://www.bing.com/webmasters> → *Import from Google Search Console* (one
   click). Set the `BING_SITE_VERIFICATION` variable the same way if you prefer the tag
   method.

Set `ANALYTICS_ID` (a GA4 `G-...` id) and `ADSENSE_CLIENT` (`ca-pub-...`) as repository
*Variables* the same way; the build injects both automatically.

## Optional LLM

The generator works with no API key using a deterministic, substantive template. Set
`GEMINI_API_KEY` to use the free Gemini tier; the same quality gates apply either way.

## Verification

```bash
python scripts/tests.py                    # unit + calculator-parity tests
python scripts/run_all.py --limit 40       # full pipeline
python -m http.server -d site 8000 &       # serve
python scripts/audit.py --base http://localhost:8000   # crawler-style audit
```

`audit.py` crawls the served site over HTTP and checks sitemap, robots, RSS, H1 counts,
duplicate meta, broken links, alt text, schema JSON and orphans.

