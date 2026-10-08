# GardenCalc promotion playbook

Base URL: https://huzaifamasood30.github.io/gardencalc

Every item below can be completed **without any GardenCalc-side technical change**; each needs *your* account only where marked. Work top to bottom. After completing an item run `python scripts/promotion.py --mark <uid>` so the same community is never re-targeted. Dedupe guard: `python scripts/promotion.py --check`.

Ethics: one link per contribution, only where the tool is the direct answer, always disclosed. No accounts created for you, no bulk posting, no paid links, no PBNs.

## [ ] Stack Exchange — Home Improvement (diy.stackexchange.com)
- **Target:** How much concrete for a fence post?
- **URL:** https://diy.stackexchange.com/questions/87204/how-much-concrete-for-a-fence-post
- **Promote:** https://huzaifamasood30.github.io/gardencalc/how-many-bags-of-concrete-do-i-need-for-a-fence-post/
- **Anchor text:** how many bags of concrete for a fence post
- **Link type:** nofollow (external links are nofollow; still sends referral traffic)
- **Requirement:** User action required (needs your Stack Exchange login; 1 rep to post)
- **Rules / notes:** Answer is self-contained; the calculator is a supporting tool, not the answer. Disclose you built it. Only one link. If a good answer already exists, improve it with an edit rather than posting a competing answer.
- **UID (for --mark):** `stackexchange:https://diy.stackexchange.com/questions/87204/how-much-concrete-for-a-fence-post`

**Exact text to post:**

```text
Concrete for a post hole is just the volume of the hole divided by the yield of the bag, so the number you need is the hole volume, not the post volume.

For a 4x4 post you want the hole wider than the post so the concrete forms a collar. A common size is a 8-10 in diameter hole, 24-30 in deep. Take a 10 in diameter hole 30 in deep: radius 5 in = 0.417 ft, area = pi x 0.417^2 = 0.546 sq ft, x 2.5 ft deep = 1.37 cu ft per hole.

Mix yield: an 80 lb bag of concrete gives about 0.60 cu ft, a 60 lb bag about 0.45 cu ft. So 1.37 / 0.60 = 2.3, i.e. buy 3 bags of 80 lb per hole (or 4 bags of 60 lb). For 10 posts that is about 14 cu ft, or 0.5 cu yd, or 24 bags of 80 lb.

Two practical notes: set the post so the concrete crowns slightly above grade and slopes away from the wood, and use fast-setting mix if you want to keep building the same day.

I built a free calculator that does the hole-volume and bag-count arithmetic for any post size, hole diameter, depth and bag size: https://huzaifamasood30.github.io/gardencalc/how-many-bags-of-concrete-do-i-need-for-a-fence-post/
```

## [ ] Stack Exchange — Home Improvement (diy.stackexchange.com)
- **Target:** How do I calculate the concrete needed for a fence post?
- **URL:** https://diy.stackexchange.com/questions/170144/how-do-i-calculate-the-concrete-needed-for-a-fence-post
- **Promote:** https://huzaifamasood30.github.io/gardencalc/how-many-bags-of-concrete-do-i-need-for-a-fence-post/
- **Anchor text:** concrete needed for a fence post
- **Link type:** nofollow (external links are nofollow; still sends referral traffic)
- **Requirement:** User action required (needs your Stack Exchange login; 1 rep to post)
- **Rules / notes:** Answer is self-contained; the calculator is a supporting tool, not the answer. Disclose you built it. Only one link. If a good answer already exists, improve it with an edit rather than posting a competing answer.
- **UID (for --mark):** `stackexchange:https://diy.stackexchange.com/questions/170144/how-do-i-calculate-the-concrete-needed-for-a-fence-post`

**Exact text to post:**

```text
The method is: (hole area x depth) x number of posts, then divide by the bag yield.

Worked for your 4x4 x 8 ft posts: assume a 10 in hole, 30 in deep. Radius = 5 in = 0.417 ft. Area = 3.1416 x 0.417^2 = 0.546 sq ft. Volume per hole = 0.546 x 2.5 = 1.37 cu ft. An 80 lb bag yields ~0.60 cu ft, so ~2.3 bags -> buy 3 per hole.

If your holes are 12 in wide, that scales to about 1.96 cu ft per hole and 4 bags of 80 lb each. Multiply by the post count for the total; a full pallet is cheaper per bag if you have many posts.

Free tool that takes post count, hole diameter, depth and bag size and returns the bag count: https://huzaifamasood30.github.io/gardencalc/how-many-bags-of-concrete-do-i-need-for-a-fence-post/
```

