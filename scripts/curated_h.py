"""Curated articles, part H (compost topdressing for lawns, gravel flower beds,
60 lb concrete bags)."""

from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-compost-to-add-to-lawn",
        "title": "How Much Compost to Add to a Lawn: Topdressing Rates",
        "cluster": "compost",
        "primary_keyword": "how much compost to add to lawn",
        "secondary_keywords": ["compost topdressing lawn how much", "topdress lawn with compost depth",
                               "how many bags of compost for lawn", "compost for lawn in spring"],
        "calculator": "compost",
        "calculator_defaults": {"length": 50, "width": 20, "depth": 0.25},
        "meta_description": "Topdressing a 1,000 sq ft lawn with a quarter inch of compost takes 20.8 cu ft, "
                            "0.77 cubic yards or 21 one-cu-ft bags. Spread thin, in the growing season.",
        "faq": [
            ("How deep should compost be when topdressing a lawn?",
             "A quarter inch is the standard dressing for a lawn you want to keep growing. "
             "The grass blades stay above the compost and keep photosynthesizing, while the "
             "material works down into the soil. A half-inch dressing is the most to use in one "
             "pass, and only on a vigorous lawn in strong growth."),
            ("When is the best time to topdress a lawn with compost?",
             "While the grass is growing strongly, in spring or early autumn. The grass needs "
             "to grow through the dressing quickly, and the soil life that breaks the compost "
             "down is most active in warm, moist soil. Avoid drought, frost and midwinter."),
            ("Should compost be dug into a lawn or left on the surface?",
             "Left on the surface and brushed in, never dug in. Digging destroys the turf you "
             "are trying to feed. Spread the compost, work it down between the blades with a "
             "stiff brush or the back of a rake, and let worms and rain carry it into the root zone."),
        ],
        "body": _body(
            lead=(
                "Topdressing a 1,000 sq ft lawn with a quarter inch of compost takes 20.8 cubic "
                "feet, which is 0.77 cubic yards or 21 bags of one cubic foot. That thin layer "
                "is the whole point of the job: topdressing feeds the soil without burying the "
                "grass, and a lawn that is smothered under compost stops growing instead of "
                "improving.\n\n"
                "The mistake most people make is treating a lawn like a garden bed and tipping "
                "on far too much. A bed can take several inches of compost dug in; a lawn can "
                "only take a dusting that the grass grows through. This page gives the amounts "
                "for a standard dressing, for a heavier one, and for the small lawns where bags "
                "beat a bulk delivery."
            ),
            worked_lead=(
                "For a lawn measuring 50 feet by 20 feet, with compost spread a quarter inch deep:"
            ),
            bullets=(
                "*   length = 50\n"
                "*   width = 20\n"
                "*   depth = 0.25\n"
                "*   Square feet: 1000.0\n"
                "*   Cubic feet: 20.8\n"
                "*   Cubic yards: 0.77\n"
                "*   1 cu ft bags: 21"
            ),
            sections=[
                ("The Quarter-Inch Rule",
                 "Grass grows through a shallow dressing because the leaf tips stay in the light. "
                 "Spread a quarter inch over the whole lawn, brush it down between the blades, "
                 "and the grass pushes through within a week or two in the growing season. The "
                 "compost then sits at the soil surface, where worms pull it down and microbes "
                 "break it into the humus that holds moisture and nutrients.\n\n"
                 "A half-inch dressing is the most to use in one pass, and only on a vigorous "
                 "lawn in strong growth. Over 1,000 sq ft, half an inch takes 41.7 cu ft, which "
                 "is 1.54 cubic yards or 42 bags of one cubic foot. Anything deeper risks "
                 "yellowing the grass underneath, and a lawn that has to regrow from its crowns "
                 "loses the season you were trying to improve."),
                ("When to Topdress, and When Not To",
                 "Topdress while the grass is growing strongly, in spring or early autumn. The "
                 "grass needs to grow through the dressing quickly, and the soil life that "
                 "breaks the compost down is most active in warm, moist soil. A dressing applied "
                 "just before steady rain is ideal, because the rain washes the fine material "
                 "down to the soil surface instead of leaving it sitting on the blades.\n\n"
                 "Avoid drought, frost and the middle of winter. In drought the compost dries "
                 "on the surface and blows about; in cold weather it sits unchanged for months. "
                 "Also skip topdressing a lawn that is already stressed, for example one cut "
                 "very short in a heatwave, until it has recovered its strength."),
                ("Spreading It Without Smothering the Grass",
                 "Mow first, a little shorter than usual, and rake up the clippings so the "
                 "compost reaches the soil instead of sitting on a thatch mat. Tip the compost "
                 "in small heaps across the lawn, spread it with a shovel, then work it down "
                 "with a stiff brush or the back of a landscape rake until the grass tips show "
                 "through everywhere.\n\n"
                 "Never dig compost into a lawn. Digging destroys the turf you are trying to "
                 "feed, and a dug patch takes a season to knit back together. The surface method "
                 "looks untidy for a few days, but the grass grows through it and the soil "
                 "improves from the top down, which is exactly where the roots need it."),
                ("Bags or Bulk for a Lawn Dressing",
                 "At 21 bags, the 1,000 sq ft dressing is a judgement call. Bags are easy to "
                 "carry, easy to tip in small heaps, and there is no delivery to arrange, but "
                 "they cost more per cubic foot and leave a pile of plastic. A bulk delivery of "
                 "0.77 cubic yards is cheaper for a lawn this size and up, and one load covers "
                 "the whole job.\n\n"
                 "Small lawns tip the balance back to bags. A 500 sq ft lawn at a quarter inch "
                 "needs only 10.4 cu ft, which is 0.39 cubic yards or 11 bags, and a bulk delivery "
                 "for that little material is rarely worth the delivery charge. A 2,000 sq ft "
                 "lawn at the same depth needs 41.7 cu ft, 1.54 cubic yards or 42 bags, where "
                 "bulk is clearly the better buy."),
                ("What Compost Does That Fertilizer Does Not",
                 "Fertilizer feeds the grass directly; compost feeds the soil that feeds the "
                 "grass. A compost dressing adds organic matter, which holds water in dry spells, "
                 "holds nutrients that would otherwise wash through, and gives soil life "
                 "something to work on. Lawns on thin, sandy or heavily compacted soil show the "
                 "biggest change, because their soil has the least organic matter to start with.\n\n"
                 "Compost is not a substitute for seed on bare patches or for levelling a bumpy "
                 "lawn. Bare ground still needs seed, and hollows still need a dressing of "
                 "topsoil or a soil and sand mix. Use compost as the annual maintenance dressing "
                 "that keeps a healthy lawn healthy, and the grass will need less fertilizer "
                 "and less water across the season."),
            ],
        ),
    },
    {
        "slug": "how-much-gravel-do-i-need-for-flower-bed",
        "title": "How Much Gravel for a Flower Bed? Depth and Tons",
        "cluster": "gravel",
        "primary_keyword": "how much gravel do i need for flower bed",
        "secondary_keywords": ["gravel for flower bed depth", "decorative stone for flower beds",
                               "how many tons of gravel for flower bed", "gravel mulch flower bed"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 20, "width": 4, "depth": 2},
        "meta_description": "A 20 by 4 ft flower bed covered 2 in deep in gravel needs 0.49 cubic yards, "
                            "about 0.69 tons. Keep stone off plant stems and lay fabric below it.",
        "faq": [
            ("How deep should gravel be in a flower bed?",
             "Two inches is the standard depth for a decorative gravel top layer in a flower "
             "bed. One inch lets weeds through and shows the fabric below, while three inches "
             "is needed only where the bed is on a slope or takes foot traffic. The worked "
             "example bed at 2 in needs 0.49 cubic yards, about 0.69 tons."),
            ("Do I need landscape fabric under gravel in a flower bed?",
             "Yes, lay a permeable landscape fabric below the gravel. It stops the stone "
             "sinking into the soil and keeps soil from washing up into the stone, which is "
             "what turns a clean gravel bed muddy. Use a permeable fabric, not plastic sheet, "
             "so water still drains through to the roots."),
            ("Is gravel or mulch better for a flower bed?",
             "Gravel suits dry, sunny beds and plants that like sharp drainage, and it does "
             "not need replacing each year. Mulch suits beds that need the soil to stay moist "
             "and be fed as it breaks down. Gravel adds no nutrients, so a gravel bed still "
             "needs feeding, and stone holds heat that tender plants dislike."),
        ],
        "body": _body(
            lead=(
                "A 20 by 4 ft flower bed covered 2 inches deep in gravel needs 0.49 cubic yards, "
                "about 0.69 tons. Gravel in a flower bed is a top layer, not a soil amendment: "
                "it sits on the surface, suppresses weeds, keeps moisture in the soil below, "
                "and stays put for years where bark mulch would need replacing every season.\n\n"
                "The depth is what most people get wrong. Too thin and the fabric shows through "
                "within weeks; too thick and the bed becomes a rockery that sheds water and "
                "cooks the plants. Two inches is the depth that works for a flat bed, and this "
                "page gives the amounts for that depth and for the cases where you need more."
            ),
            worked_lead=(
                "For a flower bed measuring 20 feet by 4 feet, with gravel spread 2 inches deep:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 4\n"
                "*   depth = 2\n"
                "*   Square feet: 80.0\n"
                "*   Cubic yards: 0.49\n"
                "*   Tons: 0.69"
            ),
            sections=[
                ("Why Two Inches Is the Standard Depth",
                 "At 2 in, the stone layer is thick enough to shade the soil, which is what "
                 "stops weed seeds germinating, and to hide the landscape fabric completely. "
                 "A 20 by 4 ft bed at 2 in needs 0.49 cubic yards, about 0.69 tons, which is a "
                 "small load that one person can barrow and spread in an afternoon.\n\n"
                 "One inch is not enough. The same bed at 1 in takes only 0.25 cubic yards and "
                 "0.35 tons, but the fabric shows through in patches and weeds find the thin "
                 "spots within a season. Three inches is the depth for a bed on a slope, where "
                 "rain washes stone downhill, or for a bed that takes foot traffic. That bed at "
                 "3 in needs 0.74 cubic yards and 1.04 tons, roughly half as much again."),
                ("Fabric First, Then Stone",
                 "Lay a permeable landscape fabric below the gravel, and overlap the joins by "
                 "several inches so soil cannot work up through the gaps. The fabric stops the "
                 "stone sinking into soft soil and keeps the soil from washing up into the "
                 "stone, which is what turns a clean gravel bed muddy after the first heavy rain.\n\n"
                 "Use a permeable fabric, not a plastic sheet. Plastic traps water at the "
                 "surface, starves the roots below, and turns the bed into a puddle in wet "
                 "weather. Cut an X in the fabric where each plant goes, fold the flaps back, "
                 "and plant through it, keeping the stone pulled back from the stems."),
                ("Keeping Stone Off the Plants",
                 "Gravel against a plant stem holds moisture against the bark and invites rot, "
                 "and dark stone in full sun holds heat that scorches low leaves. Pull the "
                 "stone back a few inches from every stem and leave a ring of bare soil or "
                 "mulch around the base of each plant, so air moves and water reaches the roots.\n\n"
                 "The same care applies at the bed edge. A shallow trench or a strip of steel "
                 "or stone edging keeps the gravel in the bed and off the lawn, where a mower "
                 "turns a stray stone into a projectile. Edge the bed before you tip the gravel, "
                 "not after, because retrofitting an edge means moving stone twice."),
                ("Gravel or Mulch for This Bed?",
                 "Gravel suits dry, sunny beds and plants that like sharp drainage, and it does "
                 "not need replacing each year. A gravel bed looks the same in year five as it "
                 "did in year one, apart from the leaves that need blowing off it in autumn. "
                 "That permanence is its main advantage over bark, which rots down and needs "
                 "topping up annually.\n\n"
                 "Mulch suits beds that need the soil to stay moist and be fed as the mulch "
                 "breaks down. Gravel adds no nutrients at all, so a gravel bed still needs "
                 "feeding, and stone holds heat that tender plants dislike. For a shady, moist "
                 "bed full of hostas and ferns, mulch is the better choice; for a sunny bed of "
                 "lavender, grasses and Mediterranean plants, gravel is the natural fit."),
                ("Ordering, Delivering and Spreading",
                 "A bed of this size is a small order. At 0.49 cubic yards and 0.69 tons, a "
                 "single bulk bag or a small loose load covers it, and bags from a garden "
                 "centre are a realistic alternative where a truck cannot reach the bed. A "
                 "smaller bed, 10 by 4 ft at the same 2 in depth, needs only 0.25 cubic yards "
                 "and 0.35 tons, which is firmly bag territory.\n\n"
                 "Tip the gravel in heaps along the bed, not in one pile at the end, and rake "
                 "it out to a level 2 in layer, checking the depth with a ruler in several "
                 "places rather than by eye. Order a little extra for the spots where the "
                 "fabric dips and the stone settles, and keep the spare in a bucket for topping "
                 "up after the first winter."),
            ],
        ),
    },
    {
        "slug": "how-many-60lb-bags-of-concrete-do-i-need",
        "title": "How Many 60 Lb Bags of Concrete Do I Need?",
        "cluster": "concrete",
        "primary_keyword": "how many 60lb bags of concrete do i need",
        "secondary_keywords": ["60 lb bag concrete yield", "how many 60 pound bags per cubic yard",
                               "60 lb vs 80 lb concrete bags", "bags of concrete for slab"],
        "calculator": "concrete",
        "calculator_defaults": {"length": 10, "width": 10, "thickness": 4},
        "meta_description": "A 10 by 10 ft slab 4 in thick needs 33.3 cu ft of concrete, or 75 bags of 60 lb. "
                            "Count by bag yield, then round up and add a spare bag.",
        "faq": [
            ("How much concrete does a 60 lb bag make?",
             "A 60 lb bag yields about 0.45 cubic feet of mixed concrete. That yield is the "
             "number to divide into your slab volume: a 10 by 10 ft slab 4 in thick is 33.3 "
             "cubic feet, which needs 75 bags of 60 lb once the result is rounded up."),
            ("Should I buy 60 lb or 80 lb bags of concrete?",
             "Buy 60 lb bags when the work is spread over a long day or carried by hand, "
             "because each bag is easier to lift and mix. Buy 80 lb bags for a big slab, "
             "because the same 10 by 10 ft slab needs only 56 bags of 80 lb against 75 bags "
             "of 60 lb, which means fewer bags to open and mix."),
            ("How many extra bags of concrete should I buy?",
             "Add one spare bag, plus round every result up to a whole bag. A slab that "
             "calculates to 75 bags of 60 lb should be bought as 76, because a short pour "
             "cannot be finished the next day without a visible joint. Unopened bags keep for "
             "a later small job if stored dry."),
        ],
        "body": _body(
            lead=(
                "A 10 by 10 ft slab 4 inches thick needs 33.3 cubic feet of concrete, which is "
                "75 bags of 60 lb once the result is rounded up to whole bags. The 60 lb bag is "
                "the one most home improvers actually carry, because it is light enough to "
                "lift repeatedly through a long mixing session, and its yield is the figure "
                "that turns a slab size into a shopping list.\n\n"
                "The count itself is simple division, but two details catch people out: the "
                "yield of a 60 lb bag is smaller than most people guess, and a result that is "
                "not a whole number must always round up. A slab that is one bag short cannot "
                "be topped up the next day without a cold joint showing in the finished surface."
            ),
            worked_lead=(
                "For a slab measuring 10 feet by 10 feet, poured 4 inches thick, using 60 lb bags:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   thickness = 4\n"
                "*   Cubic feet: 33.3\n"
                "*   Cubic yards: 1.23\n"
                "*   60 lb bags: 75\n"
                "*   80 lb bags: 56"
            ),
            sections=[
                ("What a 60 Lb Bag Actually Yields",
                 "A 60 lb bag yields about 0.45 cubic feet of mixed concrete, and an 80 lb bag "
                 "yields about 0.60 cubic feet. Those two yields are all the arithmetic there "
                 "is: divide the slab volume by the yield of the bag you are buying, then round "
                 "up to the next whole bag, because a part bag cannot be bought.\n\n"
                 "The worked example shows the difference the bag size makes. The 10 by 10 ft "
                 "slab at 4 in is 33.3 cubic feet, or 1.23 cubic yards, and it needs 75 bags of "
                 "60 lb against 56 bags of 80 lb. The concrete itself is the same either way; "
                 "the 60 lb route just means opening and mixing more bags to reach the same volume."),
                ("60 Lb or 80 Lb: Which to Carry",
                 "Buy 60 lb bags when the work is spread over a long day, when the bags must be "
                 "carried through a house or up steps, or when one person is mixing alone. A "
                 "bag that is a third lighter is a real difference by the twentieth bag, and "
                 "tired mixing is how a pour ends up with dry patches and weak spots.\n\n"
                 "Buy 80 lb bags for a big slab poured with help, where fewer bags means fewer "
                 "trips to the pile and less packaging to clear. A 12 by 12 ft slab at 4 in is "
                 "48 cubic feet and needs 107 bags of 60 lb against 80 bags of 80 lb, so the "
                 "saving in handling is substantial. Either way, keep the mix ratio the same "
                 "from the first bag to the last, or the slab cures unevenly."),
                ("Sizes Beyond the Worked Example",
                 "The calculator scales the same way for any rectangle. A small 6 by 6 ft slab "
                 "at 4 in is 12 cubic feet, or 0.44 cubic yards, and needs 27 bags of 60 lb or "
                 "20 bags of 80 lb. A garden path 20 ft long and 3 ft wide at 4 in is 20 cubic "
                 "feet, or 0.74 cubic yards, and needs 45 bags of 60 lb or 34 bags of 80 lb.\n\n"
                 "Thickness changes the count faster than most people expect, because it "
                 "multiplies the whole area. The same 10 by 10 ft slab poured 6 in thick instead "
                 "of 4 in is 50 cubic feet, or 1.85 cubic yards, and needs 112 bags of 60 lb or "
                 "84 bags of 80 lb. Check the thickness before ordering, and measure it at "
                 "several points across the formwork, because a base that dips in the middle "
                 "quietly adds bags."),
                ("Rounding Up and the Spare Bag",
                 "Round every result up to a whole bag, and then add one spare bag on top. A "
                 "slab that calculates to 75 bags of 60 lb should be bought as 76, because a "
                 "short pour cannot be finished the next day without a visible joint where the "
                 "old concrete had started to set. The spare bag also covers the inevitable "
                 "spillage and the formwork that is slightly deeper than planned.\n\n"
                 "Unopened bags keep for a later small job if they are stored dry and off the "
                 "ground. A bag that has gone damp sets in lumps inside the paper and is no "
                 "longer reliable, so store the spare under cover rather than leaving it out "
                 "by the slab overnight."),
                ("When Bags Stop Making Sense",
                 "At 75 bags, the worked example slab is already a long mixing session, and "
                 "anything much bigger deserves a price for ready-mix. A cubic yard of concrete "
                 "is 27 cubic feet, so the 1.23 cubic yards in the example is a small ready-mix "
                 "load, and many suppliers deliver that size with a minimum-load charge that is "
                 "still cheaper than the bags and the labour of mixing them.\n\n"
                 "Bags win for small slabs, for sites a truck cannot reach, and for jobs poured "
                 "in stages over several weekends. Ready-mix wins once the count passes roughly "
                 "a hundred bags, or when the slab must be poured in one continuous session to "
                 "avoid joints. Either way, the bag count from the calculator is the figure to "
                 "compare against the ready-mix quote."),
            ],
        ),
    },
]
