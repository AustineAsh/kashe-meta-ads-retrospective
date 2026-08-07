# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| `campaign_row_id` | integer | Stable sequential identifier added for this repository; campaign names are not necessarily unique. |
| `campaign_name` | text | Campaign name from the export, with phone-number material redacted. |
| `delivery_status` | text | Exported delivery status. |
| `delivery_level` | text | Exported delivery level (campaign in this dataset). |
| `attribution_setting` | text | Attribution setting reported by Meta. |
| `result_type` | text | Outcome Meta reported for the campaign row. |
| `results` | number | Count of the reported result type. |
| `reach` | number | Exported campaign reach. Do not sum and interpret as unique people across campaigns. |
| `impressions` | number | Exported impressions. |
| `cost_per_result_ngn` | number | Exported cost per reported result in Nigerian naira. |
| `amount_spent_ngn` | number | Exported campaign spend in Nigerian naira. |
| `reporting_starts` | date text | Reporting-window start repeated in the source export; not treated as campaign start date. |
| `reporting_ends` | date text | Reporting-window end repeated in the source export; not treated as campaign end date. |
| `impressions_per_reach` | number | Derived: impressions / campaign reach. Frequency-like descriptor, not an independently exported Meta metric here. |
| `results_per_1000_impressions` | number | Derived: results / impressions * 1,000. Only meaningful within a result type. |
| `cpm_ngn` | number | Derived: spend / impressions * 1,000. |
| `data_quality_flag` | text | Flags known ambiguity. `ambiguous_result_type` is used for four malformed rows. |
| `cpr_recalculation_abs_diff` | number | Absolute difference between exported cost per result and spend/results, used as a diagnostic. |
