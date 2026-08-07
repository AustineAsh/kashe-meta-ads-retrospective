# Evidence provenance

## Source workbook

- Original local filename: `30-01-23.xlsx`
- Source sheet used: `Raw Data Report`
- Source range inspected: `A1:R129`
- Campaign rows extracted: **126**
- Export/reporting window shown in source: **2023-07-07 to 2026-08-07**
- Attribution setting shown throughout the recognized rows: **7-day click or 1-day view**
- SHA-256 of original workbook: `5facbe664cfd86bdc64822ed081c43668637a67dff59ce754dc97eb5397e5dc0`

The original workbook is intentionally not included in the public repository because one campaign name contains a historical WhatsApp phone number. `data/meta_campaign_export_sanitized.csv` is a derived copy in which phone-number material is redacted and analysis flags/derived metrics are added.

## Account-spend screenshot

- File in repository: `evidence/meta_account_spend_screenshot.png`
- Visible account: `Austine Ashogbon`
- Account-level amount shown as spent: **NGN 1,492,844.45**
- SHA-256 of supplied screenshot: `9917c389153119b95e30c44c15bcb84482269567db4993995b363fa64def3d7c`

The screenshot is separate evidence and is not assumed to cover the identical reporting scope as the spreadsheet. The spreadsheet records NGN 1,029,228.11, so the two sources are not forced to reconcile.

## Transformation

The public CSV:

1. extracts campaign rows from the raw-data sheet;
2. removes the duplicate campaign-name column and unused source fields;
3. redacts phone-number material from campaign names;
4. converts numeric fields into analysis-ready values;
5. adds arithmetic diagnostics and derived measures;
6. flags four ambiguous rows rather than silently repairing them.

No campaign performance value is manually substituted to make the data look cleaner.