## [ ] Stack Exchange — Home Improvement (diy.stackexchange.com)
- **Target:** How do I determine the amount of paint needed for a room?
- **URL:** https://diy.stackexchange.com/questions/18483/how-do-i-determine-the-amount-of-paint-needed-for-a-room
- **Promote:** https://huzaifamasood30.github.io/gardencalc/how-much-paint-do-i-need-for-a-bedroom/
- **Anchor text:** how much paint a room needs
- **Link type:** nofollow (external links are nofollow; still sends referral traffic)
- **Requirement:** User action required (needs your Stack Exchange login; 1 rep to post)
- **Rules / notes:** Answer is self-contained; the calculator is a supporting tool, not the answer. Disclose you built it. Only one link. If a good answer already exists, improve it with an edit rather than posting a competing answer.
- **UID (for --mark):** `stackexchange:https://diy.stackexchange.com/questions/18483/how-do-i-determine-the-amount-of-paint-needed-for-a-room`

**Exact text to post:**

```text
Paint estimating is wall area divided by coverage, multiplied by the number of coats, after subtracting openings.

Wall area = perimeter x ceiling height. For a 12 x 10 ft room with 8 ft walls that is 44 x 8 = 352 sq ft. Subtract a door (~21 sq ft) and two windows (~2 x 15 sq ft) and you have about 301 sq ft of paintable wall. One gallon covers roughly 350-400 sq ft per coat on a smooth surface, so two coats needs 301 x 2 / 350 ~ 1.7 gal, round up to 2 gallons. Ceiling adds length x width, about another half gallon for two coats.

Buy the two gallons up front and keep one unopened so the second coat is the exact same batch if you need a touch-up later.

I built a free paint calculator that does this and lets you vary coats, doors and windows: https://huzaifamasood30.github.io/gardencalc/how-much-paint-do-i-need-for-a-bedroom/
```

## [ ] Stack Exchange — Gardening & Landscaping
- **Target:** Advice for a new planting bed
- **URL:** https://gardening.stackexchange.com/questions/18072/advice-for-a-new-planting-bed
- **Promote:** https://huzaifamasood30.github.io/gardencalc/how-much-mulch-do-i-need-for-500-sq-ft/
- **Anchor text:** how much mulch do i need for 500 sq ft
- **Link type:** nofollow (external links are nofollow; still sends referral traffic)
- **Requirement:** User action required (needs your Stack Exchange login; 1 rep to post)
- **Rules / notes:** Answer is self-contained; the calculator is a supporting tool, not the answer. Disclose you built it. Only one link. If a good answer already exists, improve it with an edit rather than posting a competing answer.
- **UID (for --mark):** `stackexchange:https://gardening.stackexchange.com/questions/18072/advice-for-a-new-planting-bed`

**Exact text to post:**

```text
For 650 sq ft you are looking at a bulk order, not bags. At the standard 3 in deep, volume = 650 x 0.25 ft = 162.5 cu ft, which is 162.5 / 27 = 6.0 cubic yards. That is about 82 bags of 2 cu ft if you go that route, which is why bulk delivery is cheaper at this size.

On the grass coming back through: mulch only suppresses seed that has already germinated under it. For a bed with established weeds, cut them down first, put down a layer of cardboard or 6 sheets of newspaper overlapping by 6 in, then the 3 in of mulch on top. Keep the mulch a couple of inches back from tree trunks and shrub stems so the bark does not stay wet.

I put a mulch calculator with the bags/cubic-yards conversion here if it helps: https://huzaifamasood30.github.io/gardencalc/how-much-mulch-do-i-need-for-500-sq-ft/
```

## [ ] Stack Exchange — Gardening & Landscaping
- **Target:** Ideal way to fill in a large hole (from a goldfish pond)
- **URL:** https://gardening.stackexchange.com/questions/37993/ideal-way-to-fill-in-a-large-hole-from-a-goldfish-pond
- **Promote:** https://huzaifamasood30.github.io/gardencalc/topsoil-calculator/
- **Anchor text:** how much topsoil to fill it
- **Link type:** nofollow (external links are nofollow; still sends referral traffic)
- **Requirement:** User action required (needs your Stack Exchange login; 1 rep to post)
- **Rules / notes:** Answer is self-contained; the calculator is a supporting tool, not the answer. Disclose you built it. Only one link. If a good answer already exists, improve it with an edit rather than posting a competing answer.
- **UID (for --mark):** `stackexchange:https://gardening.stackexchange.com/questions/37993/ideal-way-to-fill-in-a-large-hole-from-a-goldfish-pond`

