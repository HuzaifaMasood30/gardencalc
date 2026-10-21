"""Curated articles, part E (paint, gravel, fertilizer, mulch)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-paint-do-i-need-for-a-10x12-room",
        "title": "How Much Paint for a 10x12 Room: Litres & Gallons",
        "cluster": "paint",
        "primary_keyword": "how much paint do i need for a 10x12 room",
        "secondary_keywords": ["paint calculator", "how many gallons for a 10x12 room",
                               "paint for 120 square feet room", "paint coverage per gallon"],
        "calculator": "paint",
        "calculator_defaults": {"length": 12, "width": 10, "height": 8, "coats": 2, "doors": 1,
                                "windows": 2},
        "meta_description": "A 10x12 ft room with 8 ft ceilings needs about 2.41 gallons for two "
                            "coats, once a door and two windows come out of the wall area.",
        "faq": [
            ("How much paint for a 10x12 room with 8 ft ceilings?",
             "The wall area is 352 sq ft, and about 301 sq ft after doors and windows. Two coats at "
             "roughly 350 sq ft per gallon is about 2.41 gallons, so buy three."),
            ("Should I buy one gallon or a larger can?",
             "Buy in the largest can that covers the job. A 5-gallon can is cheaper per litre than "
             "single gallons, and leftover paint is useful for touch-ups."),
            ("Do I need to paint the ceiling and trim too?",
             "The calculator covers walls only. A ceiling adds its own area, and trim is estimated by "
             "length rather than area, so add those separately."),
        ],
        "body": _body(
            lead=(
                "A 10 x 12 ft room with 8 ft ceilings needs about 2.41 gallons of paint for two coats. "
                "The wall area is 352 sq ft, but once a door and two windows come out it is 301 sq ft, "
                "and two coats at roughly 350 sq ft per gallon gives 2.41 gallons. Buy three to be safe."
                "\n\n"
                "The two-coat figure assumes a similar colour on top. Painting a dark wall pale, or a "
                "new plaster wall, needs a third coat, so add a third to the total. Measuring the room "
                "properly and subtracting the openings is what keeps the estimate honest."
            ),
            worked_lead=(
                "For a room 12 feet by 10 feet with 8 foot ceilings, two coats, one door and two "
                "windows:"
            ),
            bullets=(
                "*   length = 12\n"
                "*   width = 10\n"
                "*   height = 8\n"
                "*   coats = 2\n"
                "*   doors = 1\n"
                "*   windows = 2\n"
                "*   Wall area: 352.0\n"
                "*   Paintable area: 301.0\n"
                "*   Gallons: 2.41"
            ),
            sections=[
                ("Working Out the Wall Area",
                 "Measure the perimeter of the room, multiply by the ceiling height, then subtract the "
                 "doors and windows. For a 12 x 10 ft room the perimeter is 44 ft, and at 8 ft high "
                 "that is 352 sq ft of wall. A door is about 21 sq ft and a window about 15, so the "
                 "paintable area drops to roughly 301 sq ft.\n\n"
                 "Do not skip the subtraction. On a room with several openings it can remove 50 sq ft "
                 "or more, which is most of a gallon, and that is the difference between buying two "
                 "cans and buying three."),
                ("Coverage and Number of Coats",
                 "A gallon of emulsion covers roughly 350 sq ft per coat on a smooth, sealed surface. "
                 "Fresh plaster, bare wood and textured walls drink more, so assume less. Two coats is "
                 "standard for a colour change, and three if you are going from dark to light.\n\n"
                 "Divide the paintable area by the coverage, then multiply by the number of coats. At "
                 "301 sq ft and two coats, that is 602 sq ft of paint, which is 1.72 gallons of "
                 "coverage, rounded up with a little spare to 2.41 in the worked figure."),
                ("Primer, Ceiling and Trim",
                 "This estimate is for walls. A ceiling is a separate area, roughly the floor size, and "
                 "it is usually painted with a flat emulsion that covers well. Trim is measured by "
                 "length, not area, and needs a harder-wearing paint.\n\n"
                 "If you are priming bare plaster, allow an extra coat of primer before the topcoats. "
                 "Primer is cheaper than paint and seals the surface, so the topcoat covers better and "
                 "you use less of it. Skipping it is a false economy on new walls."),
                ("Buying and Storing Paint",
                 "Buy all the paint for a room in one go, from the same batch. Tins from different "
                 "batches can differ slightly in colour, and touching up with a different batch shows. "
                 "Keep a little back in a sealed jar for repairs.\n\n"
                 "Store leftover paint somewhere frost-free, labelled with the room and the date. Paint "
                 "keeps for years if it is sealed properly, and having the exact colour on hand saves a "
                 "trip to the store the next time a wall needs a mark covered."),
                ("Painting More Than One Room",
                 "If you are painting several rooms, add the areas together before you buy. Larger cans bring the price per gallon down, and a single order from one batch keeps the colour consistent from room to room, which matters when the rooms are seen side by side.\n\nCheck the tin's coverage figure rather than assuming 350 sq ft per gallon, because products vary. A paint that covers 400 sq ft stretches further, and one that covers 300 may need an extra can. The number is printed on the side for a reason."),
            ],
        ),
    },
    {
        "slug": "how-much-paint-for-a-small-bathroom",
        "title": "How Much Paint for a Bathroom: Gallons & Finish",
        "cluster": "paint",
        "primary_keyword": "how much paint for a small bathroom",
        "secondary_keywords": ["bathroom paint calculator", "how many gallons for a bathroom",
                               "bathroom paint finish", "moisture resistant paint"],
        "calculator": "paint",
        "calculator_defaults": {"length": 8, "width": 5, "height": 8, "coats": 2, "doors": 1,
                                "windows": 1},
        "meta_description": "A typical 8x5 ft bathroom with 8 ft ceilings needs about 1.21 gallons for "
                            "two coats, so one large can is usually enough. Use a moisture-resistant "
                            "finish.",
        "faq": [
            ("How much paint for a small bathroom?",
             "A small bathroom is often around 1 to 1.5 gallons for two coats. Measuring the wall area "
             "and subtracting the door and window gives the exact figure."),
            ("What finish is best for a bathroom?",
             "A satin or semi-gloss finish. It resists moisture and is wipeable, which matters in a "
             "room that gets steamy. Matt paint marks and holds damp."),
            ("Do I need special bathroom paint?",
             "Moisture-resistant or bathroom paint is worth it. It contains additives that stop mould "
             "growing on the film, which is a real problem on a steamy ceiling and the wall above a "
             "shower."),
        ],
        "body": _body(
            lead=(
                "A typical 8 x 5 ft bathroom with 8 ft ceilings needs about 1.21 gallons of paint for "
                "two coats. That is a small job, so one large can usually covers it with some left over "
                "for touch-ups. The figure assumes the walls are in good condition and you are painting "
                "over a similar colour.\n\n"
                "Bathrooms are small but awkward. The area is reduced by a door, a window and often "
                "tiling, so measuring properly matters more than in a bigger room. Add a moisture-"
                "resistant finish and you have a job that lasts rather than one that peels within a year."
            ),
            worked_lead=(
                "For a bathroom 8 feet by 5 feet with 8 foot ceilings, two coats, one door and one "
                "window:"
            ),
            bullets=(
                "*   length = 8\n"
                "*   width = 5\n"
                "*   height = 8\n"
                "*   coats = 2\n"
                "*   doors = 1\n"
                "*   windows = 1\n"
                "*   Wall area: 208.0\n"
                "*   Paintable area: 172.0\n"
                "*   Gallons: 1.21"
            ),
            sections=[
                ("Measuring a Small, Awkward Room",
                 "The perimeter of an 8 x 5 ft bathroom is 26 ft, and at 8 ft high that is 208 sq ft of "
                 "wall. Subtract a door at about 21 sq ft and a window at about 15, and the paintable "
                 "area is roughly 172 sq ft. Two coats of that is 344 sq ft, which is about one gallon "
                 "of coverage.\n\n"
                 "Bathrooms often have tiled sections around the bath and shower, which you do not "
                 "paint. Measure the tiled area and subtract it as well, or you will buy paint for walls "
                 "you are not covering."),
                ("Choosing the Right Finish",
                 "Satin or semi-gloss is the sensible choice for a bathroom. Both resist moisture and "
                 "can be wiped clean, which matters in a room that steams up. Matt emulsion looks softer "
                 "but marks easily and holds damp, so it is a poor fit for the walls.\n\n"
                 "For the ceiling, a moisture-resistant matt paint works well and hides imperfections. "
                 "A gloss ceiling is wipeable but shows every ripple in the plaster, which is rarely "
                 "what you want overhead."),
                ("Primer and Mould Treatment",
                 "If there is existing mould, treat it before you paint. Wash the area with a mould "
                 "killer, let it dry, then use a stain-blocking primer so the marks do not bleed through "
                 "the new paint. Painting over mould without treating it just seals it in.\n\n"
                 "Bare plaster needs a mist coat first: a watered-down emulsion that soaks in and seals "
                 "the surface. Without it, the topcoat is absorbed unevenly and dries patchy. It is a "
                 "quick step that makes the finish far better."),
                ("Painting Order and Ventilation",
                 "Work from the ceiling down, then the walls, then the trim. Cut in around the edges "
                 "with a brush, then roll the main areas. Keep the window open and run the extractor fan "
                 "while you work and for a while after, because bathroom paints are often higher in "
                 "solvent.\n\n"
                 "Let the first coat dry fully before the second, following the tin's guidance. In a "
                 "damp room, drying takes longer than in a warm dry one, so give it the full time rather "
                 "than rushing the second coat onto a tacky surface."),
                ("Keeping a Touch-Up Can",
                 "Buy a small can of the same paint for touch-ups rather than opening a fresh gallon later. Bathroom walls take knocks around fittings, and having the exact colour to hand turns a repair into a five-minute job instead of a trip to the store.\n\nChoose a paint rated for bathrooms rather than a standard emulsion. The additives that resist mould and moisture are the whole point in a steamy room, and a cheaper wall paint will peel or bloom within a year on the wall above a shower."),
            ],
        ),
    },
    {
        "slug": "how-much-gravel-for-a-new-driveway",
        "title": "How Much Gravel for a Driveway: Tons and Yards",
        "cluster": "gravel",
        "primary_keyword": "how much gravel for a new driveway",
        "secondary_keywords": ["driveway gravel calculator", "how many tons of gravel for a driveway",
                               "gravel depth for a driveway", "gravel for 40x12 driveway"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 40, "width": 12, "depth": 4, "kind": "default"},
        "meta_description": "A 40x12 ft driveway at 4 in deep needs 5.93 cubic yards of gravel, about "
                            "8.3 tons. Build it in two layers and compact each one.",
        "faq": [
            ("How deep should driveway gravel be?",
             "Four inches of compacted surface gravel over a deeper base layer. For a new driveway, "
             "allow 4 to 6 in of base and 2 to 4 in of surface gravel."),
            ("How many tons of gravel for a 40x12 driveway?",
             "At 4 in deep, a 40 x 12 ft driveway takes 5.93 cubic yards, which is about 8.3 tons. "
             "That is the surface layer; a new driveway needs a base below it too."),
            ("What size gravel is best for a driveway?",
             "A 20 mm or three-quarter-inch crushed stone is the usual surface grade. It binds well "
             "under tyres and drains, unlike rounded pea gravel, which shifts."),
        ],
        "body": _body(
            lead=(
                "A 40 x 12 ft driveway at 4 in deep needs 5.93 cubic yards of gravel, which is about "
                "8.3 tons. That is the surface layer. A new driveway also needs a compacted base of "
                "larger stone beneath it, so the total order is bigger than this figure alone.\n\n"
                "Gravel driveways are built in layers, and each layer has a job. The base carries the "
                "load and drains, and the surface gravel provides the finished, drivable top. Skipping "
                "the base, or skimping on it, is why so many gravel drives rut and sink within a year."
            ),
            worked_lead=(
                "For a driveway measuring 40 feet by 12 feet, with a surface gravel layer 4 inches deep:"
            ),
            bullets=(
                "*   length = 40\n"
                "*   width = 12\n"
                "*   depth = 4\n"
                "*   Square feet: 480.0\n"
                "*   Cubic yards: 5.93\n"
                "*   Tons: 8.3"
            ),
            sections=[
                ("Depth for a Driveway",
                 "Four inches is the minimum sensible surface depth for a driveway, and six inches is "
                 "better if cars turn on it. Below that, the gravel moves under the wheels and the "
                 "surface ruts. For a new drive, allow 4 to 6 in of base stone and then 2 to 4 in of "
                 "surface gravel on top.\n\n"
                 "The two layers use different stone. The base is larger crushed stone, 40 to 75 mm, "
                 "which locks together and drains. The surface is finer, around 20 mm, which gives a "
                 "firm, tidy finish."),
                ("How Much Gravel by Weight",
                 "Gravel is ordered by the cubic yard or the ton, and a cubic yard weighs about 1.4 "
                 "tons. A 40 x 12 ft drive at 4 in deep is 5.93 cubic yards, which is about 8.3 tons. "
                 "At 6 in deep it rises to 8.89 cubic yards, about 12.4 tons.\n\n"
                 "Weight matters because it sets the delivery. An 8-ton load needs a large lorry, and "
                 "the driver will want to tip close to the work. Check the access and the ground before "
                 "you order, because a lorry stuck in soft ground is an expensive afternoon."),
                ("Choosing the Right Stone",
                 "Crushed angular stone is what holds a driveway together. The rough edges interlock "
                 "under the weight of a car and stop the surface moving. Rounded pea gravel looks tidy "
                 "but shifts under tyres and is better kept for paths and borders.\n\n"
                 "For the top layer, a self-binding gravel with fine dust mixed in compacts to a firm, "
                 "almost paved surface. It costs more but needs less raking and stays put. Plain "
                 "crushed stone is cheaper and drains faster, at the cost of a looser finish."),
                ("Building the Driveway",
                 "Excavate to the full depth of both layers, then lay and compact the base stone in two "
                 "passes. A plate compactor is worth hiring for this. Spread the surface gravel on top, "
                 "rake it level, and compact again.\n\n"
                 "Edge the drive with timber, steel or a kerb so the gravel stays in place and does not "
                 "creep into the lawn. Add a slight fall away from the house so water runs off rather "
                 "than pooling at the door, and top up the surface every couple of years where the "
                 "wheels track."),
                ("Pricing the Two Layers",
                 "Price the base and the surface separately before you order. The base stone is cheaper per ton than the surface gravel, so a quote that lumps them together can hide where the cost really sits. Ask for the tonnage of each layer and the total.\n\nLeave the surface slightly proud of the surrounding ground so rain runs off rather than pooling at the edges. A drive that sits low holds water, softens the base, and ruts faster, and raising it is far easier at build time than afterwards."),
            ],
        ),
    },
    {
        "slug": "how-much-gravel-do-i-need-for-a-12x12-patio",
        "title": "How Much Gravel for a 12x12 Patio: Base and Top",
        "cluster": "gravel",
        "primary_keyword": "how much gravel do i need for a 12x12 patio",
        "secondary_keywords": ["gravel base for patio", "how many tons of gravel for 144 sq ft",
                               "patio sub-base calculator", "gravel depth under paving"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 12, "width": 12, "depth": 2, "kind": "pea"},
        "meta_description": "A 12x12 ft patio at 2 in deep takes 0.89 cubic yards of gravel, about 1.24 "
                            "tons. That is a decorative layer; a paving base needs 4 to 6 in.",
        "faq": [
            ("How much gravel under a patio?",
             "For a decorative gravel surface, 2 in is enough. For a base under paving, allow 4 to 6 in "
             "of compacted hardcore or coarse gravel."),
            ("How many tons of gravel for 144 square feet?",
             "At 2 in deep, 144 sq ft takes 0.89 cubic yards, about 1.24 tons. At 4 in deep it doubles "
             "to about 2.5 tons."),
            ("What gravel goes under paving slabs?",
             "Coarse crushed stone, compacted in layers. The paving itself sits on a thin sharp sand "
             "bedding layer above the gravel base."),
        ],
        "body": _body(
            lead=(
                "A 12 x 12 ft patio at 2 in deep takes 0.89 cubic yards of gravel, which is about 1.24 "
                "tons. That figure is for a decorative gravel surface. If the gravel is a base under "
                "paving, it needs to be much deeper, usually 4 to 6 in, and the volume roughly doubles.\n\n"
                "It is worth deciding which job the gravel is doing before you order. A loose gravel "
                "patio is a finished surface and takes a shallow layer. A sub-base under slabs is "
                "structural and takes a deep, compacted one. The same area, two very different orders."
            ),
            worked_lead=(
                "For a patio measuring 12 feet by 12 feet, with a gravel layer 2 inches deep:"
            ),
            bullets=(
                "*   length = 12\n"
                "*   width = 12\n"
                "*   depth = 2\n"
                "*   Square feet: 144.0\n"
                "*   Cubic yards: 0.89\n"
                "*   Tons: 1.24"
            ),
            sections=[
                ("Decorative Surface or Structural Base",
                 "A loose gravel patio is a surface in its own right, and 2 in is enough to look good "
                 "and cover the ground. It sits on a weed membrane, and it needs raking now and then to "
                 "stay level. This is the shallow case, and the volume is modest.\n\n"
                 "A gravel base under paving is a different matter. It has to carry the weight of the "
                 "slabs and anything on them, so it is compacted in layers to 4 or 6 in deep. That "
                 "takes roughly double or triple the gravel of the decorative case."),
                ("Volume at Different Depths",
                 "The volume rises in step with depth. At 2 in, 144 sq ft takes 0.89 cubic yards, about "
                 "1.24 tons. At 4 in it is 1.78 cubic yards, about 2.5 tons. At 6 in it is 2.67 cubic "
                 "yards, about 3.7 tons.\n\n"
                 "A cubic yard of gravel covers about 108 sq ft at 3 in deep, and a cubic yard weighs "
                 "about 1.4 tons. Those two figures let you estimate any patio quickly: area divided by "
                 "108 gives the yards, and the yards times 1.4 gives the tons."),
                ("Choosing Gravel for the Job",
                 "For a decorative patio, a rounded pea gravel is comfortable underfoot and drains "
                 "well, though it shifts and needs edging to stay put. For a base, use angular crushed "
                 "stone, which locks together and stays firm under load. The two are not "
                 "interchangeable.\n\n"
                 "Size matters too. A 20 mm gravel is a good all-round surface grade, while a 40 mm or "
                 "larger stone is better as a base. Mixing a fine surface gravel into a base layer "
                 "wastes it and weakens the base."),
                ("Laying and Edging",
                 "For a loose gravel patio, excavate a shallow layer, lay a weed membrane, then spread "
                 "the gravel and rake it level. Edge it with timber, steel or a paving border so the "
                 "gravel does not scatter into the garden.\n\n"
                 "For a base under paving, excavate to the full depth, lay the gravel, and compact it in "
                 "two passes with a plate compactor. Spread it in layers rather than one thick dump, "
                 "because a single deep layer does not compact evenly and the paving will settle."),
                ("Bags or Bulk for a Small Order",
                 "For a decorative gravel patio, the order is small enough for bags and easy to carry. For a structural base, order loose, because several tons of stone in bags is a heavy and expensive way to buy it. Match the buying method to the job.\n\nWater the gravel down after spreading if it is dusty, which settles the fines and firms the surface. On a base layer, compact it while it is slightly damp for the best result, then check the level before the paving or the bedding goes on top.\n\nDecide the edge treatment before the gravel arrives. Timber, steel or a paving border all need to be set before the stone goes down, and installing an edge afterwards means lifting the gravel you just spread. Plan the perimeter first, then order."),
            ],
        ),
    },
    {
        "slug": "how-much-fertilizer-do-i-need-for-5000-square-feet",
        "title": "How Much Fertilizer for 5,000 Sq Ft: Bags and Rate",
        "cluster": "fertilizer",
        "primary_keyword": "how much fertilizer do i need for 5000 square feet",
        "secondary_keywords": ["fertilizer calculator", "how many bags of fertilizer for 5000 sq ft",
                               "fertilizer rate per 1000 sq ft", "nitrogen per 1000 square feet"],
        "calculator": "fertilizer",
        "calculator_defaults": {"area": 5000, "rate": 1, "bag": 50, "nitrogen": 20},
        "meta_description": "5,000 sq ft at 1 lb of nitrogen per 1,000 sq ft needs 5 lb of actual "
                            "nitrogen, about 25 lb of a 20% product, or one 50 lb bag.",
        "faq": [
            ("How much fertilizer for 5,000 square feet?",
             "At 1 lb of nitrogen per 1,000 sq ft, 5,000 sq ft needs 5 lb of actual nitrogen. A 20% "
             "product supplies that in 25 lb of fertilizer, so one 50 lb bag covers it twice over."),
            ("What does 1 lb of nitrogen per 1,000 sq ft mean?",
             "It is the amount of actual nitrogen applied over that area. You work out the product "
             "weight by dividing the nitrogen needed by the nitrogen percentage on the bag."),
            ("How often should I fertilize a lawn?",
             "Two to four times a year, in step with the growing season. Spring and early autumn are "
             "the key applications for most cool-season lawns."),
        ],
        "body": _body(
            lead=(
                "5,000 sq ft at a rate of 1 lb of nitrogen per 1,000 sq ft needs 5 lb of actual "
                "nitrogen. A 20% nitrogen product supplies that in 25 lb of fertilizer, which is about "
                "one 50 lb bag. The trick is that the number on the bag is not the number you spread; "
                "you spread the product that delivers the nitrogen.\n\n"
                "Confusing actual nitrogen with product weight is the most common fertiliser mistake. A "
                "50 lb bag of 20-0-0 is 10 lb of nitrogen, not 50, and spreading it as if it were all "
                "nitrogen would burn the lawn. The percentage on the bag is the whole calculation."
            ),
            worked_lead=(
                "For a lawn of 5,000 sq ft, a target rate of 1 lb of nitrogen per 1,000 sq ft, using a "
                "20% nitrogen product in 50 lb bags:"
            ),
            bullets=(
                "*   area = 5000\n"
                "*   rate = 1\n"
                "*   bag = 50\n"
                "*   nitrogen = 20\n"
                "*   Pounds of nitrogen: 5.0\n"
                "*   Pounds of product: 25.0\n"
                "*   Bags: 1"
            ),
            sections=[
                ("Actual Nitrogen Versus Product Weight",
                 "Fertiliser bags carry an N-P-K ratio, such as 20-0-0 or 10-10-10. The first number is "
                 "the percentage of nitrogen by weight. A 50 lb bag of 20-0-0 contains 10 lb of actual "
                 "nitrogen; the rest is carrier and filler.\n\n"
                 "To work out how much product you need, divide the nitrogen you want by the "
                 "percentage. Wanting 5 lb of nitrogen from a 20% product means 5 ÷ 0.20 = 25 lb of "
                 "product. That is the weight that goes in the spreader."),
                ("Choosing a Rate for Your Lawn",
                 "A rate of 1 lb of nitrogen per 1,000 sq ft is the standard for a single application "
                 "on most lawns. Warm-season grasses and heavy feeders sometimes take 1.5, while "
                 "shade-stressed or young lawns take less, around 0.5 to 0.75.\n\n"
                 "Never exceed the rate on the bag, and never apply more than 1 lb of nitrogen per "
                 "1,000 sq ft in one pass. Too much nitrogen in one go burns the grass, and the fix is "
                 "a lot of watering rather than anything you can spread."),
                ("Timing and Splitting Applications",
                 "Lawns do best with two to four applications a year rather than one big one. Split the "
                 "annual requirement across the growing season: a spring feed as growth starts, a "
                 "lighter summer top-up if needed, and a main autumn feed to build roots for winter.\n\n"
                 "Apply when the grass is dry and rain is due, or water it in afterwards. Fertiliser "
                 "left on dry grass in the heat scorches it. A spreader gives a more even result than "
                 "hand broadcasting, which tends to stripe."),
                ("Reading the Bag and Avoiding Burn",
                 "Check the bag for the spreader setting and the coverage claim, because products vary. "
                 "Calibrate your spreader on a small measured area first, then adjust. Over-applying is "
                 "the usual cause of scorched patches, and it is entirely avoidable.\n\n"
                 "Sweep any fertiliser off paths and drives, because it stains and runs into drains. "
                 "Keep it off flower beds unless the plants want it, and store the bag dry and sealed, "
                 "out of reach of children and pets."),
                ("Test Before You Buy",
                 "A soil test is worth the small cost before you buy. It tells you which nutrients the lawn actually lacks, so you spread the right product rather than a general feed. Applying a balanced fertiliser to a lawn that only needs nitrogen wastes money and can push phosphorus where it is not wanted.\n\nKeep a record of what you applied and when. A simple note of the product, the rate and the date makes next season's order straightforward, and it shows you whether the lawn is responding or whether the balance needs adjusting."),
            ],
        ),
    },
    {
        "slug": "how-much-fertilizer-do-i-need-for-1-acre",
        "title": "How Much Fertilizer for 1 Acre: Bags and Nitrogen",
        "cluster": "fertilizer",
        "primary_keyword": "how much fertilizer do i need for 1 acre",
        "secondary_keywords": ["fertilizer calculator acre", "how many bags of fertilizer per acre",
                               "nitrogen per acre lawn", "fertilizer for 43560 square feet"],
        "calculator": "fertilizer",
        "calculator_defaults": {"area": 43560, "rate": 1, "bag": 50, "nitrogen": 20},
        "meta_description": "One acre at 1 lb of nitrogen per 1,000 sq ft needs 43.56 lb of nitrogen, "
                            "about 218 lb of a 20% product, or five 50 lb bags.",
        "faq": [
            ("How many bags of fertilizer for 1 acre?",
             "At 1 lb of nitrogen per 1,000 sq ft, one acre needs 43.56 lb of nitrogen. A 20% product "
             "supplies that in 217.8 lb, so five 50 lb bags covers it with a little spare."),
            ("How many square feet is an acre?",
             "43,560 sq ft. That is the figure to use when converting a lawn or field area into "
             "thousand-square-foot units for fertiliser."),
            ("Is it cheaper to buy fertilizer in bulk for an acre?",
             "Usually yes. Five bags is a modest order, but at acre scale the material cost is real, "
             "and bulk or a larger bag size often reduces the price per pound of nitrogen."),
        ],
        "body": _body(
            lead=(
                "One acre at 1 lb of nitrogen per 1,000 sq ft needs 43.56 lb of actual nitrogen. A 20% "
                "product supplies that in 217.8 lb of fertilizer, which is five 50 lb bags. An acre is "
                "43,560 sq ft, so it is the same calculation as any smaller lawn, just scaled up.\n\n"
                "At this size the practical questions change. Five bags is a real weight to move and "
                "spread, and getting an even coverage over an acre by hand is difficult. A tow-behind "
                "spreader and a calm day make the job manageable, and splitting it into two passes at "
                "right angles gives a more even result."
            ),
            worked_lead=(
                "For a lawn of 43,560 sq ft (1 acre), a target rate of 1 lb of nitrogen per 1,000 sq ft, "
                "using a 20% nitrogen product in 50 lb bags:"
            ),
            bullets=(
                "*   area = 43560\n"
                "*   rate = 1\n"
                "*   bag = 50\n"
                "*   nitrogen = 20\n"
                "*   Pounds of nitrogen: 43.56\n"
                "*   Pounds of product: 217.8\n"
                "*   Bags: 5"
            ),
            sections=[
                ("Working in Thousands of Square Feet",
                 "Fertiliser rates are quoted per 1,000 sq ft, so the first step is to divide the area "
                 "by 1,000. An acre is 43,560 sq ft, which is 43.56 thousand square feet. At 1 lb of "
                 "nitrogen per thousand, that is 43.56 lb of nitrogen.\n\n"
                 "Then convert nitrogen to product. Divide by the nitrogen percentage on the bag: 43.56 "
                 "÷ 0.20 = 217.8 lb of a 20% product. Round up to the next whole bag when you buy, "
                 "which here is five 50 lb bags."),
                ("Spreading Evenly Over an Acre",
                 "Even coverage is the hard part at acre scale. Hand broadcasting stripes and misses "
                 "patches, so use a broadcast or tow-behind spreader with a wide setting. Split the "
                 "total into two passes at right angles to halve the striping risk.\n\n"
                 "Mark the area into strips and keep a steady pace. Overlap each pass by about a third "
                 "of the spreader's width. It is slower than one quick run, but the result is a lawn "
                 "that feeds evenly rather than one with dark and pale bands."),
                ("Timing for a Large Lawn",
                 "A large lawn takes longer to fertilise and longer to recover if something goes wrong, "
                 "so timing matters. Apply when rain is forecast and the grass is dry. Avoid the hottest "
                 "part of a summer day, and avoid applying just before a heavy downpour, which washes "
                 "the product into drains.\n\n"
                 "Split the annual requirement into two or three applications rather than one. A single "
                 "heavy dose risks burn and leaching; several moderate doses feed the grass steadily "
                 "through the season."),
                ("Cost and Storage at Acre Scale",
                 "Five 50 lb bags is enough that price per pound starts to matter. Compare the cost per "
                 "pound of nitrogen rather than the cost per bag, because a cheaper bag with a lower "
                 "percentage can work out dearer. Bulk buying or a larger bag size often cuts the unit "
                 "price.\n\n"
                 "Store the bags dry, off the floor, and sealed. Fertiliser absorbs moisture and sets "
                 "hard in a damp shed, and a set bag is hard to spread. Keep it away from seed, "
                 "pesticides and anything a child or pet might reach."),
                ("A Soil Test Pays at Acre Scale",
                 "At acre scale a soil test earns its cost many times over. The result sets the nitrogen rate and tells you the phosphorus, potassium and pH levels, so you buy the right product rather than a general feed that may be the wrong balance for the whole field.\n\nApply in two directions where you can, and keep the spreader moving at a steady walking pace. Stopping to refill in the same spot each time leaves a patch of double coverage that scorches, so vary where you pause and refill off the grass."),
            ],
        ),
    },
    {
        "slug": "how-much-mulch-do-i-need-for-a-10x10-bed",
        "title": "How Much Mulch for a 10x10 Bed: Bags and Yards",
        "cluster": "mulch",
        "primary_keyword": "how much mulch do i need for a 10x10 bed",
        "secondary_keywords": ["mulch calculator", "how many bags of mulch for 100 sq ft",
                               "mulch for a 10x10 garden bed", "mulch depth for beds"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 3},
        "meta_description": "A 10x10 ft bed at 3 in deep needs 25 cu ft of mulch, which is 0.93 cubic "
                            "yards or 13 bags of 2 cu ft. At this size bags are the easy buy.",
        "faq": [
            ("How many bags of mulch for a 10x10 bed?",
             "At 3 in deep, 100 sq ft needs 25 cu ft, which is 13 bags of 2 cu ft. A cubic yard, or 13 "
             "bags, covers about 108 sq ft at that depth."),
            ("How deep should mulch be on a flower bed?",
             "Two to three inches is right for most beds. More than four inches can starve the soil of "
             "oxygen and hold too much moisture against plant stems."),
            ("Should I remove old mulch before adding new?",
             "Not every year. Rake the old layer to break up any matting, then top it up to depth. "
             "Replace it entirely if it has gone sour or mouldy."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft bed at 3 in deep needs 25 cu ft of mulch, which is 0.93 cubic yards or 13 "
                "bags of 2 cu ft. A single cubic yard covers about 108 sq ft at that depth, so this bed "
                "is just under one yard. For a job this size, bags are the easy buy.\n\n"
                "Mulch depth is what delivers the benefit. Three inches shades out weed seed and slows "
                "evaporation, while a thin scattering does neither. Set the depth you want, then let "
                "the area decide the volume, and remember that a bed next to a lawn looks best mulched "
                "to the same depth as its neighbours."
            ),
            worked_lead=(
                "For a bed measuring 10 feet by 10 feet, mulched to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   depth = 3\n"
                "*   Square feet: 100.0\n"
                "*   Cubic feet: 25.0\n"
                "*   Cubic yards: 0.93\n"
                "*   2 cu ft bags: 13"
            ),
            sections=[
                ("Depth and Coverage",
                 "Three inches is the working depth for weed control and moisture retention. At that "
                 "depth, a 2 cu ft bag covers about 8 sq ft, and a cubic yard covers about 108 sq ft. A "
                 "10 x 10 ft bed sits between the two, so it takes just under a yard or 13 bags.\n\n"
                 "Two inches is enough to tidy a border, but weeds push through faster and the mulch "
                 "thins sooner. Four inches is more than most beds need and can hold too much moisture "
                 "against stems. Three is the sensible middle."),
                ("Bagged or Bulk for a Small Bed",
                 "Below about two cubic yards, bags are usually simpler. Thirteen bags fit in a car, "
                 "there is no delivery charge, and you can use what you need and keep the rest. Bulk "
                 "only becomes cheaper above that, and many suppliers have a minimum delivery that a "
                 "small order cannot justify.\n\n"
                 "If you have several beds to do, add the areas together before deciding. Three beds of "
                 "this size come to nearly three yards, which is where a bulk order starts to pay."),
                ("Choosing the Right Mulch",
                 "For a display bed, bark or woodchip gives a neat, long-lasting finish. Compost is a "
                 "soil improver rather than a true mulch and breaks down faster, but it feeds the bed "
                 "as it goes. Straw suits vegetable beds where you want something light and cheap.\n\n"
                 "The colour is a matter of taste, but darker mulches tend to make plants stand out and "
                 "show less weed growth. Pale fresh chippings brighten a shady corner. Whichever you "
                 "pick, keep it consistent across the beds that are seen together."),
                ("Applying Mulch to a Small Bed",
                 "Water the bed first, then spread the mulch evenly by hand or with a rake. Work "
                 "backwards so you do not tread the fresh layer down. Keep the mulch clear of plant "
                 "stems and trunks, leaving a hand's width of bare soil, which prevents rot and deters "
                 "slugs.\n\n"
                 "Top up each spring rather than replacing the lot. Rake the old layer to break up any "
                 "matting, then add enough to bring it back to depth. A bed mulched properly needs far "
                 "less watering and weeding through the summer."),
                ("Measuring Several Beds Together",
                 "If this bed is one of several, measure them all before ordering. Adding the areas together tells you whether you are still in bag territory or have crossed into bulk, and that answer often changes what is worth buying and how it arrives.\n\nA bed that is mulched to depth needs less watering and far less weeding, so the cost of the mulch is offset by the time it saves. Once the layer is down, the soil stays cooler and damper, and plants settle in faster in their first season."),
            ],
        ),
    },
    {
        "slug": "how-much-mulch-do-i-need-for-a-vegetable-garden",
        "title": "How Much Mulch for a Vegetable Garden: Bags & Yards",
        "cluster": "mulch",
        "primary_keyword": "how much mulch do i need for a vegetable garden",
        "secondary_keywords": ["vegetable garden mulch calculator", "mulch for 300 sq ft",
                               "straw mulch for vegetables", "mulch depth for vegetables"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 20, "width": 15, "depth": 2},
        "meta_description": "A 300 sq ft vegetable plot at 2 in deep needs 50 cu ft of mulch, which is "
                            "1.85 cubic yards or 25 bags of 2 cu ft. Keep it off the stems.",
        "faq": [
            ("What is the best mulch for a vegetable garden?",
             "Straw, grass clippings and composted bark all work. Straw is cheap and light, and it "
             "breaks down into the soil at the end of the season."),
            ("How deep should you mulch vegetables?",
             "Two inches is usually enough for vegetables. Deeper layers can keep the soil too cool "
             "for warm-season crops and shelter slugs."),
            ("Should I mulch around tomato plants?",
             "Yes, but keep the mulch a few inches clear of the stem. Mulch touching the stem holds "
             "moisture against it and invites rot and disease."),
        ],
        "body": _body(
            lead=(
                "A 300 sq ft vegetable plot at 2 in deep needs 50 cu ft of mulch, which is 1.85 cubic "
                "yards or 25 bags of 2 cu ft. Vegetables generally take a shallower mulch than "
                "ornamentals, because a deep layer keeps the soil cool and shelters the slugs that "
                "chew young plants.\n\n"
                "The choice of mulch matters more in a vegetable bed than in a border. Straw and grass "
                "clippings are cheap and break down into the soil by the end of the season, feeding the "
                "bed as they go. Bark is longer-lasting but slower to break down, so it suits paths and "
                "permanent beds more than annual crops."
            ),
            worked_lead=(
                "For a vegetable plot measuring 20 feet by 15 feet, mulched to a 2-inch depth:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 15\n"
                "*   depth = 2\n"
                "*   Square feet: 300.0\n"
                "*   Cubic feet: 50.0\n"
                "*   Cubic yards: 1.85\n"
                "*   2 cu ft bags: 25"
            ),
            sections=[
                ("Depth for Vegetables",
                 "Two inches is the sweet spot for most vegetable beds. It suppresses weeds and holds "
                 "moisture without cooling the soil too much for warm-season crops like tomatoes and "
                 "courgettes. Three inches is fine for cool-season crops and permanent beds.\n\n"
                 "Do not mulch until the soil has warmed in spring, or you will trap the cold in and "
                 "slow growth. Wait until the seedlings are up and the ground is warm, then lay the "
                 "mulch around them rather than over them."),
                ("Choosing a Vegetable-Friendly Mulch",
                 "Straw is the classic choice: cheap, light, and easy to move aside when you need to "
                 "plant through it. Grass clippings work if spread thin, because a thick layer mats and "
                 "smells. Compost doubles as a soil improver and feeds the bed as it breaks down.\n\n"
                 "Avoid fresh woodchip on vegetable beds. As it decomposes it ties up nitrogen at the "
                 "soil surface, which is exactly where shallow-rooted vegetables need it. Use woodchip "
                 "on paths instead."),
                ("Mulching Around Plants",
                 "Keep the mulch a few inches clear of stems and trunks. Piling it against a tomato "
                 "stem or a young courgette holds moisture against the plant and invites rot. A clear "
                 "ring of soil around each stem also keeps slugs from using the mulch as a bridge to "
                 "tender growth.\n\n"
                 "Water the bed before you mulch, because a dry layer sheds light rain and the plants "
                 "underneath stay thirsty. Once mulched, the bed needs far less watering, and the soil "
                 "stays more even, which suits vegetables that dislike drying out."),
                ("Working Mulch Into the Rotation",
                 "At the end of the season, dig the spent straw or clippings into the soil or leave "
                 "them on the surface for the worms. Either way, the organic matter improves the bed "
                 "for next year. This is the quiet benefit of mulching vegetables: you are building "
                 "soil while you suppress weeds.\n\n"
                 "Keep a note of how much you used. A bed this size takes about 25 bags, so a small "
                 "bulk order of two yards covers it with a little spare. Next year the same bed will "
                 "need roughly the same amount, and knowing that makes ordering a one-minute job."),
                ("The Time Mulch Saves",
                 "Mulch is one of the cheapest ways to cut the work in a vegetable garden. Once the beds are covered, weeding drops away and watering is less frequent, which frees the time for the planting and picking that make the plot worth keeping.\n\nBuy straw from a supplier who can confirm it was not treated with a persistent herbicide, which can damage tomatoes and other crops for years. It is a rare problem, but the question is worth asking before you spread a whole bed with it."),
            ],
        ),
    },
]
