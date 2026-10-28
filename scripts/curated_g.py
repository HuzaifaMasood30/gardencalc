"""Curated articles, part G (lawn levelling, river rock, paver sand, acre rates, backsplash)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-topsoil-do-i-need-to-level-my-lawn",
        "title": "How Much Topsoil to Level a Lawn: Depths and Yards",
        "cluster": "topsoil",
        "primary_keyword": "how much topsoil do i need to level my lawn",
        "secondary_keywords": ["topsoil for lawn levelling", "top dressing lawn how much",
                               "how many yards of topsoil for 1000 sq ft", "fix a bumpy lawn"],
        "calculator": "topsoil",
        "calculator_defaults": {"length": 50, "width": 20, "depth": 0.5},
        "meta_description": "Levelling a 1,000 sq ft lawn with a half-inch of topsoil takes 41.7 cu ft, "
                            "1.54 cubic yards or 56 bags of 40 lb. Fill hollows gradually, in stages.",
        "faq": [
            ("How deep can I fill a hollow in my lawn in one go?",
             "About half an inch over grass you want to keep, so the blades still poke through and "
             "keep growing. Deeper hollows need two or three passes a few weeks apart, or strip the "
             "turf, fill to the full depth and reseed."),
            ("Is topsoil or sand better for levelling a lawn?",
             "A topsoil and sand mix, or straight topsoil on thin soil, feeds the grass as it levels. "
             "Pure sand suits warm-season lawns levelled professionally; on a typical home lawn "
             "topsoil is the safer all-round choice."),
            ("When is the best time to level a lawn?",
             "While the grass is growing strongly, spring or early autumn. The grass needs to grow "
             "through the dressing quickly, so avoid drought, frost and the middle of winter."),
        ],
        "body": _body(
            lead=(
                "Levelling a 1,000 sq ft lawn with a half-inch layer of topsoil takes 41.7 cubic feet, "
                "which is 1.54 cubic yards or 56 bags of 40 lb. Half an inch sounds like nothing, but "
                "it is the most you can spread over living grass in one pass without smothering it, "
                "and repeated light passes are how a bumpy lawn actually gets flat.\n\n"
                "The method matters as much as the amount. You are not burying the lawn and starting "
                "again; you are filling the low spots so the mower stops scalping the high ones. This "
                "page gives the amounts for topdressing and for deeper fills, and when each is the "
                "right approach."
            ),
            worked_lead=(
                "For a lawn measuring 50 feet by 20 feet, with topsoil spread half an inch deep:"
            ),
            bullets=(
                "*   length = 50\n"
                "*   width = 20\n"
                "*   depth = 0.5\n"
                "*   Square feet: 1000.0\n"
                "*   Cubic feet: 41.7\n"
                "*   Cubic yards: 1.54\n"
                "*   40 lb bags: 56"
            ),
            sections=[
                ("The Half-Inch Rule for Living Grass",
                 "Grass grows through a shallow dressing because the leaf tips stay in the light. "
                 "Spread half an inch over the whole lawn, work it into the hollows with the back of "
                 "a rake or a stiff brush, and the grass pushes through within a week or two in the "
                 "growing season. A full inch in one pass yellows the grass under it and can kill "
                 "patches outright.\n\n"
                 "So deep hollows are a staged job: half an inch now, let the grass recover, then "
                 "another half inch over just the remaining dips. Two or three passes across a "
                 "season will take out a two-inch hollow without any reseeding."),
                ("When the Hollow Is Too Deep to Topdress",
                 "If a dip is more than about 2 in deep, or the lawn has sunk along a trench line, "
                 "topdressing takes forever. Cut the turf out with a spade, fork it up and set it "
                 "aside, fill the hollow with topsoil to just above the surrounding level, firm it, "
                 "then relay the turf on top.\n\n"
                 "For a filled area, the depth in the calculator is the real depth of the fill, not "
                 "the half-inch dressing figure. A 10 x 10 ft patch filled 3 in deep takes 25 cu ft "
                 "of topsoil, just under a cubic yard, and it will settle by roughly a fifth, so "
                 "mound it slightly high."),
                ("How Much Topsoil at Each Depth",
                 "The volume rises in a straight line with depth, so the worked example scales "
                 "easily. At a quarter inch over 1,000 sq ft you need about 0.77 cubic yards. At "
                 "half an inch it is 1.54 cubic yards, and at a full inch 3.09 cubic yards.\n\n"
                 "A cubic yard of topsoil covers about 650 sq ft at half an inch deep. Measure your "
                 "lawn, decide whether you are dressing the whole area or only the worst third of "
                 "it, and let the calculator turn that into yards or bags. Most home lawns only "
                 "need the hollows treated, which cuts the order substantially."),
                ("Spreading and Settling It In",
                 "Mow short first and rake up the clippings, so the soil reaches the ground instead "
                 "of sitting on a thatch mat. Tip the topsoil in small heaps across the lawn, spread "
                 "it with the back of a landscape rake, then brush or drag it so the low spots keep "
                 "more and the high spots keep almost none.\n\n"
                 "Water it in, or time the job before steady rain. Water washes the soil down around "
                 "the grass crowns and shows you the true level while you can still adjust it. "
                 "Overseed any thin patches at the same visit while the surface is open."),
                ("Bags or Bulk for a Lawn Job",
                 "At 56 bags, the 1,000 sq ft dressing sits past the point where bags make sense for "
                 "most people: a bulk delivery of a yard and a half is cheaper and far less "
                 "packaging. Bags still win for a small front lawn or where a truck cannot tip "
                 "anywhere near the grass.\n\n"
                 "Screened topsoil is worth the small premium for levelling. Lumpy, stony soil does "
                 "not spread thin, and thin and even is the entire point of the job. Order about 10% "
                 "extra for the hollows you only discover once you start spreading."),
            ],
        ),
    },
    {
        "slug": "how-much-river-rock-do-i-need-for-landscaping",
        "title": "How Much River Rock for Landscaping: Depth and Tons",
        "cluster": "gravel",
        "primary_keyword": "how much river rock do i need for landscaping",
        "secondary_keywords": ["river rock coverage", "river rock depth for beds",
                               "how many tons of river rock", "decorative stone calculator"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 3, "kind": "river"},
        "meta_description": "A 10x10 ft bed covered 3 in deep takes 0.93 cubic yards of river rock, about "
                            "1.3 tons. Two inches shows soil between the stones; 3 in gives full cover.",
        "faq": [
            ("How deep should river rock be in a garden bed?",
             "Three inches for full cover that hides the soil and the membrane under it. Two inches "
             "is the minimum and tends to show gaps once the stones settle; much deeper than 4 in "
             "wastes money and makes the bed hard to plant into later."),
            ("Do I need landscape fabric under river rock?",
             "Yes, more than with bark. Rock does not knit together or shade the soil surface the "
             "way organic mulch does, so a membrane underneath is what stops weeds coming up "
             "between the stones. Pin it well; edges that lift will show."),
            ("How many square feet does a ton of river rock cover?",
             "About 85 sq ft at 3 in deep, or about 125 sq ft at 2 in. A ton is roughly 0.71 cubic "
             "yards of stone."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft bed covered with river rock 3 inches deep takes 0.93 cubic yards of "
                "stone, about 1.3 tons. River rock is a surface finish, not a base: the depth is "
                "about hiding the ground completely and keeping the stones from migrating, not about "
                "strength.\n\n"
                "Because the stones are rounded and graded to a fairly even size, the layer behaves "
                "differently from crushed gravel. It does not compact, it shifts underfoot a little, "
                "and it needs a membrane under it to stay clean. Get the depth and the preparation "
                "right and it is one of the longest-lasting finishes a bed can have."
            ),
            worked_lead=(
                "For a bed measuring 10 feet by 10 feet, with river rock spread 3 inches deep:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   depth = 3\n"
                "*   Square feet: 100.0\n"
                "*   Cubic yards: 0.93\n"
                "*   Tons: 1.3"
            ),
            sections=[
                ("Why Three Inches Is the Cover Depth",
                 "River rock stones are typically 1 to 3 in across, and a layer needs to be at least "
                 "one stone deeper than the largest stones in the mix, or the ground shows through "
                 "the gaps. At 2 in deep the bigger stones sit proud and the small ones fall between "
                 "them, leaving a speckled finish that looks under-ordered.\n\n"
                 "Three inches gives a closed surface with a little depth to rake level after "
                 "settling. Beyond 4 in you are paying for stone nobody sees, and deep rock makes "
                 "future planting miserable, because every new plant means excavating a bucket of "
                 "stones first."),
                ("How Much Rock at Each Depth",
                 "Depth drives the order on a decorative layer just as it does on a base. At 2 in "
                 "deep, 100 sq ft takes 0.62 cubic yards, about 0.87 tons. At 3 in it is 0.93 cubic "
                 "yards, about 1.3 tons. At 4 in it is 1.23 cubic yards, about 1.73 tons.\n\n"
                 "The quick check: a cubic yard of river rock covers about 108 sq ft at 3 in deep "
                 "and weighs about 1.4 tons. Measure each bed separately and add the areas "
                 "together; rock ordered for the whole garden at once is far cheaper per ton than "
                 "several small orders."),
                ("Membrane, Edging and the Ground Beneath",
                 "Strip weeds and level the soil first, then lay a permeable landscape membrane and "
                 "pin it, especially on slopes and edges. The membrane keeps soil from working up "
                 "into the stones and muddying them, which is what ruins the finish within a couple "
                 "of winters.\n\n"
                 "Fit a firm edge, steel, stone or timber, at lawn borders. Rounded stones roll, "
                 "and a rock bed against grass without an edge sheds stones into the lawn "
                 "continuously, where they meet the mower. The edge is not decoration; it is what "
                 "keeps 1.3 tons of stone where you put it."),
                ("Stone Size Changes the Look and the Depth",
                 "Small river rock, around 1 in, settles into a tight, almost gravel-like surface "
                 "and works around stepping stones and in narrow beds. Larger stone, 2 to 3 in, "
                 "reads as a bolder, more architectural finish and is easier to keep free of leaves "
                 "with a blower, but it needs the full 3 in depth to cover.\n\n"
                 "Whatever size you choose, order the whole job in one batch. River rock is a "
                 "natural material and the colour mix shifts between loads; a second delivery for "
                 "the last bed can visibly mismatch the first."),
                ("Bags, Bulk Bags and Loose Loads",
                 "A 10 x 10 ft bed at 1.3 tons is a bulk-bag job: one one-ton bag plus a few small "
                 "bags, or a loose tip if access allows. Small 20 kg bags only make sense for "
                 "patching an existing bed or for a single feature pot.\n\n"
                 "Have the bag set down as close to the bed as the crane or truck can reach, "
                 "because barrowing stone is the slowest part of the job. Rake the rock out in "
                 "small heaps and level as you go; dumping it all in the middle and spreading "
                 "outward pushes the membrane around and wrinkles it."),
            ],
        ),
    },
    {
        "slug": "how-much-sand-do-i-need-for-paver-base",
        "title": "How Much Sand for a Paver Base: The 1-Inch Layer",
        "cluster": "sand",
        "primary_keyword": "how much sand do i need for paver base",
        "secondary_keywords": ["paver bedding sand depth", "how many bags of paver sand",
                               "leveling sand for pavers", "sand layer under pavers"],
        "calculator": "sand",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 1},
        "meta_description": "A 10x10 ft paver base needs a 1 in sand layer: 0.31 cubic yards, about 0.42 "
                            "tons or 17 bags of 0.5 cu ft. Coarse bedding sand, never play sand.",
        "faq": [
            ("How thick should the sand layer be under pavers?",
             "One inch of coarse bedding sand, screeded level over the compacted gravel base. "
             "Thicker is not better: a deep sand layer shifts underfoot and the pavers rock and dip."),
            ("What kind of sand goes under pavers?",
             "Coarse, angular bedding sand, often sold as concrete sand. Play sand and kiln-dried "
             "jointing sand are too fine and round for the bedding layer; jointing sand is only for "
             "the joints at the end."),
            ("How many bags of sand do I need for a patio base?",
             "For 100 sq ft at 1 in deep, about 17 bags of 0.5 cu ft. Past a few hundred square feet "
             "a bulk bag or loose load is cheaper and easier to screed from."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft paver base with a sand layer 1 inch deep takes 0.31 cubic yards of sand, "
                "about 0.42 tons or 17 bags of 0.5 cu ft. The sand is the last layer of the base: it "
                "goes over the compacted gravel, is screeded dead level, and is what each paver is "
                "bedded into.\n\n"
                "Of all the layers, this is the one people most often over-order or under-order, "
                "because the instinct is to spread it thick like the gravel. One inch is the engineered "
                "depth. This page gives the amounts and explains why more sand makes a worse patio."
            ),
            worked_lead=(
                "For a paver base measuring 10 feet by 10 feet, with a sand layer 1 inch deep:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   depth = 1\n"
                "*   Square feet: 100.0\n"
                "*   Cubic yards: 0.31\n"
                "*   Tons: 0.42\n"
                "*   0.5 cu ft bags: 17"
            ),
            sections=[
                ("One Inch, and Why Not More",
                 "The bedding layer exists to take out the last few millimetres of unevenness in the "
                 "gravel base and give every paver an identical bed. At 1 in it does that job and "
                 "then locks up when the pavers are compacted into it.\n\n"
                 "Spread it 2 or 3 in deep and it never firms up: foot traffic keeps re-arranging it, "
                 "pavers tilt, and the surface develops dips along the walking lines within a season. "
                 "If your gravel base is too uneven for a 1 in sand layer to hide, the fix is to "
                 "re-grade the gravel, not to bury the problem in sand."),
                ("Bedding Sand Is Not Jointing Sand",
                 "Bedding sand is coarse and angular, with grains that lock against each other; it is "
                 "often the same material sold as concrete sand. That angular shape is the whole "
                 "reason the layer firms up under the pavers.\n\n"
                 "Play sand is washed round and never locks, and kiln-dried jointing sand is far too "
                 "fine for a bedding layer — it belongs in the joints at the very end of the job. "
                 "Using either one as bedding is one of the most common reasons a new patio feels "
                 "spongy. Check the bag or the bulk bay label before you order."),
                ("How Much Sand at Patio Scale",
                 "The layer is thin, so quantities stay modest. At 1 in deep, 100 sq ft takes "
                 "0.31 cubic yards, about 0.42 tons. A 200 sq ft patio takes about 0.62 cubic yards, "
                 "and a 12 x 12 ft base about 0.44 cubic yards.\n\n"
                 "Order roughly 10% extra. Some sand is lost into the surface of the gravel as you "
                 "screed, some spills at the edges, and you will want a little left over for the "
                 "final jointing pass if you are using the same coarse sand on a rustic finish. One "
                 "bulk bag covers most home patios with sand to spare."),
                ("Screeding the Layer Level",
                 "Lay two parallel rails (screed pipes or straight timber battens) on the gravel, "
                 "spaced a little narrower than your straightedge, and rest them at a height that "
                 "leaves exactly 1 in of sand. Tip the sand between them, pull the straightedge "
                 "along the rails to level it, then lift the rails out and fill their tracks "
                 "carefully by hand.\n\n"
                 "Work in sections the size of an afternoon's laying, because a screeded layer "
                 "cannot be walked on. Lay the pavers straight onto the finished sand, working from "
                 "the laid surface, and never re-level with a trowel under individual pavers — that "
                 "creates the soft spots you were avoiding."),
                ("After the Pavers: The Other Sand Job",
                 "Once the field is laid and edged, sweep dry jointing sand across the surface and "
                 "run the plate compactor over it so the joints fill and the pavers lock together. "
                 "This is a separate, smaller quantity of a finer sand, and it is not included in "
                 "the bedding figure the calculator gives.\n\n"
                 "Expect to sweep more jointing sand in after the first few rains, as the joints "
                 "settle. Keep a bag in the shed for the first season; topped-up joints are what "
                 "keep the whole surface acting as one slab instead of individual stones."),
            ],
        ),
    },
    {
        "slug": "how-many-pounds-of-fertilizer-per-acre",
        "title": "How Many Pounds of Fertilizer per Acre: Rates",
        "cluster": "fertilizer",
        "primary_keyword": "how many pounds of fertilizer per acre",
        "secondary_keywords": ["fertilizer rate per acre lawn", "how much nitrogen per acre",
                               "bags of fertilizer per acre", "fertilizer per 43560 sq ft"],
        "calculator": "fertilizer",
        "calculator_defaults": {"area": 43560, "rate": 1, "bag": 40, "nitrogen": 20},
        "meta_description": "One acre at 1 lb of nitrogen per 1,000 sq ft needs 43.6 lb of nitrogen, which "
                            "is 217.8 lb of a 20% nitrogen fertilizer, about 6 bags of 40 lb.",
        "faq": [
            ("How much fertilizer does an acre of lawn need?",
             "At the standard 1 lb of nitrogen per 1,000 sq ft, one acre needs 43.6 lb of actual "
             "nitrogen. With a 20-0-0 product that is 217.8 lb of fertilizer, about six 40 lb bags."),
            ("Why is the rate quoted per 1,000 sq ft when my lawn is an acre?",
             "Because the bag label rates are written that way. An acre is 43,560 sq ft, so you "
             "multiply the per-1,000 figure by 43.56 to get your nitrogen target, then divide by "
             "the product's nitrogen percentage to get the weight to spread."),
            ("Should I put the whole amount on in one application?",
             "One pound of nitrogen per 1,000 sq ft is about the most a lawn should get in a single "
             "application. Seasonal totals of 2 to 4 lb are split across two to four feeds, not "
             "dumped on at once."),
        ],
        "body": _body(
            lead=(
                "One acre fertilized at 1 pound of nitrogen per 1,000 sq ft needs 43.6 pounds of "
                "nitrogen, which is 217.8 pounds of a fertilizer that is 20% nitrogen, about 6 bags "
                "of 40 lb. The acre figure looks big, but it is just the familiar per-1,000 sq ft rate "
                "scaled by 43.56, the number of thousands in an acre.\n\n"
                "Working at acre scale, the most common mistake is confusing pounds of nitrogen with "
                "pounds of product. A 40 lb bag of 20-0-0 holds only 8 lb of nitrogen. This page "
                "keeps the two separate and shows how the bag count follows from the rate."
            ),
            worked_lead=(
                "For one acre (43,560 sq ft) at 1 lb of nitrogen per 1,000 sq ft, using a 20% "
                "nitrogen fertilizer in 40 lb bags:"
            ),
            bullets=(
                "*   area = 43560\n"
                "*   rate = 1\n"
                "*   bag = 40\n"
                "*   nitrogen = 20\n"
                "*   Pounds of nitrogen: 43.56\n"
                "*   Pounds of product: 217.8\n"
                "*   Bags: 6"
            ),
            sections=[
                ("Nitrogen Pounds vs Product Pounds",
                 "Fertilizer recommendations are written in pounds of nitrogen, because nitrogen is "
                 "what the lawn mostly responds to and what can scorch it in excess. The number on "
                 "the bag, the first of the three figures, is the percentage of nitrogen by weight. "
                 "A 20-0-0 bag is one fifth nitrogen.\n\n"
                 "So the arithmetic runs: area rate gives 43.56 lb of nitrogen for the acre, and "
                 "dividing by 0.20 gives 217.8 lb of product to deliver it. Change the product to a "
                 "10-10-10 and the same nitrogen target needs about 436 lb of product. The rate did "
                 "not change; the concentration did."),
                ("How the Bag Size Changes the Count",
                 "At 217.8 lb of product, 40 lb bags round up to 6 bags, and you will have a little "
                 "left over, which is normal — spreaders are calibrated to the rate, not to emptying "
                 "bags exactly. In 50 lb bags the same job is 5 bags.\n\n"
                 "For areas bigger than an acre of lawn, product is often cheaper in bulk or in "
                 "half-ton sacks from an agricultural supplier. The maths is identical; only the "
                 "packaging changes. Keep the leftover part-bag dry and sealed, because fertilizer "
                 "absorbs moisture and cakes hard in the bag."),
                ("Splitting the Season's Total",
                 "An acre of lawn typically gets 2 to 4 lb of nitrogen per 1,000 sq ft across a "
                 "whole season, which is 87 to 174 lb of nitrogen, or roughly 11 to 22 bags of the "
                 "worked example's product across the year. Almost none of that should arrive in "
                 "one pass.\n\n"
                 "Split it into applications of about 1 lb at a time: early spring, late spring, "
                 "early autumn, and for cool-season lawns a late-autumn feed. Heavy single doses "
                 "push soft growth that diseases love, leach below the roots in wet weather, and "
                 "can scorch in dry weather."),
                ("Calibrating a Spreader at This Scale",
                 "On a garden lawn you can forgive a spreader that is roughly right; on an acre, "
                 "being 20% out is a whole bag wasted or a visible striping of dark and pale grass. "
                 "Weigh the product for a test area of exactly 1,000 sq ft, set the spreader, and "
                 "walk it at your normal pace.\n\n"
                 "Apply in two passes at right angles, each at half rate. It takes longer, but it "
                 "erases the stripes that a single-pass calibration error leaves behind, and on a "
                 "large lawn those stripes are visible from the road for a month."),
                ("When the Rate Should Not Be 1 Pound",
                 "One pound per 1,000 is the standard maintenance feed, not a universal constant. A "
                 "soil test that shows a phosphorus or potassium shortage changes the product choice "
                 "entirely, and a newly seeded acre is usually fed lighter and with a starter "
                 "product that carries phosphorus for root growth.\n\n"
                 "If the acre is pasture or meadow rather than lawn, rates and products differ "
                 "again, and local extension guidance for your grass type and soil is the figure to "
                 "trust. The calculator's job is the conversion from rate to bags; the rate itself "
                 "should come from a test or a label, not from habit."),
            ],
        ),
    },
    {
        "slug": "how-much-tile-do-i-need-for-kitchen-backsplash",
        "title": "How Much Tile for a Kitchen Backsplash: Counts",
        "cluster": "tile",
        "primary_keyword": "how much tile do i need for kitchen backsplash",
        "secondary_keywords": ["backsplash tile calculator", "how many subway tiles for backsplash",
                               "backsplash square footage", "tile waste for backsplash"],
        "calculator": "tile",
        "calculator_defaults": {"length": 10, "width": 1.5, "tile_w": 3, "tile_h": 6, "waste": 15},
        "meta_description": "A 10 ft run of backsplash 18 in high is 15 sq ft: with 3x6 in subway tiles "
                            "that is 120 tiles, or 138 with a 15% waste allowance for cuts and outlets.",
        "faq": [
            ("How do I measure my backsplash area?",
             "Measure the length of each run in feet and the height from countertop to the underside "
             "of the wall cabinets, usually 18 in. Multiply them for each run and add the runs "
             "together. Add the area behind a range hood separately if it goes higher."),
            ("How much extra tile should I buy for a backsplash?",
             "Allow 15% for a simple straight run with subway tiles, and 20% for diagonal or "
             "herringbone layouts, small mosaics, or a run broken up by many outlets and corners."),
            ("How many subway tiles are in a square foot?",
             "A 3x6 in tile covers 0.125 sq ft, so there are 8 tiles per square foot before waste. "
             "A 15 sq ft backsplash is 120 tiles, or about 138 with the waste allowance added."),
        ],
        "body": _body(
            lead=(
                "A 10 ft run of kitchen backsplash 18 inches high is 15 sq ft, and with standard "
                "3 x 6 in subway tiles it takes 120 tiles, or 138 tiles with a 15% waste allowance. "
                "Backsplashes are small areas with a lot of cuts, which is why the waste percentage "
                "matters more here than on any floor.\n\n"
                "Almost every backsplash order that goes wrong does so for one of two reasons: the "
                "area behind the cooker, where the splashback often runs higher, was never measured, "
                "or the box quantity was rounded down instead of up. Measure each run, then let the "
                "calculator add the allowance."
            ),
            worked_lead=(
                "For a backsplash measuring 10 feet long by 1.5 feet (18 inches) high, using "
                "3 x 6 inch tiles with a 15% waste allowance:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 1.5\n"
                "*   tile_w = 3\n"
                "*   tile_h = 6\n"
                "*   waste = 15\n"
                "*   Floor area: 15.0\n"
                "*   Tile area: 0.125\n"
                "*   Tiles: 120\n"
                "*   Tiles with waste: 138"
            ),
            sections=[
                ("Measuring the Runs You Actually Have",
                 "A backsplash is rarely one rectangle. Measure the main run along the worktop, "
                 "then any return along a side wall, then the area behind the hob or range, which "
                 "often continues up to the extractor and can double that section's height. Add "
                 "each rectangle's area separately.\n\n"
                 "Do not subtract the outlets and switches. The tile that comes out of those cutouts "
                 "is waste, and the cuts are exactly where tiles break. Measuring the gross area and "
                 "adding the waste allowance already accounts for them honestly."),
                ("Why Backsplash Waste Runs High",
                 "On a floor, a 10% allowance covers cuts because most tiles go down whole. A "
                 "backsplash is mostly edges: the top and bottom rows are often cut to fit the "
                 "cabinet line, every outlet needs a notched tile, and corners break the pattern. "
                 "Fifteen percent is the realistic floor for a straight subway layout.\n\n"
                 "Herringbone and diagonal layouts cut nearly every boundary tile, so allow 20%. "
                 "Mosaic sheets waste less on cuts but more on partial sheets at the edges; 15% "
                 "still applies. Leftover tiles are cheap insurance for a cracked tile in five "
                 "years, when the batch is no longer sold."),
                ("Tile Size Changes the Count, Not the Area",
                 "The area is fixed at 15 sq ft; the count is not. With 3 x 6 in subway tiles at "
                 "8 per sq ft, the job is 120 tiles before waste. With 2 x 4 in tiles it doubles "
                 "to 240. With large 12 x 24 in tiles it falls to about 8 tiles, but a single "
                 "breakage then wipes out your whole waste allowance.\n\n"
                 "Buy by the box and round the box count up, never down. Boxes of subway tile "
                 "commonly cover 5 to 12 sq ft; check the coverage printed on the box rather than "
                 "the tile count, because grout joints mean real coverage is slightly less than the "
                 "bare arithmetic."),
                ("Layout Choices That Change the Count",
                 "Where you start tiling decides how many tiles get cut. Starting from the centre of "
                 "the main run leaves equal part-tiles at both ends, which looks best on a long "
                 "symmetrical wall but cuts two tiles per row. Starting from the most visible corner "
                 "keeps full tiles where the eye lands first and pushes the cuts into the far corner, "
                 "which usually wastes less.\n\n"
                 "Grout width plays a small part too. The calculator counts tiles at their bare "
                 "dimensions; with a standard 2 to 3 mm joint, real coverage per tile creeps up "
                 "slightly, which quietly absorbs a tile or two of the waste allowance on a small "
                 "backsplash. It is a bonus, not a reason to order less."),
                ("What the Tile Count Does Not Include",
                 "The calculator counts tiles. The job also needs: adhesive (a small backsplash "
                 "uses roughly one small bag or tub per 15 to 20 sq ft), grout (one small bag is "
                 "plenty for most kitchens), trim or edging strip for the exposed edges, and "
                 "silicone where the tile meets the worktop — never grout that joint, because it "
                 "needs to flex.\n\n"
                 "If the wall behind is painted plaster in good condition, you can tile straight "
                 "onto it after a primer. Over old tiles or damaged plaster, a backer board adds "
                 "thickness that changes how the run meets the cabinets, so decide before you "
                 "measure the height."),
            ],
        ),
    },
]