**Exact text to post:**

```text
That hole is about 1.5 m x 1.5 m x 1 m, so roughly 2.25 cubic metres (~2.9 cubic yards) of fill. Don't fill it all with topsoil: topsoil settles and compresses, and a 1 m depth of it would be a lot of settling.

Fill the bottom ~80% with subsoil or a cheaper loam, compact it in 20 cm layers (water each layer), and finish with 15-20 cm of good topsoil for the planting. That cuts the topsoil you need to about 0.3-0.45 cubic metres (~0.4-0.6 cubic yards, or roughly 14-20 cubic feet).

One caution: if the pond was lined, remove the liner so water drains; otherwise you have made a bog. And let the topsoil settle for a few weeks before seeding or planting, topping it up as it drops.

I made a free topsoil calculator that converts area x depth to cubic yards and bags: https://huzaifamasood30.github.io/gardencalc/topsoil-calculator/
```

## [ ] Reddit — r/landscaping
- **Target:** Weekly/simple questions and 'how much material' threads
- **URL:** https://www.reddit.com/r/landscaping/
- **Promote:** https://huzaifamasood30.github.io/gardencalc/mulch-calculator/ (or the matching calculator for the thread)
- **Anchor text:** mulch calculator
- **Link type:** nofollow
- **Requirement:** User action required (needs your Reddit account, with some genuine comment history first)
- **Rules / notes:** Follow the 90/10 rule: be an active commenter first. Never post a bare link; lead with the answer. Check r/landscaping sidebar rules before posting; many subs limit self-promo to specific threads or days. If unsure, put the link in a comment, not the post body.
- **UID (for --mark):** `reddit:r/landscaping`

**Exact text to post:**

```text
Reply inside an existing question thread (do not start a new promotional post): '[Actual arithmetic for their numbers]. 3 in deep is the usual depth for beds. For that area that is X cu yd / Y bags. I built a free calculator that does the bags-vs-cubic-yards conversion: https://huzaifamasood30.github.io/gardencalc/mulch-calculator/ (I run the site).'
```

## [ ] Reddit — r/HomeImprovement
- **Target:** Material-quantity questions (concrete, paint, tile)
- **URL:** https://www.reddit.com/r/HomeImprovement/
- **Promote:** https://huzaifamasood30.github.io/gardencalc/concrete-calculator/ or https://huzaifamasood30.github.io/gardencalc/paint-calculator/
- **Anchor text:** concrete calculator / paint calculator
- **Link type:** nofollow
- **Requirement:** User action required (needs your Reddit account)
- **Rules / notes:** Same 90/10 rule and sidebar check. One link, only when it answers the post.
- **UID (for --mark):** `reddit:r/HomeImprovement`

**Exact text to post:**

```text
Answer the specific thread with the full formula, then add one line: 'I built a free calculator that does this for your dimensions and bag size: https://huzaifamasood30.github.io/gardencalc/concrete-calculator/ (site I run).'
```

## [ ] Quora — Quora — 'How much mulch do I need?'
- **Target:** Search: how much mulch do I need / for 500 sq ft / for 200 sq ft
- **URL:** https://www.quora.com/search?q=how%20much%20mulch%20do%20i%20need
- **Promote:** https://huzaifamasood30.github.io/gardencalc/mulch-calculator/
- **Anchor text:** mulch calculator
- **Link type:** nofollow
- **Requirement:** User action required (needs your Quora account)
- **Rules / notes:** One link per answer; Quora may collapse answers that are mostly promotional. Answer several related questions with the method, linking only where the calculator is the direct tool.
- **UID (for --mark):** `quora:how-much-mulch-do-i-need`

**Exact text to post:**

```text
Answer with the worked method: 'Multiply the bed length by width to get square feet. Convert your depth to feet (3 in = 0.25 ft) and multiply for cubic feet. Divide cubic feet by 27 for cubic yards, or by 2 for 2-cu-ft bags. Example: 500 sq ft x 0.25 ft = 125 cu ft = 4.63 cu yd = 63 bags. I wrote this up with a calculator that does it for any size: https://huzaifamasood30.github.io/gardencalc/mulch-calculator/ (site I run).'
```

