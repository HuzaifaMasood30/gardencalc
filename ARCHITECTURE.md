# Architecture & Verified Free Stack

## 1. Niche decision (this drives everything)

**Chosen niche: home & garden calculators and how-to guides** (mulch, soil, gravel,
paint, tile, grass seed, fertilizer, concrete).

Why this niche and not something else:

- **Real search demand with low competition.** "How much mulch do I need for 500 sq ft"
  and similar long-tails are searched constantly and served mostly by weak pages.
- **Calculator intent = high engagement.** People want a *number*, so they stay, scroll,
  use the tool, and return. That behaviour is what Google rewards.
- **Calculators are legitimate link magnets.** Other sites embed free tools, which earns
  backlinks naturally — the one sustainable off-page lever.
- **It monetises cleanly.** AdSense pays well on home-improvement traffic (contractor
  and product ads), and the audience is not ad-blind like some niches.
- **Tool pages are not "thin AI content".** A calculator plus a real explanation is
  genuinely useful and is exactly what Google's spam policies protect.

It also reuses the pattern already built for the water-calculator site, so the system is
proven, not theoretical.

## 2. Verified free stack

Every row below was checked on 2026-10-06. "Verified" = I fetched the endpoint or read the
current pricing page during this build.

| Layer | Service | Cost | Free-tier limit | Card needed | Automation-safe? | Verified |
|---|---|---|---|---|---|---|
| Hosting | **GitHub Pages** | $0 | 1 GB repo, 100 GB/mo soft bandwidth, 10 builds/hr | No | Yes (git push) | ✅ reachable |
| Subdomain | `*.github.io` | $0 | 1 site per repo | No | Yes | ✅ |
| SSL | GitHub Pages (Let's Encrypt) | $0 | auto, all sites | No | Yes | ✅ |
| CDN | GitHub Pages (Fastly) | $0 | included | No | Yes | ✅ |
| DNS | GitHub Pages default; **Cloudflare** if custom domain | $0 | Cloudflare free plan | No | Yes | ✅ |
| Static site | **Python + Jinja2** (own generator) | $0 | — | No | Yes | ✅ |
| Automation runner | **GitHub Actions** | $0 | **Unlimited on public repos** | No | Yes | ✅ confirmed |
| Keyword source | **Google/Bing autosuggest** | $0 | unofficial but stable, no key | No | Yes | ✅ live-tested |
| Keyword source 2 | **Wikipedia/RelatedTopics API** | $0 | free, no key | No | Yes | ✅ |
| Content LLM | **Google Gemini API** (Flash) | $0 | ~250–1,500 requests/day (model-dependent) | No | Yes | ✅ pricing page |
| Search Console | Google Search Console API | $0 | free | No (OAuth) | Yes | ✅ |
| Analytics | **GA4** + Measurement Protocol | $0 | free | No | Yes | ✅ |
| Sitemap/ping | IndexNow (Bing/Yandex) | $0 | free, needs 1 key file | No | Yes | ✅ |
| Monitoring | GitHub Actions + repo JSON | $0 | included | No | Yes | ✅ |

### Honest notes on the free tiers

- **Gemini free tier:** Google reduced quotas in Dec 2025 and moved Pro models to paid in
  Apr 2026. Flash/Flash-Lite remain free with roughly **250–1,500 requests/day**, resetting
  midnight Pacific. That is plenty for ~2–5 quality articles/day. If you exceed it you get
  HTTP 429 and the pipeline simply pauses until the next run — it does not silently spend
  money. **No credit card is required for the free tier.**
- **GitHub Actions:** genuinely unlimited for public repos. Sources disagree about the
  2,000-minute figure because that cap applies to *private* repos only. The system uses a
  public repo, so runs are free.
- **No permanent free custom domain exists.** `.tk`/`.ml`/`.ga`/`.cf`/`.gq` free domains
  were discontinued (Freenom stopped registrations; many were withdrawn by the registry).
  I will not invent one. The system therefore uses the free `*.github.io` subdomain and is
  **built so a custom domain can be attached later** with a one-line config change plus a
  DNS record.

## 3. System architecture

```
                    ┌─────────────────────────────────────────────┐
                    │            GitHub repository (public)        │
                    │  content/  data/  site/  scripts/  .github/  │
                    └─────────────────────────────────────────────┘
                                        │
     ┌──────────────────────────────────┼──────────────────────────────────┐
     │                                  │                                  │
┌────▼─────────┐              ┌─────────▼──────────┐             ┌─────────▼────────┐
│ 1. KEYWORD   │              │ 2. CONTENT PIPELINE │             │ 5. MONITORING    │
│   ENGINE     │              │                     │             │                  │
│ autosuggest  │──clusters───▶│ outline → draft     │             │ GSC + GA4 APIs   │
│ + related    │              │ → quality gates     │             │ → reports/       │
│ + classify   │              │ → SEO optimize      │             │ → dashboard.json │
└──────────────┘              │ → internal links    │             └──────────────────┘
                              │ → schema + images   │
                              └─────────┬───────────┘
                                        │
                              ┌─────────▼───────────┐
                              │ 3. SITE GENERATOR    │
                              │ Jinja2 → static HTML │
                              │ sitemap, robots, RSS │
                              └─────────┬───────────┘
                                        │
                              ┌─────────▼───────────┐
                              │ 4. PUBLISH (Actions) │
                              │ commit → Pages build │
                              │ → IndexNow ping      │
                              └─────────────────────┘
```

### The end-to-end flow you asked for

`Niche → Keyword Research → Topic Clustering → Content Planning → Article Creation →
Quality Checks → SEO Optimization → Internal Linking → Website Publishing → Sitemap →
Search Engine Monitoring → Legitimate Traffic Distribution → Performance Analysis →
Content Updates → AdSense Readiness`

Each arrow maps to a module:

| Stage | Module | Runs |
|---|---|---|
| Keyword research | `scripts/keywords.py` | weekly |
| Topic clustering | `scripts/cluster.py` | weekly |
| Content planning | `scripts/plan.py` (content calendar) | weekly |
| Article creation | `scripts/generate.py` (Gemini) | daily |
| Quality checks | `scripts/quality.py` (12 gates) | per article |
| SEO optimization | `scripts/seo.py` | per article |
| Internal linking | `scripts/interlink.py` | per article + weekly sweep |
| Publishing | `scripts/build.py` + GitHub Actions | daily |
| Sitemap/RSS/robots | `scripts/build.py` | per build |
| Monitoring | `scripts/monitor.py` | daily |
| Traffic distribution | `scripts/distribute.py` (RSS/IndexNow/webhook) | per publish |
| Performance analysis | `scripts/analyze.py` | weekly |
| Content updates | `scripts/refresh.py` | monthly |
| AdSense readiness | `scripts/adsense_check.py` | weekly |

## 4. What is genuinely automated vs. what needs you

**Fully automated after setup:** keyword discovery, clustering, drafting, quality gates,
SEO tags, schema, internal links, build, publish, sitemap, RSS, IndexNow ping, daily/weekly/
monthly reports, dashboard refresh, AdSense readiness scoring, content refresh.

**Needs a one-time action from you:** create the GitHub repo, add the `GEMINI_API_KEY`
secret, paste the Search Console verification token, connect GA4.

**Cannot be automated (by design, and correctly):** creating social accounts, posting to
Reddit/Quora/Pinterest (ToS + CAPTCHA), and any paid link building. The system prepares
everything for those channels but does not fake them.

## 5. Guardrails (so this does not become spam)

- **Hard cap of 3 articles/day**, default 1. Never thousands.
- **Quality gates block publishing.** An article that fails thin-content, duplication,
  keyword-stuffing or AI-cliché checks is quarantined, not published.
- **Original data.** Every article includes a real, working calculator with computed
  outputs, which makes it materially useful and not a template.
- **Human-approval mode is available** (`AUTOPUBLISH=false`): articles go to `drafts/`
  for review instead of live.
- **No promises.** No guaranteed rankings, traffic, links, AdSense approval or income.
  The system maximises the *probability* of success by following Google's published
  guidelines; it cannot guarantee outcomes.

## 6. Cost summary

| Scenario | Monthly cost |
|---|---|
| Default (1–3 articles/day, GitHub Pages, Gemini free) | **$0.00** |
| If you exceed Gemini free tier | ~$0.10–$2.00 (Flash-Lite is ~$0.05/1M input tokens) |
| Custom domain (optional, later) | ~$10–12/year |
| Everything else | $0.00 |

## 7. Repository layout

```
seo-autoblog/
├── config/
│   ├── site.json            # site name, URL, niche, author, social
│   ├── topics.json          # seed topics + calculator definitions
│   └── seo.json             # SEO defaults, limits, gates
├── data/
│   ├── keywords.json        # discovered keywords + intent + score
│   ├── clusters.json        # topic clusters
│   ├── articles.json        # the content database (source of truth)
│   ├── links.json           # internal link graph
│   └── metrics.json         # GSC/GA4 snapshots
├── content/
│   ├── published/*.md       # live articles
│   ├── drafts/*.md          # awaiting approval
│   └── rejected/*.md        # failed quality gates (with reasons)
├── templates/               # Jinja2: base, home, article, category, calculator, legal
├── static/                  # css, js, images
├── scripts/                 # the pipeline (see table above)
├── reports/                 # generated markdown reports + dashboard.json
├── site/                    # GENERATED static site (output of build.py)
├── .github/workflows/       # daily.yml, weekly.yml, monthly.yml
├── requirements.txt
└── README.md
```

## 8. Data model

`data/articles.json` — the source of truth. One record per article:

```json
{
  "id": "how-much-mulch-do-i-need",
  "title": "...", "slug": "...", "cluster": "mulch",
  "primary_keyword": "...", "secondary_keywords": ["..."],
  "intent": "informational|commercial|calculator",
  "status": "published|draft|rejected",
  "created": "ISO date", "updated": "ISO date",
  "meta_description": "...", "word_count": 0,
  "schema_types": ["Article","FAQPage","HowTo"],
  "calculator": "mulch|soil|gravel|null",
  "internal_links": [{"to":"...","anchor":"..."}],
  "quality": {"score": 0, "gates": {"thin": true, "dup": true, ...}},
  "metrics": {"clicks":0,"impressions":0,"ctr":0,"position":0},
  "revision": 1
}
```

The build reads only `status == "published"` records, so the site can never accidentally
publish a quarantined article.

## 9. Decision points for you

1. **Niche:** home & garden calculators (recommended) — or tell me another and I will
   re-seed `config/topics.json`.
2. **Autopublish:** `true` (hands-off) or `false` (you approve drafts). Default `false`
   for the first two weeks, then switch.
3. **Cadence:** 1, 2 or 3 articles/day. Default 1.
4. **Site name / brand** for `config/site.json`.

If you are happy with this, the next message contains the working implementation, and I
will proceed module by module.
