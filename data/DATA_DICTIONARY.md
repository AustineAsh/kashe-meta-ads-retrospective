# Data dictionary

This dictionary describes the columns actually published in
`meta_campaign_export_sanitized.csv`. The unit of observation is one row from
the historical Meta campaign export, not one unique creative asset or person.

| Field | Type | Meaning |
|---|---|---|
| `campaign_row_id` | integer | Stable sequential row identifier added by this project. It is not a Meta campaign ID. |
| `source_excel_row` | integer | Original Excel row number retained for source traceability. |
| `campaign_name` | text | Exported campaign name, with the historical WhatsApp phone number redacted. Names are not necessarily unique. |
| `result_type` | text | Outcome label exported by Meta. Four rows are blank and explicitly flagged. |
| `results` | number or blank | Count for the reported result type. Blank on the four rows whose result type is missing. Results from unlike types must not be added together. |
| `reach` | number | Exported row-level campaign reach. Do not sum it and interpret the total as unique people across rows. |
| `impressions` | number | Exported campaign-row impressions. |
| `cost_per_result_ngn` | number or blank | Meta's exported cost per reported result in Nigerian naira. Blank on the four rows whose result type is missing. |
| `amount_spent_ngn` | number | Exported campaign-row spend in Nigerian naira. |
| `data_quality_flag` | text | Blank for recognised result types. `missing_result_type` marks the four rows with blank result type, Results and Cost per result. |

The source attribution setting and global reporting-window values are recorded in
`analysis/data_preparation_summary.json`, but are not columns in the public CSV.
Derived CPC, CTR, CPM and impressions/reach measures are generated in the analysis
products rather than stored as source fields.
