# Fixing the "Couldn't fetch" sitemap error in Google Search Console

Verified on 2026-10-26 against the live site. Read this before changing any code:
**the sitemap file itself is not broken**, so no code change can fix this error.
The problem is *which property* the sitemap was submitted to and *what was typed*
in the submission box.

## What was tested (all live, 2026-10-26)

| Check | Result |
|---|---|
| `GET https://huzaifamasood30.github.io/gardencalc/sitemap.xml` | **200 OK**, `Content-Type: application/xml`, 52,274 bytes |
| XML well-formed, sitemap namespace correct | Yes |
| URLs in sitemap | **157, all unique** |
| Every one of the 157 URLs fetched individually | **All 200 OK** (no redirects, no 404s) |
| Every image URL referenced in the sitemap | **All 200 OK** |
| Canonical on each page | Self-referencing, matches the sitemap URL exactly |
| `noindex` pages in the sitemap | None |
| `GET https://huzaifamasood30.github.io/sitemap.xml` (host root) | **404** — there is no site at the host root |
| `GET https://huzaifamasood30.github.io/robots.txt` (host root) | **404** — treated by Google as "allow everything" |

## Root cause

GardenCalc is a GitHub Pages **project site**: it lives under the path
`/gardencalc/` on the shared host `huzaifamasood30.github.io`. It is not the
host itself.

That means the sitemap only exists at:

```
https://huzaifamasood30.github.io/gardencalc/sitemap.xml
```

Two submission mistakes both produce exactly the "Couldn't fetch" status:

1. **Wrong property.** If the Search Console property is the bare host
   `https://huzaifamasood30.github.io/` (or a Domain property), then entering
   `sitemap.xml` makes Google fetch `https://huzaifamasood30.github.io/sitemap.xml`,
   which is a **404** (verified above). Google reports that as "Couldn't fetch".
2. **Full URL pasted into the box.** In a URL-prefix property for
   `https://huzaifamasood30.github.io/gardencalc/`, the *Sitemaps* box already
   contains that prefix. Pasting the full URL produces
   `https://huzaifamasood30.github.io/gardencalc/https://huzaifamasood30.github.io/gardencalc/sitemap.xml`,
   which is also a 404.

A related dead end: Google only reads `robots.txt` from the host root
(`https://huzaifamasood30.github.io/robots.txt`). A project site cannot serve
that file, so a `Sitemap:` line in `/gardencalc/robots.txt` is never read by
Google. That is why `scripts/seo.py` deliberately does not emit one, and why
sitemap discovery for this site must happen through Search Console (below),
the `<link rel="sitemap">` tag every page already carries, and the RSS feed.

## The fix (5 minutes, in the owner's Google account)

1. Open <https://search.google.com/search-console> and open the property
   dropdown (top left).
2. The property you need is a **URL-prefix** property named exactly:
   `https://huzaifamasood30.github.io/gardencalc/`
   - If it is not in the list: *Add property → URL prefix →* paste that URL →
     verify with the **HTML tag** method. The tag is already on every page
     (it comes from `google_site_verification` in `config/site.json`), so
     verification succeeds immediately.
   - If you also have a bare-host or Domain property, leave it alone — just
     do not use it for this site.
3. In that property, go to **Indexing → Sitemaps**.
4. If there is an existing entry showing "Couldn't fetch", click it → ⋮ →
   **Remove sitemap**. (Removing it loses nothing; it never worked.)
5. In *"Add a new sitemap"*, type **only**:

   ```
   sitemap.xml
   ```

   Nothing else — no domain, no leading slash. The full URL Google will fetch
   is shown above the box; confirm it reads
   `https://huzaifamasood30.github.io/gardencalc/sitemap.xml`, then **Submit**.
6. The status should turn **Success** with **157 discovered pages** within a
   few minutes to a few hours. "Couldn't fetch" can linger in the UI from the
   old entry — judge the *new* entry, not the cached row.

## Then: ask Google to crawl the important pages

Sitemap submission puts pages in the crawl queue; it does not jump it. For the
pages that matter, use **URL Inspection → Request Indexing** (about 10/day is
the practical limit). The priority list is in
`reports/request-indexing-urls.txt` — homepage first, then the 13 calculator
pillars, then the planners.

## Then: Bing (one import, fixes IndexNow too)

1. <https://www.bing.com/webmasters> → **Import from Google Search Console**.
2. Submit the same sitemap URL there.
3. This also unblocks IndexNow: Bing returns `403 UserForbiddedToAccessSite`
   for this site until it is verified in Bing Webmaster Tools, because the
   IndexNow key file cannot be served from the `github.io` host root.

## What "fixed" looks like

- Sitemaps report: **Success**, 157 discovered URLs.
- Pages report: over the following 1–3 weeks, pages move from
  "Discovered – currently not indexed" / "Crawled – currently not indexed"
  to "Indexed". A brand-new site with no backlinks will not index all
  157 pages at once, and that is normal — see `reports/seo-audit-2026-10-26.md`.
