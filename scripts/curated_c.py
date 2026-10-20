"""Curated articles, part C (soil, topsoil, bark, compost)."""
from __future__ import annotations

from curated_articles import _body

ARTICLES: list[dict] = [
    {
        "slug": "how-much-soil-for-an-8x4-raised-bed",
        "title": "How Much Soil for an 8x4 Raised Bed? Bags and Yards",
        "cluster": "soil",
        "primary_keyword": "how much soil for an 8x4 raised bed",
        "secondary_keywords": ["raised bed soil calculator", "soil for 4x8 raised bed",
                               "how many bags of soil for a raised bed", "raised bed soil mix"],
        "calculator": "soil",
        "calculator_defaults": {"length": 8, "width": 4, "height": 12},
        "meta_description": "An 8x4 ft raised bed filled 12 in deep needs 32 cu ft of soil, about 1.19 "
                            "cu yd or 22 bags of 1.5 cu ft. Blend topsoil with compost.",
        "faq": [
            ("How much soil for a 4x8 raised bed?",
             "About 32 cu ft at 12 in deep, which is 1.19 cu yd or roughly 22 bags of 1.5 cu ft."),
            ("What mix should I fill a raised bed with?",
             "A common blend is 60% topsoil, 30% compost and 10% perlite or coarse grit for "
             "drainage. Root crops prefer a sandier mix."),
            ("How deep should a raised bed be?",
             "Ten to twelve inches suits most vegetables. Root crops and deep-rooted plants do "
             "better at 12 to 18 in."),
        ],
        "body": _body(
            lead=(
                "An 8 x 4 ft raised bed filled 12 in deep needs 32 cu ft of soil, which is about "
                "1.19 cu yd or 22 bags of 1.5 cu ft. Fill it in layers and water as you go so the "
                "mix settles evenly.\n\n"
                "A raised bed is a fixed volume, so the depth you choose sets the bill. Most "
                "vegetables do well at 10 to 12 in, and going deeper mainly helps root crops and "
                "plants that need drainage. Working out the volume first avoids a mid-build dash for "
                "more bags."
            ),
            worked_lead=(
                "For a raised bed measuring 8 feet by 4 feet, filled 12 inches deep:"
            ),
            bullets=(
                "*   length = 8\n"
                "*   width = 4\n"
                "*   height = 12\n"
                "*   Cubic feet: 32.0\n"
                "*   Cubic yards: 1.19\n"
                "*   1.5 cu ft bags: 22"
            ),
            sections=[
                ("Choose the Depth by Crop",
                 "Ten to twelve inches covers most vegetables and flowering plants. Salad leaves "
                 "and herbs manage in 6 in. Carrots, parsnips and tomatoes do better at 12 to 18 in "
                 "because their roots need room to run straight.\n\n"
                 "Depth also decides how the bed drains. A deep bed holds more water in reserve, "
                 "which helps in dry spells, but it needs a freer mix so it does not stay soggy. If "
                 "the bed sits on heavy clay, add drainage before you fill it."),
                ("Mixing the Fill",
                 "A reliable general blend is 60% topsoil, 30% compost and 10% perlite or coarse "
                 "grit. The topsoil gives body, the compost feeds the plants and holds moisture, and "
                 "the grit keeps the mix open.\n\n"
                 "Root crops prefer more sand and less compost, while hungry feeders such as "
                 "tomatoes and courgettes take a compost-heavy mix. Buy the components separately "
                 "and blend them, rather than trusting a bag labelled as raised-bed mix, which "
                 "varies widely in what it contains."),
                ("Filling and Settling",
                 "Add the mix in layers and water each one before the next. Watering as you go "
                 "settles the soil and shows up any low spots while you can still fix them. Leave "
                 "about two inches of freeboard so soil does not wash out over the edge.\n\n"
                 "Expect the level to drop by around a tenth over the first season as the compost "
                 "breaks down. Topping the bed up each year is normal, not a sign that something "
                 "went wrong."),
                ("How Much Soil for Common Bed Sizes",
                 "At 12 in deep, a 4 x 4 ft bed takes 16 cu ft, a 4 x 8 ft bed takes 32 cu ft, and a "
                 "4 x 12 ft bed takes 48 cu ft. Going to 18 in deep on the 4 x 8 ft bed raises it "
                 "from 32 cu ft to 48 cu ft, a half-again increase.\n\n"
                 "Run your own dimensions through the raised bed soil calculator, because beds are "
                 "often built to fit a space rather than to a standard size. Measure the inside of "
                 "the frame, not the outside, or you will over-buy."),
                ("Topping Up Over the Years",
                 "A raised bed is not filled once and forgotten. The organic part of the mix breaks "
                 "down every season, so the level falls and the soil loses structure. Top up each "
                 "spring with compost rather than fresh topsoil, which keeps the fertility rising "
                 "as the volume is restored.\n\n"
                 "Rotate crops between beds and refresh the compost each year. A bed that is fed "
                 "and topped up holds its depth and keeps producing, while one that is left alone "
                 "slowly turns into compacted subsoil."),
                ("Common Mistakes to Avoid",
                 "*   Filling with garden soil alone, which compacts and drains poorly in a bed.\n"
                 "*   Skipping the grit, then watching the mix turn to a wet slab.\n"
                 "*   Filling to the rim, so the first heavy rain spills soil over the sides.\n"
                 "*   Forgetting the annual top-up as the compost breaks down.\n"
                 "*   Measuring the outside of the frame and buying soil for the timber."),
            ],
        ),
    },
    {
        "slug": "how-much-topsoil-to-cover-1-acre",
        "title": "How Much Topsoil to Cover 1 Acre? Depth and Yards",
        "cluster": "topsoil",
        "primary_keyword": "how much topsoil to cover 1 acre",
        "secondary_keywords": ["topsoil per acre", "topsoil calculator", "yards of topsoil per acre",
                               "how much topsoil for a lawn"],
        "calculator": "topsoil",
        "calculator_defaults": {"length": 208.7, "width": 208.7, "depth": 1},
        "meta_description": "One acre dressed with 1 in of topsoil needs about 3,630 cu ft, or 134 cu "
                            "yd. Order by the cubic yard and allow for settling.",
        "faq": [
            ("How much topsoil for 1 acre?",
             "About 134 cu yd for a 1 in layer over 43,560 sq ft. Doubling the depth doubles the "
             "volume."),
            ("How deep should topsoil be for a lawn?",
             "A dressing of a quarter to half an inch levels a lawn. A new lawn over poor ground "
             "needs 4 to 6 in of topsoil to root into."),
            ("How is topsoil sold?",
             "By the cubic yard in bulk, or by the bag for small areas. Bulk is far cheaper at acre "
             "scale, though delivery access matters."),
        ],
        "body": _body(
            lead=(
                "An acre dressed with 1 in of topsoil needs about 3,630 cu ft, which is 134 cu yd. "
                "At that volume, order by the cubic yard in bulk rather than by the bag.\n\n"
                "One acre is 43,560 sq ft, so a thin layer still adds up to a large volume. The "
                "depth you actually need depends on whether you are levelling an existing lawn or "
                "building up ground to sow into, and the two cases differ by a factor of ten or more."
            ),
            worked_lead=(
                "For one acre (about 208.7 feet by 208.7 feet) dressed with a 1-inch layer of "
                "topsoil:"
            ),
            bullets=(
                "*   length = 208.7\n"
                "*   width = 208.7\n"
                "*   depth = 1\n"
                "*   Square feet: 43555.7\n"
                "*   Cubic feet: 3629.6\n"
                "*   Cubic yards: 134.43\n"
                "*   40 lb bags: 4840"
            ),
            sections=[
                ("Decide the Depth First",
                 "A light dressing to level a lawn and improve its surface runs a quarter to half an "
                 "inch. A new lawn over poor subsoil needs 4 to 6 in to give the roots something to "
                 "grow into.\n\n"
                 "The difference is enormous at acre scale. Going from half an inch to two inches "
                 "quadruples the volume, so settle the depth before you call for a quote. A tenth of "
                 "an inch either way is tens of cubic yards."),
                ("Ordering in Bulk",
                 "Topsoil is sold by the cubic yard. A cubic yard is 27 cu ft, so the 3,630 cu ft "
                 "this acre needs is about 134 cu yd. That is several lorry loads, and delivery "
                 "access matters as much as price.\n\n"
                 "Screened topsoil costs more than unscreened but spreads far more easily and is "
                 "free of stones and roots. For a lawn dressing, screened is usually worth it. Ask "
                 "what the soil is screened to and where it came from, because the quality of bulk "
                 "topsoil varies enormously."),
                ("Spreading and Settling",
                 "Spread with a rake in small sections rather than trying to level the whole acre at "
                 "once. A landscape rake or a drag mat behind a mower speeds this up considerably.\n\n"
                 "Allow for settling. Freshly spread topsoil drops in volume as it compacts and "
                 "dries, so order a little more than the calculated figure and expect to top up the "
                 "low spots after the first rain. Renting a powered spreader for an acre is usually "
                 "cheaper than the extra days of hand work."),
                ("Test Before You Buy",
                 "A soil test tells you whether the ground actually needs topsoil or just feeding. "
                 "If the existing soil is only short of organic matter, working in compost costs far "
                 "less than dressing the acre with imported soil.\n\n"
                 "Test the pH and the nutrient levels at the same time. Correcting a pH problem "
                 "across an acre takes a lot of material, and it is worth knowing before you place "
                 "the topsoil order."),
                ("New Lawn Versus Levelling",
                 "Levelling an established lawn is a light dressing spread over the surface and "
                 "worked into the hollows. Building a new lawn means a much deeper layer over the "
                 "whole area, and it needs to be firmed and watered before seed or turf goes down.\n\n"
                 "For a new lawn, spread the topsoil, roll it, and let it settle for a few days "
                 "before sowing. That gives you a chance to fill any hollows that appear, rather "
                 "than finding them after the grass is up."),
                ("Common Mistakes to Avoid",
                 "*   Choosing the depth after ordering, then running short.\n"
                 "*   Buying bagged soil for an acre, where bulk is far cheaper.\n"
                 "*   Skipping a soil test, so you build up ground that was already fine.\n"
                 "*   Spreading onto waterlogged ground, which ruts and compacts.\n"
                 "*   Forgetting to allow for settling, then leaving hollows after the first rain."),
            ],
        ),
    },
    {
        "slug": "how-much-bark-do-i-need-for-a-10x4-bed",
        "title": "How Much Bark for a 10x4 Bed? Depth and Bags",
        "cluster": "bark",
        "primary_keyword": "how much bark do i need for a 10x4 bed",
        "secondary_keywords": ["bark mulch calculator", "how much bark chippings",
                               "bark mulch depth", "bags of bark for a border"],
        "calculator": "bark",
        "calculator_defaults": {"length": 10, "width": 4, "depth": 2},
        "meta_description": "A 10x4 ft bed at 2 in deep needs 6.7 cu ft of bark, about 0.25 cu yd or "
                            "4 bags of 2 cu ft. Keep bark clear of stems.",
        "faq": [
            ("How much bark for a 10x4 bed?",
             "About 6.7 cu ft at 2 in deep, which is 0.25 cu yd or 4 bags of 2 cu ft."),
            ("How deep should bark mulch be?",
             "Two to three inches suppresses weeds and holds moisture. More than 4 in against stems "
             "can cause rot."),
            ("Does bark mulch need topping up?",
             "Yes. It breaks down over a season or two, so top up with a thin layer each spring "
             "rather than one thick one."),
        ],
        "body": _body(
            lead=(
                "A 10 x 4 ft bed at 2 in deep needs 6.7 cu ft of bark, which is about 0.25 cu yd or "
                "4 bags of 2 cu ft. Bark is lighter than gravel, so bagged is convenient for a bed "
                "this size.\n\n"
                "Bark chippings suppress weeds, hold moisture and slowly feed the soil as they break "
                "down. A layer of two to three inches does the work; going much deeper is wasted "
                "material and can harm plants. Measure the bed, pick the depth, and the bag count "
                "falls out of the arithmetic."
            ),
            worked_lead=(
                "For a bed measuring 10 feet by 4 feet, covered with 2 inches of bark:"
            ),
            bullets=(
                "*   length = 10\n"
                "*   width = 4\n"
                "*   depth = 2\n"
                "*   Square feet: 40.0\n"
                "*   Cubic feet: 6.7\n"
                "*   Cubic yards: 0.25\n"
                "*   2 cu ft bags: 4"
            ),
            sections=[
                ("Pick the Depth for the Job",
                 "Two inches refreshes an established border. Two to three inches suppresses weeds "
                 "in a bed that is already planted. Three to four inches suits a new bed where you "
                 "want a longer gap before weeds return.\n\n"
                 "Avoid going deeper than four inches, and keep the bark clear of trunks and stems. "
                 "Piled against a plant, it holds moisture where it does the most damage, and it "
                 "gives slugs and rodents somewhere to hide."),
                ("Bark, Chips or Compost",
                 "Bark chippings are decorative and slow to break down, which makes them a good "
                 "surface for borders and around shrubs. Wood chips are coarser and last longer but "
                 "can rob nitrogen from the soil at the surface as they decompose. Compost is "
                 "finer and feeds the soil faster, but it disappears sooner.\n\n"
                 "For a bed that is mostly about appearance and weed control, bark is the usual "
                 "choice. For feeding the soil, compost worked in does more, and the two can be "
                 "combined if you want both."),
                ("Laying It and Topping Up",
                 "Water the bed before you spread, then lay the bark to an even depth. Rake it level "
                 "and pull it back a few inches from any stems. Even coverage matters more than a "
                 "thick layer in one spot, and a level surface is easier to top up later.\n\n"
                 "Bark breaks down over a season or two. Top up with a thin layer each spring rather "
                 "than one thick layer, and rake the old surface first so water can pass through. "
                 "Matted bark sheds water, which defeats the purpose."),
                ("How Much Bark for Common Bed Sizes",
                 "At 2 in deep, a 10 x 4 ft bed takes 6.7 cu ft and a 10 x 8 ft bed takes 13.3 cu ft, "
                 "so the bag count doubles with the area. At 3 in deep the same 10 x 4 ft bed takes "
                 "10 cu ft, which is 5 bags.\n\n"
                 "Measure the planted area, not the whole garden, and leave gaps for paths and "
                 "patios. Ordering bark for ground you are not covering is the most common way to "
                 "buy twice as much as you need."),
                ("Bark Around Different Plants",
                 "Shrubs and trees take bark well, provided it is kept off the stems. Perennials "
                 "that die back to the ground each year are trickier, because a thick layer can "
                 "smother the crowns. Use a thinner layer around them, or lift the bark back in "
                 "spring.\n\n"
                 "Vegetable beds are usually better with compost than bark, because bark adds little "
                 "nutrition and can tie up nitrogen at the surface where seedlings are trying to "
                 "grow."),
                ("Common Mistakes to Avoid",
                 "*   Piling bark against trunks and stems, which invites rot.\n"
                 "*   Going deeper than 4 in to save a return trip for more bags.\n"
                 "*   Using fresh chips that draw nitrogen from the soil as they break down.\n"
                 "*   Skipping the spring top-up, then losing weed control by midsummer.\n"
                 "*   Measuring the whole garden rather than the area you will actually cover."),
            ],
        ),
    },
    {
        "slug": "how-much-compost-do-i-need-for-a-garden-bed",
        "title": "How Much Compost for a Garden Bed? Depth and Bags",
        "cluster": "compost",
        "primary_keyword": "how much compost do i need for a garden bed",
        "secondary_keywords": ["compost calculator", "compost per square foot",
                               "how much compost to add to soil", "bags of compost for a bed"],
        "calculator": "compost",
        "calculator_defaults": {"length": 8, "width": 4, "depth": 2},
        "meta_description": "An 8x4 ft bed at 2 in of compost needs 5.3 cu ft, about 0.2 cu yd or 6 "
                            "bags of 1 cu ft. Work it into the top layer.",
        "faq": [
            ("How much compost for a garden bed?",
             "About 5.3 cu ft for an 8x4 ft bed at 2 in deep, which is roughly 6 bags of 1 cu ft."),
            ("How deep should compost be?",
             "One to three inches worked into the top layer of soil is the usual rate. A quarter "
             "inch is plenty as a lawn top-dressing."),
            ("Can you add too much compost?",
             "Yes. Repeated heavy dressings build up phosphorus and salts, so test the soil and "
             "work to a rate rather than guessing."),
        ],
        "body": _body(
            lead=(
                "An 8 x 4 ft bed dressed with 2 in of compost needs 5.3 cu ft, which is about 0.2 cu "
                "yd or 6 bags of 1 cu ft. Work it into the top few inches rather than leaving it as "
                "a layer on the surface.\n\n"
                "Compost feeds soil life, improves structure and holds moisture, and a little goes a "
                "long way. The usual rate is one to three inches worked into the top layer, not a "
                "thick blanket, and the bed benefits most when it is added before planting."
            ),
            worked_lead=(
                "For a bed measuring 8 feet by 4 feet, dressed with 2 inches of compost:"
            ),
            bullets=(
                "*   length = 8\n"
                "*   width = 4\n"
                "*   depth = 2\n"
                "*   Square feet: 32.0\n"
                "*   Cubic feet: 5.3\n"
                "*   Cubic yards: 0.2\n"
                "*   1 cu ft bags: 6"
            ),
            sections=[
                ("The Right Rate",
                 "One to three inches worked into the top layer is the standard for beds. A quarter "
                 "inch is enough as a top-dressing on a lawn, and less is more once soil is already "
                 "in good heart.\n\n"
                 "Compost is a soil amendment, not a fertiliser, so it does not replace feeding. It "
                 "improves how the soil holds water and nutrients, which lets the plants make use "
                 "of what is already there. Expect the effect to build over several seasons."),
                ("Working It In",
                 "Spread the compost and fork or till it into the top four to six inches. Leaving it "
                 "as a distinct layer on top keeps the roots in the compost rather than the soil "
                 "below, which makes plants less resilient in dry spells.\n\n"
                 "If you are not digging, spread it as a mulch and let worms pull it down. It takes "
                 "longer to incorporate, but it protects the soil structure and feeds the worms "
                 "that do the work for you."),
                ("Don't Overdo It",
                 "Repeated heavy dressings can push phosphorus and soluble salts to levels that "
                 "harm plants. A soil test every few years tells you whether the bed actually needs "
                 "more, and it is cheaper than guessing.\n\n"
                 "For a bed that has had compost for several years, a single inch, or a light mulch, "
                 "is often enough. Rotate what you grow, and let the soil catch up between heavy "
                 "applications.\n\n"
                 "If a soil test shows high phosphorus, switch to a compost made from leaves or "
                 "garden waste rather than manure, which is usually much lower in phosphorus and "
                 "safer to apply again the following season."),
                ("How Much Compost for Common Bed Sizes",
                 "At 2 in deep, a 4 x 4 ft bed takes 2.7 cu ft, an 8 x 4 ft bed takes 5.3 cu ft, and "
                 "a 12 x 4 ft bed takes 8 cu ft. Doubling the depth doubles the volume, so a 4 in "
                 "dressing on the 8 x 4 ft bed takes 10.7 cu ft.\n\n"
                 "Run your own dimensions through the compost calculator, and remember that the "
                 "figure is the volume of compost, not of soil. A bag of compost settles as it is "
                 "worked in, so buy a little over the calculated amount."),
                ("Compost as Mulch Versus Amendment",
                 "Spread thinly on the surface, compost acts as a mulch: it slows evaporation and "
                 "suppresses weeds while slowly feeding the soil. Dug into the top layer, it is an "
                 "amendment that changes the structure of the soil itself.\n\n"
                 "For heavy clay, working it in does more, because it opens up the soil. For sandy "
                 "ground, both help, but the amendment route holds moisture better. A bed that is "
                 "already good benefits most from the thin mulch treatment."),
                ("Common Mistakes to Avoid",
                 "*   Spreading compost as a thick layer and never working it in.\n"
                 "*   Adding more every year without testing the soil.\n"
                 "*   Using unfinished compost, which can burn roots and harbour pests.\n"
                 "*   Treating compost as a substitute for fertiliser on hungry crops.\n"
                 "*   Buying compost when the bed would be better served by a soil test."),
            ],
        ),
    },
]
