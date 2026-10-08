"""Seasonal, evergreen guide pages.

Four guides that answer the timing questions people search every year ("when to mulch",
"when to overseed"). The URLs are stable and the dates are updated in place, so the same
page can earn links and rank season after season. Every number quoted here matches
scripts/calculators.py and the coverage charts; nothing is invented.
"""
from __future__ import annotations

SEASONAL: list[dict] = [
    {
        "slug": "when-to-mulch",
        "question": "When is the best time to mulch garden beds?",
        "title": "When to Mulch: The Best Time of Year for Beds",
        "description": ("The best time to mulch is mid-to-late spring once the soil has "
                        "warmed, with a second pass in autumn. How deep, and what to avoid."),
        "keyword": "when to mulch",
        "cluster": "mulch",
        "calculator": "mulch-calculator",
        "chart": "mulch-coverage-chart",
        "updated": "2026-03-01",
        "intro": ("Mulch is a timing job as much as a quantity job. Spread it at the wrong "
                  "moment and you trap cold, wet soil in spring or smother roots in summer; "
                  "spread it at the right moment and you cut watering, suppress weeds and "
                  "steady soil temperature for the whole season."),
        "table": {
            "caption": "Mulch quantity by bed size at 3 inches deep",
            "head": ["Bed / area", "Cubic feet", "Cubic yards", "2 cu ft bags"],
            "rows": [
                ["12 ft x 4 ft (48 sq ft)", "12", "0.44", "6"],
                ["10 ft x 10 ft (100 sq ft)", "25", "0.93", "13"],
                ["20 ft x 20 ft (400 sq ft)", "100", "3.70", "50"],
                ["500 sq ft", "125", "4.63", "63"],
            ],
            "note": "Volume = length x width x depth (ft). At 3 in the depth is 0.25 ft. One cubic yard is 27 cubic feet; bags are 2 cubic feet.",
        },
        "sections": [
            {"h2": "The short answer",
             "paras": [
                 "Apply mulch in mid-to-late spring, once the soil has warmed and you have "
                 "finished weeding. In most temperate gardens that is late April through "
                 "early June.",
                 "Add a second, thinner layer in early to mid autumn to top up what broke "
                 "down over summer and to insulate roots through winter.",
             ]},
            {"h2": "Why soil temperature decides the date",
             "paras": [
                 "Mulch slows the movement of heat in both directions. Put it on too early "
                 "and it keeps spring soil cold, which delays growth for warm-season plants "
                 "and can keep wet soil wet for longer than the roots can cope with.",
                 "Wait until the soil has warmed to roughly 55-60 F (13-16 C) at 4 inches "
                 "deep. A cheap soil thermometer is the reliable test; if you do not have "
                 "one, wait until weeds have started growing strongly, which is a good sign "
                 "the soil is awake.",
             ]},
            {"h2": "How deep should mulch be?",
             "paras": [
                 "Two to three inches is the working range for most beds. That is deep "
                 "enough to block light from weed seeds and slow evaporation, without "
                 "burying the crown of perennials or holding moisture against stems.",
                 "Three to four inches suits a coarse bark mulch that will settle; use the "
                 "shallower end for fine mulches, which mat down and shed less water if "
                 "piled high.",
                 "To turn a depth into a quantity, multiply length by width by the depth in "
                 "feet to get cubic feet, then divide by 27 for cubic yards. A 12 ft x 4 ft "
                 "bed at 3 inches needs about 12 cubic feet, or one cubic yard, which is "
                 "13.5 bags of 2 cubic feet.",
             ]},
            {"h2": "Mulch around trees: keep it off the trunk",
             "paras": [
                 "Pull mulch back so it is a few inches clear of the trunk and any stems. "
                 "Mulch piled against bark keeps the surface damp, which invites rot and "
                 "pest damage, and a deep cone can hide girdling roots.",
                 "A flat, wide ring out to the drip line is far better for the tree than a "
                 "tall mound at the base.",
             ]},
            {"h2": "A simple seasonal schedule",
             "paras": [
                 "Spring (late April to early June): weed, edge the bed, then top up to a "
                 "2-3 inch layer with a fresh mulch.",
                 "Summer: leave it alone. Top-ups in high heat can bake shallow roots; water "
                 "the soil beneath the mulch if the season is dry.",
                 "Autumn (September to November): add a thin layer to replace what "
                 "decomposed, or refresh only the beds where the layer has thinned below an "
                 "inch.",
             ]},
        ],
        "faqs": [
            ("Can I mulch in summer?",
             "Yes, but top up rather than apply a full layer. In high heat a thick fresh "
             "layer can hold warmth and stress shallow roots, so add only enough to restore "
             "the 2-3 inch depth and water the soil first."),
            ("Can I mulch in winter?",
             "A thin layer in late autumn insulates roots over winter, but a thick layer on "
             "cold, wet ground keeps soil cold and can delay spring growth. Wait until the "
             "soil has warmed before the main application."),
            ("How many bags of mulch is a cubic yard?",
             "One cubic yard is 27 cubic feet, which is 13.5 bags of 2 cubic feet. A 12 ft x "
             "4 ft bed at 3 inches deep needs about one cubic yard, so 13-14 bags."),
            ("Should I remove old mulch before adding new?",
             "Not usually. Fluff it with a rake to break up any matting, then top up to "
             "depth. Remove it only if it has formed a water-shedding crust or shows signs "
             "of disease."),
            ("Does mulch need to be watered in?",
             "Yes after a dry spell. Water the soil before mulching and give the bed a soak "
             "afterwards so the layer does not shed light rain away from the roots."),
        ],
    },
    {
        "slug": "when-to-overseed-a-lawn",
        "question": "When is the best time to overseed a lawn?",
        "title": "When to Overseed a Lawn: Best Time and Seed Rate",
        "description": ("Overseed cool-season lawns in late summer to early autumn, about "
                        "4-6 weeks before the first frost. Timing, seed rate and follow-up."),
        "keyword": "when to overseed a lawn",
        "cluster": "grass-seed",
        "calculator": "grass-seed-calculator",
        "chart": "grass-seed-rate-chart",
        "planner": "new-lawn-planner",
        "updated": "2026-03-01",
        "intro": ("Overseeding thickens a thin lawn without starting over, but it only works "
                  "if the seed has warm soil and enough time to establish before winter. "
                  "Choosing the window is the whole job."),
        "table": {
            "caption": "Grass seed to buy by lawn size",
            "head": ["Lawn area", "New lawn (4-5 lb/1,000)", "Overseed (2-4 lb/1,000)"],
            "rows": [
                ["1,000 sq ft", "4-5 lb", "2-4 lb"],
                ["2,500 sq ft", "10-13 lb", "5-10 lb"],
                ["5,000 sq ft", "20-25 lb", "10-20 lb"],
                ["10,000 sq ft", "40-50 lb", "20-40 lb"],
            ],
            "note": "Rates are per 1,000 sq ft and depend on the seed label and species. Match the bag rate to your grass type and seed size.",
        },
        "sections": [
            {"h2": "The short answer",
             "paras": [
                 "For cool-season grasses (fescue, rye, bluegrass), overseed in late summer "
                 "to early autumn, aiming to finish about four to six weeks before the first "
                 "expected frost. In most temperate regions that is early August to mid "
                 "September.",
                 "In the transition and warm-season zones, or where summer heat lingers, "
                 "shift that window later so the seedlings miss the worst heat.",
             ]},
            {"h2": "Why autumn beats spring",
             "paras": [
                 "Autumn gives seedlings warm soil for fast germination and cooler air for "
                 "steady growth, with fewer weeds competing and less pressure from heat and "
                 "drought.",
                 "Spring overseeding can work in mild regions, but the young grass then runs "
                 "straight into summer heat and crabgrass pressure, and it has less time to "
                 "deepen roots before the ground heats up.",
             ]},
            {"h2": "Check your soil temperature",
             "paras": [
                 "Seed germinates fastest when the soil is around 50-65 F (10-18 C). Below "
                 "that, germination stalls; far above it, tender seedlings dry out.",
                 "If you have no thermometer, watch for nights that are reliably cool and "
                 "days still in the 60s and low 70s F, and for the late-summer flush of "
                 "weeds to be tapering off.",
             ]},
            {"h2": "Seed rate and how much to buy",
             "paras": [
                 "Overseeding uses about half the seed of a new lawn. A typical overseeding "
                 "rate is 3-4 lb of seed per 1,000 sq ft; a new lawn is roughly 6-8 lb per "
                 "1,000 sq ft.",
                 "For example, 5,000 sq ft overseeded at 4 lb per 1,000 sq ft needs about 20 "
                 "lb of seed, which is around seven 3 lb bags. Match the rate to the seed "
                 "label, which varies by species and blend.",
             ]},
            {"h2": "The follow-up that makes it work",
             "paras": [
                 "Keep the top inch of soil moist, not soaked, for the first two to three "
                 "weeks. Light, frequent watering beats one heavy soak while roots are "
                 "shallow.",
                 "Mow high and only once the new grass is tall enough to need it. Hold off "
                 "on weed killers until the new grass has been mown at least two or three "
                 "times, and apply a starter fertilizer at seeding to feed the seedlings.",
             ]},
        ],
        "faqs": [
            ("What is the best month to overseed?",
             "For cool-season grass, late August to mid September suits most temperate "
             "regions: the soil is warm, the air is cooling and there is time to establish "
             "before frost. Adjust earlier in short-season climates and later in hot ones."),
            ("Can I overseed in spring?",
             "You can in mild climates, but seedlings then face summer heat and weed "
             "competition. If spring is your only window, seed early and water carefully "
             "through the first summer."),
            ("How soon after overseeding can I mow?",
             "Wait until the new grass reaches about 3 inches, then mow high with a sharp "
             "blade. Mowing too short or too early uproots young seedlings."),
            ("How much seed do I need per 1,000 square feet?",
             "Overseeding uses about 3-4 lb per 1,000 sq ft, roughly half the rate of a new "
             "lawn. A 5,000 sq ft lawn at 4 lb per 1,000 sq ft needs about 20 lb of seed."),
            ("Should I fertilize when overseeding?",
             "Yes. A starter fertilizer at seeding supplies the phosphorus and nitrogen "
             "young roots need. For a new lawn, apply about 1 lb of nitrogen per 1,000 sq ft "
             "and water it in."),
        ],
    },
    {
        "slug": "spring-garden-bed-checklist",
        "question": "What should I do first in a garden bed in spring?",
        "title": "Spring Garden Bed Checklist: What to Do First",
        "description": ("A practical spring garden bed checklist in order: soil, compost, "
                        "edging, mulch timing and planting, with quantities for each step."),
        "keyword": "spring garden bed checklist",
        "cluster": "soil",
        "calculator": "raised-bed-soil-calculator",
        "chart": "raised-bed-soil-chart",
        "planner": "garden-bed-makeover-planner",
        "updated": "2026-03-01",
        "intro": ("Spring work in a garden bed is a sequence, not a list. Do the steps in "
                  "the wrong order and you undo your own effort, especially if you mulch "
                  "before the soil has warmed or plant before you have fixed drainage."),
        "table": {
            "caption": "Compost and mulch for a 4 ft x 8 ft bed",
            "head": ["Job", "Depth", "Cubic feet", "2 cu ft bags"],
            "rows": [
                ["Compost (top-dress)", "2 in", "5.3", "3"],
                ["Mulch", "3 in", "8.0", "4"],
                ["Mulch", "4 in", "10.7", "6"],
            ],
            "note": "Volume = 4 x 8 x depth (ft). Two inches is 0.167 ft, three inches 0.25 ft, four inches 0.333 ft. Bags are 2 cubic feet.",
        },
        "sections": [
            {"h2": "1. Clear and assess before you feed",
             "paras": [
                 "Remove winter debris, dead annuals and any matted leaves, then look at "
                 "drainage. If water sat in the bed over winter, fix that before adding "
                 "compost or plants, because most garden plants rot in standing water.",
             ]},
            {"h2": "2. Feed the soil, not just the plants",
             "paras": [
                 "Spread two to three inches of compost or well-rotted organic matter over "
                 "the bed and work it into the top layer. For a 4 ft x 8 ft bed at 2 inches, "
                 "that is about 5.3 cubic feet, or four 1.5 cubic foot bags.",
                 "Do not dig wet soil. If a handful crumbles when squeezed, it is ready; if "
                 "it forms a slick ball, wait for it to dry.",
             ]},
            {"h2": "3. Edge and level",
             "paras": [
                 "Cut a clean edge along the bed so grass cannot creep in, and rake the "
                 "surface level. A level bed takes water evenly and is far easier to plant "
                 "into than a lumpy one.",
             ]},
            {"h2": "4. Mulch only after the soil warms",
             "paras": [
                 "This is the step people rush. Mulching cold, wet soil traps the cold in "
                 "and keeps roots slow. Weed first, wait until the soil has warmed, then "
                 "apply two to three inches of mulch.",
                 "A 4 ft x 8 ft bed at 3 inches needs about 8 cubic feet, or four to five "
                 "bags of 2 cubic feet. Keep mulch clear of stems and crowns.",
             ]},
            {"h2": "5. Plant and water in",
             "paras": [
                 "Plant after the last expected frost for tender crops, and water each plant "
                 "in to settle the soil around its roots. Then start a regular watering "
                 "routine rather than occasional heavy soaks.",
             ]},
        ],
        "faqs": [
            ("What should I do first in a garden bed in spring?",
             "Clear debris and check drainage first, then add compost and level the bed. "
             "Mulch and plant last, once the soil has warmed, so you do not trap cold, wet "
             "soil around roots."),
            ("How much compost does a raised bed need?",
             "About two to three inches worked into the top layer. A 4 ft x 8 ft bed at 2 "
             "inches needs roughly 5.3 cubic feet, or four 1.5 cubic foot bags."),
            ("Should I mulch in early spring?",
             "Not usually. Mulching cold soil keeps it cold and delays growth. Weed and "
             "feed first, then mulch once the soil has warmed to around 55-60 F."),
            ("How deep should raised bed soil be?",
             "Twelve inches suits most vegetables and flowers; ten to twelve is a good "
             "target. Shallower beds dry out faster and restrict larger roots."),
            ("When can I plant after adding compost?",
             "Compost can be worked in and planted immediately if it is well rotted. Plant "
             "tender crops only after the last expected frost for your area."),
        ],
    },
    {
        "slug": "fall-lawn-fertilizer-timing",
        "question": "When should I fertilize my lawn in fall?",
        "title": "Fall Lawn Fertilizer Timing: When and How Much",
        "description": ("Feed cool-season lawns in early autumn and again in late autumn, "
                        "about 1 lb of nitrogen per 1,000 sq ft each time. Timing and rates."),
        "keyword": "fall lawn fertilizer timing",
        "cluster": "fertilizer",
        "calculator": "fertilizer-calculator",
        "chart": "fertilizer-rate-chart",
        "updated": "2026-03-01",
        "intro": ("Autumn is the most valuable feeding of the year for a cool-season lawn. "
                  "Roots are growing strongly, top growth is slowing, and the nutrients go "
                  "into storage rather than into leaves you then have to mow."),
        "table": {
            "caption": "Fertilizer product to deliver 1 lb nitrogen per 1,000 sq ft",
            "head": ["Bag N-P-K", "Product per 1,000 sq ft", "Product for 5,000 sq ft"],
            "rows": [
                ["10-10-10", "10 lb", "50 lb"],
                ["20-5-10", "5 lb", "25 lb"],
                ["24-0-6", "4.2 lb", "21 lb"],
            ],
            "note": "Product = 100 divided by the first number in the N-P-K ratio. Divide again by the bag size to count bags.",
        },
        "sections": [
            {"h2": "The short answer",
             "paras": [
                 "Apply the main autumn feed in early autumn, around late summer to late "
                 "September, and a second, lighter feed in late autumn as growth slows, "
                 "roughly late October to mid November.",
                 "Use about 1 lb of actual nitrogen per 1,000 sq ft per application. Stop "
                 "when the ground is frozen or the grass has stopped growing.",
             ]},
            {"h2": "Why autumn feeding matters most",
             "paras": [
                 "Cool-season grasses put on their strongest root growth in autumn. Nitrogen "
                 "applied now builds root reserves and stored carbohydrates that carry the "
                 "lawn through winter and fuel a fast, even green-up in spring.",
                 "Spring-heavy feeding pushes leafy growth that needs constant mowing and "
                 "can weaken roots, which is why the emphasis belongs in autumn.",
             ]},
            {"h2": "How much to apply",
             "paras": [
                 "Match the application to the nitrogen number on the bag. To deliver 1 lb of "
                 "nitrogen per 1,000 sq ft, divide 100 by the first number in the N-P-K "
                 "ratio. A 20-5-10 blend needs 5 lb of product per 1,000 sq ft; a 30-0-5 "
                 "blend needs about 3.3 lb.",
                 "For a 5,000 sq ft lawn at 1 lb N per 1,000 sq ft on a 20-5-10 blend, you "
                 "need about 25 lb of product."],
             },
            {"h2": "Late-season and winterizer feeds",
             "paras": [
                 "A late-autumn feed, sometimes sold as a winterizer, tops up reserves just "
                 "before dormancy. Keep the rate the same or slightly lower, and apply it "
                 "while the grass is still growing so the roots can take it up.",
                 "Do not fertilize frozen ground. Nutrients cannot be taken up and are far "
                 "more likely to run off into water.",
             ]},
            {"h2": "Water it in and keep it even",
             "paras": [
                 "Water lightly after applying to move the granules off the blades and into "
                 "the soil, and use a spreader setting that gives two passes at half rate in "
                 "crossing directions for even coverage.",
             ]},
        ],
        "faqs": [
            ("When should I fertilize my lawn in fall?",
             "Feed in early autumn, around late summer to late September, then again as "
             "growth slows in late October to mid November. These two feeds matter more than "
             "a spring application for cool-season grass."),
            ("How much fertilizer per 1,000 square feet in fall?",
             "About 1 lb of actual nitrogen per 1,000 sq ft. On a 20-5-10 blend that is 5 lb "
             "of product per 1,000 sq ft; on a 30-0-5 blend it is about 3.3 lb."),
            ("Can I fertilize after the first frost?",
             "Apply while the grass is still growing. Once the ground is frozen the roots "
             "cannot take up nutrients and the risk of runoff rises sharply."),
            ("What fertilizer is best for fall?",
             "A blend with a moderate to high nitrogen number and some potassium supports "
             "root growth and winter hardiness. A 20-5-10 or a dedicated winterizer blend is "
             "a common choice; match the rate to the label."),
            ("Should I fertilize in spring too?",
             "A light spring feed can help, but autumn is the priority for cool-season "
             "grass. Heavy spring nitrogen pushes leaf growth and weakens roots."),
        ],
    },
]


def page(item: dict, base: str, site: dict) -> dict:
    """Render context for one seasonal guide."""
    calc = item.get("calculator", "")
    return {
        "slug": item["slug"],
        "question": item.get("question", ""),
        "cluster": item["cluster"],
        "url": f"{base}/{item['slug']}/",
        "intro": item["intro"],
        "sections": item["sections"],
        "table": item.get("table"),
        "faqs": [{"q": q, "a": a} for q, a in item["faqs"]],
        "calculator": f"{base}/{calc}/" if calc else "",
        "chart": f"{base}/{item['chart']}/" if item.get("chart") else "",
        "planner": f"{base}/{item['planner']}/" if item.get("planner") else "",
        "category": f"{base}/category/{item['cluster']}/",
        "updated": item["updated"],
    }
