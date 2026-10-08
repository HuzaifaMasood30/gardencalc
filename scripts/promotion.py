"""Promotion: curated, no-login backlink targets with exact ready-to-post copy.

This is the actionable layer over ``distribution.py``. Where the distribution pack
describes *channels*, this module names the *specific* place (a real, currently open
question; a real resource page), the exact GardenCalc page to promote, the exact text,
the anchor, and the known link type and posting rules. It writes a single playbook the
site owner can work top-to-bottom.

It also owns the dedupe guard: every opportunity carries a stable ``uid`` of
``<platform>:<target-url>``. ``done`` marks a uid as used so the same community or
question is never targeted twice by accident, and ``check`` fails loudly on a duplicate.

Nothing here posts, registers, or emails on the owner's behalf: those need the owner's
account. What this removes is the thinking and typing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, REPORTS, load_json, save_json  # noqa: E402

BASE = "https://huzaifamasood30.github.io/gardencalc"
LOG = DATA / "promotion-log.json"

# Link type by platform, as commonly implemented (platforms change this without
# notice; verify with a browser dev tools > inspect > rel attribute after posting).
LINK_TYPE = {
    "stackexchange": "nofollow (external links are nofollow; still sends referral traffic)",
    "reddit": "nofollow",
    "quora": "nofollow",
    "pinterest": "nofollow (outbound pins are nofollow)",
    "hackernews": "nofollow",
    "blog-outreach": "depends on the publisher (often dofollow in-post)",
    "resource-page": "depends on the publisher (often dofollow)",
    "directory": "varies; prefer curated listings that use dofollow",
    "citation": "nofollow (Wikipedia) / depends elsewhere",
}

STOP = "Disclose that the site is yours. Give the full method, not just a link."


def _se(todo, title, url, site, promote, anchor, answer):
    return {
        "platform": "Stack Exchange",
        "uid": f"stackexchange:{url}",
        "community": site,
        "target": title,
        "url": url,
        "promote": promote,
        "anchor": anchor,
        "copy": answer,
        "link_type": LINK_TYPE["stackexchange"],
        "notes": ("Answer is self-contained; the calculator is a supporting tool, not the answer. "
                  "Disclose you built it. Only one link. If a good answer already exists, improve "
                  "it with an edit rather than posting a competing answer."),
        "requirement": "User action required (needs your Stack Exchange login; 1 rep to post)",
        "publish": todo,
    }


def opportunities() -> list[dict]:
    return [
        _se(
            False,
            "How much concrete for a fence post?",
            "https://diy.stackexchange.com/questions/87204/how-much-concrete-for-a-fence-post",
            "Home Improvement (diy.stackexchange.com)",
            f"{BASE}/how-many-bags-of-concrete-do-i-need-for-a-fence-post/",
            "how many bags of concrete for a fence post",
            (
                "Concrete for a post hole is just the volume of the hole divided by the yield of "
                "the bag, so the number you need is the hole volume, not the post volume.\n\n"
                "For a 4x4 post you want the hole wider than the post so the concrete forms a "
                "collar. A common size is a 8-10 in diameter hole, 24-30 in deep. Take a 10 in "
                "diameter hole 30 in deep: radius 5 in = 0.417 ft, area = pi x 0.417^2 = 0.546 sq ft, "
                "x 2.5 ft deep = 1.37 cu ft per hole.\n\n"
                "Mix yield: an 80 lb bag of concrete gives about 0.60 cu ft, a 60 lb bag about "
                "0.45 cu ft. So 1.37 / 0.60 = 2.3, i.e. buy 3 bags of 80 lb per hole (or 4 bags of "
                "60 lb). For 10 posts that is about 14 cu ft, or 0.5 cu yd, or 24 bags of 80 lb.\n\n"
                "Two practical notes: set the post so the concrete crowns slightly above grade and "
                "slopes away from the wood, and use fast-setting mix if you want to keep building "
                "the same day.\n\n"
                "I built a free calculator that does the hole-volume and bag-count arithmetic for "
                "any post size, hole diameter, depth and bag size: "
                f"{BASE}/how-many-bags-of-concrete-do-i-need-for-a-fence-post/"
            ),
        ),
        _se(
            False,
            "How do I calculate the concrete needed for a fence post?",
            "https://diy.stackexchange.com/questions/170144/how-do-i-calculate-the-concrete-needed-for-a-fence-post",
            "Home Improvement (diy.stackexchange.com)",
            f"{BASE}/how-many-bags-of-concrete-do-i-need-for-a-fence-post/",
            "concrete needed for a fence post",
            (
                "The method is: (hole area x depth) x number of posts, then divide by the bag yield.\n\n"
                "Worked for your 4x4 x 8 ft posts: assume a 10 in hole, 30 in deep. Radius = 5 in = "
                "0.417 ft. Area = 3.1416 x 0.417^2 = 0.546 sq ft. Volume per hole = 0.546 x 2.5 = "
                "1.37 cu ft. An 80 lb bag yields ~0.60 cu ft, so ~2.3 bags -> buy 3 per hole.\n\n"
                "If your holes are 12 in wide, that scales to about 1.96 cu ft per hole and 4 bags "
                "of 80 lb each. Multiply by the post count for the total; a full pallet is cheaper "
                "per bag if you have many posts.\n\n"
                "Free tool that takes post count, hole diameter, depth and bag size and returns the "
                "bag count: "
                f"{BASE}/how-many-bags-of-concrete-do-i-need-for-a-fence-post/"
            ),
        ),
        _se(
            False,
            "How do I determine the amount of paint needed for a room?",
            "https://diy.stackexchange.com/questions/18483/how-do-i-determine-the-amount-of-paint-needed-for-a-room",
            "Home Improvement (diy.stackexchange.com)",
            f"{BASE}/how-much-paint-do-i-need-for-a-bedroom/",
            "how much paint a room needs",
            (
                "Paint estimating is wall area divided by coverage, multiplied by the number of "
                "coats, after subtracting openings.\n\n"
                "Wall area = perimeter x ceiling height. For a 12 x 10 ft room with 8 ft walls that "
                "is 44 x 8 = 352 sq ft. Subtract a door (~21 sq ft) and two windows (~2 x 15 sq ft) "
                "and you have about 301 sq ft of paintable wall. One gallon covers roughly 350-400 "
                "sq ft per coat on a smooth surface, so two coats needs 301 x 2 / 350 ~ 1.7 gal, "
                "round up to 2 gallons. Ceiling adds length x width, about another half gallon for "
                "two coats.\n\n"
                "Buy the two gallons up front and keep one unopened so the second coat is the exact "
                "same batch if you need a touch-up later.\n\n"
                "I built a free paint calculator that does this and lets you vary coats, doors and "
                "windows: " + f"{BASE}/how-much-paint-do-i-need-for-a-bedroom/"
            ),
        ),
        _se(
            False,
            "Advice for a new planting bed",
            "https://gardening.stackexchange.com/questions/18072/advice-for-a-new-planting-bed",
            "Gardening & Landscaping",
            f"{BASE}/how-much-mulch-do-i-need-for-500-sq-ft/",
            "how much mulch do i need for 500 sq ft",
            (
                "For 650 sq ft you are looking at a bulk order, not bags. At the standard 3 in deep, "
                "volume = 650 x 0.25 ft = 162.5 cu ft, which is 162.5 / 27 = 6.0 cubic yards. That is "
                "about 82 bags of 2 cu ft if you go that route, which is why bulk delivery is "
                "cheaper at this size.\n\n"
                "On the grass coming back through: mulch only suppresses seed that has already "
                "germinated under it. For a bed with established weeds, cut them down first, put "
                "down a layer of cardboard or 6 sheets of newspaper overlapping by 6 in, then the "
                "3 in of mulch on top. Keep the mulch a couple of inches back from tree trunks and "
                "shrub stems so the bark does not stay wet.\n\n"
                "I put a mulch calculator with the bags/cubic-yards conversion here if it helps: "
                f"{BASE}/how-much-mulch-do-i-need-for-500-sq-ft/"
            ),
        ),
        _se(
            False,
            "Ideal way to fill in a large hole (from a goldfish pond)",
            "https://gardening.stackexchange.com/questions/37993/ideal-way-to-fill-in-a-large-hole-from-a-goldfish-pond",
            "Gardening & Landscaping",
            f"{BASE}/topsoil-calculator/",
            "how much topsoil to fill it",
            (
                "That hole is about 1.5 m x 1.5 m x 1 m, so roughly 2.25 cubic metres (~2.9 cubic "
                "yards) of fill. Don't fill it all with topsoil: topsoil settles and compresses, and "
                "a 1 m depth of it would be a lot of settling.\n\n"
                "Fill the bottom ~80% with subsoil or a cheaper loam, compact it in 20 cm layers "
                "(water each layer), and finish with 15-20 cm of good topsoil for the planting. That "
                "cuts the topsoil you need to about 0.3-0.45 cubic metres (~0.4-0.6 cubic yards, or "
                "roughly 14-20 cubic feet).\n\n"
                "One caution: if the pond was lined, remove the liner so water drains; otherwise you "
                "have made a bog. And let the topsoil settle for a few weeks before seeding or "
                "planting, topping it up as it drops.\n\n"
                "I made a free topsoil calculator that converts area x depth to cubic yards and bags: "
                f"{BASE}/topsoil-calculator/"
            ),
        ),
        {
            "platform": "Reddit",
            "uid": "reddit:r/landscaping",
            "community": "r/landscaping",
            "target": "Weekly/simple questions and 'how much material' threads",
            "url": "https://www.reddit.com/r/landscaping/",
            "promote": f"{BASE}/mulch-calculator/ (or the matching calculator for the thread)",
            "anchor": "mulch calculator",
            "copy": (
                "Reply inside an existing question thread (do not start a new promotional post): "
                "'[Actual arithmetic for their numbers]. 3 in deep is the usual depth for beds. "
                "For that area that is X cu yd / Y bags. I built a free calculator that does the "
                "bags-vs-cubic-yards conversion: " + f"{BASE}/mulch-calculator/ (I run the site).'"
            ),
            "link_type": LINK_TYPE["reddit"],
            "notes": ("Follow the 90/10 rule: be an active commenter first. Never post a bare link; "
                      "lead with the answer. Check r/landscaping sidebar rules before posting; many "
                      "subs limit self-promo to specific threads or days. If unsure, put the link in "
                      "a comment, not the post body."),
            "requirement": "User action required (needs your Reddit account, with some genuine comment history first)",
            "publish": False,
        },
        {
            "platform": "Reddit",
            "uid": "reddit:r/HomeImprovement",
            "community": "r/HomeImprovement",
            "target": "Material-quantity questions (concrete, paint, tile)",
            "url": "https://www.reddit.com/r/HomeImprovement/",
            "promote": f"{BASE}/concrete-calculator/ or {BASE}/paint-calculator/",
            "anchor": "concrete calculator / paint calculator",
            "copy": (
                "Answer the specific thread with the full formula, then add one line: 'I built a "
                "free calculator that does this for your dimensions and bag size: "
                + f"{BASE}/concrete-calculator/ (site I run).'"
            ),
            "link_type": LINK_TYPE["reddit"],
            "notes": "Same 90/10 rule and sidebar check. One link, only when it answers the post.",
            "requirement": "User action required (needs your Reddit account)",
            "publish": False,
        },
        {
            "platform": "Quora",
            "uid": "quora:how-much-mulch-do-i-need",
            "community": "Quora — 'How much mulch do I need?'",
            "target": "Search: how much mulch do I need / for 500 sq ft / for 200 sq ft",
            "url": "https://www.quora.com/search?q=how%20much%20mulch%20do%20i%20need",
            "promote": f"{BASE}/mulch-calculator/",
            "anchor": "mulch calculator",
            "copy": (
                "Answer with the worked method: 'Multiply the bed length by width to get square "
                "feet. Convert your depth to feet (3 in = 0.25 ft) and multiply for cubic feet. "
                "Divide cubic feet by 27 for cubic yards, or by 2 for 2-cu-ft bags. Example: 500 sq "
                "ft x 0.25 ft = 125 cu ft = 4.63 cu yd = 63 bags. I wrote this up with a calculator "
                "that does it for any size: " + f"{BASE}/mulch-calculator/ (site I run).'"
            ),
            "link_type": LINK_TYPE["quora"],
            "notes": ("One link per answer; Quora may collapse answers that are mostly promotional. "
                      "Answer several related questions with the method, linking only where the "
                      "calculator is the direct tool."),
            "requirement": "User action required (needs your Quora account)",
            "publish": False,
        },
        {
            "platform": "Pinterest",
            "uid": "pinterest:gardencalc-boards",
            "community": "Pinterest — create boards 'Garden Calculators', 'Lawn Care', 'Home Projects'",
            "target": "Pin each calculator's social image to the matching board",
            "url": "https://www.pinterest.com/",
            "promote": f"{BASE}/mulch-coverage-chart/ etc. (16 ready pins in /static/img/pins/)",
            "anchor": "pin title (e.g. 'Mulch Coverage Chart: Bags & Yards')",
            "copy": (
                "Pin title: use the article title. Pin description (200-300 chars): 'How much "
                "mulch for your bed? Coverage chart for 50-1000 sq ft at 2, 3 and 4 in deep, with "
                "cubic yards and 2-cu-ft bag counts. Free calculator linked.' Destination link: the "
                "article URL + ?utm_source=pinterest&utm_medium=social&utm_campaign=<slug>."
            ),
            "link_type": LINK_TYPE["pinterest"],
            "notes": ("Assets already generated: site/static/img/pins/*.png (1200x630). Pin to a "
                      "relevant board, not a generic one; use descriptive alt text. 3-5 pins/day max, "
                      "spaced out."),
            "requirement": "User action required (needs your Pinterest account)",
            "publish": False,
        },
        {
            "platform": "Hacker News",
            "uid": "hackernews:show-hn",
            "community": "Hacker News — 'Show HN'",
            "target": "Show HN: I built a free garden-materials calculator with the formulas shown",
            "url": "https://news.ycombinator.com/submit",
            "promote": f"{BASE}/",
            "anchor": "Show HN (title field)",
            "copy": (
                "Title: 'Show HN: GardenCalc - free home and garden calculators that show the "
                "formula'. First comment: 'I kept seeing the same \"how much mulch/soil/gravel\" "
                "questions answered ambiguously, so I built a static site where every calculator "
                "shows the formula and a worked example rather than just a number. No account, no "
                "tracking. Feedback welcome.' Link: " + f"{BASE}/"
            ),
            "link_type": LINK_TYPE["hackernews"],
            "notes": ("Show HN is explicitly for your own work and is allowed here. One submission "
                      "only; do not resubmit. Be present in the comments."),
            "requirement": "User action required (needs your HN account; posting a URL needs a little karma)",
            "publish": False,
        },
        {
            "platform": "Blog outreach",
            "uid": "blog-outreach:edenbrothers-top-blogs",
            "community": "Eden Brothers - 'Top Gardening Blogs' roundup",
            "target": "Suggests readers email favourite gardening bloggers to service@edenbrothers.com",
            "url": "https://grow.edenbrothers.com/top-10-gardening-blogs/",
            "promote": f"{BASE}/ (calculator hub)",
            "anchor": "GardenCalc",
            "copy": (
                "Subject: Free garden calculators your readers might find useful\n\nHi, I run a "
                "small free site of garden-material calculators - mulch, soil, gravel, seed and "
                "fertilizer - that show the formula and a worked example rather than just a number. "
                "I noticed your gardening resources page and thought it could be a fit. No "
                "reciprocation wanted; happy for you to skip it if it is not a match. "
                + BASE + "/"
            ),
            "link_type": LINK_TYPE["blog-outreach"],
            "notes": ("Only pitch pages that genuinely list tools/resources. Personalise each email; "
                      "do not send a template blast. Expect a low hit rate - that is normal."),
            "requirement": "User action required (email from your address)",
            "publish": False,
        },
        {
            "platform": "Resource page",
            "uid": "resource-page:homegardenseedassociation",
            "community": "Home Garden Seed Association - Recommended Resources",
            "target": "Page invites readers to submit resources they love via the contact form",
            "url": "https://homegardenseedassociation.com/new-page-2",
            "promote": f"{BASE}/ (or {BASE}/grass-seed-calculator/)",
            "anchor": "GardenCalc calculators",
            "copy": (
                "Use the page's own contact form/link: 'Hi - your Recommended Resources page invited "
                "suggestions. I built a free set of garden-material calculators (mulch, soil, seed, "
                "fertilizer) that show the formula and a worked example. If useful for your readers, "
                "feel free to include it: " + BASE + "/ - no reciprocal link requested.'"
            ),
            "link_type": LINK_TYPE["resource-page"],
            "notes": "Only submit where the page's stated policy invites suggestions. Never pay.",
            "requirement": "User action required (contact form usually needs your email)",
            "publish": False,
        },
        {
            "platform": "Resource page",
            "uid": "resource-page:cornell-cce",
            "community": "Cornell Cooperative Extension - county gardening resource pages",
            "target": "County offices publish 'Gardening Resources' link lists",
            "url": "https://stlawrence.cce.cornell.edu/home-gardens-grounds/gardening-resources",
            "promote": f"{BASE}/",
            "anchor": "the GardenCalc calculators",
            "copy": (
                "Email the county office's growline: 'I help run a free, non-commercial set of "
                "garden calculators (volumes and rates for mulch, soil, seed). I thought it might "
                "suit your Gardening Resources list if you keep one. " + BASE + "/'"
            ),
            "link_type": LINK_TYPE["resource-page"],
            "notes": ("Educational/extension sites are high-trust. Only where a resource list "
                      "exists and the tool is genuinely relevant; departments are selective."),
            "requirement": "User action required (email from your address)",
            "publish": False,
        },
        {
            "platform": "RSS aggregators",
            "uid": "rss-aggregators:feedly",
            "community": "feedly / feedly cloud + general feed readers",
            "target": "Anyone can subscribe to a public RSS feed; feed directories index it",
            "url": f"{BASE}/rss.xml",
            "promote": f"{BASE}/rss.xml",
            "anchor": "GardenCalc feed",
            "copy": "Feed URL: " + f"{BASE}/rss.xml",
            "link_type": LINK_TYPE["directory"],
            "notes": ("The feed is live. Submitting it to feed directories needs a form, but anyone "
                      "can add it to a reader. A public web page hosting the feed URL is the "
                      "no-login equivalent and is already served at /rss.xml."),
            "requirement": "User action required for directories that need a form/account",
            "publish": False,
        },
        {
            "platform": "Directory",
            "uid": "directory:home-improvement-tools",
            "community": "Curated home-improvement / DIY tool directories",
            "target": "Reputable, editorially-reviewed tool listings (skip paid link farms)",
            "url": "https://www.google.com/search?q=%22submit%22+OR+%22add+your+tool%22+home+improvement+calculator+directory",
            "promote": f"{BASE}/",
            "anchor": "GardenCalc",
            "copy": (
                "Standard listing blurb (40-60 words): 'GardenCalc is a free set of home and garden "
                "calculators for mulch, topsoil, gravel, concrete, paint, tile, grass seed and "
                "fertilizer. Every tool shows the formula and a worked example, with results in "
                "bags, cubic feet, cubic yards and tons. No account or tracking.'"
            ),
            "link_type": LINK_TYPE["directory"],
            "notes": ("Add only where there is real editorial review and a relevant category. Avoid "
                      "bulk '5000 directories' lists, paid PBNs, and anything promising instant DA. "
                      "Check whether the listing link is dofollow before investing time."),
            "requirement": "User action required (most submission forms need an email account)",
            "publish": False,
        },
        {
            "platform": "Citation",
            "uid": "citation:wikipedia-mulch",
            "community": "Wikipedia - Mulch article (reference improvement only)",
            "target": "Only if a reliable secondary source supports the same claim",
            "url": "https://en.wikipedia.org/wiki/Mulch",
            "promote": "n/a - do not cite GardenCalc",
            "anchor": "n/a",
            "copy": (
                "Do not add a GardenCalc link. Wikipedia needs independent, reliable, secondary "
                "sources; a self-published calculator is not one, and adding it is link spam that "
                "will be reverted. This is listed only to record the decision."
            ),
            "link_type": LINK_TYPE["citation"],
            "notes": "Not recommended. Recorded so it is not attempted.",
            "requirement": "Not recommended",
            "publish": False,
        },
    ]


def _load_log() -> dict:
    return load_json(LOG, default={"done": [], "events": []}) or {"done": [], "events": []}


def check() -> list[str]:
    opps = opportunities()
    seen: dict[str, str] = {}
    dupes: list[str] = []
    for o in opps:
        uid = o["uid"]
        if uid in seen:
            dupes.append(f"duplicate uid {uid}: {o['target']!r} vs {seen[uid]!r}")
        seen[uid] = o["target"]
    return dupes


def mark(uid: str) -> dict:
    import datetime as dt
    opps = {o["uid"] for o in opportunities()}
    if uid not in opps:
        raise SystemExit(f"unknown uid: {uid}\nknown: {', '.join(sorted(opps))}")
    log = _load_log()
    if uid not in log["done"]:
        log["done"].append(uid)
        log["events"].append({"uid": uid, "at": dt.datetime.now(dt.timezone.utc).isoformat()})
    save_json(LOG, log)
    return log


def _md() -> str:
    log = _load_log()
    done = set(log.get("done", []))
    lines = [
        "# GardenCalc promotion playbook",
        "",
        f"Base URL: {BASE}",
        "",
        "Every item below can be completed **without any GardenCalc-side technical change**; "
        "each needs *your* account only where marked. Work top to bottom. After completing an "
        "item run `python scripts/promotion.py --mark <uid>` so the same community is never "
        "re-targeted. Dedupe guard: `python scripts/promotion.py --check`.",
        "",
        "Ethics: one link per contribution, only where the tool is the direct answer, always "
        "disclosed. No accounts created for you, no bulk posting, no paid links, no PBNs.",
        "",
    ]
    for o in opportunities():
        mark_box = "x" if o["uid"] in done else " "
        lines += [
            f"## [{mark_box}] {o['platform']} — {o['community']}",
            f"- **Target:** {o['target']}",
            f"- **URL:** {o['url']}",
            f"- **Promote:** {o['promote']}",
            f"- **Anchor text:** {o['anchor']}",
            f"- **Link type:** {o['link_type']}",
            f"- **Requirement:** {o['requirement']}",
            f"- **Rules / notes:** {o['notes']}",
            f"- **UID (for --mark):** `{o['uid']}`",
            "",
            "**Exact text to post:**",
            "",
            "```text",
            o["copy"],
            "```",
            "",
        ]
    lines += [
        "## Steps that need your account (summary)",
        "",
        "1. Google Search Console — verify the URL-prefix property (the HTML meta tag is already "
        "live), then submit the sitemap. This is the single highest-impact action.",
        "2. Bing Webmaster Tools — sign in, then 'Import from Google Search Console'.",
        "3. Reddit / Quora / Stack Exchange / Pinterest / HN — use the ready text above.",
        "4. Directory and resource-page forms — use the ready blurbs above.",
        "",
        "## Not recommended",
        "- Paid directories, PBNs, 'instant DA' services, link exchanges, comment spam, or "
        "auto-submitters that post to hundreds of directories.",
        "- Citing GardenCalc on Wikipedia — a self-published tool is not a reliable source and "
        "any such edit is link spam.",
        "",
    ]
    return "\n".join(lines)


def write() -> dict:
    dupes = check()
    if dupes:
        raise SystemExit("DUPLICATE promotion targets:\n" + "\n".join(dupes))
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / "promotion-playbook.md"
    path.write_text(_md(), encoding="utf-8")
    log = _load_log()
    return {
        "playbook": str(path),
        "opportunities": len(opportunities()),
        "completed": len(log.get("done", [])),
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", help="uid to mark complete")
    ap.add_argument("--check", action="store_true", help="only run the duplicate check")
    a = ap.parse_args()
    if a.mark:
        mark(a.mark)
        print("marked", a.mark)
    elif a.check:
        d = check()
        print("duplicates:", d or "none")
    else:
        print(json.dumps(write(), indent=2))
