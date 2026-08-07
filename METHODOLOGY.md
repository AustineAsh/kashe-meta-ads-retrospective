# Methodology and analytical guardrails

## Purpose

This repository asks descriptive questions of a historical Meta Ads export. Its purpose is to document what the available data show, verify what can be supported from the surviving evidence, and identify questions that a richer dataset could investigate. It does **not** estimate causal creative effects.

## Unit of analysis

Each row in the sanitized CSV represents one campaign row from the source export. Campaign names are not guaranteed to be unique: the source contains **126 rows but 96 distinct campaign-name strings**. Because campaign/ad IDs are not available, `campaign_row_id` is the stable row identifier used here and no attempt is made to deduplicate rows solely by name.

## Verification checks

The raw-data sheet was re-read and the calculations were re-run before the current verified version of the repository was published.

- 126 total campaign rows were recovered.
- 122 rows have recognized result types.
- Four rows contain an ambiguous result type/value (`2`).
- For **all 122 recognized rows**, `amount spent / results` reproduces the exported `cost per result` to within `1e-6` (maximum absolute floating-point difference approximately `4.95e-09`).
- The campaign-name columns duplicated in the source workbook agree on all 126 rows.
- The quality, engagement-rate and conversion-rate ranking columns are `-` for every row and therefore contain no usable ranking information.

## Comparison rules

1. **Compare cost per result only within the same result type.** A link click cannot be compared directly with a Facebook like, ThruPlay, post engagement, lead or messaging conversation.
2. **Treat link clicks as link clicks.** They are not equated with landing-page views, YouTube views, purchases or revenue.
3. **Do not sum reach and call it unique people.** Reach can overlap between campaigns. Campaign reach is summed only as an export-level descriptive total and is always labelled as summed campaign reach.
4. **Use weighted cost per result for grouped summaries.** This is `total spend / total results`, rather than the arithmetic mean of campaign-level cost-per-result values.
5. **Distinguish weighted and typical campaign performance.** A weighted KPI can be dominated by a few high-volume rows. For link-click rows, both weighted values and campaign-level medians are reported where useful.
6. **Derived metrics are labelled as derived.** The export provides the component fields, but CTR, CPM, frequency-style ratios and result rates are recalculated arithmetically.
7. **Treat the repeated reporting dates as an export window.** They do not establish campaign-specific active dates or permit time-series/fatigue analysis.
8. **Flag malformed rows instead of repairing them silently.** Four rows have `result_type = 2`; they are retained with `data_quality_flag = ambiguous_result_type` and excluded from result-type summaries.
9. **No retrospective creative coding where the asset is missing.** Most posts were deleted or disabled, so campaign names alone are insufficient to infer format, hook, creator, audience or creative angle reliably.
10. **No causal attribution.** The campaigns were not recovered as controlled experimental cells. Audience, placement, budget strategy, optimization, timing and other confounders are unavailable.
11. **No ecommerce ROI/ROAS inference.** The workbook does not provide purchase revenue, purchase counts, AOV, customer identity or verified downstream sales.

## Derived KPI formulas

For rows where the required components are available:

- **CPC / weighted cost per link click** = `spend / link clicks`
- **Derived link CTR** = `link clicks / impressions × 100`
- **CPM** = `spend / impressions × 1,000`
- **Frequency-style ratio** = `impressions / reach`
- **Result rate** = `results / impressions × 100`

The frequency-style ratio can be interpreted at an individual row as impressions per reached account/person estimate. When campaign reach is first summed across multiple rows, the resulting ratio is only a descriptive export-level proxy because audiences may overlap across rows.

## Video metrics

The export includes six rows optimized/reported as `ThruPlay` and one row reported as `3-second video plays`.

A three-second-view rate can be derived for the one row where three-second plays are present, and a ThruPlay/impression rate can be calculated for the ThruPlay rows. A conventional creative `hold rate` is **not** calculated because three-second plays and ThruPlays were not recorded for the same set of creatives/campaign rows. Joining unlike rows would create a false denominator relationship.

## Commercial KPIs unavailable from this export

A modern ecommerce/performance-marketing dataset would ideally allow analysis of metrics such as:

- outbound clicks and outbound CTR;
- landing-page views, landing-page-view rate and cost per landing-page view;
- add-to-cart and checkout rates;
- purchases/conversions;
- conversion rate;
- CPA/CAC;
- purchase/conversion value and revenue;
- ROAS;
- average order value;
- new-customer acquisition economics and, where relevant, broader efficiency/profit metrics.

Those cannot be reconstructed reliably from this workbook.

## Source-informed metric notes

Meta describes reach as an estimated count of people who saw content and impressions as the number of times content entered a person's screen:
https://www.facebook.com/help/274400362581037

Meta describes cost per result as a central performance metric for the Traffic objective and notes that traffic campaigns can optimize for outcomes including link clicks and landing-page views:
https://www.facebook.com/business/ads/ad-objectives/traffic

Meta describes frequency in practical terms as how often people see an ad, and defines ThruPlay optimization as showing shorter videos to people likely to watch them in full or longer videos to people likely to watch at least 15 seconds:
https://www.facebook.com/business/ads/ad-objectives/awareness

Google Ads defines CTR as clicks divided by impressions and average CPC as cost divided by clicks; its performance reporting also uses CPM, conversion rate, cost per conversion and conversion value/ROAS-style metrics:
https://support.google.com/google-ads/answer/2615875
https://support.google.com/google-ads/answer/2454071
https://support.google.com/google-ads/answer/6270625

These sources help define standard advertising metrics. They do **not** validate the historical outcomes in this repository; those outcomes come from the supplied Meta export and account evidence.
