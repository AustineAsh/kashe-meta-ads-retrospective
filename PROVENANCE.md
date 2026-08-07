# Evidence provenance

## Source workbook

- Original local filename: `30-01-23.xlsx`
- Source sheet: `Raw Data Report`
- Source range represented: `A1:R129`
- Campaign rows prepared: **126**
- Recognised result rows: **122**
- Rows with blank result type/results/cost-per-result fields: **4**
- Export/reporting window shown in source: **2023-07-07 to 2026-08-07**
- Attribution setting shown throughout recognised rows: **7-day click or 1-day view**
- SHA-256: `5facbe664cfd86bdc64822ed081c43668637a67dff59ce754dc97eb5397e5dc0`

The original workbook is intentionally **not committed** because one campaign name contains a historical WhatsApp phone number. The verified source can be placed at `data/private/30-01-23.xlsx` in an authorised local environment. `scripts/prepare_data.py` checks its SHA-256 before generating the public derivative.

## Correction made during end-to-end reproduction

An earlier manual inspection of the XLSX internals described four records as having result type `2`. Reproducing the workbook ingestion with a proper shared-string resolver showed that shared-string index `2` is an empty string. The four records actually have **blank result type, blank Results and blank Cost per result** fields.

The reproducible pipeline preserves those four rows and flags them as `missing_result_type`. Their spend and delivery values remain in the public dataset, while they are excluded only from analyses that require a known result type. They account for **NGN 126.39 spend** and **462 impressions**, so the correction does not change the previously reported result-type KPIs.

## Targeted preparation

The public CSV is a generated, sanitised derivative rather than a manually edited copy. `scripts/prepare_data.py`:

1. verifies the expected workbook hash;
2. locates the header from the source labels;
3. checks that the duplicated campaign-name columns agree;
4. verifies that the three ranking columns contain no usable values before omitting them;
5. verifies that `Results (initial)` is blank on the campaign rows before omitting it;
6. preserves all 126 source rows and records the original Excel row number;
7. converts analysis fields to consistent numeric/text representations;
8. redacts only the phone digits in the historical WhatsApp URL;
9. flags blank or unknown result types instead of imputing them; and
10. records source/output hashes in `analysis/data_preparation_summary.json`.

No genuine high- or low-performing campaign is removed as an outlier. No deleted creative characteristic is inferred from an incomplete name, and no missing campaign/ad identifier is invented.

## Account-spend screenshot

- File: `evidence/meta_account_spend_screenshot.png`
- Visible account: `Austine Ashogbon`
- Amount shown as spent: **NGN 1,492,844.45**
- SHA-256: `9917c389153119b95e30c44c15bcb84482269567db4993995b363fa64def3d7c`

The screenshot is separate evidence and is not assumed to cover the identical scope as the workbook. The workbook records **NGN 1,029,228.11** spend, so it is treated as a partial surviving export.

## Author-reported historical campaign context

Some contextual information in the report is not contained in the Meta workbook. It comes from my historical records/recollection and is labelled as author-reported context. This includes:

- the **Bunda music-video production cost of more than NGN 5 million**;
- the **30+ person production team/set** and specialist production roles;
- the chronology between the manager-led phase, *Let's Fly Away* and Bunda;
- the four Portable opening appearances occurring in the earlier manager-led phase;
- X Ads, Google Ads and traditional/offline promotion not quantified by this Meta export; and
- my historical belief that cumulative traction supported media/live outreach and negotiation, which the report now treats as an **untested managerial hypothesis**.

## Explicit Bunda-name reconstruction

The analysis selects recognised rows whose surviving campaign name explicitly contains `Bunda`. This returns **18 rows**, **NGN 450,035.75 spend** and **3,085,893 impressions**. It is explicitly a **lower-bound identifiable subset** because generic or truncated campaign names may relate to Bunda without retaining the song title.

## Reproducibility records

- `analysis/data_preparation_summary.json` records preparation decisions and hashes.
- `analysis/validation_report.json` records automated validation results.
- `analysis/run_manifest.json` records runtime versions and SHA-256 hashes of code/configuration and derived products.
- `tests/test_pipeline.py` includes an end-to-end private-source test requiring the preparation stage to reproduce the committed public CSV byte-for-byte when the verified workbook is present.