## [ ] Pinterest — Pinterest — create boards 'Garden Calculators', 'Lawn Care', 'Home Projects'
- **Target:** Pin each calculator's social image to the matching board
- **URL:** https://www.pinterest.com/
- **Promote:** https://huzaifamasood30.github.io/gardencalc/mulch-coverage-chart/ etc. (16 ready pins in /static/img/pins/)
- **Anchor text:** pin title (e.g. 'Mulch Coverage Chart: Bags & Yards')
- **Link type:** nofollow (outbound pins are nofollow)
- **Requirement:** User action required (needs your Pinterest account)
- **Rules / notes:** Assets already generated: site/static/img/pins/*.png (1200x630). Pin to a relevant board, not a generic one; use descriptive alt text. 3-5 pins/day max, spaced out.
- **UID (for --mark):** `pinterest:gardencalc-boards`

**Exact text to post:**

```text
Pin title: use the article title. Pin description (200-300 chars): 'How much mulch for your bed? Coverage chart for 50-1000 sq ft at 2, 3 and 4 in deep, with cubic yards and 2-cu-ft bag counts. Free calculator linked.' Destination link: the article URL + ?utm_source=pinterest&utm_medium=social&utm_campaign=<slug>.
```

## [ ] Hacker News — Hacker News — 'Show HN'
- **Target:** Show HN: I built a free garden-materials calculator with the formulas shown
- **URL:** https://news.ycombinator.com/submit
- **Promote:** https://huzaifamasood30.github.io/gardencalc/
- **Anchor text:** Show HN (title field)
- **Link type:** nofollow
- **Requirement:** User action required (needs your HN account; posting a URL needs a little karma)
- **Rules / notes:** Show HN is explicitly for your own work and is allowed here. One submission only; do not resubmit. Be present in the comments.
- **UID (for --mark):** `hackernews:show-hn`

**Exact text to post:**

```text
Title: 'Show HN: GardenCalc - free home and garden calculators that show the formula'. First comment: 'I kept seeing the same "how much mulch/soil/gravel" questions answered ambiguously, so I built a static site where every calculator shows the formula and a worked example rather than just a number. No account, no tracking. Feedback welcome.' Link: https://huzaifamasood30.github.io/gardencalc/
```

## [ ] Blog outreach — Eden Brothers - 'Top Gardening Blogs' roundup
- **Target:** Suggests readers email favourite gardening bloggers to service@edenbrothers.com
- **URL:** https://grow.edenbrothers.com/top-10-gardening-blogs/
- **Promote:** https://huzaifamasood30.github.io/gardencalc/ (calculator hub)
- **Anchor text:** GardenCalc
- **Link type:** depends on the publisher (often dofollow in-post)
- **Requirement:** User action required (email from your address)
- **Rules / notes:** Only pitch pages that genuinely list tools/resources. Personalise each email; do not send a template blast. Expect a low hit rate - that is normal.
- **UID (for --mark):** `blog-outreach:edenbrothers-top-blogs`

**Exact text to post:**

```text
Subject: Free garden calculators your readers might find useful

Hi, I run a small free site of garden-material calculators - mulch, soil, gravel, seed and fertilizer - that show the formula and a worked example rather than just a number. I noticed your gardening resources page and thought it could be a fit. No reciprocation wanted; happy for you to skip it if it is not a match. https://huzaifamasood30.github.io/gardencalc/
```

## [ ] Resource page — Home Garden Seed Association - Recommended Resources
- **Target:** Page invites readers to submit resources they love via the contact form
- **URL:** https://homegardenseedassociation.com/new-page-2
- **Promote:** https://huzaifamasood30.github.io/gardencalc/ (or https://huzaifamasood30.github.io/gardencalc/grass-seed-calculator/)
- **Anchor text:** GardenCalc calculators
- **Link type:** depends on the publisher (often dofollow)
- **Requirement:** User action required (contact form usually needs your email)
- **Rules / notes:** Only submit where the page's stated policy invites suggestions. Never pay.
- **UID (for --mark):** `resource-page:homegardenseedassociation`

**Exact text to post:**

```text
Use the page's own contact form/link: 'Hi - your Recommended Resources page invited suggestions. I built a free set of garden-material calculators (mulch, soil, seed, fertilizer) that show the formula and a worked example. If useful for your readers, feel free to include it: https://huzaifamasood30.github.io/gardencalc/ - no reciprocal link requested.'
```

## [ ] Resource page — Cornell Cooperative Extension - county gardening resource pages
- **Target:** County offices publish 'Gardening Resources' link lists
- **URL:** https://stlawrence.cce.cornell.edu/home-gardens-grounds/gardening-resources
- **Promote:** https://huzaifamasood30.github.io/gardencalc/
- **Anchor text:** the GardenCalc calculators
- **Link type:** depends on the publisher (often dofollow)
- **Requirement:** User action required (email from your address)
- **Rules / notes:** Educational/extension sites are high-trust. Only where a resource list exists and the tool is genuinely relevant; departments are selective.
- **UID (for --mark):** `resource-page:cornell-cce`

**Exact text to post:**

```text
Email the county office's growline: 'I help run a free, non-commercial set of garden calculators (volumes and rates for mulch, soil, seed). I thought it might suit your Gardening Resources list if you keep one. https://huzaifamasood30.github.io/gardencalc/'
```

## [ ] RSS aggregators — feedly / feedly cloud + general feed readers
- **Target:** Anyone can subscribe to a public RSS feed; feed directories index it
- **URL:** https://huzaifamasood30.github.io/gardencalc/rss.xml
- **Promote:** https://huzaifamasood30.github.io/gardencalc/rss.xml
- **Anchor text:** GardenCalc feed
- **Link type:** varies; prefer curated listings that use dofollow
- **Requirement:** User action required for directories that need a form/account
- **Rules / notes:** The feed is live. Submitting it to feed directories needs a form, but anyone can add it to a reader. A public web page hosting the feed URL is the no-login equivalent and is already served at /rss.xml.
- **UID (for --mark):** `rss-aggregators:feedly`

**Exact text to post:**

```text
Feed URL: https://huzaifamasood30.github.io/gardencalc/rss.xml
```

## [ ] Directory — Curated home-improvement / DIY tool directories
- **Target:** Reputable, editorially-reviewed tool listings (skip paid link farms)
- **URL:** https://www.google.com/search?q=%22submit%22+OR+%22add+your+tool%22+home+improvement+calculator+directory
- **Promote:** https://huzaifamasood30.github.io/gardencalc/
- **Anchor text:** GardenCalc
- **Link type:** varies; prefer curated listings that use dofollow
- **Requirement:** User action required (most submission forms need an email account)
- **Rules / notes:** Add only where there is real editorial review and a relevant category. Avoid bulk '5000 directories' lists, paid PBNs, and anything promising instant DA. Check whether the listing link is dofollow before investing time.
- **UID (for --mark):** `directory:home-improvement-tools`

**Exact text to post:**

```text
Standard listing blurb (40-60 words): 'GardenCalc is a free set of home and garden calculators for mulch, topsoil, gravel, concrete, paint, tile, grass seed and fertilizer. Every tool shows the formula and a worked example, with results in bags, cubic feet, cubic yards and tons. No account or tracking.'
```

## [ ] Citation — Wikipedia - Mulch article (reference improvement only)
- **Target:** Only if a reliable secondary source supports the same claim
- **URL:** https://en.wikipedia.org/wiki/Mulch
- **Promote:** n/a - do not cite GardenCalc
- **Anchor text:** n/a
- **Link type:** nofollow (Wikipedia) / depends elsewhere
- **Requirement:** Not recommended
- **Rules / notes:** Not recommended. Recorded so it is not attempted.
- **UID (for --mark):** `citation:wikipedia-mulch`

**Exact text to post:**

```text
Do not add a GardenCalc link. Wikipedia needs independent, reliable, secondary sources; a self-published calculator is not one, and adding it is link spam that will be reverted. This is listed only to record the decision.
```

## Steps that need your account (summary)

1. Google Search Console — verify the URL-prefix property (the HTML meta tag is already live), then submit the sitemap. This is the single highest-impact action.
2. Bing Webmaster Tools — sign in, then 'Import from Google Search Console'.
3. Reddit / Quora / Stack Exchange / Pinterest / HN — use the ready text above.
4. Directory and resource-page forms — use the ready blurbs above.

## Not recommended
- Paid directories, PBNs, 'instant DA' services, link exchanges, comment spam, or auto-submitters that post to hundreds of directories.
- Citing GardenCalc on Wikipedia — a self-published tool is not a reliable source and any such edit is link spam.
