"""Curated articles, part A (mulch, sand, tile)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-mulch-do-i-need-for-a-playground",
        "title": "How Much Mulch for a Playground: Depth & Bag Counts",
        "cluster": "mulch",
        "primary_keyword": "how much mulch do i need for a playground",
        "secondary_keywords": ["playground mulch depth", "how much rubber mulch for a playground",
                               "playground mulch calculator", "how many bags of mulch for a playground"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 30, "width": 30, "depth": 6},
        "meta_description": "A 30x30 ft playground needs 450 cu ft of mulch at 6 in deep, about "
                            "16.67 cu yd or 225 bags. Match the depth to the fall height.",
        "faq": [
            ("How deep should playground mulch be?",
             "Six inches is a common starting point for equipment up to about 5 feet high; "
             "taller climbers need 9 to 12 inches. Check the manufacturer's fall-height table."),
            ("Should I use wood chips or rubber mulch?",
             "Engineered wood fibre and rubber both cushion falls. Rubber lasts far longer and "
             "does not compact, but costs several times more per square foot."),
            ("How do I stop the mulch spreading?",
             "Excavate to the depth you want, line the area with geotextile, and edge the "
             "perimeter so the surface stays level with the surrounding grass."),
        ],
        "body": _body(
            lead=(
                "A 30 x 30 ft playground at 6 in deep needs 450 cu ft of mulch, which is 16.67 cu yd "
                "or 225 bags of 2 cu ft. Depth, not area, is the number that keeps a play area safe, "
                "so set that first and let the calculator work out the volume.\n\n"
                "Playground surfacing is judged against the height a child can fall from, not by how "
                "the bed looks. A bed that is generous in area but only 3 in deep fails the same test "
                "as one that is too small, and it needs topping up far sooner. Buying the right "
                "volume the first time saves a second order partway through the build."
            ),
            worked_lead=(
                "For a square play area measuring 30 feet by 30 feet, mulched to a 6-inch depth:"
            ),
            bullets=(
                "*   length = 30\n"
                "*   width = 30\n"
                "*   depth = 6\n"
                "*   Square feet: 900.0\n"
                "*   Cubic feet: 450.0\n"
                "*   Cubic yards: 16.67\n"
                "*   2 cu ft bags: 225"
            ),
            sections=[
                ("Choosing the Depth for the Fall Height",
                 "The depth you need depends on the highest platform a child can reach. As a rough "
                 "guide, equipment up to 4 feet high is usually specified at 6 in of loose fill, and "
                 "climbers up to 8 feet commonly call for 9 to 12 in. Swings need more depth over a "
                 "wider footprint, because a child travels further through the air.\n\n"
                 "Loose fill also settles and compacts underfoot, and it thins fastest exactly where "
                 "children land. Budget for a top-up each year, because the surface that cushions a "
                 "fall is the loose layer on top, not the compacted material below it."),
                ("How Much Mulch for Common Playground Sizes",
                 "The volume scales with area at a fixed depth. A 10 x 10 ft area at 6 in deep takes "
                 "50 cu ft, a 20 x 20 ft play zone takes 200 cu ft, and a 30 x 30 ft area takes the "
                 "450 cu ft worked out above.\n\n"
                 "Run your own measurements through the playground mulch calculator rather than "
                 "scaling from a table, because play areas are rarely square. Measure each rectangle "
                 "separately if the equipment sits in an L or T shape, and add the volumes together."),
                ("Wood Chips, Engineered Fibre or Rubber",
                 "Three materials dominate home play areas. Wood chips are the cheapest and drain "
                 "well, but they break down and need replacing every year or two. Engineered wood "
                 "fibre (EWF) is shredded and tested for impact absorption, so it holds its rating "
                 "longer. Rubber mulch lasts the longest and stays loose, but costs several times "
                 "more and can get uncomfortably hot in direct sun.\n\n"
                 "Whichever you choose, keep the layer loose. Raking it over each season restores the "
                 "cushioning that foot traffic flattens, and it takes only a few minutes."),
                ("Preparing and Edging the Area",
                 "Clear the ground and dig out to your target depth so the finished surface sits "
                 "flush with the lawn. A geotextile membrane underneath stops weeds and keeps the "
                 "chips from working into the soil. Edge the perimeter with timber or steel so the "
                 "fill stays in place and does not spill onto grass.\n\n"
                 "If the site holds water, add a shallow drainage trench before you lay anything. "
                 "Standing water under a play surface turns the base to mud and speeds decay, and it "
                 "is far easier to fix before the mulch goes down than after."),
                ("Keeping the Surface Safe Over Time",
                 "Check the depth every few months at the spots under swings and at the bottom of "
                 "slides, where the fill compacts fastest. Top those areas up rather than spreading a "
                 "thin layer over the whole bed. Keep the surface raked and free of buried toys, "
                 "which are what turn a soft landing into a hard one.\n\n"
                 "Inspect the timber edging and the equipment fixings at the same time. A loose bolt "
                 "or a rotted edge board matters more to safety than an inch of mulch either way."),
                ("Common Mistakes to Avoid",
                 "*   Mulching a large area too shallow, because area without depth cushions nothing.\n"
                 "*   Skipping the weed membrane, then fighting weeds through the chips.\n"
                 "*   Forgetting the annual top-up, so the surface thins where feet land most.\n"
                 "*   Buying bags when bulk delivery is far cheaper above about 10 cu yd.\n"
                 "*   Letting the fill spill over the edge and thin out in the middle."),
            ],
        ),
    },
    {
        "slug": "how-much-mulch-do-i-need-around-a-tree",
        "title": "How Much Mulch Around a Tree: Depth, Ring Size, Bags",
        "cluster": "mulch",
        "primary_keyword": "how much mulch do i need around a tree",
        "secondary_keywords": ["mulch ring size for a tree", "mulch volcano", "how deep to mulch a tree",
                               "how many bags of mulch around a tree"],
        "calculator": "mulch",
        "calculator_defaults": {"length": 6, "width": 6, "depth": 3},
        "meta_description": "A 6x6 ft mulch ring at 3 in deep needs 9 cu ft of mulch, about 0.33 cu yd "
                            "or 5 bags. Keep the mulch clear of the trunk.",
        "faq": [
            ("How wide should a mulch ring be?",
             "Three to five feet out from the trunk is typical for a young tree. A wider ring over "
             "the root zone is better than a deep one."),
            ("Why should mulch not touch the trunk?",
             "Mulch held against bark traps moisture and invites rot, and it gives rodents cover "
             "to gnaw the bark. Pull it back a few inches."),
            ("What is a mulch volcano?",
             "A cone of mulch piled against the trunk. It looks tidy and harms the tree, because "
             "roots suffocate and the bark stays wet."),
        ],
        "body": _body(
            lead=(
                "A 6 x 6 ft mulch ring at 3 in deep needs 9 cu ft of mulch, which is 0.33 cu yd or "
                "5 bags of 2 cu ft. The ring should be wide rather than deep, and the mulch should "
                "never touch the trunk.\n\n"
                "A tree's fine roots sit in the top few inches of soil and reach well past the "
                "canopy. Mulching that zone holds moisture and keeps mowers and string trimmers away "
                "from the bark, which is where most young trees are damaged. A bag or two of mulch is "
                "cheap insurance for a tree that will stand for decades."
            ),
            worked_lead=(
                "For a square mulch ring measuring 6 feet by 6 feet, spread to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 6\n"
                "*   width = 6\n"
                "*   depth = 3\n"
                "*   Square feet: 36.0\n"
                "*   Cubic feet: 9.0\n"
                "*   Cubic yards: 0.33\n"
                "*   2 cu ft bags: 5"
            ),
            sections=[
                ("Size the Ring, Not Just the Depth",
                 "Work out the ring from the trunk outwards, not the whole canopy. For a young tree, "
                 "three to five feet in every direction is a good start; a mature tree can take a "
                 "ring that reaches the drip line, where the rain falls off the leaves.\n\n"
                 "A wide, shallow ring does more for the tree than a narrow, deep one. The goal is to "
                 "cover the root zone and suppress competition from grass, not to bury the roots. If "
                 "you only have a couple of bags, spend them on width."),
                ("Keep the Mulch Off the Trunk",
                 "Leave a gap of a few inches between the mulch and the bark. Mulch pressed against "
                 "the trunk holds moisture there, softens the bark, and lets rodents work unseen. "
                 "Spread the mulch level rather than mounded, and taper it down towards the trunk.\n\n"
                 "The mounded shape people build around trees, often called a mulch volcano, is the "
                 "single most common mistake. It traps water against the trunk and starves the roots "
                 "of oxygen, and the damage often shows up a season or two later."),
                ("Depth and Refresh Rate",
                 "Two to four inches is the working range. Deeper than that and water struggles to "
                 "reach the soil, and roots grow up into the mulch instead of down into the ground. "
                 "Organic mulch breaks down over a season, so top it up in spring rather than adding "
                 "one thick layer.\n\n"
                 "Before topping up, rake the old layer to break up any matted surface. A matted top "
                 "sheds water instead of letting it through, which is the opposite of what the tree "
                 "needs in a dry summer."),
                ("Mulching a Newly Planted Tree",
                 "A new tree benefits most from mulch in its first three years, while it is "
                 "establishing. Keep the ring clear of grass and weeds, which compete directly for "
                 "water and nutrients, and keep the mulch away from the trunk as always.\n\n"
                 "Do not fertilise a newly planted tree to push growth. Roots need to spread first, "
                 "and mulch is enough. Water deeply and less often so the roots chase moisture down "
                 "into the soil rather than staying at the surface."),
                ("Weed Control and Watering",
                 "A mulch ring is the easiest weed control you can give a tree. A two to four inch "
                 "layer stops most annual weeds germinating, and any that do appear are easy to pull "
                 "from loose mulch. Avoid landscape fabric under the mulch if you can, because it "
                 "can girdle roots as the tree grows.\n\n"
                 "Water the tree before you mulch, then let the mulch hold that moisture. In the "
                 "first summer after planting, a deep soak every week or two does more than a daily "
                 "sprinkle, which only wets the surface."),
                ("Common Mistakes to Avoid",
                 "*   Piling mulch against the trunk in a cone.\n"
                 "*   Going deeper than 4 in to save a trip for more bags.\n"
                 "*   Mulching right up to the base of a grafted tree, which invites rot.\n"
                 "*   Using fresh wood chips that rob nitrogen as they break down.\n"
                 "*   Making the ring too narrow, so grass still competes at the roots."),
            ],
        ),
    },
    {
        "slug": "how-much-sand-do-i-need-for-a-sandbox",
        "title": "How Much Sand for a Sandbox: Depth and Bag Counts",
        "cluster": "sand",
        "primary_keyword": "how much sand do i need for a sandbox",
        "secondary_keywords": ["sandbox sand depth", "play sand calculator",
                               "how many bags of sand for a sandbox", "how deep should sandbox sand be"],
        "calculator": "sand",
        "calculator_defaults": {"length": 4, "width": 4, "depth": 3},
        "meta_description": "A 4x4 ft sandbox filled 3 in deep needs 0.15 cu yd of sand, about 0.2 tons "
                            "or 8 bags of 0.5 cu ft. Use washed play sand, not builder's sand.",
        "faq": [
            ("How deep should sand be in a sandbox?",
             "Two to four inches is enough to dig and build with. Deeper sand is harder to keep "
             "clean and heavier to turn over."),
            ("Which sand is safe for a sandbox?",
             "Use washed, rounded play sand. Builder's sand and sharp sand are dusty and angular, "
             "and some contain crystalline silica."),
            ("How often should sandbox sand be replaced?",
             "Refresh it every year or two, and cover the box when it is not in use to keep out "
             "leaves, rain and animals."),
        ],
        "body": _body(
            lead=(
                "A 4 x 4 ft sandbox filled 3 in deep needs 0.15 cu yd of sand, which is about 0.2 "
                "tons or 8 bags of 0.5 cu ft. Buy washed play sand rather than builder's sand, and "
                "keep the layer to a few inches.\n\n"
                "Sand quantity is easy to overestimate. The box looks large, but a shallow layer "
                "over that footprint is a small volume, and sand is heavy enough that a wrong guess "
                "is felt in the back rather than the wallet. Weighing the options before you buy "
                "saves both a return trip and a wasted bag."
            ),
            worked_lead=(
                "For a square sandbox measuring 4 feet by 4 feet, filled to a 3-inch depth:"
            ),
            bullets=(
                "*   length = 4\n"
                "*   width = 4\n"
                "*   depth = 3\n"
                "*   Square feet: 16.0\n"
                "*   Cubic yards: 0.15\n"
                "*   Tons: 0.2\n"
                "*   0.5 cu ft bags: 8"
            ),
            sections=[
                ("Pick the Right Sand",
                 "Play sand is washed and rounded. Builder's sand and sharp sand are angular and "
                 "dusty, and the dust is a breathing hazard when it dries out. Look for a bag "
                 "labelled as play sand and, where it is stated, free of crystalline silica.\n\n"
                 "Coloured play sand is usually coated quartz. It is safe, but the dye can transfer "
                 "to hands and clothes when wet, so plain washed sand is the simpler choice. Avoid "
                 "any sand that has been treated for construction use, since additives are not meant "
                 "for play."),
                ("Depth, Drainage and Cover",
                 "Two to four inches lets children dig and build without turning the whole box into "
                 "a quarry. Any deeper and the sand is harder to sift clean and heavier to rake. "
                 "Deeper sand also stays damp at the bottom, which is where mould starts.\n\n"
                 "A sandbox needs to drain. If the base is solid, drill holes or set the box on "
                 "gravel so rain does not pool. A fitted cover keeps out leaves and, more "
                 "importantly, keeps cats out, which is the main reason sand has to be replaced."),
                ("How Much to Order",
                 "Small boxes are cheapest to fill by the bag, because a 0.5 cu ft bag is easy to "
                 "carry and you can stop when the box is full. Larger boxes tip over into bulk "
                 "territory: above about half a cubic yard, a bulk bag or a delivery is cheaper per "
                 "cubic foot.\n\n"
                 "Leave the sand an inch or two below the rim so it does not spill over the sides "
                 "when the box is covered. A box that is overfilled loses sand with every rainstorm "
                 "and every cover that goes back on."),
                ("Keeping the Sand Clean",
                 "Rake the sand once a week to bring debris to the surface and remove it. Sift out "
                 "leaves and twigs, which rot down and stain the sand. If the box is uncovered, "
                 "check it before children use it, since animals treat an open box as a litter tray.\n\n"
                 "Replace the sand every year or two, or sooner if it smells sour or has been "
                 "soiled. Sand is cheap compared with the effort of scrubbing a box that has gone "
                 "bad, and a fresh fill gives the whole toy a second life."),
                ("Building the Box",
                 "A sandbox needs a solid base or a weed membrane underneath, so sand does not "
                 "disappear into the soil and weeds do not come up through it. Timber boxes are "
                 "simplest, and a hinged lid doubles as a bench. Line the base with landscape fabric "
                 "before the sand goes in.\n\n"
                 "Leave the box open at the bottom only if you have laid gravel and drainage first. "
                 "A box set directly on soil will lose sand to the ground and gain weeds within a "
                 "season."),
                ("Common Mistakes to Avoid",
                 "*   Filling to the rim, then losing sand over the edge on the first wet day.\n"
                 "*   Using builder's sand, which is dusty and unpleasant to play in.\n"
                 "*   Skipping a cover and having to replace the sand every season.\n"
                 "*   Forgetting drainage, so the sand turns to a wet slab after rain.\n"
                 "*   Buying bulk for a small box, where bagged sand is easier to handle."),
            ],
        ),
    },
    {
        "slug": "how-many-6-inch-tiles-do-i-need",
        "title": "How Many 6 Inch Tiles Do I Need? Count and Waste",
        "cluster": "tile",
        "primary_keyword": "how many 6 inch tiles do i need",
        "secondary_keywords": ["6x6 tile coverage", "how many 6x6 tiles per square foot",
                               "6 inch tile calculator", "how many tiles in a box of 6x6"],
        "calculator": "tile",
        "calculator_defaults": {"length": 10, "width": 10, "tile_w": 6, "tile_h": 6, "waste": 10},
        "meta_description": "A 10x10 ft floor in 6x6 in tiles needs 400 tiles, or 441 with 10% waste. "
                            "Each 6x6 tile covers a quarter of a square foot.",
        "faq": [
            ("How many 6x6 tiles are in a square foot?",
             "Four. A 6 in square is a quarter of a square foot, so a square foot holds exactly "
             "four of them."),
            ("How many 6x6 tiles come in a box?",
             "It varies by maker. Boxes are usually sold by coverage in square feet, so read the "
             "box area rather than counting tiles."),
            ("How much waste should I add for small tiles?",
             "Add 10% for a straight layout and 15% for diagonal or offset patterns. Small tiles "
             "mean more cuts along every edge."),
        ],
        "body": _body(
            lead=(
                "A 10 x 10 ft floor laid in 6 x 6 in tiles needs 400 tiles, or 441 once you add 10% "
                "for waste. Each 6 in tile covers a quarter of a square foot, so four tiles cover "
                "one square foot.\n\n"
                "Small tiles are counted, not measured by coverage, and the count rises quickly as "
                "the tile shrinks. Working from square footage and tile size keeps the arithmetic "
                "honest, especially once waste and cuts are included. A 6 in tile is a quarter of "
                "the area of a 12 in tile, so the same floor needs four times as many."
            ),
            worked_lead=(
                "For a 10 foot by 10 foot floor using 6 x 6 inch tiles with a 10% waste allowance:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 10\n"
                "*   tile_w = 6\n"
                "*   tile_h = 6\n"
                "*   waste = 10\n"
                "*   Floor area: 100.0\n"
                "*   Tile area: 0.25\n"
                "*   Tiles: 400\n"
                "*   Tiles with waste: 441"
            ),
            sections=[
                ("Work From Square Feet, Not Tile Count",
                 "Divide the floor area by the area of one tile. A 6 x 6 in tile is 36 sq in, which "
                 "is 0.25 sq ft, so four tiles make a square foot and a 100 sq ft floor needs 400 of "
                 "them. Measure each rectangular area and add them up before you divide.\n\n"
                 "Grout lines add a little, but the effect is small for a 6 in tile and is normally "
                 "swamped by the waste allowance. If you want to be precise, add the joint width to "
                 "each tile dimension before dividing, which accounts for the few millimetres of "
                 "grout between tiles."),
                ("Add Waste for Cuts",
                 "Every edge, corner and fixture forces a cut, and small tiles mean more of them. "
                 "Add 10% for a simple straight layout, 15% for diagonal or offset work, and up to "
                 "20% for a busy floor with many obstacles. A small bathroom can sit at the top of "
                 "that range once the toilet, basin and door frame are allowed for.\n\n"
                 "Keep the offcuts. A part-box of spare tiles is the only way to repair a cracked "
                 "tile later, because dye lots shift between production runs and a fresh box may not "
                 "match."),
                ("Buying by Box",
                 "Boxes are usually labelled with the coverage in square feet rather than a tile "
                 "count. Multiply the number of boxes by the box coverage and compare that with the "
                 "tiles-with-waste figure, then round up. If the box covers 10 sq ft, a 100 sq ft "
                 "floor needs 11 boxes to leave the waste covered.\n\n"
                 "Buy the whole job in one order so it comes from a single dye lot. Two deliveries "
                 "of the same product can differ enough in tone to show as a patch, and no amount of "
                 "grout hides that."),
                ("Laying a 6 Inch Tile Floor",
                 "Small tiles suit rooms with awkward shapes, because there is less waste around "
                 "fittings and the pattern flexes to the space. Plan the layout from the centre of "
                 "the room outwards, so the cut tiles end up along the walls rather than in the "
                 "middle of the floor.\n\n"
                 "Use a notched trowel sized for the tile and comb the adhesive in one direction. "
                 "Back-butter any tile that sits over a hollow in the floor. Leave the spacers in "
                 "until the adhesive sets, then grout once the tiles are firm."),
                ("Where 6 Inch Tiles Work Best",
                 "Six inch tiles are a classic choice for bathroom floors, utility rooms and "
                 "hallways, where their grip and small format suit the space. They also handle "
                 "uneven subfloors better than large format tiles, because each small tile can "
                 "follow the surface without rocking.\n\n"
                 "On a wall, they read as a traditional splashback and can be laid in a grid or "
                 "offset pattern. In a large open room, a 6 in tile can look busy, so consider a "
                 "larger format there and keep the small tile for the smaller rooms."),
                ("Common Mistakes to Avoid",
                 "*   Counting tiles and forgetting the waste allowance.\n"
                 "*   Buying box by box over several weeks, which mixes dye lots.\n"
                 "*   Forgetting that small tiles multiply the number of cuts.\n"
                 "*   Not keeping spares, then having no match for a later repair.\n"
                 "*   Starting the layout at a wall, so the cut tiles land in the doorway."),
            ],
        ),
    },
]
