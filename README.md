# Kashe Music Group Meta Ads — Retrospective Creative Performance Analysis

> **Verification status:** The historical campaigns and source data in this repository relate to work I personally carried out. I have reviewed the source export and the analysis. For additional diligence, the calculations were re-run directly against the raw-data sheet and cross-checked with ChatGPT assistance. All **122 rows with recognized result types** reconcile their exported cost-per-result values to `spend / results` within normal floating-point precision. ChatGPT also assisted with the reproducible code and drafted much of the explanatory text. I retain responsibility for the published interpretation and evidence boundaries.

This repository is a **retrospective, exploratory analysis** of historical Meta Ads campaign data from my work at Kashe Music Group / Santeri. I originally ran these campaigns before completing my later formal training in Information Technology, Information Systems, statistics, research methods and data analysis.

I built this repository for two reasons:

1. to re-examine the surviving campaign data with the analytical discipline I have developed since; and
2. to provide a transparent evidence trail for claims in my CV and cover letter about having run paid media and used Meta performance data to inform creative decisions.

**This is not a causal or explanatory study.** It does not claim that a particular hook, creator, format, audience or campaign setting caused the observed performance differences. Most historical posts/creatives are no longer publicly available, and the export does not contain enough controls or metadata for causal attribution.

The only surviving public artist account is the [Santeri Facebook page](https://www.facebook.com/therealsanteri).

## What the surviving evidence shows

The sanitized export contains **126 campaign rows** and records:

- **NGN 1,029,228.11** campaign spend;
- **10,332,896 impressions**;
- **8,630,892 summed campaign-level reach** — not unique people;
- **635,240 link clicks** across 106 link-click rows;
- **3,977 attributed Facebook likes** across two audience-growth rows;
- **86 messaging conversations started** across two messaging rows;
- **58,112 ThruPlays** across six video-view rows.

A separate Meta account screenshot records **NGN 1,492,844.45 spent at account level**. The workbook therefore represents about **68.94%** of that account-level figure and should be treated as a surviving subset rather than a complete lifetime account export.

## Derived link-click KPIs

Across the 106 rows using `Link clicks` as the result type:

- **NGN 907,409.25 spend**;
- **9,725,211 impressions**;
- **635,240 link clicks**;
- **NGN 1.43 weighted CPC** (`spend / clicks`);
- **6.53% derived link CTR** (`clicks / impressions`);
- **NGN 93.30 derived CPM** (`spend / impressions × 1,000`);
- **1.20 impressions per summed campaign reach**.

The aggregate is highly concentrated. The **median campaign-level CPC is NGN 19.81**, versus the **NGN 1.43 weighted CPC**. The median campaign-level derived CTR is **0.51%**. This difference matters because a few very high-volume rows dominate the account-wide weighted figures.

Using Python's `statistics.quantiles(..., method="exclusive")`, campaign-level CPC ranges from **NGN 0.29 to NGN 397.11**, with sample quartiles of **NGN 12.88** and **NGN 36.06**.

## Bunda traffic case

The two rows explicitly named `Bunda Youtube – official` and `Bunda Youtube` record:

- **565,764 Meta link clicks**;
- **2,613,269 impressions**;
- **NGN 391,913.64 spend**;
- **NGN 0.69 weighted CPC**;
- **21.65% derived link CTR**;
- **NGN 149.97 derived CPM**;
- **1.61 impressions per summed campaign reach**.

Together they account for **89.06% of all link clicks**, **43.19% of link-campaign spend**, **38.08% of total export spend**, and **26.87% of link-campaign impressions**.

A useful descriptive observation is that the low CPC was not produced by unusually cheap impressions: the Bunda CPM was higher than the overall link-campaign CPM. Arithmetically, the low CPC coincided with a much higher click rate. That does **not** prove which creative, audience or delivery factor caused the difference.

As a sensitivity check, excluding the two Bunda rows raises weighted CPC across the remaining link-click rows to **NGN 7.42** and reduces derived CTR to **0.98%**. Excluding both Bunda rows and the unusually strong `Pressure` row raises weighted CPC to **NGN 14.02** and reduces derived CTR to **0.52%**.

These are Meta campaign outcomes, not YouTube analytics. A Meta link click is **not** treated as equivalent to a YouTube view, completed video view, purchase, revenue event or unique person.

## Why this is useful for creative analysis

The performance spread provides legitimate **exploratory questions**. With the original assets and complete account metadata, I would want to compare hooks, formats, angles, creators, CTAs and placements within properly comparable test cells and then connect those upstream creative signals to downstream conversion and commercial outcomes.

The current export cannot answer that causal question because most assets are no longer available and it lacks reliable audience, placement, creative-taxonomy, campaign-specific timing, purchase and revenue fields.

The charts below are descriptive visualisations generated from the sanitized campaign data.

![Distribution of campaign cost per link click](assets/01_link_click_cost_distribution.svg)

![Spend versus link clicks](assets/02_spend_vs_link_clicks.svg)

![Top campaigns by link clicks](assets/03_top_link_click_campaigns.svg)

See [reports/exploratory_findings.md](reports/exploratory_findings.md) for the fuller breakdown and [analysis/summary.json](analysis/summary.json) for machine-readable verified outputs.

## Evidence boundary

| Claim | Evidence in this repository | Status |
|---|---|---|
| I ran Meta advertising campaigns | 126 campaign rows plus account-level spend evidence | Supported by surviving source material |
| I used Meta performance data to compare campaign/post performance | Large observed variation in comparable link-click outcomes plus historical work context | Supported as work practice; not a causal claim |
| Meta account spend reached about NGN 1.49m | Account screenshot supplied for the analysis | Supported at account level |
| Two Bunda YouTube traffic rows generated 565k+ Meta link clicks | Sanitized export | Supported by the export |
| Two audience-growth rows generated 3,977 attributed Facebook likes | Sanitized export | Supported by the export |
| Messaging rows generated 86 conversations started | Sanitized export | Supported by the export |
| The Facebook page grew from 0 to about 5,000 followers in four months | Historical account record/recollection; export partially supports paid audience growth through 3,977 attributed likes | Partially supported; no follower time series in this export |
| The Bunda video reached 230k+ YouTube views | Historical campaign record/recollection; original video is no longer publicly available | Not independently reproduced from this Meta export |
| Meta caused later shows, media appearances or industry opportunities | Not established by this dataset | Not claimed |

## Key limitations

- The analysis is **exploratory and descriptive**, not causal.
- Most original posts and creative assets were later deleted or disabled, so retrospective coding of hooks, formats, angles and creators is incomplete.
- The original workbook contains a historical WhatsApp phone number in one campaign name. The raw workbook is therefore **not published publicly**; a sanitized derivative is provided instead.
- The workbook's `Reporting starts` and `Reporting ends` values are repeated across campaign rows, so they are treated as the **export/reporting window**, not individual campaign start/end dates.
- Four rows contain an ambiguous result type/value (`2`). They remain in the sanitized dataset with a `data_quality_flag` but are excluded from result-type performance summaries.
- Reach is estimated and can overlap across campaigns. Summed campaign reach is therefore **not unique people reached**.
- Result types are not directly comparable. A Facebook like, link click, ThruPlay, post engagement and messaging conversation represent different optimization goals.
- The workbook contains no purchase revenue, verified ecommerce conversions, ROAS, AOV or customer acquisition cost.
- Meta's 7-day click / 1-day view attribution setting describes how results were attributed in the export; it should not be read as proof of causal effect.
- Google Ads and X Ads were also used historically, but this repository contains **Meta evidence only**.

See [METHODOLOGY.md](METHODOLOGY.md) for the analytical rules and [PROVENANCE.md](PROVENANCE.md) for the evidence chain.

## Reproduce the analysis

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analysis/retrospective_analysis.py
```

The script reads `data/meta_campaign_export_sanitized.csv`, regenerates `analysis/summary.json` and the descriptive charts, and applies the same guardrails documented in `METHODOLOGY.md`.

## AI assistance and author responsibility

The underlying historical advertising activity and source data relate to work I personally carried out. **ChatGPT did not participate in the original campaigns.**

I have reviewed the source export and the analytical interpretation. ChatGPT was subsequently used to re-run and cross-check calculations, assist with reproducible Python code, identify additional descriptive KPIs and draft/structure much of the repository text. The numerical claims presented here have been checked against the source data; AI-generated prose is not treated as independent evidence.

I retain responsibility for the final interpretation, for distinguishing source-recorded metrics from derived calculations, and for the limitations stated in this repository.
