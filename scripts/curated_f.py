"""Curated articles, part F (bases, playground surfacing, weed control, soil amendment)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-gravel-do-i-need-for-a-shed-base",
        "title": "How Much Gravel for a Shed Base: Depth and Tons",
        "cluster": "gravel",
        "primary_keyword": "how much gravel do i need for a shed base",
        "secondary_keywords": ["gravel pad for shed", "shed base depth",
                               "how many tons of gravel for a shed base", "crushed stone shed foundation"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 10, "width": 12, "depth": 4, "kind": "crushed"},
        "meta_description": "A 10x12 ft shed base 4 in deep takes 1.48 cubic yards of gravel, about 2.07 "
                            "tons. Dig the pad a foot wider than the shed and add 10% for compaction.",
        "faq": [
            ("How deep should gravel be under a shed?",
             "Four inches of compacted crushed stone is the standard shed base. Go to 6 in for a "
             "large or heavy shed, or where the ground is soft and poorly drained."),
            ("Can I use pea gravel for a shed base?",
             "No. Pea gravel is rounded and rolls under load, so the shed settles unevenly. Use angular "
             "crushed stone with fines, which locks together when compacted."),
            ("Do I need a membrane under a shed base?",
             "A geotextile membrane helps on soft soil by stopping the stone sinking into the ground. "
             "On firm, free-draining ground you can lay the stone straight onto the excavated soil."),
        ],
        "body": _body(
            lead=(
                "A 10 x 12 ft shed base with a gravel pad 4 inches deep takes 1.48 cubic yards of "
                "crushed stone, which is about 2.07 tons. That pad sits in a shallow excavation, "
                "compacted in two layers, and it is the cheapest foundation that keeps a shed level, "
                "dry and off the soil.\n\n"
                "The depth is the decision that drives the order. Four inches is the standard for a "
                "garden shed on reasonable ground. Two inches looks similar on the day you spread it "
                "but settles and lets the bearers touch damp soil; six inches is for big, heavy sheds "
                "or soft ground. The calculator above uses the same figures for your own shed size."
            ),
            worked_lead=(
                "For a shed base measuring 10 feet by 12 feet, with a gravel layer 4 inches deep:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 12\n"
                "*   depth = 4\n"
                "*   Square feet: 120.0\n"
                "*   Cubic yards: 1.48\n"
                "*   Tons: 2.07"
            ),
            sections=[
                ("How Deep a Shed Base Should Be",
                 "Four inches of compacted stone carries a typical timber or metal shed without "
                 "moving. The pad spreads the weight of the walls and floor bearers over the whole "
                 "footprint, so no single point digs into the soil. It also lifts the shed clear of "
                 "ground moisture, which is what rots floor bearers first.\n\n"
                 "On soft clay or made-up ground, dig deeper and lay 6 in. At 6 in deep the same "
                 "10 x 12 ft footprint takes 2.22 cubic yards, about 3.11 tons. The extra stone is "
                 "cheap insurance against one corner sinking over the first winter."),
                ("Build the Pad Bigger Than the Shed",
                 "Extend the pad at least 12 in beyond the shed on every side. The extra border "
                 "carries the drip line from the roof, keeps the edge of the base from crumbling "
                 "away, and gives you somewhere to stand while you work. A pad exactly the size of "
                 "the shed sheds its edge stone within a season.\n\n"
                 "For a 10 x 12 ft shed, that makes the pad 12 x 14 ft, or 168 sq ft. At 4 in deep "
                 "it takes 2.07 cubic yards, about 2.9 tons. Run the calculator with the pad "
                 "dimensions, not the shed dimensions, before you order."),
                ("Which Gravel Compacts Into a Base",
                 "Use angular crushed stone with a spread of sizes down to dust, often sold as "
                 "crusher run or road base. The fines fill the gaps between the stones, and when "
                 "you compact it the whole layer locks into a firm slab that water still drains "
                 "through slowly.\n\n"
                 "Rounded gravels, pea gravel and river stone never lock. Each stone rolls against "
                 "its neighbours, the pad creeps, and the shed ends up rocking on its bearers. They "
                 "are surface materials, not foundation materials, whatever the bag says."),
                ("Laying the Base in Lifts",
                 "Excavate the full pad area to your depth plus the thickness of any edging, and "
                 "level the soil. Set a timber frame or edging boards if you want a crisp edge "
                 "that holds the stone in. Spread half the stone, compact it with a plate "
                 "compactor or a hand tamper, then spread and compact the second half.\n\n"
                 "Compacting in two lifts, rather than one thick layer, is what makes the base "
                 "stay level. A single deep layer compacts at the top and stays loose underneath, "
                 "and the shed settles into it over the following months."),
                ("Bags, Bulk and the Compaction Allowance",
                 "Two tons is far beyond bag territory: it is roughly eighty 25 kg bags, at several "
                 "times the bulk price. Order loose or in one-ton bulk bags and have it tipped as "
                 "close to the pad as the truck can reach.\n\n"
                 "Order about 10% more than the calculated figure. Loose stone compacts down when "
                 "you run the plate over it, and excavations are never perfectly flat, so the pad "
                 "always swallows a little more than the arithmetic says. The surplus is useful "
                 "for topping up the border later."),
            ],
        ),
    },
    {
        "slug": "how-much-gravel-do-i-need-for-a-paver-base",
        "title": "How Much Gravel for a Paver Base: Layers and Tons",
        "cluster": "gravel",
        "primary_keyword": "how much gravel do i need for a paver base",
        "secondary_keywords": ["paver base depth", "crushed stone under pavers",
                               "how many tons of gravel for pavers", "paver base calculator"],
        "calculator": "gravel",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 4, "kind": "crushed"},
        "meta_description": "A 10x10 ft paver base 4 in deep takes 1.23 cubic yards of crushed stone, "
                            "about 1.73 tons, plus a 1 in bedding sand layer above it before the pavers go down.",
        "faq": [
            ("How deep should a paver base be?",
             "Four inches of compacted crushed stone for patios and walkways, 6 in for driveways and "
             "anywhere a vehicle will stand. Add a 1 in bedding sand layer on top in both cases."),
            ("Can I lay pavers straight on gravel without sand?",
             "Not well. The sand layer is what you screed level and bed each paver into. Without it "
             "the surface waves, individual pavers rock, and the joints open up within a year."),
            ("How much extra gravel should I order for compaction?",
             "About 10% more than the calculated volume. Loose crushed stone compacts down under the "
             "plate, so a layer spread at 4 in loose finishes thinner than 4 in."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft paver base with a gravel layer 4 inches deep takes 1.23 cubic yards of "
                "crushed stone, about 1.73 tons. That is the structural layer only: above it goes a "
                "1-inch bedding layer of coarse sand, and the pavers sit in that.\n\n"
                "Most paver failures are base failures. Pavers laid on too little stone, or on stone "
                "that was never compacted, dip and spread within a couple of winters. Getting the "
                "gravel quantity and depth right is most of the job, and it is the part you cannot "
                "fix later without lifting the whole surface."
            ),
            worked_lead=(
                "For a paver base measuring 10 feet by 10 feet, with a gravel layer 4 inches deep:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   depth = 4\n"
                "*   Square feet: 100.0\n"
                "*   Cubic yards: 1.23\n"
                "*   Tons: 1.73"
            ),
            sections=[
                ("The Two Layers of a Paver Base",
                 "A paver base is two layers doing different jobs. The gravel layer is structural: "
                 "4 in compacted for a patio or path, 6 in where vehicles drive or park. It spreads "
                 "the load and drains water away from the surface. The sand layer above it, about "
                 "1 in of coarse bedding sand, is not structural at all. It is the adjustable layer "
                 "you screed flat and tap each paver down into.\n\n"
                 "Keeping the two separate in your order matters, because they are different "
                 "materials bought in different quantities, and the gravel calculator on this page "
                 "covers only the stone layer."),
                ("How Much Gravel at Each Depth",
                 "Depth changes the order more than area does. At 4 in deep, 100 sq ft takes "
                 "1.23 cubic yards, about 1.73 tons. At 6 in deep, the driveway standard, the same "
                 "area takes 1.85 cubic yards, about 2.59 tons.\n\n"
                 "The quick check for any area: a cubic yard of crushed stone covers about 81 sq ft "
                 "at 4 in deep, and weighs about 1.4 tons. Measure your area, choose the depth for "
                 "how the surface will be used, and let the calculator turn it into an order "
                 "quantity."),
                ("Use Crushed Stone With Fines, Not Pea Gravel",
                 "The base material is angular crushed stone graded down to dust, sold as crusher "
                 "run, road base or 3/4-inch minus. Compacted, the angular faces lock and the fines "
                 "fill the voids, giving a surface hard enough to screed sand on without it "
                 "shifting under your boots.\n\n"
                 "Clean, single-size stone and pea gravel never lock in the same way. A base built "
                 "from them keeps moving a fraction every time weight crosses it, and the pavers "
                 "above follow it. Save the rounded stone for drainage trenches and decorative "
                 "surfaces."),
                ("Compact in Lifts or the Pavers Will Settle",
                 "Spread the stone in lifts of about 2 in and run a plate compactor over each one. "
                 "A 4 in base is two lifts, a 6 in base is three. Dampen dusty stone lightly before "
                 "compacting; it binds the fines and firms up faster.\n\n"
                 "Once the last lift is level, screed the bedding sand between two rails, lay the "
                 "pavers, then compact the finished surface with sand spread over it to fill the "
                 "joints. Settling after that is minimal if the lifts were compacted properly."),
                ("What the Gravel Figure Does Not Include",
                 "The bedding sand is a separate, smaller order. One inch over 100 sq ft is about "
                 "8.3 cu ft, roughly 0.31 cubic yards, so a single bulk bag covers a patio base "
                 "with some to spare for jointing.\n\n"
                 "Also outside the gravel figure: edge restraints, which every paver field needs "
                 "to stop it spreading sideways, and the pavers themselves. Order the stone first "
                 "and build the base before the pavers arrive, so a delivery delay does not leave "
                 "an open excavation."),
            ],
        ),
    },
    {
        "slug": "how-much-rubber-mulch-do-i-need-for-a-playground",
        "title": "How Much Rubber Mulch for a Playground: Safe Depths",
        "cluster": "mulch",
        "primary_keyword": "how much rubber mulch do i need for a playground",
        "secondary_keywords": ["rubber mulch depth for swings", "playground surfacing calculator",
                               "how many bags of rubber mulch", "loose fill rubber mulch"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 20, "width": 20, "depth": 6},
        "meta_description": "A 20x20 ft playground at 6 in deep needs 200 cu ft of rubber mulch, 7.41 "
                            "cubic yards or 100 bags of 2 cu ft. Match the depth to the equipment's fall height.",
        "faq": [
            ("How deep should rubber mulch be under a swing set?",
             "Six inches is the usual residential depth for equipment with a fall height up to about "
             "6 ft. For taller equipment, follow the mulch manufacturer's tested depth for that fall "
             "height, and keep the layer topped up to it."),
            ("Does rubber mulch need replacing like wood mulch?",
             "It does not rot or break down, so there is no annual replacement. It does get kicked "
             "out of swing and slide landing zones, so rake it back and top up those spots once or "
             "twice a year."),
            ("Can I lay rubber mulch straight over grass?",
             "No. Strip the turf and level the soil first, then lay a weed membrane. Mulch over "
             "grass ends up uneven, and the grass rots into a slippery layer underneath."),
        ],
        "body": _body(
            lead=(
                "A 20 x 20 ft playground surfaced 6 inches deep takes 200 cubic feet of rubber mulch, "
                "which is 7.41 cubic yards or 100 bags of 2 cu ft. Six inches is the depth most "
                "residential play equipment needs; the layer's job is to cushion falls, not to look "
                "tidy, so depth matters here more than on any flower bed.\n\n"
                "Work out the area under and around the equipment, including the swing arc and the "
                "slide exit, and surface all of it to the full depth. A border at least as deep as "
                "the mulch keeps it contained. The calculator above turns your own measurements into "
                "bags or yards."
            ),
            worked_lead=(
                "For a playground area measuring 20 feet by 20 feet, with rubber mulch 6 inches deep:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 20\n"
                "*   depth = 6\n"
                "*   Square feet: 400.0\n"
                "*   Cubic feet: 200.0\n"
                "*   Cubic yards: 7.41\n"
                "*   2 cu ft bags: 100"
            ),
            sections=[
                ("Depth Is Set by Fall Height, Not Looks",
                 "The right depth is the one tested for the height a child can fall from. For "
                 "typical home equipment, swings and slides with fall heights up to around 6 ft, "
                 "6 in of loose-fill rubber mulch is the widely used figure. Taller equipment needs "
                 "more, and the mulch manufacturer's tested depth for your fall height is the "
                 "number to follow, not a guess.\n\n"
                 "Whatever depth you install, the layer only protects at that depth while it stays "
                 "there. Loose fill migrates out of the busiest landing zones first, which are "
                 "exactly the places it is needed most."),
                ("How Much Rubber Mulch at Each Depth",
                 "Volume scales directly with depth. At 3 in deep, a 20 x 20 ft area takes 100 cu "
                 "ft, which is 3.7 cubic yards or 50 bags of 2 cu ft. At 6 in it doubles to 200 cu "
                 "ft, 7.41 cubic yards or 100 bags.\n\n"
                 "A cubic yard of rubber mulch covers about 54 sq ft at 6 in deep. Use that for a "
                 "quick estimate of any play area, then run the calculator for the bag count, "
                 "because rubber mulch is usually sold bagged rather than loose."),
                ("Bags, Bulk and Weight",
                 "Rubber mulch is sold by volume in bags, commonly 1.5 or 2 cu ft, and in bulk by "
                 "the cubic yard or by the pallet for big areas. At 100 bags, compare the pallet "
                 "price before buying individually; for a home playground the pallet usually wins "
                 "and arrives in one delivery.\n\n"
                 "It is much lighter than stone or soil, so bags are easy to carry and spread, but "
                 "it is bulky. A 20 x 20 ft playground at full depth is a van-load of material "
                 "whichever way you buy it, so have it delivered rather than collecting it in a "
                 "car."),
                ("Containment, Drainage and Upkeep",
                 "Loose rubber mulch travels. Fit a border at least 6 in high around the play area "
                 "before you spread it, or a third of your order will migrate into the lawn within "
                 "a year. Underneath, strip the turf, level the ground so water does not pool, and "
                 "lay a permeable weed membrane.\n\n"
                 "Rake the surface level every few weeks in heavy use, and rake the kicked-out "
                 "mulch back under swings and slide exits. Top up the landing zones when the depth "
                 "there drops noticeably below the rest, rather than re-doing the whole area."),
                ("Rubber Mulch vs Wood Mulch Under Equipment",
                 "Wood mulch is cheaper to buy and needs topping up every year or two as it rots "
                 "down, which steadily reduces the depth you installed for safety. Rubber mulch "
                 "costs more at the start, does not decompose, and holds its depth for years with "
                 "only raking and small top-ups.\n\n"
                 "Rubber's downsides are real too: it can smell for the first few weeks, and dark "
                 "rubber gets hot in direct summer sun, which matters for bare feet. In a shaded "
                 "garden with equipment that will be used for years, the long life usually "
                 "outweighs both."),
            ],
        ),
    },
    {
        "slug": "how-much-mulch-do-i-need-to-prevent-weeds",
        "title": "How Much Mulch to Prevent Weeds: The Depth That Works",
        "cluster": "mulch",
        "primary_keyword": "how much mulch do i need to prevent weeds",
        "secondary_keywords": ["mulch depth for weed control", "how deep should mulch be",
                               "mulch to stop weeds", "weed suppression mulch"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 3},
        "meta_description": "A 10x10 ft bed mulched 3 in deep takes 25 cu ft of mulch, 0.93 cubic yards "
                            "or 13 bags of 2 cu ft. Three inches blocks light without smothering plant roots.",
        "faq": [
            ("Will mulch stop all weeds?",
             "No mulch stops everything. A 3 in layer stops most seeds already in the soil from "
             "germinating, but wind-blown seeds land on top and root into the mulch itself. Those "
             "pull out easily if you catch them small."),
            ("Should I put landscape fabric under mulch for weeds?",
             "Usually not. Fabric under organic mulch traps the mulch as it decomposes, roots of "
             "weeds grow into it, and it is miserable to remove later. Mulch at full depth on "
             "weeded soil works better."),
            ("How often do I need to top up mulch for weed control?",
             "Once a year for most organic mulches. It decomposes from the bottom up, so the layer "
             "thins even when it looks intact. Top back up to 3 in each spring."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft bed mulched 3 inches deep takes 25 cubic feet of mulch, which is "
                "0.93 cubic yards or 13 bags of 2 cu ft. Three inches is the depth that works for "
                "weed control: thick enough to block the light weed seeds need to germinate, "
                "without the problems a deeper blanket causes.\n\n"
                "Mulch suppresses weeds; it does not sterilise soil. The depth, the preparation "
                "beforehand and a yearly top-up decide how well it works. Going deeper than 3 in "
                "buys almost nothing and costs both money and, in a wet season, plant health."
            ),
            worked_lead=(
                "For a bed measuring 10 feet by 10 feet, mulched to a depth of 3 inches:"
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
                ("Why Three Inches Is the Weed Depth",
                 "Most weed seeds need light, or the temperature swing that comes with light, to "
                 "germinate. Two inches of mulch leaks enough of both that annual weeds push "
                 "through by midsummer. Three inches cuts germination sharply and keeps the soil "
                 "cool and damp underneath, which suits the plants you want.\n\n"
                 "Four inches and more adds cost without adding much suppression, and very deep "
                 "mulch can shed light rain off the bed, mat into a crust, and keep crowns too "
                 "wet. For weed control specifically, 3 in is the settled figure, not a "
                 "compromise."),
                ("Mulch Does Not Kill Weeds That Are Already There",
                 "Mulch laid over established perennial weeds just gives them a darker place to "
                 "grow from. Couch grass, bindweed and dandelions push through 3 in of mulch "
                 "without slowing down. Weed the bed properly first, digging out perennial roots "
                 "rather than chopping them off.\n\n"
                 "For a bed that is badly infested, the reliable sequence is: weed it, lay "
                 "cardboard over the soil with the sheets overlapped, soak it, then mulch 3 in "
                 "deep over the top. The cardboard smothers what is left and rots away within a "
                 "season."),
                ("Fine and Coarse Mulches Behave Differently",
                 "Coarse bark and wood chips knit into a loose mat that seeds struggle to root "
                 "into, and they last longest before decomposing. Fine compost-like mulches feed "
                 "the soil faster but also give wind-blown seeds a perfect seedbed on the "
                 "surface, so they need more frequent hoeing on top.\n\n"
                 "Fresh mulch can itself carry seed if it was stored badly. Buy from a supplier "
                 "whose stock turns over, and if a new layer sprouts a green haze in the first "
                 "fortnight, hoe it off on a dry day before the roots establish."),
                ("Weeds That Grow in the Mulch Itself",
                 "Even a perfect 3 in layer collects wind-blown seed on its surface, and after "
                 "rain those seeds germinate into the top of the mulch. They are not rooted in "
                 "the soil, so they pull out with two fingers if you catch them in the first "
                 "couple of weeks.\n\n"
                 "Leave them and their roots thread down through the mulch into the soil, and "
                 "the easy pull becomes a proper weeding job. A quick pass with a hoe on a dry, "
                 "breezy day, just disturbing the surface, kills seedlings at the thread stage "
                 "and is the cheapest maintenance a mulched bed ever needs."),
                ("Keeping the Layer Working All Season",
                 "Organic mulch decomposes from the bottom, so by the following spring a 3 in "
                 "layer is often under 2 in even though it still looks covered. That thinning is "
                 "when weeds return. Top up to the full 3 in every spring, forking the old layer "
                 "lightly first if it has matted.\n\n"
                 "Keep the mulch a few inches clear of stems and trunks. A heap piled against a "
                 "stem, the mulch volcano, holds moisture against the bark and invites rot and "
                 "disease. The weed benefit comes from covering the soil, not the plant."),
            ],
        ),
    },
    {
        "slug": "how-much-compost-to-add-to-garden-soil",
        "title": "How Much Compost to Add to Garden Soil: Ratios",
        "cluster": "compost",
        "primary_keyword": "how much compost to add to garden soil",
        "secondary_keywords": ["compost to soil ratio", "how much compost per square foot",
                               "amending soil with compost", "compost for garden beds"],
        "calculator": "compost",
        "calculator_defaults": {"length": 20, "width": 10, "depth": 2},
        "meta_description": "A 20x10 ft bed at 2 in deep takes 33.3 cu ft of compost, 1.23 cubic yards "
                            "or 34 bags of 1 cu ft, worked into the top 6 to 8 inches of soil.",
        "faq": [
            ("What ratio of compost to soil is best for a new bed?",
             "About one part compost to three parts soil in the layer you dig, which is what a 2 in "
             "layer worked into the top 6 to 8 in gives you. More than a third compost risks excess "
             "phosphorus and a bed that shrinks as the compost breaks down."),
            ("Can I plant straight into pure compost?",
             "It is not ideal. Pure compost dries out fast, shrinks noticeably as it continues to "
             "decompose, and can be too rich in phosphorus and salts. Mix it with the soil it is "
             "amending instead."),
            ("When is the best time to add compost to a garden?",
             "Autumn is ideal, so worms and weather work it in over winter. Spring, a few weeks "
             "before planting, is the other good window. Avoid spreading on frozen or waterlogged "
             "soil."),
        ],
        "body": _body(
            lead=(
                "A 20 x 10 ft bed dressed with compost 2 inches deep takes 33.3 cubic feet, which is "
                "1.23 cubic yards or 34 bags of 1 cu ft. Worked into the top 6 to 8 inches of soil, "
                "that layer makes compost about a quarter of the dug volume, which is the share a new "
                "or tired bed wants.\n\n"
                "The question is really one of proportion, not just volume. Too little and the soil "
                "barely changes; too much, repeated year after year, overloads the soil with "
                "phosphorus. This page gives the amounts for building a bed up, and the smaller "
                "amounts for keeping one in shape."
            ),
            worked_lead=(
                "For a bed measuring 20 feet by 10 feet, with compost spread 2 inches deep:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 10\n"
                "*   depth = 2\n"
                "*   Square feet: 200.0\n"
                "*   Cubic feet: 33.3\n"
                "*   Cubic yards: 1.23\n"
                "*   1 cu ft bags: 34"
            ),
            sections=[
                ("The Quarter-Volume Rule for New Beds",
                 "When you dig a bed over, you are working the top 6 to 8 in of soil. A 2 in layer "
                 "of compost forked through that depth ends up as roughly 25 to 30% of the mix, "
                 "which is the proportion that transforms a poor soil without unbalancing it. "
                 "Clay soils open up, sandy soils hold water, and both grow better roots.\n\n"
                 "For a bed being built from scratch on really poor ground, such as subsoil left "
                 "by builders, 3 in is justified for the first dressing. That is 50 cu ft on "
                 "200 sq ft, 1.85 cubic yards. After that first year, drop back to maintenance "
                 "amounts."),
                ("Established Beds Need Much Less",
                 "A bed that is already in good heart needs only a 1 in top-up each year or two. "
                 "That is 16.7 cu ft on a 20 x 10 ft bed, about 0.62 cubic yards or 17 bags of "
                 "1 cu ft. The compost feeds the soil biology and replaces what decomposition "
                 "and cropping take out.\n\n"
                 "Resist the urge to add the full building dose every year. Compost carries "
                 "phosphorus that plants use slowly, and soil tests on heavily composted gardens "
                 "regularly show phosphorus levels far above what anything needs."),
                ("Work It In, or Lay It on Top",
                 "Forking the compost into the top few inches puts it where roots and soil life "
                 "use it immediately, and it is the right approach before planting a new bed. "
                 "The cost is that digging disturbs the soil structure and brings weed seeds to "
                 "the surface.\n\n"
                 "The no-dig alternative is to spread the same layer on the surface in autumn "
                 "and let worms pull it down. It works, just more slowly, and it suits beds that "
                 "are already planted. Both methods need the same volume; the calculator figure "
                 "does not change, only the timing."),
                ("Bags or Bulk for Amending a Bed",
                 "At 34 bags, the 2 in dressing for a 20 x 10 ft bed sits right at the crossover. "
                 "Bagged compost is cleaner to handle and easy to spread evenly a bag at a time, "
                 "but a single cubic yard of bulk compost, 1.23 yards is the order here, usually "
                 "costs noticeably less and involves no plastic.\n\n"
                 "Buy bulk if you have somewhere to tip it near the bed and a wheelbarrow to move "
                 "it. Buy bags if access is through the house or the bed is small. Either way, "
                 "check the compost is fully finished: dark, crumbly and earthy-smelling, not "
                 "hot or full of recognisable scraps."),
                ("Too Much Compost Is a Real Problem",
                 "Compost is an amendment, not a soil replacement. Beds filled with a half-and-"
                 "half mix or pure compost shrink by a third or more as the material continues to "
                 "break down, dry out faster than soil in summer, and can hold so much phosphorus "
                 "and soluble salt that some crops struggle.\n\n"
                 "If you have been adding compost generously for years, take a basic soil test "
                 "before the next dressing. If phosphorus comes back high, rest the bed from "
                 "compost for a season or two and mulch with bark or leaf mould instead, which "
                 "feed the soil without the phosphorus load."),
            ],
        ),
    },
]
