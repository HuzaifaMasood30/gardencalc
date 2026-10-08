# AGENTS.md — repository memory (GardenCalc)

## What this is
Automated static SEO site: home & garden calculators + how-to guides.
Live: https://huzaifamasood30.github.io/gardencalc/  (GitHub Pages, project site)
Repo: HuzaifaMasood30/gardencalc. Deploy = GitHub Actions `SEO pipeline`.

## Pipeline
`python scripts/run_all.py --limit N` runs the whole chain:
generate -> internal links -> quality gates -> build -> monitor -> dashboard -> report.
- `scripts/generate.py` needs `GEMINI_API_KEY`. Without it, long-tail articles are
  deliberately SKIPPED (templated fallbacks would be thin/duplicate). Pillars still use
  the curated fallback text.
- `scripts/llm.py` uses a MODEL_CHAIN fallback. gemini-3.6-flash frequently returns
  HTTP 429/503, so gemini-3.1-flash-lite is the usual effective model.
- Workflows: `.github/workflows/pipeline.yml` (daily 06:17 UTC, also workflow_dispatch
  with input `limit`), `.github/workflows/health.yml` (daily 07:43 UTC).
- There is no push trigger; changes to scripts/data only redeploy after a dispatch or
  the scheduled run. Dispatch: POST /actions/workflows/pipeline.yml/dispatches.

## Conventions / gotchas
- Cluster assignment lives in `scripts/keywords.py` (`guess_cluster`, `CLUSTER_HINTS`)
  and is reused by `scripts/cluster.py`. Matching is word-boundary based so "topsoil"
  is not captured by the "soil" cluster.
- Off-topic autosuggest results are blocked in `NOISE` (board games, aquariums, etc.).
  Add new distractors there rather than deleting pages after the fact.
- Calculators are implemented twice and MUST stay in sync:
  `scripts/calculators.py` (Python) and `static/js/main.js` (browser).
  Parity is tested in `scripts/tests.py` via `scripts/calc_parity.js`.
- `data/articles.json` is the source of truth for published pages; status must be
  `approved` to publish. Internal links are rebuilt every run (do not clear links on
  rejection — that caused a permanent re-reject loop).

## Validation
```bash
python3 scripts/tests.py                 # 8 unit/parity tests
python3 scripts/live_audit.py https://huzaifamasood30.github.io/gardencalc/
```

## Internal linking rules (important)
- Same-cluster siblings are linked as a stable ring so every article has inbound
  links; do not revert `build_for` to a greedy "top N", which starves the
  lowest-ranked sibling once a cluster passes the link cap.
