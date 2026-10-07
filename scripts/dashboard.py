"""Build a single-file HTML dashboard from the data/ JSON artifacts."""
from __future__ import annotations

import datetime as dt
import json

from common import DATA, REPORTS, SITE, load_json, save_json, site_config

TEMPLATE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEO Autoblog Dashboard</title>
<style>
body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#0f172a;color:#e2e8f0}
.wrap{max-width:1080px;margin:0 auto;padding:24px}
h1{font-size:1.5rem}h2{font-size:1.1rem;margin-top:1.6em;color:#94a3b8}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.card{background:#1e293b;border-radius:10px;padding:14px}
.card .n{font-size:1.7rem;font-weight:700;color:#4ade80}
.card .l{font-size:.8rem;color:#94a3b8}
table{width:100%;border-collapse:collapse;font-size:.86rem;margin-top:8px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #334155}
.ok{color:#4ade80}.bad{color:#f87171}.warn{color:#fbbf24}
a{color:#60a5fa}
</style></head><body><div class="wrap">
<h1>SEO Autoblog Dashboard <span style="font-size:.7rem;color:#64748b">{{built}}</span></h1>
<div class="cards">
{% for c in cards %}<div class="card"><div class="n">{{c.n}}</div><div class="l">{{c.l}}</div></div>{% endfor %}
</div>

<h2>Articles</h2>
<table><tr><th>Slug</th><th>Status</th><th>Words</th><th>Score</th><th>Links</th><th>Failing gates</th></tr>
{% for a in articles %}<tr>
<td><a href="../site/{{a.slug}}/index.html">{{a.slug}}</a></td>
<td class="{{'ok' if a.status in ['approved','published'] else 'bad'}}">{{a.status}}</td>
<td>{{a.words}}</td><td>{{a.score}}</td><td>{{a.links}}</td>
<td class="warn">{{a.fails|join(', ')}}</td></tr>{% endfor %}</table>

<h2>Site health</h2>
<p>Pages: {{health.pages}} · Issues: <span class="{{'ok' if health.issues_total==0 else 'bad'}}">{{health.issues_total}}</span></p>
{% if health.by_type %}<ul>{% for k,v in health.by_type.items() %}<li>{{k}}: {{v}}</li>{% endfor %}</ul>{% endif %}

<h2>AdSense readiness</h2>
<p>Passed {{adsense.passed}}/{{adsense.total}} {% if adsense.ready %}<span class="ok">READY</span>{% else %}<span class="bad">not ready</span>{% endif %}</p>
<ul>{% for k,v in adsense.checks.items() %}<li class="{{'ok' if v.ok else 'bad'}}">{{k}}: {{v.detail}}</li>{% endfor %}</ul>

<h2>Growth history</h2>
<table><tr><th>Date</th><th>Articles</th><th>Total words</th><th>Avg score</th></tr>
{% for h in history %}<tr><td>{{h.date}}</td><td>{{h.articles}}</td><td>{{h.total_words}}</td><td>{{h.avg_seo_score}}</td></tr>{% endfor %}</table>

<h2>Distribution</h2>
<p>Manual actions completed: {{dist.done}}/{{dist.total}}</p>
<ul>{% for i in dist.actions %}<li class="{{'ok' if i.done else 'warn'}}">{{'[x]' if i.done else '[ ]'}} {{i.title}}</li>{% endfor %}</ul>

</div></body></html>"""


def build() -> dict:
    site = site_config()
    arts = load_json(DATA / "articles.json", default=[])
    health = load_json(DATA / "health.json", default={"pages": 0, "issues_total": 0, "by_type": {}})
    ads = load_json(DATA / "adsense.json", default={"passed": 0, "total": 0, "ready": False, "checks": {}})
    hist = load_json(DATA / "history.json", default=[])
    dist = load_json(DATA / "distribution.json", default={"items": [], "done": 0, "total": 0})
    buildinfo = load_json(DATA / "build.json", default={})

    rows = []
    for a in arts:
        gates = a.get("quality", {}).get("gates", {})
        rows.append({
            "slug": a["slug"], "status": a.get("status"),
            "words": a.get("word_count", 0),
            "score": a.get("quality", {}).get("score", 0),
            "links": len(a.get("internal_links", [])),
            "fails": [k for k, v in gates.items() if not v.get("pass")],
        })

    published = [a for a in arts if a.get("status") in ("published", "approved")]
    cards = [
        {"n": len(published), "l": "published articles"},
        {"n": sum(a.get("word_count", 0) for a in published), "l": "total words"},
        {"n": health.get("issues_total", 0), "l": "health issues"},
        {"n": ads.get("passed", 0), "l": "adsense checks"},
        {"n": len(hist), "l": "monitor snapshots"},
    ]

    from jinja2 import Environment
    html = Environment(autoescape=True).from_string(TEMPLATE).render(
        built=buildinfo.get("built", ""), cards=cards, articles=rows,
        health=health, adsense=ads, history=hist[-14:], dist=dist)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "dashboard.html").write_text(html, encoding="utf-8")
    print(f"[dashboard] wrote {REPORTS / 'dashboard.html'}")
    return {"path": str(REPORTS / "dashboard.html")}


if __name__ == "__main__":
    build()
