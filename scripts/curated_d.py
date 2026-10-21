"""Curated articles, part D (sod, bark, sand, compost)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-sod-do-i-need-for-1000-square-feet",
        "title": "How Much Sod for 1,000 Sq Ft: Rolls and Pallets",
        "cluster": "sod",
        "primary_keyword": "how much sod do i need for 1000 square feet",
        "secondary_keywords": ["how many rolls of sod for 1000 sq ft", "sod calculator",
                               "pallets of sod per 1000 square feet", "sod cost per square foot"],
        "calculator": "sod",
        "calculator_defaults": {"length": 40, "width": 25, "waste": 10},
        "meta_description": "1,000 sq ft of lawn needs 100 rolls of sod, or 110 with a 10% waste "
                            "allowance, roughly two pallets. Remove the beds and paths first.",
        "faq": [
            ("How many rolls of sod are in a pallet?",
             "A pallet usually holds 450 to 500 sq ft, which is 45 to 50 rolls at 10 sq ft each. "
             "Two pallets cover 1,000 sq ft with room for trimming."),
            ("How soon should sod be laid after delivery?",
             "Lay it the same day if you can. Sod is a living plant and starts to heat and yellow "
             "within a day or two in warm weather."),
            ("Do I need to rototill before laying sod?",
             "Yes. Loosen the top few inches, rake it level, and firm it so the roots make contact. "
             "Sod laid on hard ground dries out and dies at the seams."),
        ],
        "body": _body(
            lead=(
                "A 1,000 sq ft lawn needs 100 rolls of sod, which is 110 rolls once you add a 10% "
                "waste allowance, or about two pallets. Sod is sold by the roll, so the count matters "
                "more than the weight, and the count is driven by the area you actually have to cover."
                "\n\n"
                "Before you order, walk the area and subtract the beds, paths and anything you are not "
                "turfing. It is common to find that a tidy 1,000 sq ft measurement is closer to 850 "
                "once the borders come out, and that difference is several rolls. Getting the number "
                "right saves a return trip with a pallet that is already warming up."
            ),
            worked_lead=(
                "For a 40 foot by 25 foot lawn covered with sod, allowing 10% for cutting in around "
                "the edges:"
            ),
            bullets=(
                "*   length = 40\n"
                "*   width = 25\n"
                "*   waste = 10\n"
                "*   Square feet: 1000.0\n"
                "*   Rolls: 100\n"
                "*   Rolls with waste: 110\n"
                "*   Pallets: 2"
            ),
            sections=[
                ("How Sod Is Sold",
                 "Sod comes in rolls, and a standard roll covers about 10 sq ft, though some "
                 "suppliers cut 8 or 12 sq ft rolls. It is stacked on pallets of 450 to 500 sq ft. "
                 "Ordering by the pallet is normal for anything above a few hundred square feet, and "
                 "the supplier will usually round up to the nearest pallet.\n\n"
                 "Ask what size roll the supplier uses before you convert area to rolls. A 1,000 sq ft "
                 "lawn is 100 rolls at 10 sq ft, but 125 rolls at 8 sq ft, and that gap is a whole "
                 "extra pallet."),
                ("Measuring the Lawn and Removing What Is Not Turf",
                 "Measure the lawn in rectangles and add them together, the same way you would for "
                 "seed. Walk the boundary and note every bed, path, tree circle and shed footprint, "
                 "then subtract those areas. Slopes and curves are best measured by breaking them into "
                 "short straight sections.\n\n"
                 "Add the waste allowance at the end, not to each rectangle. Ten per cent covers the "
                 "cuts around edges and any roll that is damaged or short. If the lawn has many "
                 "corners or a lot of curves, lean towards 15%."),
                ("Preparing the Ground Before It Arrives",
                 "Sod is unforgiving about poor preparation. Clear weeds, rototill the top few inches, "
                 "and rake the surface level. Firm it with a roller or by treading it so the ground "
                 "does not settle under the turf, leaving hollows.\n\n"
                 "Water the prepared ground the day before so it is damp, not soaked, and have the "
                 "sprinkler ready. Lay the rolls in a brick pattern, butting the seams tight, and keep "
                 "them off any freshly watered mud until the last minute."),
                ("Watering and the First Few Weeks",
                 "New sod needs water every day for the first week or two, then every other day, then "
                 "weekly as it knits into the soil. Lift a corner after a week to check that roots are "
                 "reaching down; if the sod pulls up easily, it needs more water.\n\n"
                 "Keep foot traffic off it for at least two weeks, and hold off on fertiliser until the "
                 "roots have taken. Mow gently once the grass is a third taller than the height you "
                 "want, and never take more than a third of the blade at once."),
                ("Cost and Delivery for a 1,000 Sq Ft Lawn",
                 "Sod is priced per square foot, per roll, or per pallet, and a job this size usually clears the free-delivery threshold that smaller orders miss. Ask whether delivery is included and what roll size the supplier uses before comparing quotes, because an 8 sq ft roll needs a quarter more of them than a 10 sq ft roll for the same lawn."),
            ],
        ),
    },
    {
        "slug": "how-much-sod-do-i-need-for-a-20x20-lawn",
        "title": "How Much Sod for a 20x20 Lawn: Rolls and Cost",
        "cluster": "sod",
        "primary_keyword": "how much sod do i need for a 20x20 lawn",
        "secondary_keywords": ["sod for 400 square feet", "how many rolls of sod for 400 sq ft",
                               "20x20 sod cost", "sod rolls per square foot"],
        "calculator": "sod",
        "calculator_defaults": {"length": 20, "width": 20, "waste": 10},
        "meta_description": "A 20x20 ft lawn is 400 sq ft, which is 40 rolls of sod or 44 with waste, "
                            "about one pallet. Prep the soil and lay it the day it arrives.",
        "faq": [
            ("How many rolls of sod is 400 square feet?",
             "At the standard 10 sq ft roll, 400 sq ft is 40 rolls, or 44 once you add 10% for cuts "
             "and edges. That is a single pallet on most suppliers' counts."),
            ("How much does sod cost for 400 square feet?",
             "Sod is usually priced per square foot or per roll. A 400 sq ft job is a small order, so "
             "expect to pay a minimum delivery charge unless you collect it yourself."),
            ("Can I lay sod over an old lawn?",
             "No. Remove the old turf first, or the new sod roots into thatch and dies. Strip the top "
             "inch, improve the soil, then lay the fresh turf."),
        ],
        "body": _body(
            lead=(
                "A 20 x 20 ft lawn is 400 sq ft, which needs 40 rolls of sod, or 44 once you allow 10% "
                "for trimming around the edges. That is roughly one pallet. A small lawn like this is "
                "usually a single day's work, so the timing matters as much as the count.\n\n"
                "Because the job is small, the sod should be laid the day it is delivered. Turf is a "
                "living plant that begins to heat up in the stack, and a pallet left overnight in warm "
                "weather can yellow before it ever touches the ground. Order for a morning delivery and "
                "have the ground ready the day before."
            ),
            worked_lead=(
                "For a square lawn measuring 20 feet by 20 feet, allowing 10% for cutting in:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 20\n"
                "*   waste = 10\n"
                "*   Square feet: 400.0\n"
                "*   Rolls: 40\n"
                "*   Rolls with waste: 44\n"
                "*   Pallets: 1"
            ),
            sections=[
                ("Working Out the Area",
                 "Multiply the length by the width to get square feet, then divide by the roll size. A "
                 "20 x 20 ft lawn is 400 sq ft, and at 10 sq ft per roll that is 40 rolls. Add 10% for "
                 "the cuts around the boundary, which brings it to 44.\n\n"
                 "If the lawn is not square, split it into rectangles and add them. A 20 x 20 lawn with "
                 "a curved bed in one corner is really a smaller rectangle plus a sliver, and measuring "
                 "the sliver properly can save two or three rolls."),
                ("What a 20x20 Sod Job Costs",
                 "Sod is priced by the square foot, the roll, or the pallet, and the price swings with "
                 "the grass variety and the season. A 400 sq ft job sits below most suppliers' free "
                 "delivery threshold, so either collect it yourself or accept a small-order charge.\n\n"
                 "Budget for the preparation as well as the turf. Topsoil, compost and a roller hire can "
                 "add up, and sod laid on a poor base is money wasted. The turf is only as good as the "
                 "ground under it."),
                ("Preparing a Small Lawn",
                 "Strip any old turf, dig over the top few inches, and mix in compost if the soil is "
                 "heavy or sandy. Rake it level and firm it, then water it lightly so the surface is "
                 "damp. A small lawn is easy to get right because you can work the whole area by hand.\n\n"
                 "Check the levels with a straight edge and a spirit level. Hollows show up within weeks "
                 "as the sod settles, and fixing them later means lifting turf. Ten minutes with a rake "
                 "now avoids that."),
                ("Laying and Watering",
                 "Start at a straight edge and work across in a brick pattern, staggering the seams. "
                 "Butt the rolls tight and press them down so the roots contact the soil. Trim the "
                 "edges with a knife once the area is covered.\n\n"
                 "Water daily for the first week, then taper off. A 400 sq ft lawn is small enough to "
                 "water with a hose and sprinkler, so there is no excuse for letting it dry out. Keep "
                 "off it for two weeks and mow lightly after three."),
                ("Starting Small and Scaling Up",
                 "A small lawn is the easiest place to learn how sod behaves. Once you have laid 400 sq ft and watched it knit into the soil, a larger job holds no surprises: the same steps of clearing, levelling, laying and watering simply scale up. Doing one small area well teaches more than reading about a big one.\n\nIf you are collecting the sod yourself, take a friend and a tarpaulin. A pallet of turf is heavier than it looks and awkward to lift, and a load that slides about on the way home arrives bruised. Strap it down and drive gently."),
            ],
        ),
    },
    {
        "slug": "how-much-bark-do-i-need-for-600-square-feet",
        "title": "How Much Bark for 600 Sq Ft: Yards and Bags",
        "cluster": "bark",
        "primary_keyword": "how much bark do i need for 600 square feet",
        "secondary_keywords": ["bark chippings calculator", "bark for 600 sq ft",
                               "how many bags of bark for 600 square feet", "bark mulch coverage"],
        "calculator": "bark",
        "calculator_defaults": {"length": 30, "width": 20, "depth": 3},
        "meta_description": "600 sq ft at 3 in deep needs 150 cu ft of bark, which is 5.56 cubic yards "
                            "or 75 bags of 2 cu ft. Order by the yard for a job this size.",
        "faq": [
            ("How many bags of bark is a cubic yard?",
             "A cubic yard is 27 cu ft, so it is about 13 bags of 2 cu ft. At 3 in deep, 600 sq ft "
             "needs 5.56 cubic yards, which is 75 bags."),
            ("How deep should bark be spread?",
             "Three inches is the usual depth for weed control and moisture retention. Two inches "
             "works on a tidy border, but weeds push through it faster."),
            ("Does bark need replacing every year?",
             "Decorative bark breaks down slowly and usually lasts two to three years. Top up the "
             "thinnest patches each spring rather than replacing the lot."),
        ],
        "body": _body(
            lead=(
                "600 sq ft of border at 3 in deep needs 150 cu ft of bark, which is 5.56 cubic yards or "
                "75 bags of 2 cu ft. Bark is sold both bagged and loose, and at this volume the loose "
                "price per cubic foot is usually lower, so it pays to compare before ordering.\n\n"
                "The depth is what does the work. A three-inch layer shades out weed seed and slows "
                "evaporation, while a thin scattering does neither and still costs almost as much. Set "
                "the depth you want first, then let the area decide the volume."
            ),
            worked_lead=(
                "For a border measuring 30 feet by 20 feet, covered with bark to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 30\n"
                "*   width = 20\n"
                "*   depth = 3\n"
                "*   Square feet: 600.0\n"
                "*   Cubic feet: 150.0\n"
                "*   Cubic yards: 5.56\n"
                "*   2 cu ft bags: 75"
            ),
            sections=[
                ("Bark, Chippings and Composted Bark",
                 "Bark comes in three broad grades. Ornamental bark chippings are large and slow to "
                 "break down, so they last well on a display border. Composted bark is finer, darker "
                 "and partly rotted, which suits beds where you want the material to feed the soil as "
                 "it breaks down. Bark fines are the smallest grade, useful for pots and fine borders.\n\n"
                 "For weed suppression, the larger grades are better because they knit into a mat. For "
                 "improving the soil, the finer composted grade is better. Buying the right grade "
                 "matters as much as buying the right volume."),
                ("Coverage at Different Depths",
                 "Volume scales in a straight line with depth. At 2 in deep, 600 sq ft takes 100 cu ft, "
                 "or 3.7 cubic yards. At 3 in it takes 150 cu ft, or 5.56 cubic yards. At 4 in it takes "
                 "200 cu ft, or 7.41 cubic yards.\n\n"
                 "A cubic yard covers about 108 sq ft at 3 in deep. That single figure is the quickest "
                 "way to estimate a job: divide your area by 108 to get the yards you need, then add a "
                 "little for uneven ground."),
                ("Bags or Bulk for 600 Square Feet",
                 "Seventy-five bags is a lot of lifting, and the plastic adds to the cost. Loose bark "
                 "delivered by the cubic yard is almost always cheaper above two or three yards, and "
                 "600 sq ft at 3 in needs 5.56 yards, so bulk wins on price.\n\n"
                 "The catch is access and storage. A bulk delivery is tipped in one place and you move "
                 "it by wheelbarrow. If the border is at the back of the garden with no side access, "
                 "the saving may not be worth the effort, and bags become the sensible choice."),
                ("Laying Bark Without Smothering Plants",
                 "Clear weeds first, because bark suppresses new growth but does not kill established "
                 "weeds. Spread it to an even depth with a rake or by hand, working backwards so you do "
                 "not tread it down.\n\n"
                 "Keep the bark clear of stems and trunks. A layer piled against a shrub holds moisture "
                 "against the bark and invites rot. Leave a hand's width of bare soil around each "
                 "plant, and the border will look tidier and last longer."),
                ("Planning the Next Top-Up",
                 "Keep a note of the depth and the area. A border this size will want a light top-up the following spring, and knowing that 600 sq ft at 3 in takes five and a half yards makes reordering a two-minute job rather than a fresh calculation.\n\nBark also fades in strong sun, so a border that faces south may want a top-up sooner than one in shade. A light rake over the surface each spring lifts the colour and breaks up any matting before the new layer goes down."),
            ],
        ),
    },
    {
        "slug": "how-much-bark-do-i-need-for-200-square-feet",
        "title": "How Much Bark for 200 Sq Ft: Bags or Bulk",
        "cluster": "bark",
        "primary_keyword": "how much bark do i need for 200 square feet",
        "secondary_keywords": ["bark for 200 sq ft", "how many bags of bark for 200 square feet",
                               "bark chippings coverage", "bark mulch calculator"],
        "calculator": "bark",
        "calculator_defaults": {"length": 20, "width": 10, "depth": 3},
        "meta_description": "200 sq ft at 3 in deep takes 50 cu ft of bark, about 1.85 cubic yards or 25 "
                            "bags of 2 cu ft. At this size bags are usually the easier buy.",
        "faq": [
            ("How many bags of bark do I need for 200 square feet?",
             "At 3 in deep, 200 sq ft needs 50 cu ft, which is 25 bags of 2 cu ft. Bags are convenient "
             "at this size because there is no delivery charge and no pile to move."),
            ("How much area does a 2 cu ft bag of bark cover?",
             "A 2 cu ft bag covers about 8 sq ft at 3 in deep, or 12 sq ft at 2 in deep. Divide your "
             "area by that figure to get a rough bag count."),
            ("Can I use bark around vegetables?",
             "Bark is fine on paths and around fruit bushes, but keep it away from vegetable beds. It "
             "ties up nitrogen as it breaks down, which vegetable crops need."),
        ],
        "body": _body(
            lead=(
                "200 sq ft at 3 in deep takes 50 cu ft of bark, which is 1.85 cubic yards or 25 bags of "
                "2 cu ft. At this size the choice between bags and bulk is close, and convenience "
                "usually tips it towards bags because there is no delivery charge.\n\n"
                "A small border or island bed is easy to mulch in an afternoon. The main decision is "
                "depth: two inches is enough to tidy a border and hold some moisture, while three "
                "inches is what actually keeps weeds down for a season. Pick the depth for the job and "
                "the volume follows."
            ),
            worked_lead=(
                "For a border measuring 20 feet by 10 feet, covered with bark to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 10\n"
                "*   depth = 3\n"
                "*   Square feet: 200.0\n"
                "*   Cubic feet: 50.0\n"
                "*   Cubic yards: 1.85\n"
                "*   2 cu ft bags: 25"
            ),
            sections=[
                ("Bags Versus Bulk at This Size",
                 "Below about two cubic yards, bags are usually the simpler choice. Twenty-five bags "
                 "fit in a car boot over a couple of trips, there is no delivery fee, and you can use "
                 "part of the order now and keep the rest for another bed.\n\n"
                 "Bulk only becomes cheaper once the volume rises, and many suppliers set a minimum "
                 "delivery that a small order cannot justify. If you have other beds to do at the same "
                 "time, combining them into one bulk order can swing the decision the other way."),
                ("Choosing a Bark Grade",
                 "For a small display border, ornamental chippings give the neatest finish and last the "
                 "longest. Composted bark is finer and darker, which suits a mixed bed where you also "
                 "want the soil improved. Fines are best kept for pots.\n\n"
                 "Colour is worth a thought. Fresh chippings are pale and settle to a mid-brown, while "
                 "composted bark is dark from the start. If the bed sits against a light wall, the "
                 "darker grade often looks better and shows fewer weeds."),
                ("Getting the Depth Right",
                 "Three inches is the practical depth for weed control. Two inches looks tidy and "
                 "suppresses some weeds, but annual weeds push through it, and you will be back with "
                 "the hoe by midsummer. Four inches is rarely needed on a border and wastes material.\n\n"
                 "Spread it evenly rather than heaping it. An uneven layer leaves thin patches where "
                 "weeds appear first, and thick patches where water runs off instead of soaking in."),
                ("Mulching Around Plants",
                 "Water the border thoroughly before you mulch, because a dry layer of bark repels "
                 "light rain. Then spread the chippings to depth, working around the plants and keeping "
                 "the material clear of stems and trunks.\n\n"
                 "A hand's width of clear soil around each plant prevents rot and stops slugs using the "
                 "bark as cover to reach tender growth. It also makes the border easier to weed later, "
                 "because you can see the soil line."),
                ("Storing Spare Bark",
                 "The border will need a top-up each spring, so buy a couple of spare bags if you have somewhere dry to keep them. Matching the grade and colour later is easier when you know exactly what went down the first time, and a dry bag keeps for months.\n\nIf the border has shrubs that spread, mulch a little further out than the current spread. Roots move outwards each year, and mulch laid only to the old edge leaves the new growth on bare soil, where it dries out and weeds take hold.\n\nWeigh the trade-off between cost and effort honestly. If the border is a short wheelbarrow run from the road, bulk saves money; if it is up steps or through a narrow gate, the bags earn their premium. There is no single right answer, only the one that suits the access."),
            ],
        ),
    },
    {
        "slug": "how-much-sand-do-i-need-for-a-20x40-area",
        "title": "How Much Sand for a 20x40 Area: Yards and Tons",
        "cluster": "sand",
        "primary_keyword": "how much sand do i need for a 20x40 area",
        "secondary_keywords": ["sand calculator", "how many tons of sand for 800 sq ft",
                               "sand for a 20x40 pad", "sand coverage per ton"],
        "calculator": "sand",
        "calculator_defaults": {"length": 40, "width": 20, "depth": 3},
        "meta_description": "A 20x40 ft area at 3 in deep needs 7.41 cubic yards of sand, about 10 tons, "
                            "or 400 bags of 0.5 cu ft. Order bulk at this volume.",
        "faq": [
            ("How many tons is a cubic yard of sand?",
             "A cubic yard of sand weighs about 1.35 tons. At 3 in deep, an 800 sq ft area is 7.41 "
             "cubic yards, which is roughly 10 tons."),
            ("What is sand used for under a patio?",
             "A thin bedding layer of sharp sand levels the paving units and helps them seat evenly. "
             "It is not a structural base; that is compacted hardcore or gravel below it."),
            ("How deep should a sand bedding layer be?",
             "Twenty to thirty millimetres, about one inch, is typical for paving. Deeper layers "
             "compact unevenly and let the units rock."),
        ],
        "body": _body(
            lead=(
                "A 20 x 40 ft area at 3 in deep needs 7.41 cubic yards of sand, which is about 10 tons, "
                "or 400 bags of 0.5 cu ft. At this volume, bulk delivery is the only sensible option, "
                "because 400 bags is a fortnight of lifting and the plastic alone would cost more than "
                "the sand.\n\n"
                "Sand is heavy, and the weight is the number that catches people out. A cubic yard "
                "weighs about 1.35 tons, so 7.41 yards is close to 10 tons arriving on a lorry. Check "
                "the delivery access before you order, and have the tipping point decided in advance."
            ),
            worked_lead=(
                "For an area measuring 40 feet by 20 feet, filled with sand to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 40\n"
                "*   width = 20\n"
                "*   depth = 3\n"
                "*   Square feet: 800.0\n"
                "*   Cubic yards: 7.41\n"
                "*   Tons: 10.0\n"
                "*   0.5 cu ft bags: 400"
            ),
            sections=[
                ("Sand by the Yard, Ton or Bag",
                 "Sand is sold loose by the cubic yard or the ton, and bagged by the 0.5 or 1 cu ft "
                 "bag. The three units trip people up, so it helps to hold one conversion in mind: a "
                 "cubic yard is 27 cu ft and weighs about 1.35 tons.\n\n"
                 "Bagged sand is convenient for small jobs and for mixing, but it is expensive per "
                 "cubic foot. Anything above a couple of yards is cheaper loose, even after the "
                 "delivery charge, and a job like this one is far beyond the bagged range."),
                ("What Sand Is Used For",
                 "Sand turns up in three main garden and building jobs. As a bedding layer under "
                 "paving, a thin inch of sharp sand levels the units. As a base for artificial grass or "
                 "block paving, it is compacted in layers. As a soil improver, it opens up heavy clay, "
                 "though it takes a lot to make a difference.\n\n"
                 "The grade matters. Sharp sand has angular grains and locks together, so it is the one "
                 "for bedding and bases. Soft builder's sand is rounder and finer, and it compacts "
                 "poorly under load."),
                ("Coverage at Different Depths",
                 "Volume scales with depth. At 2 in, 800 sq ft takes 4.94 cubic yards, about 6.67 tons. "
                 "At 3 in it takes 7.41 cubic yards, about 10 tons. At 4 in it takes 9.88 cubic yards, "
                 "about 13.3 tons.\n\n"
                 "A cubic yard of sand covers about 108 sq ft at 3 in deep, the same figure as gravel "
                 "and mulch, because it is simply a volume spread over an area. Divide the area by 108 "
                 "to get a quick yard estimate."),
                ("Handling a Bulk Delivery",
                 "Ten tons of sand is a serious delivery. Decide where it will tip, put a tarpaulin "
                 "down to protect the surface, and plan the route to the work area before it arrives. A "
                 "wheelbarrow holds about a tenth of a cubic yard, so expect many trips.\n\n"
                 "If the ground is soft, the lorry may not be able to reach the spot, and some "
                 "suppliers will only tip on a hard road. Ask before ordering. Moving ten tons by hand "
                 "from the kerb is a long job, and it is cheaper to pay for a smaller delivery than to "
                 "spend a weekend shifting it."),
                ("Deciding How the Sand Will Be Used",
                 "It helps to know the job before the sand arrives. A bedding layer goes down thin, while a base is compacted in layers, and the two need different grades as well as different volumes. Ordering before the design is settled is how people end up with the wrong sand in the wrong quantity."),
            ],
        ),
    },
    {
        "slug": "how-much-sand-do-i-need-for-a-10x12-patio",
        "title": "How Much Sand for a 10x12 Patio: Bags and Tons",
        "cluster": "sand",
        "primary_keyword": "how much sand do i need for a 10x12 patio",
        "secondary_keywords": ["patio sand calculator", "sand bedding layer for paving",
                               "how many bags of sand for a patio", "sharp sand for paving"],
        "calculator": "sand",
        "calculator_defaults": {"length": 12, "width": 10, "depth": 2},
        "meta_description": "A 10x12 ft patio at 2 in deep takes 0.74 cubic yards of sand, about one "
                            "ton, or 40 bags of 0.5 cu ft. That is the bedding layer only.",
        "faq": [
            ("How much sand do I need under a patio?",
             "A bedding layer of about one inch under the paving units. For a 10x12 ft patio that is "
             "roughly 0.4 cubic yards, though the calculator here allows a deeper 2 in layer."),
            ("Is sharp sand or builder's sand better for paving?",
             "Sharp sand. Its angular grains interlock, so the bedding layer stays firm under the "
             "units. Builder's sand is too soft and lets the paving rock."),
            ("Do I need a base under the sand?",
             "Yes. Sand is a bedding layer, not a base. Below it you need compacted hardcore or gravel "
             "to carry the load and stop the patio sinking."),
        ],
        "body": _body(
            lead=(
                "A 10 x 12 ft patio at 2 in deep takes 0.74 cubic yards of sand, which is about one "
                "ton, or 40 bags of 0.5 cu ft. That figure is the bedding layer, and it sits on top of a "
                "compacted base, not directly on the soil.\n\n"
                "It is worth being clear about the layers, because sand alone will not hold a patio. "
                "The base of hardcore or gravel carries the weight and drains, and the sand levels the "
                "paving units so they seat evenly. Skip the base and the patio will settle and rock "
                "within a season."
            ),
            worked_lead=(
                "For a patio measuring 12 feet by 10 feet, with a sand bedding layer 2 inches deep:"
            ),
            bullets=(
                "*   length = 12\n"
                "*   width = 10\n"
                "*   depth = 2\n"
                "*   Square feet: 120.0\n"
                "*   Cubic yards: 0.74\n"
                "*   Tons: 1.0\n"
                "*   0.5 cu ft bags: 40"
            ),
            sections=[
                ("The Layers Under a Patio",
                 "A well-built patio is a sandwich. At the bottom is compacted hardcore or gravel, 4 to "
                 "6 in deep, which spreads the load and lets water drain. Above that is a thin bedding "
                 "layer of sharp sand, about an inch, which levels the paving. On top sits the paving "
                 "itself, with joints filled with kiln-dried sand.\n\n"
                 "Each layer has one job. The base carries weight, the bedding levels, and the joint "
                 "sand locks the units together. Confusing the bedding with the base is the most common "
                 "reason a patio sinks."),
                ("How Much Sand for the Bedding",
                 "The bedding layer is thin, so the volume is smaller than people expect. At one inch "
                 "deep, a 10 x 12 ft patio needs 0.37 cubic yards, about half a ton. At the two-inch "
                 "depth used here it is 0.74 cubic yards, about one ton.\n\n"
                 "That is why the sand for a patio is often bought in bags rather than by the lorry. "
                 "Forty bags is manageable in a car, and there is no minimum delivery charge to absorb. "
                 "For a larger patio, the numbers shift and bulk becomes worthwhile."),
                ("Choosing the Right Sand",
                 "Sharp sand, also called concrete sand or grit sand, is the correct choice. Its "
                 "angular grains lock together under the paving and hold the units steady. Soft "
                 "builder's sand has rounded grains that shift, so the patio rocks and the joints open.\n\n"
                 "For the joints themselves, use kiln-dried sand, which flows into the gaps and sets "
                 "firm. It is a different product from the bedding sand, so do not try to use one for "
                 "both jobs."),
                ("Laying the Bedding Layer",
                 "Compact the base, then spread the sharp sand to an even depth and screed it level. "
                 "Use a straight edge across two rails to get a flat surface, because the paving will "
                 "follow whatever the sand does.\n\n"
                 "Lay the units onto the loose sand and tap them down with a rubber mallet, checking the "
                 "level as you go. Do not walk on the finished bedding ahead of the paving, and work "
                 "from one corner so you are always standing on laid units rather than disturbed sand."),
                ("Keeping Leftover Sand",
                 "Keep the leftover sand covered and dry. A part bag is useful for pointing, for bedding a loose slab, or for topping up a low corner later, and it costs nothing to keep compared with buying a fresh bag for a small repair.\n\nCheck the base before you lay the sand. A base that is not compacted will settle under the bedding, and the patio will dip no matter how level the sand was. Take the extra time on the base and the rest of the job goes smoothly.\n\nOrder a little more than the calculation suggests for the bedding, because screeding always loses some sand to the edges and the joints. Half a bag spare is cheaper than stopping the job to fetch one more, and any excess is useful for pointing later."),
            ],
        ),
    },
    {
        "slug": "how-much-compost-do-i-need-for-400-square-feet",
        "title": "How Much Compost for 400 Sq Ft: Yards and Bags",
        "cluster": "compost",
        "primary_keyword": "how much compost do i need for 400 square feet",
        "secondary_keywords": ["compost calculator", "how many bags of compost for 400 sq ft",
                               "compost coverage per square foot", "compost depth for garden beds"],
        "calculator": "compost",
        "calculator_defaults": {"length": 20, "width": 20, "depth": 2},
        "meta_description": "400 sq ft dressed 2 in deep needs 66.7 cu ft of compost, which is 2.47 cubic "
                            "yards or 67 bags of 1 cu ft. A 2 in layer suits most beds.",
        "faq": [
            ("How deep should compost be spread on a bed?",
             "One to two inches worked into the topsoil is right for most beds. Three inches or more is "
             "for a new bed being built up, or a soil that is very poor."),
            ("How many bags of compost is a cubic yard?",
             "A cubic yard is 27 cu ft, so it is 27 bags of 1 cu ft. At 2 in deep, 400 sq ft needs "
             "2.47 cubic yards, which is 67 bags."),
            ("Can you put too much compost on a garden?",
             "Yes. Repeated heavy dressings raise phosphorus and salts. A soil test every few years "
             "tells you whether the bed actually needs more."),
        ],
        "body": _body(
            lead=(
                "400 sq ft dressed 2 in deep needs 66.7 cu ft of compost, which is 2.47 cubic yards or "
                "67 bags of 1 cu ft. Compost is a soil improver, not a mulch, so the depth and the way "
                "you apply it matter more than the volume alone.\n\n"
                "A two-inch layer worked into the top few inches of soil feeds the bed and improves its "
                "structure. Piling it on the surface without digging it in does far less, and a layer "
                "that is too thick can smother the soil beneath. Match the depth to what the bed needs."
            ),
            worked_lead=(
                "For a bed measuring 20 feet by 20 feet, dressed with compost to a 2-inch depth:"
            ),
            bullets=(
                "*   length = 20\n"
                "*   width = 20\n"
                "*   depth = 2\n"
                "*   Square feet: 400.0\n"
                "*   Cubic feet: 66.7\n"
                "*   Cubic yards: 2.47\n"
                "*   1 cu ft bags: 67"
            ),
            sections=[
                ("How Much Compost and How Deep",
                 "A one to two-inch layer worked into the topsoil is the standard dressing for an "
                 "established bed. New beds, or beds on poor ground, sometimes take three or four "
                 "inches to build the soil up. The volume scales with depth, so decide the depth before "
                 "you order.\n\n"
                 "More is not better. Compost is rich in nutrients, and repeated heavy applications "
                 "build up phosphorus and soluble salts, which harms plants. A soil test every few "
                 "years is the honest way to know whether the bed needs feeding at all."),
                ("Compost, Mulch or Topsoil",
                 "The three are often confused. Compost is decomposed organic matter, used to feed the "
                 "soil and improve its structure. Mulch is a surface layer, often bark or woodchip, "
                 "used to suppress weeds and hold moisture. Topsoil is the growing medium itself, used "
                 "to raise levels or fill beds.\n\n"
                 "For a bed that needs feeding, compost is right. For a bed that needs filling, "
                 "topsoil. For a bed that needs a weed-suppressing surface, mulch. Mixing them up "
                 "wastes money and does the wrong job."),
                ("Bagged Compost Versus Bulk",
                 "Sixty-seven bags is a lot of plastic and a lot of lifting, so bulk is worth "
                 "considering above a cubic yard or so. Bulk compost is delivered by the yard and "
                 "tipped in one place, which is cheaper per cubic foot but needs access and somewhere "
                 "to put it.\n\n"
                 "For a bed at the front of the house with easy access, bulk wins. For a bed at the "
                 "back with no side gate, bags may be the only practical route, and the extra cost is "
                 "the price of convenience."),
                ("Working Compost Into the Soil",
                 "Spread the compost over the bed to an even depth, then dig or fork it into the top "
                 "few inches. On a no-dig bed, spread it on the surface and let the worms pull it down "
                 "over the season. Both work; the digging version is faster.\n\n"
                 "Do not leave a thick layer sitting on the surface unworked for long, because it can "
                 "form a crust that sheds water. Water the bed after spreading if rain is not due, and "
                 "avoid working wet soil, which damages its structure."),
                ("Where the Compost Comes From",
                 "It pays to know the source. Well-rotted garden compost and a bought soil conditioner behave differently, and a bed that has had one may need less of the other. A soil test takes the guesswork out and tells you whether the bed needs feeding at all this year.\n\nSpread the compost when the soil is damp but not wet, and work it in within a day or two of delivery. Compost left in a heap against a wall can go sour, and a bed dressed and then left unplanted for weeks loses some of the benefit to rain and weeds."),
            ],
        ),
    },
    {
        "slug": "how-much-compost-do-i-need-for-100-square-feet",
        "title": "How Much Compost for 100 Sq Ft: Bags and Cost",
        "cluster": "compost",
        "primary_keyword": "how much compost do i need for 100 square feet",
        "secondary_keywords": ["compost for 100 sq ft", "how many bags of compost for 100 square feet",
                               "compost coverage", "compost for a small bed"],
        "calculator": "compost",
        "calculator_defaults": {"length": 10, "width": 10, "depth": 2},
        "meta_description": "100 sq ft at 2 in deep needs 16.7 cu ft of compost, about 0.62 cubic yards "
                            "or 17 bags of 1 cu ft. Bags are the simple choice at this size.",
        "faq": [
            ("How many bags of compost for 100 square feet?",
             "At 2 in deep, 100 sq ft needs 16.7 cu ft, which is 17 bags of 1 cu ft. For a bed this "
             "size, bags are easier than a bulk delivery."),
            ("How much area does a 1 cu ft bag of compost cover?",
             "A 1 cu ft bag covers about 6 sq ft at 2 in deep, or 12 sq ft at 1 in deep. Divide your "
             "area by that to get a rough bag count."),
            ("Can I make my own compost for a small bed?",
             "Yes. A small bed is well within reach of a home bin. A cubic yard of finished compost is "
             "roughly 27 bags, which is more than most bins produce in a year."),
        ],
        "body": _body(
            lead=(
                "100 sq ft at 2 in deep needs 16.7 cu ft of compost, which is about 0.62 cubic yards or "
                "17 bags of 1 cu ft. For a bed this size, bags are the practical choice: there is no "
                "delivery charge, no pile to move, and you can buy exactly what you need.\n\n"
                "A small bed is also the easiest place to get compost right. You can spread it by hand, "
                "work it into the top few inches with a fork, and see the difference within a season. "
                "The volume is small enough that a couple of bags either way makes little difference to "
                "the cost."
            ),
            worked_lead=(
                "For a bed measuring 10 feet by 10 feet, dressed with compost to a 2-inch depth:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   depth = 2\n"
                "*   Square feet: 100.0\n"
                "*   Cubic feet: 16.7\n"
                "*   Cubic yards: 0.62\n"
                "*   1 cu ft bags: 17"
            ),
            sections=[
                ("How Deep to Dress a Small Bed",
                 "One to two inches is right for most established beds. Work it into the top few inches "
                 "of soil so it feeds the roots and improves structure. A new bed on poor ground may "
                 "take three inches to build it up, but that is the exception.\n\n"
                 "At this scale you can be precise. Spread half the compost, fork it in, then judge "
                 "whether the bed needs the rest. It is easier to add more than to take it back out."),
                ("Bagged Versus Bulk for a Small Area",
                 "Seventeen bags is a comfortable car load, and there is no minimum delivery to worry "
                 "about. Bulk compost makes no sense at a fraction of a cubic yard, because the "
                 "delivery charge alone would cost more than the material.\n\n"
                 "Buying bags also lets you choose a specific type. Seed and potting composts are "
                 "different products from soil conditioner, and a small bed gives you the room to pick "
                 "the right one rather than taking whatever the lorry brought."),
                ("What to Look For in Bagged Compost",
                 "Good compost smells earthy and crumbles in the hand. If it smells sour or is heavy and "
                 "waterlogged, it has not finished breaking down and will not do the soil much good. "
                 "Check the bag for the intended use: soil conditioner for beds, multi-purpose for "
                 "containers.\n\n"
                 "Peat-free composts have improved a great deal and are now the default in many stores. "
                 "They behave slightly differently, drying out faster and needing a little more water, "
                 "but they work well in beds and are the better environmental choice."),
                ("Applying Compost to a Small Bed",
                 "Spread the compost to an even depth, then fork it into the top few inches. On a "
                 "no-dig bed, spread it on the surface and let the worms take it down. Water it in if "
                 "rain is not due, and avoid walking on the bed while it is wet.\n\n"
                 "Mark the bed and keep a note of how much you used. The same bed next year will need "
                 "roughly the same amount, and knowing that makes the next order a one-minute job."),
                ("Trying a New Method on a Small Bed",
                 "A small bed is the ideal size for trying a new compost or a no-dig approach without committing a large area. If it works, the same method scales up to the rest of the garden next season, and if it does not, the cost of the experiment is one bed.\n\nWear gloves and a mask when you open a dusty bag, and wash your hands afterwards. Bought compost is usually clean, but garden compost and soil conditioners can carry dust that irritates the lungs, and it costs nothing to be careful."),
            ],
        ),
    },
]
