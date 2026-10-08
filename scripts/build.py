"""Static site build. Reads data/articles.json + config, writes site/."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

import charts
import images
import mdrender
import planners
import seo as seolib
from common import (CONFIG, CONTENT, DATA, SITE, STATIC, TEMPLATES, load_json,
                    save_json, seo_config, site_config, topics_config)

YEAR = dt.date.today().year

# Cross-cluster "next step" links: after the primary job, these are the usual follow-ups.
# Links between calculator pillars spread crawl equity and match how a real project flows.
PROJECT_NEXT_STEPS = {
    "mulch": ["soil", "topsoil", "fertilizer"],
    "soil": ["mulch", "topsoil", "gravel"],
    "topsoil": ["grass-seed", "soil", "fertilizer"],
    "gravel": ["concrete", "soil", "mulch"],
    "concrete": ["gravel", "paint", "tile"],
    "paint": ["tile", "concrete", "gravel"],
    "tile": ["paint", "concrete", "gravel"],
    "grass-seed": ["topsoil", "fertilizer", "soil"],
    "fertilizer": ["grass-seed", "topsoil", "soil"],
}

# Extra indexable site pages, appended to the sitemap with a real lastmod.
EXTRA_PAGES = ["/calculators/", "/guides/", "/sitemap/", "/for-publishers/"]
# Inline SVG icon id for each project category (symbols live in base.html).
CATEGORY_ICONS = {
    "mulch": "mulch", "soil": "soil", "gravel": "gravel", "paint": "paint",
    "tile": "tile", "grass-seed": "seed", "concrete": "concrete",
    "topsoil": "topsoil", "fertilizer": "fertilizer",
}
BLURBS = {
    "mulch": "Work out bags or cubic yards of mulch for any bed size and depth.",
    "soil": "Fill raised beds with the right amount of soil mix.",
    "gravel": "Calculate cubic yards and tons of gravel for paths and drives.",
    "paint": "Estimate gallons of paint per room, coats and openings.",
    "tile": "Count tiles and waste allowance for floors and walls.",
    "grass-seed": "Seed a new lawn or overseed an existing one at the right rate.",
    "concrete": "Get cubic yards and bag counts for slabs and footings.",
    "topsoil": "Estimate cubic yards or bags of topsoil to fill or level any area.",
    "fertilizer": "Find pounds and bags of fertilizer for your lawn at the right rate.",
}
# What the figure shows, per category — used for the caption and image alt text.
FIG_CAPTION = {
    "mulch": "Cross-section of a mulched bed: area x depth gives the volume to order.",
    "soil": "Cross-section of a raised bed being filled to its working height.",
    "topsoil": "Cross-section of an area being levelled with topsoil.",
    "gravel": "Cross-section of a gravel layer at the chosen depth.",
    "concrete": "Cross-section of a concrete slab at the chosen thickness.",
    "paint": "How the number of coats multiplies the paint you need.",
    "grass-seed": "Sowing rates per 1,000 sq ft for new lawns and overseeding.",
    "fertilizer": "Application rates per 1,000 sq ft at light, standard and heavy doses.",
    "tile": "Tile layout showing the waste allowance added for cuts and breakage.",
}


def _env() -> Environment:
    return Environment(loader=FileSystemLoader(str(TEMPLATES)),
                       autoescape=select_autoescape(["html", "xml"]))


def _base(site: dict) -> str:
    return (site.get("custom_domain") or site["base_url"]).rstrip("/")


def _abs(site: dict, path: str) -> str:
    return _base(site) + "/" + path.lstrip("/")


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _contact_block(site: dict) -> str:
    """Honest contact route: a real email if configured, otherwise the repo issues page."""
    email = site.get("contact_email", "").strip()
    if email and "example.com" not in email:
        return f"Email us at **{email}** and we will reply within a few working days."
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if repo:
        return (f"The fastest way to reach us is to open an issue on the project's "
                f"[GitHub repository](https://github.com/{repo}/issues). We reply within "
                f"a few working days.")
    return ("Contact details will be published here shortly. In the meantime, please use "
            "the repository's issue tracker if you found this project through GitHub.")


def _reading_time(words: int) -> int:
    return max(1, round(words / 220))


def _thumb(site: dict, art: dict) -> str:
    """Article thumbnail URL (theme figure), with a CSS fallback if images were skipped."""
    return _abs(site, f"/static/img/thumb/{art['slug']}.webp")


def _fig(site: dict, art: dict) -> str:
    return _abs(site, f"/static/img/fig/{art['slug']}.webp")


def _card_meta(site: dict, art: dict, category: str | None = None) -> dict:
    return {
        "slug": art["slug"],
        "title": art["title"],
        "desc": art.get("meta_description", "")[:120],
        "thumb": _thumb(site, art),
        "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        "category": category,
        "updated": art.get("updated", ""),
    }


def _calc_context(art: dict, cfg: dict, site: dict) -> dict | None:
    calc_key = art.get("calculator")
    defs = cfg.get("calculators", {}).get(calc_key)
    if not defs:
        return None
    inputs = []
    defaults = {}
    for inp in defs.get("inputs", []):
        d = dict(inp)
        d.setdefault("step", "0.1")
        inputs.append(d)
        defaults[d["id"]] = d.get("default")
    return {
        "key": calc_key,
        "title": art.get("calculator_title") or defs.get("title", "Calculator"),
        "sub": "Change any value and the answer updates instantly. Nothing is sent anywhere — it runs in your browser.",
        "hint": "Estimates only. Round up when ordering and check with your supplier.",
        "inputs": inputs,
        "defaults": defaults,
        "slug": art["slug"],
    }


def build() -> dict:
    site = site_config()
    tcfg = topics_config()
    arts = load_json(DATA / "articles.json", default=[])
    published = [a for a in arts
                 if a.get("status") in ("published", "approved")
                 and a.get("quality", {}).get("passed")]
    published.sort(key=lambda a: a.get("created", ""), reverse=True)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    base = _base(site)
    categories = tcfg.get("clusters", [])
    for c in categories:
        c["blurb"] = BLURBS.get(c["id"], "Free calculators and practical guides.")
        c["icon"] = CATEGORY_ICONS.get(c["id"], "leaf")
    cat_map = {c["id"]: c for c in categories}
    nav_categories = [{"id": c["id"], "name": c["name"]} for c in categories]

    env = _env()
    env.globals.update(base_url=base, site=site, year=YEAR,
                       nav_categories=nav_categories, calc_defs=tcfg.get("calculators", {}))

    default_og = _thumb(site, published[0]) if published else _abs(site, "/static/img/og-default.png")

    def common(title, description, canonical, og_type="website", og_image=None,
               schemas=None, robots=None, keywords=None):
        return dict(title=title, description=description, canonical=canonical,
                    og_type=og_type, og_image=og_image or default_og,
                    schemas=schemas or [],
                    robots=robots or "index, follow, max-snippet:-1, max-image-preview:large",
                    keywords=keywords, base_url=base)

    # Index for prev/next within each cluster, ordered by creation date.
    by_cluster: dict[str, list[dict]] = {}
    for a in sorted(published, key=lambda x: x.get("created", "")):
        by_cluster.setdefault(a.get("cluster", ""), []).append(a)
    order_index = {a["slug"]: i for lst in by_cluster.values() for i, a in enumerate(lst)}
    pillar_by_cluster = {a.get("cluster"): a for a in published if a.get("is_pillar")}
    chart_cards = [{"slug": ch["slug"], "title": ch["title"], "description": ch["description"],
                    "cluster_name": cat_map.get(ch["cluster"], {}).get("name", ch["cluster"].title())}
                   for ch in charts.CHARTS]
    planner_cards = [{"slug": pl["slug"], "title": pl["title"], "description": pl["description"],
                      "cluster_name": cat_map.get(pl["cluster"], {}).get("name", pl["cluster"].title())}
                     for pl in planners.PLANNERS]

    # --- articles ---
    for art in published:
        body_html, toc = mdrender.render_with_toc(art.get("body_markdown", ""),
                                                  {x["slug"]: f"{base}/{x['slug']}/" for x in published})
        figure = {
            "src": _fig(site, art),
            "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
            "caption": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        }
        ct = cat_map.get(art.get("cluster", ""), {})
        category_name = ct.get("name", "Guides")

        # Related: sibling articles in the same cluster, excluding self.
        cl = by_cluster.get(art.get("cluster", ""), [])
        sib = [a for a in cl if a["slug"] != art["slug"]]
        pos = next((i for i, a in enumerate(cl) if a["slug"] == art["slug"]), 0)
        prev_art = cl[pos - 1] if pos > 0 else None
        next_art = cl[pos + 1] if pos + 1 < len(cl) else None
        related = [_card_meta(site, a, category_name) for a in sib[:3]]

        # "Plan the whole project": link to the pillar calculator of the usual follow-up
        # clusters, so crawl equity moves between categories and users find the next step.
        project_links = []
        for cid in PROJECT_NEXT_STEPS.get(art.get("cluster", ""), []):
            p = pillar_by_cluster.get(cid)
            if p and p["slug"] != art["slug"]:
                project_links.append({"slug": p["slug"], "title": p["title"],
                                      "desc": p.get("meta_description", "")[:90]})

        # Answer-first block (featured-snippet bait): the first FAQ answer is a direct,
        # numeric answer to the page's main question.
        faq_items = art.get("faq") or []
        answer_first = faq_items[0]["a"] if faq_items else art.get("meta_description", "")

        schemas = [json.dumps(s, ensure_ascii=False) for s in
                   seolib.all_schema(art, site, figure=_fig(site, art))]
        calc_ctx = _calc_context(art, tcfg, site)
        if calc_ctx:
            schemas.append(json.dumps(seolib.webapp_schema(
                calc_ctx["title"], _abs(site, f"/{art['slug']}/"),
                art.get("meta_description", ""), site), ensure_ascii=False))
        ctx = common(title=art["title"], description=art["meta_description"],
                     canonical=_abs(site, f"/{art['slug']}/"), og_type="article",
                     og_image=_fig(site, art), schemas=schemas,
                     keywords=", ".join([art.get("primary_keyword", "")] +
                                        art.get("secondary_keywords", [])))
        ctx.update(article=art, body_html=body_html, toc=toc, figure=figure,
                   calc=calc_ctx, faq=faq_items, answer_first=answer_first,
                   category_name=category_name, reading_time=_reading_time(art.get("word_count", 0)),
                   related=related, project_links=project_links,
                   pager={"prev": {"slug": prev_art["slug"], "title": prev_art["title"]} if prev_art else None,
                          "next": {"slug": next_art["slug"], "title": next_art["title"]} if next_art else None})
        _write(SITE / art["slug"] / "index.html",
               env.get_template("article.html").render(**ctx))

    # --- categories ---
    for c in categories:
        items = [a for a in published if a.get("cluster") == c["id"]]
        pillars = [a for a in items if a.get("is_pillar")]
        others = [a for a in items if not a.get("is_pillar")]
        og = _thumb(site, pillars[0]) if pillars else (_thumb(site, items[0]) if items else _abs(site, "/static/img/og-default.png"))
        ctx = common(title=f"{c['name']} Calculators | {site['name']}",
                     description=(c["blurb"] + " Free, instant calculators with the formula shown.")[:155],
                     canonical=_abs(site, f"/category/{c['id']}/"), og_image=og,
                     schemas=[json.dumps(seolib.collection_schema(
                         c, items, site), ensure_ascii=False)])
        ctx.update(category=c,
                   pillars=[_card_meta(site, a, c["name"]) for a in pillars],
                   others=[_card_meta(site, a, c["name"]) for a in others])
        _write(SITE / "category" / c["id"] / "index.html",
               env.get_template("category.html").render(**ctx))

    # --- homepage ---
    pillars = [a for a in published if a.get("is_pillar")][:8]
    ctx = common(title=f"{site['name']} — Free Home & Garden Calculators",
                 description=("Free mulch, soil, topsoil, gravel, fertilizer, paint, tile, seed and "
                              "concrete calculators. Instant answers with the formula shown."),
                 canonical=_abs(site, "/"),
                 schemas=[json.dumps(seolib.website_schema(site), ensure_ascii=False),
                          json.dumps(seolib.organization_schema(site), ensure_ascii=False)])
    ctx.update(categories=categories, articles=published[:12],
               article_count=len(published), category_count=len(categories),
               chart_count=len(charts.CHARTS), chart_cards=chart_cards,
               planner_cards=planner_cards,
               pillar_cards=[_card_meta(site, a) for a in pillars])
    _write(SITE / "index.html", env.get_template("index.html").render(**ctx))

    # --- legal / info pages ---
    pages = [
        ("about", "About", "Who we are and how our calculators work."),
        ("contact", "Contact", "Get in touch with the team."),
        ("privacy-policy", "Privacy Policy", "How we handle data and cookies."),
        ("terms", "Terms of Use", "The terms for using this site."),
        ("disclaimer", "Disclaimer", "Important limitations of our calculators."),
    ]
    for slug, title, desc in pages:
        src = CONTENT / "pages" / f"{slug}.md"
        body = src.read_text(encoding="utf-8") if src.exists() else f"# {title}\n\nComing soon."
        body = (body.replace("{{SITE_NAME}}", site["name"])
                    .replace("{{CONTACT_EMAIL}}", site.get("contact_email", ""))
                    .replace("{{CONTACT_BLOCK}}", _contact_block(site)))
        body = re.sub(r"\A\s*#\s+.*?\n", "", body)
        ctx = common(title=f"{title} | {site['name']}", description=desc[:155],
                     canonical=_abs(site, f"/{slug}/"),
                     schemas=[json.dumps(seolib.webpage_schema(title, desc, _abs(site, f"/{slug}/"), site),
                                         ensure_ascii=False),
                              json.dumps(seolib.breadcrumb_list(
                                  [("Home", "/"), (title, f"/{slug}/")], site),
                                  ensure_ascii=False)])
        ctx.update(page={"title": title, "html": mdrender.render(body)})
        _write(SITE / slug / "index.html", env.get_template("page.html").render(**ctx))

    # --- search (client-side; backs the WebSite SearchAction) ---
    search_index = [{"t": a["title"], "s": a["slug"], "k": a.get("primary_keyword", ""),
                     "c": cat_map.get(a.get("cluster", ""), {}).get("name", ""),
                     "d": a.get("meta_description", "")} for a in published]
    ctx = common(title=f"Search | {site['name']}",
                 description="Search GardenCalc's mulch, soil, gravel and other calculators.",
                 canonical=_abs(site, "/search/"), robots="noindex, follow")
    ctx.update(page={"title": "Search calculators & guides",
                     "html": '<div id="search-ui"><input type="search" id="q" '
                             'placeholder="Search calculators and guides…" aria-label="Search">'
                             '<ul id="results" class="post-list"></ul></div>',
                     "search": True})
    _write(SITE / "search" / "index.html", env.get_template("page.html").render(**ctx))

    # --- 404 ---
    cats_links = "".join(f'<li><a href="{base}/category/{c["id"]}/">{c["name"]} calculator</a></li>'
                         for c in categories)
    ctx = common(title=f"Page not found | {site['name']}",
                 description="The page you requested was not found.",
                 canonical=_abs(site, "/404.html"), robots="noindex, follow")
    ctx.update(page={"title": "Page not found",
                     "html": ("<p>That page does not exist. Try the <a href='" + base + "/'>homepage</a>, "
                              "or jump straight to a category:</p><ul>" + cats_links + "</ul>")})
    _write(SITE / "404.html", env.get_template("page.html").render(**ctx))

    # --- chart pages (linkable, formula-derived reference tables) ---
    for ch in charts.CHARTS:
        cluster = cat_map.get(ch["cluster"], {})
        cluster_name = cluster.get("name", ch["cluster"].title())
        cp = charts.page(ch, base, site)
        calc_slug = ch.get("calc", "")
        cctx = common(title=ch["title"], description=ch["description"],
                      canonical=cp["url"], og_type="article",
                      og_image=_thumb(site, pillar_by_cluster.get(ch["cluster"], published[0])),
                      keywords=ch["keyword"],
                      schemas=[json.dumps(seolib.breadcrumb_list(
                                   [("Home", "/"), (cluster_name, f"/category/{ch['cluster']}/"),
                                    (ch["title"], f"/{ch['slug']}/")], site), ensure_ascii=False),
                               json.dumps(seolib.webpage_schema(
                                   ch["title"], ch["description"], cp["url"], site),
                                   ensure_ascii=False),
                               json.dumps(seolib.faq_schema(
                                   {"faq": [{"q": q, "a": a} for q, a in ch["faqs"]]}),
                                   ensure_ascii=False)])
        cctx.update(chart=cp, cluster_name=cluster_name,
                    answer=ch["faqs"][0][1] if ch.get("faqs") else ch["description"],
                    pin_image=_abs(site, f"/static/img/pins/{ch['slug']}.png"))
        _write(SITE / ch["slug"] / "index.html",
               env.get_template("chart.html").render(**cctx))

    # --- project planners (multi-material shopping lists) ---
    for pl in planners.PLANNERS:
        cluster = cat_map.get(pl["cluster"], {})
        cluster_name = cluster.get("name", pl["cluster"].title())
        pp = planners.page(pl, base, site)
        pctx = common(title=pl["title"], description=pl["description"],
                      canonical=pp["url"], og_type="article",
                      og_image=_thumb(site, pillar_by_cluster.get(pl["cluster"], published[0])),
                      keywords=pl["question"],
                      schemas=[json.dumps(seolib.breadcrumb_list(
                                   [("Home", "/"), (cluster_name, f"/category/{pl['cluster']}/"),
                                    (pl["title"], f"/{pl['slug']}/")], site), ensure_ascii=False),
                               json.dumps(seolib.webpage_schema(
                                   pl["title"], pl["description"], pp["url"], site),
                                   ensure_ascii=False),
                               json.dumps(seolib.faq_schema(
                                   {"faq": [{"q": q, "a": a} for q, a in pl["faqs"]]}),
                                   ensure_ascii=False)])
        pctx.update(planner=pp, cluster_name=cluster_name,
                    answer=pl["faqs"][0][1] if pl.get("faqs") else pl["description"],
                    pin_image=_abs(site, f"/static/img/pins/{pl['slug']}.png"))
        _write(SITE / pl["slug"] / "index.html",
               env.get_template("planner.html").render(**pctx))

    # --- calculators hub ---
    groups = []
    for c in categories:
        cards = [_card_meta(site, a, c["name"]) for a in published
                 if a.get("cluster") == c["id"] and a.get("is_pillar")]
        if cards:
            groups.append({"id": c["id"], "name": c["name"], "cards": cards})
    ctx = common(title=f"Home & Garden Calculators | {site['name']}",
                 description=("Every free GardenCalc calculator in one place: mulch, soil, topsoil, "
                              "gravel, paint, tile, grass seed, concrete and fertilizer."),
                 canonical=_abs(site, "/calculators/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Calculators", "/calculators/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=groups, chart_cards=chart_cards, planner_cards=planner_cards)
    _write(SITE / "calculators" / "index.html",
           env.get_template("calculators.html").render(**ctx))

    # --- guides index (all non-pillar articles, grouped, filterable) ---
    guide_groups = []
    for c in categories:
        items = [_card_meta(site, a, c["name"]) for a in published
                 if a.get("cluster") == c["id"] and not a.get("is_pillar")]
        if items:
            guide_groups.append({"id": c["id"], "name": c["name"], "entries": items})
    ctx = common(title=f"Garden & Home Project Guides | {site['name']}",
                 description=("Every GardenCalc how-to guide in one place, grouped by project: "
                              "mulch, soil, gravel, paint, tile, seed, concrete and more."),
                 canonical=_abs(site, "/guides/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Guides", "/guides/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=guide_groups)
    _write(SITE / "guides" / "index.html", env.get_template("guides.html").render(**ctx))

    # --- HTML sitemap (human-readable; helps discovery and internal linking) ---
    site_pages = [{"slug": s, "title": t} for s, t, _ in pages]
    ctx = common(title=f"Sitemap | {site['name']}",
                 description=("A full list of every calculator, chart and guide on "
                              f"{site['name']}."),
                 canonical=_abs(site, "/sitemap/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Sitemap", "/sitemap/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=guide_groups,
               calculators=[_card_meta(site, a, cat_map.get(a.get("cluster", ""), {}).get("name", ""))
                            for a in published if a.get("is_pillar")],
               chart_cards=chart_cards, planner_cards=planner_cards, site_pages=site_pages)
    _write(SITE / "sitemap" / "index.html", env.get_template("sitemap.html").render(**ctx))

    # --- for publishers (indexable; explains how to embed/cite the calculators) ---
    embeds = []
    for a in published:
        if a.get("is_pillar") and a.get("calculator"):
            embeds.append({"title": a.get("calculator_title") or a["title"],
                           "calc_slug": a["slug"],
                           "embed_url": _abs(site, f"/embed/{a['calculator']}/")})
    ctx = common(title=f"Embed or Cite Our Calculators | {site['name']}",
                 description=("Free embeddable garden and home calculators. Add a mulch, soil or "
                              "concrete calculator to your site with one line of HTML."),
                 canonical=_abs(site, "/for-publishers/"),
                 schemas=[json.dumps(seolib.breadcrumb_list(
                              [("Home", "/"), ("For publishers", "/for-publishers/")], site),
                              ensure_ascii=False)])
    ctx.update(embeds=embeds)
    _write(SITE / "for-publishers" / "index.html",
           env.get_template("publishers.html").render(**ctx))

    # --- embed pages (noindex, canonical to the full calculator; not in the sitemap) ---
    for a in published:
        if not (a.get("is_pillar") and a.get("calculator")):
            continue
        calc_ctx = _calc_context(a, tcfg, site)
        if not calc_ctx:
            continue
        ectx = dict(site=site, base_url=base, calc=calc_ctx,
                    canonical=_abs(site, f"/{a['slug']}/"),
                    calc_url=_abs(site, f"/{a['slug']}/"))
        _write(SITE / "embed" / a["calculator"] / "index.html",
               env.get_template("embed.html").render(**ectx))

    # --- static (copied first so generated figures sit in site/static) ---
    static_dest = SITE / "static"
    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(STATIC, static_dest)

    # Generate original figures into the copied static dir so pages can link them.
    img_stats = images.generate(published, static_dest)
    brand_stats = images.render_brand(static_dest)
    pin_cards = [{"slug": ch["slug"], "title": ch["title"], "question": charts.CHART_QUESTIONS.get(ch["slug"], ""),
                  "cluster": ch["cluster"]} for ch in charts.CHARTS]
    pin_cards += [{"slug": pl["slug"], "title": pl["title"], "question": pl["question"],
                   "cluster": pl["cluster"]} for pl in planners.PLANNERS]
    pin_stats = images.render_pins(pin_cards, static_dest)
    _write(static_dest / "search-index.json", json.dumps(search_index, ensure_ascii=False))

    # --- sitemap, robots, rss, CNAME ---
    # Only canonical, indexable pages go in the sitemap. <priority> is omitted: it is
    # ignored by Google/Bing, so emitting it only adds noise.
    today = dt.date.today().isoformat()
    urls = [{"loc": "/", "lastmod": today,
             "image": _thumb(site, published[0]) if published else None,
             "image_title": site["name"]}]
    urls += [{"loc": f"/category/{c['id']}/", "lastmod": today} for c in categories]
    urls += [{"loc": f"/{a['slug']}/", "lastmod": a.get("updated"),
              "image": _fig(site, a), "image_title": a["title"]} for a in published]
    urls += [{"loc": f"/{ch['slug']}/", "lastmod": today} for ch in charts.CHARTS]
    urls += [{"loc": f"/{pl['slug']}/", "lastmod": today} for pl in planners.PLANNERS]
    urls += [{"loc": f"/{s}/", "lastmod": today} for s, _, _ in pages]
    urls += [{"loc": p, "lastmod": today} for p in EXTRA_PAGES]
    _write(SITE / "sitemap.xml", seolib.sitemap_xml(urls, site))
    _write(SITE / "robots.txt", seolib.robots_txt(site, _abs(site, "/sitemap.xml")))
    feed_extra = [{"title": ch["title"], "url": _abs(site, f"/{ch['slug']}/"),
                   "description": ch["description"]} for ch in charts.CHARTS]
    feed_extra += [{"title": pl["title"], "url": _abs(site, f"/{pl['slug']}/"),
                    "description": pl["description"]} for pl in planners.PLANNERS]
    _write(SITE / "rss.xml", seolib.rss_xml(published, site, extra=feed_extra))
    if site.get("custom_domain"):
        _write(SITE / "CNAME", site["custom_domain"] + "\n")
    _write(SITE / ".nojekyll", "")

    _generate_og_images(published, site)

    indexnow_key = str(site.get("indexnow_key", "")).strip()
    if indexnow_key:
        _write(SITE / f"{indexnow_key}.txt", indexnow_key)

    stats = {
        "built": dt.datetime.now(dt.timezone.utc).isoformat(),
        "articles": len(published),
        "categories": len(categories),
        "pages": len(pages) + 1,
        "urls": len(urls),
        "figures": img_stats.get("figures", 0),
    }
    save_json(DATA / "build.json", stats)
    print(f"[build] {stats}")
    return stats


def _generate_og_images(arts: list[dict], site: dict) -> None:
    """Lightweight SVG social images (no external service, no cost)."""
    out = SITE / "static" / "img" / "og"
    out.mkdir(parents=True, exist_ok=True)

    def card(title: str, sub: str) -> str:
        t = title[:70].replace("&", "&amp;").replace("<", "&lt;")
        s = sub[:90].replace("&", "&amp;").replace("<", "&lt;")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">'
                f'<rect width="1200" height="630" fill="#14532d"/>'
                f'<rect x="40" y="40" width="1120" height="550" fill="#166534" rx="24"/>'
                f'<text x="90" y="300" font-family="Georgia,serif" font-size="54" fill="#f0fdf4">{t}</text>'
                f'<text x="90" y="380" font-family="Arial" font-size="30" fill="#bbf7d0">{s}</text>'
                f'<text x="90" y="540" font-family="Arial" font-size="26" fill="#86efac">{site["name"]}</text>'
                f'</svg>')

    _write(out / ".." / "og-default.svg", card(site["name"], site.get("tagline", "")))
    for a in arts:
        _write(out / f"{a['slug']}.svg", card(a["title"], a["meta_description"]))


if __name__ == "__main__":
    build()
