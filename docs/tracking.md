# Tracking and campaign links

## Analytics

Google Analytics 4 is loaded only when `analytics_id` is set in `config/site.json`
(or the `ANALYTICS_ID` environment variable / GitHub Actions secret, which overrides it).
Set it once, in that one place, to a GA4 measurement ID like `G-XXXXXXXXXX`. When it is
empty, no analytics script is emitted and no cookies are set.

## Custom events

The site fires these GA4 events (see `static/js/main.js` and the calculator template).
Each carries `calculator_name` where a calculator is involved:

| Event | Fires when |
|---|---|
| `calculate_click` | the Calculate button is pressed |
| `copy_result` | the calculator "Copy result" button is pressed |
| `print_result` | the calculator "Print" button is pressed |
| `share_click` | any share link or button is clicked (`network` = whatsapp/facebook/x/pinterest/reddit/email/copy/link) |
| `internal_calculator_click` | reserved for the "Plan the whole project" links |

To see them: GA4 -> Reports -> Realtime, or DebugView with the Google Analytics Debugger
extension.

## UTM tagging for shared links

Tag outbound links you post so you can attribute traffic. The canonical tag on every page
stays clean, so UTM links are never indexed as separate pages.

Pattern: `?utm_source=<where>&utm_medium=<type>&utm_campaign=<name>`

Examples:

- Threads: `https://huzaifamasood30.github.io/gardencalc/mulch-calculator/?utm_source=threads&utm_medium=social&utm_campaign=mulch-calc`
- Pinterest: `.../mulch-coverage-chart/?utm_source=pinterest&utm_medium=social&utm_campaign=mulch-chart`
- Email: `.../?utm_source=newsletter&utm_medium=email&utm_campaign=spring-mulch`

## Search Console

Search Console shows Google Search traffic only. Use GA4 (above) for Threads, Pinterest,
WhatsApp, YouTube and direct visits. Use UTM tags so those visits land in the right
channel report.
