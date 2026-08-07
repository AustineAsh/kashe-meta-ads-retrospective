# Evidence provenance

## Source workbook

- Original local filename: `30-01-23.xlsx`
- Source sheet used: `Raw Data Report`
- Source range inspected: `A1:R129`
- Campaign rows extracted: **126**
- Export/reporting window shown in source: **2023-07-07 to 2026-08-07**
- Attribution setting shown throughout the recognised rows: **7-day click or 1-day view**
- SHA-256 of original workbook: `5facbe664cfd86bdc64822ed081c43668637a67dff59ce754dc97eb5397e5dc0`

The original workbook is intentionally not included in the public repository because one campaign name contains a historical WhatsApp phone number. `data/meta_campaign_export_sanitized.csv` is a derived copy in which phone-number material is redacted and analysis flags/derived metrics are added.

## Account-spend screenshot

- File in repository: `evidence/meta_account_spend_screenshot.png`
- Visible account: `Austine Ashogbon`
- Account-level amount shown as spent: **NGN 1,492,844.45**
- SHA-256 of supplied screenshot: `9917c389153119b95e30c44c15bcb84482269567db4993995b363fa64def3d7c`

The screenshot is separate evidence and is not assumed to cover the identical reporting scope as the spreadsheet. The spreadsheet records NGN 1,029,228.11, so the two sources are not forced to reconcile.

## Author-reported historical campaign context

Some contextual information in the report is not contained in the Meta workbook. It comes from my historical records/recollection of the original artist project and is labelled accordingly rather than being presented as spreadsheet-derived evidence.

This currently includes:

- the **Bunda music-video production cost of more than NGN 5 million**;
- the **production set/team of more than 30 people** and the presence of specialist production roles such as producer, director and costume/styling, alongside scripted creative work;
- the distinction between the earlier **manager-led artist-development phase**, the later *Let's Fly Away* transition to broad creative-operations ownership, and the subsequent Bunda campaign;
- the four opening-act appearances involving Portable occurring in the earlier manager-led phase rather than during my later creative-operations ownership;
- the broader use of X Ads, Google Ads and traditional/offline promotion where those activities are not quantified in the Meta workbook; and
- my contemporaneous belief that cumulative online traction could help with media/live outreach and negotiation. The report treats this as an **untested historical managerial hypothesis**, not as a causal result established by the surviving data.

Where further primary evidence such as production budgets, invoices, call sheets, media schedules or booking correspondence becomes available, it can be added as a separate evidence layer without altering the provenance of the Meta dataset.

## Explicit Bunda-name reconstruction

The reproducible analysis identifies a conservative Bunda subset by selecting recognised Meta rows whose surviving campaign-name string explicitly contains `Bunda`.

This produces **18 rows**, **NGN 450,035.75 spend** and **3,085,893 impressions**. It is described as a **lower-bound identifiable subset** because generic or truncated campaign names may relate to Bunda without retaining the song title. It is therefore not represented as the complete Bunda Meta budget.

The statement that more than **NGN 5.45 million** can be directly identified across video production plus this explicit Meta subset combines two different evidence types: author-reported historical production expenditure (>NGN 5 million) and workbook-derived Meta spend (NGN 450,035.75). It is explicitly a minimum identifiable amount, not a complete total campaign budget.

## Transformation

The public CSV:

1. extracts campaign rows from the raw-data sheet;
2. removes the duplicate campaign-name column and unused source fields;
3. redacts phone-number material from campaign names;
4. converts numeric fields into analysis-ready values;
5. adds arithmetic diagnostics and derived measures;
6. flags four ambiguous rows rather than silently repairing them.

No campaign performance value is manually substituted to make the data look cleaner.