- `_repair_orphans` guarantees an inbound link for articles in singleton/new
  clusters and must prefer sources with spare link capacity (else it pushes the
  source past `max_internal_links_per_article` and fails the source's gate).
- `run_all.py` must rebuild links as the LAST step: `quality.apply()` can reject a
  page that was another page's only inbound link.

## IndexNow / Bing
- IndexNow needs a key file at the *host root* (`https://<user>.github.io/<key>.txt`),
  which a GitHub project page cannot serve, so api.indexnow.org answers 403
  `UserForbiddedToAccessSite`. Bing's GET endpoint also 403s until the site is
  verified in Bing Webmaster Tools (or imported from Google Search Console).
- `scripts/indexnow.py` tries Bing's endpoint then the shared POST. It is best-effort
  and never fails the pipeline. Real fix = user verifies the site in Bing WMT.

## SEO / growth layer (added)
- `scripts/charts.py` holds 8 coverage/reference chart pages. Their numbers are derived
  from `scripts/calculators.py`, so a chart can never disagree with its calculator.
  Add a chart there; it is picked up by the sitemap, hubs and homepage automatically.
- Indexable hub pages: `/calculators/`, `/guides/` (client-side filter), `/sitemap/`,
  `/for-publishers/`. They live in `EXTRA_PAGES` in `build.py` (sitemap) and each has a
  template. `/embed/<calc>/` widgets are noindex and canonical to the full calculator,
  so keep them OUT of the sitemap and out of `EXTRA_PAGES`.
- Schema: `seo.all_schema` emits Article + BreadcrumbList + FAQPage. HowTo was removed
  (its steps were generic and not page-specific). Calculator articles also get
  WebApplication, the homepage gets WebSite + Organization.
- `verify.py` skips noindex pages for the meta-description and canonical checks, since
  embed/search/404 pages are not canonical landing pages.
- Analytics + GA4 events are documented in `docs/tracking.md`. `analytics_id` in
  `config/site.json` (or the `ANALYTICS_ID` secret) is the single switch; empty = no
  script, no cookies. Events: calculate_click, copy_result, print_result, share_click.

## Access notes
- Actions Secrets API is not reachable by the agent token (403); the repo secret
  GEMINI_API_KEY must be added by the user in the GitHub UI.
- The agent sandbox `GITHUB_TOKEN` is periodically invalid (401 Bad credentials), so
  `git push` can fail even when the work is committed locally. When that happens, commit
  locally and tell the user to re-authorise / push; do not force anything.
- Google/Bing console verification and sitemap submission require the user's account.
- A separate working PAT (not the system GITHUB_TOKEN, which gets 403) is needed to
  `workflow_dispatch`; system token can only read.

## Design system & figures
- `static/css/style.css` is a self-contained design system (CSS variables, no web
  fonts, no frameworks) so Core Web Vitals stay green. Templates must only use
  classes defined there.
- `scripts/images.py` generates an original WebP figure + thumbnail per article via
  Pillow (installed from requirements.txt). Figures are written into the *copied*
  `site/static/img/{fig,thumb}` during `build.py`.
- `build.py` copies static first, then generates figures, then writes pages; keep
  that order. Pillow is optional at runtime: without it the build still succeeds and
  templates fall back to CSS.
- Article bodies render via `mdrender.render_with_toc`, which adds `<h2 id>` anchors
  and returns a table of contents; `article.html` renders the TOC and a scroll-spy
  highlights the active section in `main.js`.

## FAQ blocks
- Every published article should carry a non-empty `faq` list: 13 topsoil/fertilizer
  pages originally had none, each costing ~11 SEO points and an FAQPage rich-result
  slot. Answers must restate content already visible in the body (Google requires the
  answer text on the page); never add an FAQ whose answer is not in the article.
- `seo.faq_schema` emits FAQPage JSON-LD whenever `faq` is non-empty.

## Brand assets
- `images.render_brand(static_root)` writes `logo.png`, `favicon.ico`,
  `apple-touch-icon.png` and a PNG `og-default.png`. It runs in `build.py` right after
  `images.generate`, into the copied static dir, so the Organization publisher logo
  (`config/site.json:org_logo`) actually resolves. Keep the URL as a PNG path.
- `config/site.json:base_url` must be the real deployed URL, not a placeholder; the
  distribution reports and local builds use it directly.

## Search page
- `/search/` is a client-side page backed by `static/search-index.json` (both written
  by `build.py`). The homepage `WebSite` SearchAction points at `/search/?q=`; keep
  that URL and the index in sync when either changes.

## CI note
- The pipeline's "Commit refreshed content and data" step rebases (`git pull --rebase
  --autostash`) before pushing, because a manual push during a run otherwise causes a
  non-fast-forward and the deploy is skipped.
- `pipeline.yml` only runs on the daily cron / manual dispatch, so code or template
  changes are published by `deploy.yml`, which runs on main pushes to site-affecting
  paths. Both share the `seo-pipeline` concurrency group so they serialise.
- `scripts/verify.py` exits non-zero on any issue, so the deploy gate and the health
  check actually block a bad build.

## Sitemap rules
- `seo.sitemap_xml` is the single source of truth: it emits absolute escaped `<loc>`,
  a `<lastmod>` only when it is a real non-future ISO date, and no `<priority>`
  (ignored by Google/Bing). It de-duplicates by `<loc>` and drops any URL that escapes
  `base_url`, so a wrong-host or duplicate URL cannot reach production.
- Every sitemap URL must resolve to a 200, be self-canonical and be indexable. Never
  put a `noindex` page in the sitemap; `verify.py` now fails if one appears.
- `base_url`/`custom_domain` is lower-cased in `common.site_config()` because GitHub
  Pages only answers on the lower-case host; the pipeline env var carries a
  capital-H owner, so keep that normalization.
- Google Search Console must be a URL-prefix property for the full project URL
  (`https://<user>.github.io/<repo>/`); a bare-host property cannot host this sitemap.

## Duplicate merges & renames (Phase 2)
- `scripts/merges.py` is the single source of truth. `MERGES` (old_slug -> target_slug)
  marks a page `status="merged"`; `build.py` then drops it from listings, RSS, the
  sitemap and internal links, and renders a redirect stub from `templates/redirect.html`
  (`meta refresh` + self-less `rel=canonical` to the target, no noindex, visible link).
- Adding to `MERGES` leaves the old URL alive as the stub, so indexed URLs never 404.
  Removing an entry restores the page with no other edit (`merges.apply` re-derives).
- `RENAMES` (old_slug -> cleaned_slug) is for URL cleanups, not intent merges: it emits a
  rename stub only when the old slug no longer exists as a real page.
- `run_all.py` applies merges after the quality gate and relinks, so no live page links
  to a stub. `quality.apply` and `interlink` both skip `status="merged"`.
- `verify.py` skips stubs for title/description/canonical duplication checks, because a
  stub intentionally shares those with its target.
- When auditing duplicates, differentiate by intent, not body Jaccard: sized long-tail
  pages (200 vs 300 sq ft) are distinct queries and must stay. `audit_phase0.py` splits
  `duplicates` from `sized_variants` using the slug's digits.

## Seasonal guides
- `scripts/seasonal.py` holds the four evergreen timing guides; each carries a `table`
  ({caption, head, rows, note}) rendered by `templates/seasonal.html` for featured
  snippet value. Keep the numbers consistent with `calculators.py` and `charts.py`.

## Video embeds
- `data/videos.json` maps a calculator key to `{"id": "<youtube id>", "upload": "date"}`.
  Empty = nothing renders. `templates/calculator.html` + `main.js` render a
  click-to-load `youtube-nocookie` facade only when a real id exists; `build.py` then
  adds `VideoObject` schema. Never add fake videos.



## On-page pass (2026-10-08, second run)
- Meta descriptions were being cut mid-sentence ("...this.", "...manufacturer's.")
  and many sat under 140 chars. A rewrite of 40 descriptions now targets
  140-160 display chars and always carries a concrete result (cubic yards, bags,
  tons) or a free-tool CTA. Watch for duplicate descriptions across near-twin
  pages; the raised-bed pair shipped an identical one and tripped verify.
- `verify.py` flags `duplicate_meta_description`; `build.py` must be rerun after
  any `data/articles.json` description edit before the health gate passes.

## Access reality (check this before planning anything)
- `GITHUB_TOKEN`/`GH_TOKEN` here are invalid every run: the GitHub API rejects
  them and HTTPS push fails with "Invalid username or token". `git fetch` works
  only because origin's URL still carries an old embedded credential with read
  but not write scope.
- Consequence: the agent cannot deploy. Commits accumulate locally on `main`
  and must be pushed by the owner, or by a token with `contents:write`. Verify
  with one `curl`, then hand off - do not loop on the push.
- No Blogger admin session, Search Console or Analytics credential exists here.
  IndexNow (`scripts/indexnow.py`) is available and legitimate (Bing/DuckDuckGo,
  not Google); it currently gets 403 UserForbiddedToAccessSite because the key
  file is served under /gardencalc/ rather than the host root, so Bing cannot
  verify it for a project page.
