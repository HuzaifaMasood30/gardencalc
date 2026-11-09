"""Curated articles, part I (bags of concrete in general, topsoil topdressing
for lawns, topsoil base under sod)."""

from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-many-bags-of-concrete-do-i-need",
        "title": "How Many Bags of Concrete Do I Need?",
        "cluster": "concrete",
        "primary_keyword": "how many bags of concrete do i need",
        "secondary_keywords": ["bags of concrete calculator", "how many bags of concrete mix do i need",
                               "concrete bags per cubic yard", "how many bags of ready mix concrete do i need"],
        "calculator": "concrete",
        "calculator_defaults": {"length": 15, "width": 3, "thickness": 4},
        "meta_description": "A 15 by 3 ft garden path 4 in thick needs 15 cu ft of concrete, or 34 bags "
                            "of 60 lb. Count by bag yield, round up, and keep a spare bag.",
        "faq": [
            ("How many bags of concrete are in a cubic yard?",
             "One cubic yard is 27 cubic feet, and a 60 lb bag yields about 0.45 cubic feet, "
             "so a cubic yard takes 60 bags of 60 lb. An 80 lb bag yields about 0.60 cubic "
             "feet, so the same cubic yard takes 45 bags of 80 lb. Work from the volume of "
             "your own slab first, then divide by the yield of the bag you are buying."),
            ("Should I buy 60 lb or 80 lb bags of concrete?",
             "Buy 60 lb bags when the bags must be carried by hand or mixed by one person, "
             "because each bag is a third lighter to lift. Buy 80 lb bags for a bigger pour "
             "with help, because the same 15 by 3 ft path needs 25 bags of 80 lb against 34 "
             "bags of 60 lb, which means fewer bags to open and mix."),
            ("How many extra bags of concrete should I buy?",
             "Buy one spare bag on top of the rounded-up count. A path that calculates to 34 "
             "bags of 60 lb should be bought as 35, because a short pour cannot be finished "
             "the next day without a visible joint where the old concrete had started to set. "
             "Unopened bags keep for a later small job if they are stored dry."),
        ],
        "body": _body(
            lead=(
                "A garden path 15 feet long and 3 feet wide, poured 4 inches thick, needs 15 "
                "cubic feet of concrete, which is 0.56 cubic yards or 34 bags of 60 lb. The "
                "same path in 80 lb bags needs only 25. The bag count is the last step of a "
                "short chain: measure the slab, turn it into a volume, then divide by what "
                "one bag yields.\n\n"
                "Most people start at the wrong end and guess the bag count from the size of "
                "the job in their head. A path feels small until you multiply length by width "
                "by thickness and find it holds 15 cubic feet, and a bag that yields less "
                "than half a cubic foot suddenly means dozens of bags. Work the volume first "
                "and the shopping list writes itself."
            ),
            worked_lead=(
                "For a garden path measuring 15 feet by 3 feet, poured 4 inches thick:"
            ),
            bullets=(
                "*   length = 15\n"
                "*   width = 3\n"
                "*   thickness = 4\n"
                "*   Cubic feet: 15.0\n"
                "*   Cubic yards: 0.56\n"
                "*   60 lb bags: 34\n"
                "*   80 lb bags: 25"
            ),
            sections=[
                ("How the Count Works",
                 "A bag of concrete mix is sold by weight, but a slab is bought by volume, so "
                 "the yield of one bag is the bridge between the two. A 60 lb bag yields about "
                 "0.45 cubic feet of mixed concrete, and an 80 lb bag yields about 0.60 cubic "
                 "feet. Divide the slab volume by the yield of the bag you are buying, and "
                 "round the result up to the next whole bag, because a part bag cannot be bought.\n\n"
                 "The path in the worked example is 15 cubic feet, so 15 divided by 0.45 gives "
                 "34 bags of 60 lb, and 15 divided by 0.60 gives 25 bags of 80 lb. The concrete "
                 "itself is identical either way; the heavier bag just means fewer bags to open, "
                 "mix and carry to reach the same volume."),
                ("Bags per Cubic Yard",
                 "A cubic yard is 27 cubic feet, which is the unit ready-mix is sold in and the "
                 "unit worth knowing when you compare bags against a truck. At the standard "
                 "yields, a cubic yard takes 60 bags of 60 lb or 45 bags of 80 lb. That pair of "
                 "numbers is the quickest sanity check on any bag count: if your slab is close "
                 "to a cubic yard, your count should be close to 60 or 45 bags.\n\n"
                 "Use the per-yard figures to judge whether bags are still sensible. A job "
                 "under half a cubic yard is firmly bag territory, while a job over a cubic "
                 "yard means sixty or more bags to mix by hand, which is a long day even with "
                 "a mixer. The path here is 0.56 cubic yards, just over half a yard, which is "
                 "why 34 bags feels like a lot for a small path and yet is exactly right."),
                ("Common Sizes at a Glance",
                 "The same arithmetic scales to any rectangle. A small 6 by 6 ft slab at 4 in "
                 "is 12 cubic feet, or 0.44 cubic yards, and needs 27 bags of 60 lb or 20 bags "
                 "of 80 lb. A 10 by 10 ft patio slab at the same thickness is 33.3 cubic feet, "
                 "or 1.23 cubic yards, and needs 75 bags of 60 lb or 56 bags of 80 lb.\n\n"
                 "A 12 by 12 ft slab at 4 in is 48 cubic feet, or 1.78 cubic yards, and needs "
                 "107 bags of 60 lb or 80 bags of 80 lb. At that size the bag count itself is "
                 "telling you something: over a hundred bags is a ready-mix job, not a "
                 "weekend with a wheelbarrow. A longer, narrower shape is kinder, because a "
                 "20 ft path 3 ft wide at 4 in is only 20 cubic feet, or 0.74 cubic yards, and "
                 "needs 45 bags of 60 lb or 34 bags of 80 lb."),
                ("Why Thickness Matters More Than Area",
                 "Thickness multiplies the whole area, so it changes the count faster than "
                 "length or width do. The same 10 by 10 ft slab poured 6 in thick instead of "
                 "4 in is 50 cubic feet, or 1.85 cubic yards, and needs 112 bags of 60 lb or "
                 "84 bags of 80 lb, half as much again for two extra inches.\n\n"
                 "Measure the thickness at several points across the formwork before ordering, "
                 "because a base that dips in the middle quietly adds bags. A slab that is 4 in "
                 "at the edges and 5 in in the middle is not a 4 in slab, and the extra inch "
                 "across the whole area is real concrete that has to come from somewhere. "
                 "Level the base, check it with a straight edge, and only then count the bags."),
                ("Buy One Spare, Not Ten",
                 "Round every result up to a whole bag, and then add one spare bag on top. A "
                 "path that calculates to 34 bags of 60 lb should be bought as 35, because a "
                 "short pour cannot be finished the next day without a visible joint where the "
                 "old concrete had started to set. The spare bag also covers the inevitable "
                 "spillage and the formwork that turns out slightly deeper than planned.\n\n"
                 "One spare is enough. Ten spare bags is money sitting in the garage, and a "
                 "bag that goes damp sets in lumps inside the paper and is no longer reliable. "
                 "Store the spare under cover and off the ground, and it keeps for a later "
                 "small job such as a fence post or a step repair."),
                ("When to Order Ready-Mix Instead",
                 "Bags win for small slabs, for sites a truck cannot reach, and for jobs poured "
                 "in stages over several weekends. Ready-mix wins once the count passes roughly "
                 "a hundred bags, or when the slab must be poured in one continuous session to "
                 "avoid joints. A cubic yard of concrete is 27 cubic feet, so the 0.56 cubic "
                 "yards in the path example is a small ready-mix load, and many suppliers "
                 "deliver that size with a minimum-load charge.\n\n"
                 "Compare the two prices honestly: the bags plus the hire of a mixer plus a day "
                 "of your labour, against the ready-mix quote delivered to the kerb. For the "
                 "path, bags are cheaper and simpler. For the 12 by 12 ft slab at 107 bags, "
                 "ready-mix is cheaper in money and far cheaper in effort. Either way, the bag "
                 "count from the calculator is the figure to compare against the quote."),
            ],
        ),
    },
    {
        "slug": "how-much-topsoil-do-i-need-to-topdress-a-lawn",
        "title": "How Much Topsoil Do I Need to Topdress a Lawn?",
        "cluster": "topsoil",
        "primary_keyword": "how much topsoil do i need to topdress a lawn",
        "secondary_keywords": ["topdressing lawn with topsoil how much", "topsoil top dressing lawn depth",
                               "how much topsoil for lawn top dressing", "top dress lawn with topsoil"],
        "calculator": "topsoil",
        "calculator_defaults": {"length": 60, "width": 20, "depth": 0.25},
        "meta_description": "Topdressing a 1,200 sq ft lawn with a quarter inch of topsoil takes 25 cu ft, "
                            "0.93 cubic yards or 34 forty-pound bags. Keep the layer thin.",
        "faq": [
            ("How deep should topsoil be when topdressing a lawn?",
             "A quarter inch is the standard depth for a topsoil dressing on an established "
             "lawn. The grass blades stay above the soil and keep growing, while the thin "
             "layer settles into the surface and slowly raises low spots. A half-inch dressing "
             "is the most to use in one pass, and only on a vigorous lawn in strong growth."),
            ("Is topsoil or compost better for topdressing a lawn?",
             "Topsoil is the better choice when the aim is to raise the soil level and smooth "
             "out bumps, because it adds mineral soil that stays put. Compost is the better "
             "choice when the aim is to feed the soil, because it adds organic matter and "
             "nutrients that topsoil does not. A lumpy, thin lawn wants topsoil; a hungry, "
             "pale lawn wants compost."),
            ("When is the best time to topdress a lawn with topsoil?",
             "While the grass is growing strongly, in spring or early autumn. The grass needs "
             "to grow through the dressing quickly, and rain after the job washes the fine "
             "soil down to the surface instead of leaving it sitting on the blades. Avoid "
             "drought, frost and midwinter, when the dressing sits unchanged for months."),
        ],
        "body": _body(
            lead=(
                "Topdressing a 1,200 sq ft lawn with a quarter inch of topsoil takes 25 cubic "
                "feet, which is 0.93 cubic yards or 34 bags of forty pounds. Topdressing with "
                "topsoil is a levelling job, not a feeding job: the thin layer of soil settles "
                "into the surface, fills the small hollows, and slowly raises the level of a "
                "lawn that has sunk or thinned over the years.\n\n"
                "The depth is everything. A quarter inch disappears into the grass within days "
                "and the lawn looks better for it; an inch buries the grass and the lawn has to "
                "regrow from its crowns. This page gives the amounts for the standard dressing, "
                "for a heavier one, and for the lawns where bags beat a bulk delivery."
            ),
            worked_lead=(
                "For a lawn measuring 60 feet by 20 feet, with topsoil spread a quarter inch deep:"
            ),
            bullets=(
                "*   length = 60\n"
                "*   width = 20\n"
                "*   depth = 0.25\n"
                "*   Square feet: 1200.0\n"
                "*   Cubic feet: 25.0\n"
                "*   Cubic yards: 0.93\n"
                "*   40 lb bags: 34"
            ),
            sections=[
                ("Topdressing Is Not Levelling",
                 "Topdressing and levelling use the same material at different depths, and "
                 "confusing them is how lawns get buried. Topdressing is a quarter inch spread "
                 "evenly over the whole lawn, repeated once a year, which gradually smooths the "
                 "surface and builds the soil level. Levelling is a targeted job that fills a "
                 "specific hollow with a deeper layer, and the grass in that hollow is expected "
                 "to grow back through it over several weeks.\n\n"
                 "The same 1,200 sq ft lawn dressed at half an inch instead of a quarter inch "
                 "needs 50 cubic feet, which is 1.85 cubic yards or 67 bags of forty pounds. "
                 "That is twice the material for a layer the grass may not grow through, and "
                 "it is the most to use in one pass, on a vigorous lawn in strong growth. If a "
                 "hollow needs more than half an inch, fill it in stages across the season "
                 "rather than in one deep dressing."),
                ("The Quarter-Inch Depth",
                 "Grass grows through a shallow dressing because the leaf tips stay in the "
                 "light. Spread a quarter inch over the whole lawn, brush it down between the "
                 "blades, and the grass pushes through within a week or two in the growing "
                 "season. The soil then sits at the surface, where worms pull it down and rain "
                 "washes the fine particles into the root zone.\n\n"
                 "A dressing deeper than half an inch risks yellowing the grass underneath, "
                 "and a lawn that has to regrow from its crowns loses the season you were "
                 "trying to improve. The quarter inch in the worked example is deliberately "
                 "conservative: it is the depth you can apply every year without ever worrying "
                 "about smothering the lawn, and the improvement compounds over the seasons."),
                ("Smaller and Larger Lawns",
                 "The amount scales directly with the area, because the depth never changes. A "
                 "small 600 sq ft lawn at a quarter inch needs only 12.5 cubic feet, which is "
                 "0.46 cubic yards or 17 bags of forty pounds, and a bulk delivery for that "
                 "little material is rarely worth the delivery charge.\n\n"
                 "A large 5,000 sq ft lawn at the same depth needs 104.2 cubic feet, which is "
                 "3.86 cubic yards or 139 bags, where bulk is clearly the better buy and bags "
                 "are no longer realistic. Measure the lawn in rectangles and add the areas "
                 "together rather than guessing from the fence line, because an overestimate "
                 "of the area is the commonest reason a dressing comes out too thick."),
                ("Bags or Bulk for a Dressing",
                 "At 34 bags, the 1,200 sq ft dressing is a judgement call. Bags are easy to "
                 "carry, easy to tip in small heaps, and there is no delivery to arrange, but "
                 "they cost more per cubic foot and leave a pile of plastic. A bulk delivery "
                 "of 0.93 cubic yards is cheaper for a lawn this size and up, and one load "
                 "covers the whole job.\n\n"
                 "Screened topsoil is worth asking for either way. Unscreened soil carries "
                 "stones, sticks and clods that sit on the surface of a lawn and show every "
                 "time the mower passes. A bagged topsoil is usually screened already; a bulk "
                 "load should be ordered as screened lawn topsoil, not as general fill, which "
                 "can contain rubble and weed seed."),
                ("How to Spread It Without Burying the Grass",
                 "Mow first, a little shorter than usual, and rake up the clippings so the soil "
                 "reaches the surface instead of sitting on a thatch mat. Tip the topsoil in "
                 "small heaps across the lawn, spread it with a shovel, then work it down with "
                 "a stiff brush or the back of a landscape rake until the grass tips show "
                 "through everywhere.\n\n"
                 "Water lightly after spreading if no rain is coming, because damp soil washes "
                 "down between the blades instead of blowing about. Never dig topsoil into a "
                 "lawn. Digging destroys the turf you are trying to improve, and a dug patch "
                 "takes a season to knit back together. The surface method looks untidy for a "
                 "few days, but the grass grows through it and the level improves from the top "
                 "down."),
                ("Topsoil or Compost for This Job?",
                 "Topsoil is the better choice when the aim is to raise the soil level and "
                 "smooth out bumps, because it adds mineral soil that stays put for years. "
                 "Compost is the better choice when the aim is to feed the soil, because it "
                 "adds organic matter and nutrients that topsoil does not, and a compost "
                 "dressing breaks down within a season.\n\n"
                 "A lumpy, thin lawn wants topsoil; a hungry, pale lawn wants compost. Some "
                 "lawns want both, in which case dress with topsoil first and let it settle, "
                 "then follow with compost later in the season. Never mix the two jobs into one "
                 "thick layer, because a deep combined dressing is exactly the layer that "
                 "smothers the grass you are trying to help."),
            ],
        ),
    },
    {
        "slug": "how-much-topsoil-do-i-need-for-sod",
        "title": "How Much Topsoil Do I Need for Sod?",
        "cluster": "topsoil",
        "primary_keyword": "how much topsoil do i need for sod",
        "secondary_keywords": ["topsoil depth under sod", "how much topsoil under turf",
                               "soil base for sod lawn", "how deep should topsoil be for sod"],
        "calculator": "topsoil",
        "calculator_defaults": {"length": 20, "width": 15, "depth": 4},
        "meta_description": "A 20 by 15 ft lawn needs 100 cu ft of topsoil, 3.7 cubic yards or 134 "
                            "forty-pound bags, laid 4 in deep before the sod goes down. Order by the yard.",
        "faq": [
            ("How deep should topsoil be under sod?",
             "Four inches of topsoil is the standard base under sod. The roots need that depth "
             "to anchor and to find moisture in a dry spell, and a thinner layer dries out "
             "too fast for new sod to establish. The worked example lawn at 4 in needs 100 "
             "cubic feet, 3.7 cubic yards or 134 forty-pound bags."),
            ("Can I lay sod straight on my existing soil?",
             "Only if the existing soil is already deep, loose topsoil. Most gardens sit on "
             "thin, compacted or stony ground, and sod laid on it roots into a shallow layer "
             "that dries out in the first hot week. Strip the old turf, loosen the ground "
             "below, and lay 4 in of fresh topsoil first."),
            ("Should I buy topsoil in bags or bulk for a sod base?",
             "Buy bulk for any sod base. The worked example lawn needs 134 bags, and even a "
             "small 10 by 10 ft patch needs 45 bags, which is already a heavy load to carry "
             "and open. A bulk delivery of 3.7 cubic yards is cheaper per cubic foot and "
             "arrives in one load that can be barrowed straight to the base."),
        ],
        "body": _body(
            lead=(
                "A lawn 20 feet by 15 feet needs 100 cubic feet of topsoil, which is 3.7 cubic "
                "yards or 134 bags of forty pounds, laid 4 inches deep before the sod goes "
                "down. Sod is only as good as the soil beneath it: the turf arrives with "
                "almost no root depth of its own, and the first weeks decide whether it knits "
                "into a lawn or dries into mats that lift at the corners.\n\n"
                "Four inches of topsoil is the depth that gives new roots somewhere to go. "
                "Less than that and the sod sits on a shallow layer that dries out in the "
                "first hot week; more than that is rarely needed unless the ground below is "
                "concrete-hard or pure rubble. This page gives the amounts for the standard "
                "base, for deeper and thinner layers, and for the lawn sizes around it."
            ),
            worked_lead=(
                "For a lawn measuring 20 feet by 15 feet, with topsoil laid 4 inches deep:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 15\n"
                "*   depth = 4\n"
                "*   Square feet: 300.0\n"
                "*   Cubic feet: 100.0\n"
                "*   Cubic yards: 3.7\n"
                "*   40 lb bags: 134"
            ),
            sections=[
                ("Why Sod Needs Four Inches",
                 "Sod arrives as a thin mat of grass and roots, usually less than an inch of "
                 "soil attached, so everything below that inch is ground you must provide. Four "
                 "inches of loose topsoil gives the roots depth to anchor into and a reservoir "
                 "of moisture to draw on while they establish, which is what stops the turf "
                 "curling up at the edges in the first dry spell.\n\n"
                 "The same 20 by 15 ft lawn at only 2 in deep needs 50 cubic feet, which is "
                 "1.85 cubic yards or 67 bags, but the saving is false economy: a 2 in layer "
                 "dries through in a day of sun, and sod on a dry base roots slowly or not at "
                 "all. At 6 in deep the lawn needs 150 cubic feet, 5.56 cubic yards or 200 bags, "
                 "which is the depth to use over compacted clay or rubble where the ground "
                 "below holds no moisture at all."),
                ("Bigger Lawns and Small Patches",
                 "The amount scales directly with the area, because the depth stays at 4 in. A "
                 "small 10 by 10 ft patch needs 33.3 cubic feet, which is 1.23 cubic yards or "
                 "45 bags of forty pounds, and is the largest patch where bags are still worth "
                 "considering. A 30 by 20 ft lawn needs 200 cubic feet, 7.41 cubic yards or 267 "
                 "bags, which is firmly a bulk order.\n\n"
                 "A full 1,000 sq ft lawn, 40 by 25 ft, needs 333.3 cubic feet at 4 in, which "
                 "is 12.35 cubic yards or 445 bags. Nobody carries 445 bags, so a lawn that size "
                 "is a loose bulk delivery, tipped as close to the ground as the truck can get "
                 "and barrowed from there. Measure the lawn in rectangles and add the areas "
                 "together, and order a little extra for the spots where the ground dips."),
                ("Bags or Bulk for a Sod Base",
                 "Buy bulk for any sod base. The worked example lawn needs 134 bags, and even "
                 "the small 10 by 10 ft patch needs 45 bags, which is already a heavy load to "
                 "carry and open one bag at a time. A bulk delivery of 3.7 cubic yards is "
                 "cheaper per cubic foot, arrives in one load, and can be barrowed straight "
                 "from the pile to the base.\n\n"
                 "Order screened topsoil, not general fill. Fill can contain rubble, clay lumps "
                 "and weed seed, and a sod lawn laid on it shows every stone the first time it "
                 "is mown. Screened lawn topsoil costs a little more and is the only grade "
                 "worth putting under turf that has to look good from the first month."),
                ("Preparing the Ground Below",
                 "Strip the old turf and weeds first, then loosen the ground below with a fork "
                 "or a rotavator to at least a few inches. Sod laid on hard, unbroken ground "
                 "roots into the topsoil alone and never bonds to the earth beneath, so the "
                 "first drought lifts it in sheets. Breaking the surface below lets the roots "
                 "grow down through the new topsoil and into the ground itself.\n\n"
                 "Grade the loosened ground roughly level, pick out stones and roots, and then "
                 "spread the topsoil in an even 4 in layer, firming it with a roller or by "
                 "treading it in boards. A base that is soft in one corner and hard in another "
                 "settles unevenly, and the sod follows the dips. Rake the surface fine, water "
                 "it lightly so it settles, and re-check the level before the turf arrives."),
                ("Laying Sod on the Fresh Topsoil",
                 "Lay the sod the same day the topsoil is finished, while the base is still "
                 "moist and loose. Butt the rolls tightly together with no gaps, stagger the "
                 "joints like brickwork, and roll the finished lawn so every part of the turf "
                 "touches the soil below. An air gap under a roll is a patch that dries out "
                 "and dies before it ever roots.\n\n"
                 "Water deeply on the day of laying and keep the lawn damp, not soaked, for the "
                 "first two weeks while the roots grow down into the 4 in of topsoil. Lift a "
                 "corner after a week to check: white roots reaching into the soil mean the "
                 "base is doing its job. Hold off mowing until the turf resists a gentle tug, "
                 "which is the sign the roots have taken hold."),
            ],
        ),
    },
]
