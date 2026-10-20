"""Curated articles, part B (grass seed, fertilizer, concrete)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-grass-seed-do-i-need-for-5000-square-feet",
        "title": "How Much Grass Seed for 5,000 Square Feet? Bags",
        "cluster": "grass-seed",
        "primary_keyword": "how much grass seed do i need for 5000 square feet",
        "secondary_keywords": ["grass seed per 1000 square feet", "5 lb bag grass seed coverage",
                               "how many bags of grass seed for 5000 sq ft", "grass seed calculator"],
        "calculator": "grass_seed",
        "calculator_defaults": {"area": 5000, "method": 1},
        "meta_description": "A 5,000 sq ft new lawn at 4.5 lb of seed per 1,000 sq ft needs 22.5 lb, "
                            "about 8 bags of 3 lb. Overseeding uses half that.",
        "faq": [
            ("How many pounds of grass seed for 5,000 square feet?",
             "About 22.5 lb for a new lawn at 4.5 lb per 1,000 sq ft, or roughly 11 lb if you are "
             "overseeding an existing lawn."),
            ("How many 3 lb bags is that?",
             "Eight. A 3 lb bag covers about 660 sq ft at the new-lawn rate, so 5,000 sq ft needs "
             "eight of them with a little left over."),
            ("Does the seeding rate change by species?",
             "Yes. Fine fescues go down lighter than tall fescue, and warm-season grasses such as "
             "Bermuda are often specified by pure live seed weight instead."),
        ],
        "body": _body(
            lead=(
                "A 5,000 sq ft new lawn at 4.5 lb of seed per 1,000 sq ft needs 22.5 lb of grass seed, "
                "which is about 8 bags of 3 lb. Overseeding an existing lawn uses roughly half that "
                "rate.\n\n"
                "The rate depends on the job. Bare soil needs enough seed to establish every blade "
                "from scratch, while overseeding only fills thin patches, so the two cases sit at "
                "different ends of the same range. Getting the rate right matters more than the "
                "brand on the bag, because the seed can only cover what the ground will support."
            ),
            worked_lead=(
                "For a 5,000 sq ft area sown as a new lawn at the standard rate of 4.5 lb per "
                "1,000 sq ft:"
            ),
            bullets=(
                "*   area = 5000\n"
                "*   method = 1\n"
                "*   Rate per 1000: 4.5\n"
                "*   Pounds: 22.5\n"
                "*   3 lb bags: 8"
            ),
            sections=[
                ("Match the Rate to the Job",
                 "Overseeding an established lawn needs about 2 lb per 1,000 sq ft. A new lawn on "
                 "bare soil doubles that to 4 to 5 lb. Repairing worn or sloped ground that is prone "
                 "to washout can take 5 to 6 lb.\n\n"
                 "Getting this wrong is costly in both directions. Too little and the lawn comes up "
                 "thin and patchy; too much and seedlings crowd each other and come up weak, which "
                 "shows as a lush first month and a thin lawn by autumn."),
                ("How Much Grass Seed for Common Lawn Sizes",
                 "At the new-lawn rate, a 1,000 sq ft patch takes 4.5 lb, a 2,500 sq ft lawn takes "
                 "about 11.3 lb, and a 5,000 sq ft lawn takes 22.5 lb. Doubling the area doubles the "
                 "weight, so the arithmetic scales cleanly.\n\n"
                 "Measure the lawn in rectangles and subtract the beds, paths and driveway rather "
                 "than pacing out a single rough figure. A lawn that is 20% smaller than you thought "
                 "wastes a fifth of the seed you buy."),
                ("Why the Bag Count Matters",
                 "Seed is sold by weight, and bag sizes vary. A 3 lb bag covers about 660 sq ft at "
                 "the new-lawn rate, so a 5,000 sq ft job needs eight bags. A 5 lb bag covers more "
                 "per bag, and a 20 lb bag more again, so compare the price per pound once you know "
                 "the total weight you need.\n\n"
                 "Buy a little extra rather than exactly the calculated amount. A missed corner or "
                 "a bird taking its share is easier to fix with a spare bag in the shed than with a "
                 "second trip to the store."),
                ("Sowing It Well",
                 "Spread half the seed in one direction and half across it, so the coverage overlaps "
                 "and bare stripes are less likely. Rake it lightly into the top of the soil, then "
                 "roll or tread it to get good seed-to-soil contact.\n\n"
                 "Keep the surface damp for the first fortnight. Light, frequent watering beats one "
                 "deep soak, because the seed is sitting in the top inch where it dries fastest. Once "
                 "the seedlings are an inch tall, switch to deeper and less frequent watering."),
                ("Choosing a Species",
                 "The rate on the bag assumes a general-purpose mix. Fine fescues are sown lighter "
                 "than tall fescue, and warm-season grasses such as Bermuda are usually specified by "
                 "pure live seed weight rather than total weight.\n\n"
                 "Match the species to the site: shade-tolerant fescue for a north-facing lawn, "
                 "ryegrass for quick cover and wear tolerance, and a clover blend where you want to "
                 "cut back on fertiliser. The seed weight you buy should follow the species you "
                 "choose, not the other way round."),
                ("Common Mistakes to Avoid",
                 "*   Using the overseeding rate on bare soil, then blaming the seed for a thin lawn.\n"
                 "*   Letting the surface dry out during germination.\n"
                 "*   Burying the seed under more than a dusting of soil.\n"
                 "*   Sowing in midsummer when heat and weeds out-compete young grass.\n"
                 "*   Buying the cheapest mix without checking the germination rate on the label."),
            ],
        ),
    },
    {
        "slug": "how-much-grass-seed-for-1-acre",
        "title": "How Much Grass Seed for 1 Acre? Pounds and Bags",
        "cluster": "grass-seed",
        "primary_keyword": "how much grass seed for 1 acre",
        "secondary_keywords": ["grass seed per acre", "1 acre grass seed calculator",
                               "how many pounds of grass seed per acre", "seeding rate per acre"],
        "calculator": "grass_seed",
        "calculator_defaults": {"area": 43560, "method": 1},
        "meta_description": "An acre of new lawn at 4.5 lb per 1,000 sq ft needs about 196 lb of grass "
                            "seed, roughly 66 bags of 3 lb or ten 20 lb bags.",
        "faq": [
            ("How many pounds of grass seed per acre?",
             "About 196 lb for a new lawn at 4.5 lb per 1,000 sq ft. Overseeding an established acre "
             "takes roughly half that."),
            ("How many bags is that?",
             "Around 66 bags of 3 lb, or ten 20 lb bags. Bulk or 20 lb bags are far cheaper at this "
             "scale."),
            ("Is an acre the same as 43,560 square feet?",
             "Yes. One acre is 43,560 sq ft, which is why acre seeding rates are quoted per 1,000 sq "
             "ft and then multiplied."),
        ],
        "body": _body(
            lead=(
                "An acre of new lawn at 4.5 lb of seed per 1,000 sq ft needs about 196 lb of grass "
                "seed, which is roughly 66 bags of 3 lb or ten 20 lb bags. At this scale, buy in "
                "bulk or in the largest bags you can get.\n\n"
                "An acre is 43,560 sq ft, so the arithmetic is just the per-1,000 sq ft rate "
                "multiplied out. The rate itself depends on whether you are seeding bare ground or "
                "thickening an existing stand, and the difference is measured in hundreds of pounds."
            ),
            worked_lead=(
                "For a 43,560 sq ft acre sown as a new lawn at 4.5 lb per 1,000 sq ft:"
            ),
            bullets=(
                "*   area = 43560\n"
                "*   method = 1\n"
                "*   Rate per 1000: 4.5\n"
                "*   Pounds: 196.02\n"
                "*   3 lb bags: 66"
            ),
            sections=[
                ("New Lawn Versus Overseeding",
                 "Bare ground is seeded at 4 to 5 lb per 1,000 sq ft, so an acre takes close to "
                 "200 lb. Overseeding an established lawn needs only about 2 lb per 1,000 sq ft, "
                 "which brings an acre down to roughly 87 lb.\n\n"
                 "Steep banks and areas that flood need the top of the range, because some seed "
                 "always washes away before it settles. Seed the slope across the fall line, not "
                 "straight down it, to slow the water."),
                ("Buying at Acre Scale",
                 "Small bags stop making sense here. Sixty-six 3 lb bags is a lot of plastic, and "
                 "the price per pound is usually worse than a 20 lb bag or bulk seed. Ten 20 lb bags "
                 "cover the same ground with far less packaging.\n\n"
                 "Check the seed label for purity and germination. Two bags of the same weight can "
                 "differ in how much live seed they contain, and that changes how far the bag "
                 "actually goes. A cheap bag at a low germination rate can end up costing more per "
                 "live seed than a better one."),
                ("Spreading an Acre Evenly",
                 "Calibrate the spreader on a measured strip before you start. Mark the acre into "
                 "quarters and treat each one separately, splitting the seed into two passes at "
                 "right angles. Overlap the edges so the joins do not show as stripes.\n\n"
                 "Roll or harrow after sowing to get seed-to-soil contact, and water in stages if "
                 "the acre is too large to keep damp all at once. Sow a section at a time if you "
                 "cannot keep up with the watering."),
                ("Ground Preparation at This Scale",
                 "An acre of bare ground needs levelling before seed goes down, or the low spots "
                 "will pool water and the seed will rot. Rotovate or harrow the top few inches, "
                 "remove stones and roots, and firm it with a roller before sowing.\n\n"
                 "A soil test is worth more here than on a small patch, because correcting pH across "
                 "an acre takes far more material than most people expect. Test first, then seed, "
                 "rather than sowing into ground that will not support the grass you chose."),
                ("Timing the Sowing",
                 "Early autumn is the best window for cool-season grass, because the soil is still "
                 "warm and weed competition is slowing down. Spring works as a second choice, but "
                 "young grass then has to survive a summer it is not ready for.\n\n"
                 "For an acre, the watering that follows sowing is the real constraint. If you "
                 "cannot keep the whole area damp for the first fortnight, split the job into "
                 "sections and sow one at a time rather than gambling the lot on one dry spell."),
                ("Common Mistakes to Avoid",
                 "*   Using a garden spreader that cannot be calibrated accurately at this scale.\n"
                 "*   Sowing the whole acre and then being unable to water it evenly.\n"
                 "*   Buying by bag count without comparing the price per pound.\n"
                 "*   Ignoring germination rates on the label.\n"
                 "*   Sowing onto unprepared, unlevelled ground and losing seed to the low spots."),
            ],
        ),
    },
    {
        "slug": "how-much-fertilizer-do-i-need-per-1000-sq-ft",
        "title": "How Much Fertilizer Per 1,000 Sq Ft? N-P-K Maths",
        "cluster": "fertilizer",
        "primary_keyword": "how much fertilizer do i need per 1000 sq ft",
        "secondary_keywords": ["fertilizer rate per 1000 square feet", "pounds of nitrogen per 1000 sq ft",
                               "fertilizer calculator", "how much 20-0-0 per 1000 sq ft"],
        "calculator": "fertilizer",
        "calculator_defaults": {"area": 1000, "rate": 1.0, "nitrogen": 20, "bag": 40},
        "meta_description": "At 1 lb of nitrogen per 1,000 sq ft, a 20% nitrogen product needs 5 lb of "
                            "fertilizer. Divide the target rate by the nitrogen share.",
        "faq": [
            ("How much fertilizer per 1,000 square feet?",
             "It depends on the nitrogen share. Divide 1 lb of actual nitrogen by the percentage "
             "on the bag: a 20% product needs 5 lb, a 10% product needs 10 lb."),
            ("How much actual nitrogen should I apply?",
             "Most established lawns take 0.75 to 1 lb of actual nitrogen per 1,000 sq ft per "
             "application, split across the growing season."),
            ("Why is 20-0-0 different from 10-10-10?",
             "The numbers are the percentage by weight of nitrogen, phosphorus and potassium. A "
             "higher first number means less product is needed to hit the same nitrogen rate."),
        ],
        "body": _body(
            lead=(
                "At the standard rate of 1 lb of actual nitrogen per 1,000 sq ft, a 20% nitrogen "
                "product needs 5 lb of fertilizer. The rule is simple: divide the target nitrogen "
                "rate by the nitrogen share on the bag.\n\n"
                "Fertilizer is not applied by product weight alone. The bag only tells you how much "
                "of it is nitrogen, so the percentage on the front label is the number that turns a "
                "nutrient target into a product weight. Get that wrong and the lawn is either "
                "starved or scorched."
            ),
            worked_lead=(
                "For 1,000 sq ft at 1 lb of nitrogen per 1,000 sq ft using a 20% nitrogen product:"
            ),
            bullets=(
                "*   area = 1000\n"
                "*   rate = 1.0\n"
                "*   nitrogen = 20\n"
                "*   bag = 40\n"
                "*   Pounds of nitrogen: 1.0\n"
                "*   Pounds of product: 5.0\n"
                "*   Bags: 1"
            ),
            sections=[
                ("Read the Bag First",
                 "The three numbers on a fertilizer bag are the percentage by weight of nitrogen, "
                 "phosphorus and potassium. A 20-0-0 bag is a fifth nitrogen, so 5 lb of product "
                 "supplies the 1 lb of actual nitrogen a 1,000 sq ft application calls for.\n\n"
                 "A 10-10-10 product is only a tenth nitrogen, so the same target needs 10 lb of "
                 "product. The weight changes; the nutrient rate does not. Always work back from the "
                 "nutrient the grass actually needs."),
                ("Choose the Right Rate",
                 "Established cool-season lawns usually take 0.75 to 1 lb of actual nitrogen per "
                 "1,000 sq ft per feeding, spread over two to four feedings a year. Warm-season "
                 "grasses often take a little more across their growing season.\n\n"
                 "Fast-release products should be applied at the lower end to avoid a surge of "
                 "growth and the risk of scorching. Slow-release granules are more forgiving and "
                 "can be applied at the higher end, which is why they cost more."),
                ("Calibrate Before You Spread",
                 "Spreader settings drift, so check yours on a hard surface before treating the "
                 "lawn. Weigh out enough product to cover a measured strip, run the spreader over "
                 "it, and adjust the dial until it releases the right weight.\n\n"
                 "Split the application into two passes at right angles. Overlapping half-rates "
                 "covers the lawn far more evenly than one pass, and it avoids the dark stripes "
                 "that come from a spreader overlapping too much on its own."),
                ("Timing the Applications",
                 "Feed cool-season lawns in early autumn and again in late spring, when the grass is "
                 "growing strongly. A late-autumn feed helps root growth through the winter. Avoid "
                 "feeding in the middle of a heatwave, when the grass is dormant and the fertiliser "
                 "sits unused.\n\n"
                 "Water the lawn lightly after applying granular feed, so the granules dissolve and "
                 "reach the roots. Sweep any granules off paths and driveways before they wash into "
                 "drains, where they feed algae instead of grass. Note the spreader setting that "
                 "worked, so the next application is repeatable rather than guesswork."),
                ("Why the Ratio Matters",
                 "The middle and last numbers matter as much as the first once the grass is "
                 "established. Phosphorus supports root development, so it belongs in a starter "
                 "feed for new seed or sod. Potassium helps with stress tolerance, so it earns its "
                 "place ahead of winter.\n\n"
                 "A balanced feed is not automatically the right one. Read what the lawn needs from "
                 "a soil test, and pick the ratio that supplies it rather than the one on offer."),
                ("Common Mistakes to Avoid",
                 "*   Applying by product weight and ignoring the nitrogen percentage.\n"
                 "*   Skipping spreader calibration, then over- or under-feeding.\n"
                 "*   Feeding at the top rate in hot weather and burning the lawn.\n"
                 "*   Spreading onto hard surfaces, where the granules wash into drains.\n"
                 "*   Feeding a drought-stressed lawn, which does more harm than good."),
            ],
        ),
    },
    {
        "slug": "how-many-bags-of-concrete-do-i-need-for-a-6x6-slab",
        "title": "How Many Bags of Concrete for a 6x6 Slab? 4 in Deep",
        "cluster": "concrete",
        "primary_keyword": "how many bags of concrete do i need for a 6x6 slab",
        "secondary_keywords": ["6x6 slab concrete calculator", "bags of concrete per cubic yard",
                               "how many 80 lb bags of concrete", "concrete for a 6x6 pad"],
        "calculator": "concrete",
        "calculator_defaults": {"length": 6, "width": 6, "thickness": 4},
        "meta_description": "A 6x6 ft slab at 4 in deep needs 12 cu ft of concrete, about 0.44 cu yd or "
                            "20 bags of 80 lb, or 27 bags of 60 lb.",
        "faq": [
            ("How many bags of concrete for a 6x6 slab?",
             "About 20 bags of 80 lb or 27 bags of 60 lb for a 4 in slab. That is 0.44 cu yd."),
            ("How many bags of concrete make a cubic yard?",
             "Roughly 45 bags of 80 lb or 60 bags of 60 lb. At that point a ready-mix delivery is "
             "usually cheaper."),
            ("How thick should a 6x6 slab be?",
             "Four inches suits a footpath, patio or shed base on firm ground. A pad that takes "
             "vehicle weight should be thicker and reinforced."),
        ],
        "body": _body(
            lead=(
                "A 6 x 6 ft slab at 4 in deep needs 12 cu ft of concrete, which is 0.44 cu yd or "
                "about 20 bags of 80 lb. It is a small enough job to mix by hand, but the bag count "
                "adds up quickly.\n\n"
                "Concrete is ordered by volume, and bags are sold by weight, so the bridge between "
                "the two is the yield of each bag. Working in cubic feet first keeps the arithmetic "
                "straight, and it makes the bags-versus-delivery decision obvious."
            ),
            worked_lead=(
                "For a 6 foot by 6 foot slab poured 4 inches thick:"
            ),
            bullets=(
                "*   length = 6\n"
                "*   width = 6\n"
                "*   thickness = 4\n"
                "*   Cubic feet: 12.0\n"
                "*   Cubic yards: 0.44\n"
                "*   60 lb bags: 27\n"
                "*   80 lb bags: 20"
            ),
            sections=[
                ("Bags Versus Ready-Mix",
                 "An 80 lb bag yields about 0.6 cu ft, and a 60 lb bag about 0.45 cu ft. That puts a "
                 "cubic yard at roughly 45 bags of 80 lb or 60 bags of 60 lb.\n\n"
                 "Mixing and placing that many bags by hand is hard work and slow, and concrete "
                 "begins to set while you are still pouring. Above about half a cubic yard, a "
                 "ready-mix delivery is usually both cheaper and better, because it arrives as one "
                 "consistent batch."),
                ("Getting the Thickness Right",
                 "Four inches is the standard for a footpath, patio or garden shed base on firm, "
                 "well-compacted ground. A pad that carries a vehicle, or one over soft ground, "
                 "should be thicker and reinforced with mesh.\n\n"
                 "Thickness drives volume directly, so an extra inch on a small slab is a real "
                 "increase in bags. Measure the form depth rather than assuming it, because a form "
                 "that sits an inch proud of the ground quietly adds bags to the job."),
                ("Preparing the Base",
                 "Excavate and compact a layer of hardcore before pouring. A slab on soft, "
                 "uncompacted ground cracks as it settles, no matter how well the concrete was "
                 "mixed. Aim for a base that is level and firm underfoot.\n\n"
                 "Dampen the sub-base and the formwork before pouring, so the ground does not pull "
                 "water out of the mix. Cure the slab by keeping it damp for several days, which is "
                 "what builds its strength. Concrete that dries out too fast is weak and dusty on "
                 "top."),
                ("Mixing and Placing",
                 "Mix in a wheelbarrow or a tub with a hoe or paddle mixer, adding water gradually "
                 "until the mix is workable but not sloppy. Too much water is the most common fault, "
                 "and it costs strength. Aim for a consistency that holds its shape when you drag a "
                 "shovel through it.\n\n"
                 "Pour in one go where you can, and tamp or vibrate the concrete to remove air "
                 "pockets. Level it with a screed board and float the surface once the bleed water "
                 "has gone. Add expansion joints around the edge if the slab meets a wall."),
                ("Reinforcement and Joints",
                 "A small pad on solid ground often needs no reinforcement, but a sheet of welded "
                 "mesh a third of the way up the slab adds insurance at little cost. Cut control "
                 "joints into larger slabs so cracks form where you want them rather than at random.\n\n"
                 "Keep the slab away from tree roots and drains, and give it a slight fall so water "
                 "runs off. A flat pad that holds water will spall and crack over a few winters."),
                ("Common Mistakes to Avoid",
                 "*   Mixing bag by bag and letting earlier batches start to set.\n"
                 "*   Pouring onto soft ground with no compacted base.\n"
                 "*   Forgetting the waste from spillage and uneven form depth.\n"
                 "*   Letting the slab dry too fast, which leaves it weak and crumbly.\n"
                 "*   Adding too much water to make the mix easier to work."),
            ],
        ),
    },
]
