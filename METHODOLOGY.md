# Methodology and analytical guardrails

## Purpose

This repository asks descriptive questions of a historical Meta Ads export. Its purpose is to document what the available data show and identify questions that a richer dataset could investigate. It does **not** estimate causal creative effects.

## Unit of analysis

Each row in the sanitized CSV represents one campaign row from the source export. Campaign names are not guaranteed to be unique, so `campaign_row_id` is the stable row identifier used in this repository.

## Comparison rules

1. **Compare cost per result only within the same result type.** A link click cannot be compared directly with a Facebook like, ThruPlay, post engagement or messaging conversation.
2. **Treat link clicks as link clicks.** They are not equated with landing-page views, YouTube views, purchases or revenue.
3. **Do not sum reach and call it unique people.** Meta describes reach as estimated; the same account can appear in the reach of several campaigns. Campaign reach is summed only as an export-level descriptive total and is always labelled `sum_campaign_reach`.
4. **Use weighted cost per result for grouped summaries.** This is calculated as total spend / total results, rather than averaging campaign-level cost-per-result values.
5. **Derived result rates are labelled as derived.** `results_per_1000_impressions` and link-clicks/impressions are arithmetic calculations from the export, not additional Meta-supplied metrics.
6. **Treat the repeated reporting dates as an export window.** They do not establish campaign-specific active dates.
7. **Flag malformed rows instead of repairing them silently.** Four rows have `result_type = 2`, and their exported cost-per-result value is inconsistent with spend/results. They are retained with `data_quality_flag = ambiguous_result_type` and excluded from result-type summaries.
8. **No retrospective creative coding where the asset is missing.** Most posts were deleted or disabled, so campaign names alone are insufficient to infer format, hook, creator, audience or creative angle reliably.
9. **No causal attribution.** Campaigns were not recovered as a controlled experiment. Audience, placement, budget strategy, optimisation, timing and other confounders are unavailable.
10. **No ROI/ROAS inference.** The workbook does not provide purchase revenue or verified downstream sales.

## Source-informed metric notes

Meta describes reach as the number of people who saw content (an estimated metric) and impressions as the number of times content entered a person's screen:
https://www.facebook.com/help/274400362581037

Meta describes cost per result as an important traffic-objective metric:
https://www.facebook.com/business/ads/ad-objectives/traffic

CPM is derived as amount spent / impressions * 1,000:
https://www.facebook.com/help/www/214576695231407

Meta also notes that campaign objectives influence optimisation and which outcomes the delivery system seeks:
https://www.facebook.com/business/ads/ad-objectives

These sources help define the metrics. They do not validate the historical campaign outcomes in this repository; those come from the supplied export.
