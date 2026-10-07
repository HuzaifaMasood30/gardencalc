# Legitimate traffic-generation workflow

A practical, repeatable plan you run from your own accounts. Nothing here is automated
traffic, spam, or a policy violation. Every step is something a person would do by hand,
and the goal at each stage is a real reader, not a metric.

Pipeline this supports:

```
website -> Google indexing -> genuine organic traffic -> legitimate off-site promotion
        -> content growth -> analytics -> optimization -> (later) AdSense
```

The auto-generated per-article copy and the tracked checklist live in
`reports/distribution-pack.md`. Manage its state with:

```bash
python scripts/distribution.py                 # regenerate the pack
python scripts/distribution.py --mark reddit-diy    # mark a channel done
python scripts/distribution.py --undo reddit-diy
```

---

## Ground rules

**Do**
- Answer real questions with real, complete answers. Link only when the calculator is the
  direct answer.
- Disclose that the site is yours when you link to it.
- Follow each platform's self-promotion rules. Reddit, Stack Exchange and Quora all allow
  links when the answer stands on its own.
- Post slowly. A few genuine contributions a week beats a burst that looks automated.

**Do not**
- Buy backlinks, use link exchanges, PBNs, comment spam, or directory spam.
- Post the same text across many sites (duplicate content, obvious spam signal).
- Use bots, click farms, auto-visits, or traffic exchanges. These are detectable and are
  grounds for a Google penalty and AdSense rejection.
- Keyword-stuff the off-site copy. Write like a person.

---

## Phase 0 — Launch prerequisites (done by you, once)

1. Create the public GitHub repo and enable Pages (see `README.md`).
2. Run the *SEO pipeline* workflow once; confirm the live URL returns the homepage.
3. Run the live audit:
   ```bash
   python scripts/live_audit.py https://<user>.github.io/<repo>/
   ```
   Site is ready to submit when this reports all checks passing.

## Phase 1 — Get indexed (week 1)

1. **Google Search Console.** Add a *URL prefix* property for the live URL, verify with the
   HTML tag (paste the token as the `GOOGLE_SITE_VERIFICATION` repository variable), then
   *Sitemaps* -> submit `sitemap.xml`.
2. **Bing Webmaster Tools.** *Import from Google Search Console* — one click, then confirm
   the sitemap carried over.
3. **Request indexing** for the homepage and the 7 pillar calculator pages (Search Console
   URL Inspection -> Request indexing). Do not spam this; the sitemap handles the rest.
4. Set `ANALYTICS_ID` (GA4) as a repository variable so you can see queries and traffic.

Expected at this stage: pages begin appearing in Search Console as "Discovered" then
"Indexed" over days to a few weeks. No traffic yet is normal.

## Phase 2 — On-site foundation (already built, nothing to do)

Internal links, canonicals, schema, sitemap, robots and RSS are in place and verified. This
is the part most sites get wrong; leaving it alone is deliberate.

## Phase 3 — Off-site promotion (weeks 2+, steady cadence)

One or two sessions a week, ~30 minutes each. Rotate channels.

### Q&A (highest-value legitimate links)
- **Reddit** — r/DIY, r/landscaping, r/HomeImprovement, r/gardening. Find real
  "how much mulch/soil/gravel" questions. Give the actual arithmetic for their numbers,
  then add the calculator link. Never post a bare link. Check each subreddit's rules.
- **Stack Exchange** — Gardening & Landscaping, Home Improvement. Answers must be
  self-contained; the link is a supporting tool, not the answer.
- **Quora** — answer "how much ... do I need" questions with the worked formula.
- **DIY/landscaping forums** — most have a signature or a resources area that welcomes
  genuine tool links.

### Discovery and evergreen channels
- **Pinterest** — home and garden is a large Pinterest niche. Pin each article's social
  image with the article title; link to the page.
- **RSS aggregators** — submit `https://<user>.github.io/<repo>/rss.xml` to general and
  home/garden feed directories.
- **Reddit/forum wikis** — some communities keep a tools list; suggest yours only if the
  calculator is genuinely the best fit.

### Outreach (one-off, higher effort)
- **Blog roundups** — search for "best home improvement calculators" and similar; pitch a
  two-line intro: what the tool does, who it helps. Do not ask for a link exchange.
- **Local/national suppliers' resource pages** — a landscape supplier may link to a useful
  calculator. Pitch as a free tool, no reciprocation.
- **Tool directories** — submit only to reputable, curated ones. Skip anything paid that
  cannot show real editorial value.

### Track it
Mark each completed channel: `python scripts/distribution.py --mark <id>`. Re-read the
"ready-to-paste copy" section in the pack rather than rewriting each time.

## Phase 4 — Content growth (steady, low volume)

Do not mass-generate pages. Grow a few genuinely useful articles at a time:

```bash
python scripts/run_all.py --limit 2      # add 2 gated articles
```

Roughly 2-4 new or improved articles a month, aimed at real Search Console queries. The
quality gates refuse thin or duplicate content, so the pace stays honest. Improvement
counts as growth: updating an existing page that ranks on page 2 often beats a new page.

## Phase 5 — Analytics and optimization loop (weekly)

1. Search Console -> *Performance*. Note queries with impressions but low CTR.
2. Improve those pages: tighten the title and meta description to match the query, add a
   section answering it directly, add internal links to and from related articles.
3. Rebuild and let the workflow deploy.
4. Use the built-in tools:
   - `reports/dashboard.html` — per-article SEO score, gate status, growth history.
   - `python scripts/monitor.py` — score snapshot and regression detection.
   - `python scripts/live_audit.py <url> --json reports/live-audit.json` — health over time.

This loop, not link volume, is what usually moves rankings.

## Phase 6 — AdSense (only after indexing and some traffic)

Do not apply yet. Apply when the site is indexed and has begun receiving organic visitors.

1. Confirm readiness: `python scripts/adsense.py` (all checks green).
2. Publish a real contact email (`SITE_CONTACT_EMAIL` variable) — the last open check.
3. Apply at <https://www.google.com/adsense>. Add the AdSense verification snippet.
4. Once approved, set the `ADSENSE_CLIENT` repository variable (`ca-pub-...`); the build
   injects the script automatically.

AdSense approval is not guaranteed and cannot be claimed in advance.

---

## What to do each week

| When | Task |
| --- | --- |
| Week 1 | Verify Search Console + Bing, submit sitemap, request indexing for key pages |
| Week 2 | Two Q&A answers (Reddit or Stack Exchange), set up Pinterest |
| Week 3 | Two more Q&A answers, submit RSS to two aggregators |
| Week 4 | One outreach pitch, review Search Console, improve one page |
| Weekly | Check dashboard; regenerate distribution pack; mark completed channels |
| Monthly | Add or improve 2-4 articles; review the audit report |

## Honest expectations

- Indexing: days to a few weeks after submission.
- First organic traffic: typically weeks to a few months, and it starts small.
- Rankings and links accrue slowly and compound; there is no shortcut that survives an
  update.
- Do not expect AdSense approval before the site is indexed and has real visitors.

Any report of traffic, rankings, backlinks or approval will be based on what Search Console
shows once the site is live — never assumed.
