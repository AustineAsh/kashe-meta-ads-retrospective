# Kashe Music Group Meta Ads — Retrospective Creative Performance Analysis

This repository is a **retrospective, exploratory analysis** of historical Meta Ads campaign data from my work at Kashe Music Group / Santeri. I originally ran these campaigns before completing my later formal training in Information Technology, Information Systems, statistics, research methods and data analysis.

I built this repository for two reasons:

1. to re-examine the surviving campaign data with the analytical discipline I have developed since; and
2. to provide a transparent evidence trail for claims in my CV and job applications about having run paid media and used Meta performance data to inform creative decisions.

**This is not a causal or explanatory study.** It does not claim that a particular hook, creator, format, audience or campaign setting caused the observed performance differences. Most historical posts/creatives are no longer publicly available, and the export does not contain enough controls or metadata for causal attribution.

The only surviving public artist account is the [Santeri Facebook page](https://www.facebook.com/therealsanteri).

## What the surviving evidence shows

The sanitized export contains **126 campaign rows** and records:

- **NGN 1,029,228.11** of campaign spend in the export;
- **10,332,896 impressions**;
- **635,240 link clicks** across 106 link-click campaigns;
- **NGN 1.43 weighted cost per link click** across those link-click campaigns;
- **3,977 Facebook likes attributed** to two audience-growth campaigns;
- **86 messaging conversations started** across two messaging campaigns.

A separate Meta account screenshot records **NGN 1,492,844.45 spent at account level**. Because this is higher than the export total, I treat the workbook as an incomplete subset of the account's historical spend rather than a complete lifetime account export.

## One useful retrospective case: Bunda traffic campaigns

The two campaign rows explicitly named `Bunda Youtube – official` and `Bunda Youtube` record:

- **2,613,269 impressions**;
- **565,764 link clicks**;
- **NGN 391,913.64 spend**;
- **NGN 0.69 weighted cost per link click**.

These are Meta campaign outcomes, not YouTube analytics. A Meta link click is **not** treated as equivalent to a YouTube view, completed video view, purchase, revenue event or unique person.

## Why this is useful for creative analysis

The 106 link-click campaigns show large descriptive variation in campaign-level cost per link click:

- minimum: **NGN 0.29**;
- first quartile: **NGN 12.88**;
- median: **NGN 19.81**;
- third quartile: **NGN 36.06**;
- maximum: **NGN 397.11**.

That variation is the basis for **exploratory questions**, not explanations. With the original creative assets, audience settings, placements, dates and controlled test design, I would want to investigate whether differences were associated with factors such as creative format, hook, creator, audience, placement, campaign objective, spend level or optimisation settings. Those variables are not recoverable reliably from this export alone.

![Distribution of campaign cost per link click](assets/01_link_click_cost_distribution.png)

![Spend versus link clicks](assets/02_spend_vs_link_clicks.png)

![Top campaigns by link clicks](assets/03_top_link_click_campaigns.png)

![Selected cost per result examples](assets/04_selected_cost_per_result.png)

## Evidence boundary

The analysis deliberately separates three evidence levels:

| Claim | Evidence in this repository | Status |
|---|---|---|
| I ran Meta advertising campaigns | 126 campaign rows plus account-level spend screenshot | Supported |
| I used Meta performance data to compare campaign/post performance | Large observed variation in comparable link-click campaign outcomes; my historical role/context | Supported as work practice; not a causal claim |
| Meta account spend reached about NGN 1.49m | Account screenshot | Supported at account level |
| Two Bunda YouTube traffic campaigns generated 565k+ Meta link clicks | Sanitized export | Supported |
| Two audience-growth campaigns generated 3,977 attributed Facebook likes | Sanitized export | Supported |
| Messaging campaigns generated 86 conversations started | Sanitized export | Supported |
| The Facebook page grew from 0 to about 5,000 followers in four months | Historical account recollection; export partially supports paid audience growth through 3,977 attributed likes | Partially supported; no follower time series in this export |
| The Bunda video reached 230k+ YouTube views | Historical campaign record/recollection; original video is no longer publicly available | Not independently reproduced from this Meta export |
| Meta caused later shows, media appearances or industry opportunities | Not established by this dataset | Not claimed |

## Key limitations

- The analysis is **exploratory and descriptive**, not causal.
- Most original posts and creative assets were later deleted or disabled, so retrospective coding of hooks, formats, angles and creators is incomplete.
- The original workbook contains a historical WhatsApp phone number in one campaign name. The raw workbook is therefore **not published publicly**; a sanitized derivative is provided instead.
- The workbook's `Reporting starts` and `Reporting ends` values are repeated across campaign rows, so they are treated as the **export/reporting window**, not individual campaign start/end dates.
- Four rows contain an ambiguous result type/value (`2`) and fail a simple cost-per-result reconciliation check. They remain in the sanitized dataset with a `data_quality_flag` but are excluded from result-type performance summaries.
- Reach is an estimated audience metric and can overlap across campaigns. The sum of campaign reach is therefore **not reported as unique people reached**.
- Result types are not directly comparable. A Facebook like, link click, ThruPlay, post engagement and messaging conversation represent different optimisation goals.
- The workbook contains no purchase revenue, ROAS, customer lifetime value or verified downstream conversion data.
- Meta's 7-day click / 1-day view attribution setting describes how results were attributed in the export; it should not be read as proof of causal effect.
- Google Ads and X Ads were also used historically, but this repository contains **Meta evidence only**.

See [METHODOLOGY.md](METHODOLOGY.md) for the full analytical rules and [PROVENANCE.md](PROVENANCE.md) for the evidence chain.

## Reproduce the analysis

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analysis/retrospective_analysis.py
```

The script reads `data/meta_campaign_export_sanitized.csv`, regenerates the summary and charts, and applies the same guardrails documented in `METHODOLOGY.md`.

## AI assistance disclosure

Generative AI assisted with code development, documentation structure and quality checks. I defined the analytical purpose and evidence boundaries, selected the comparisons, checked the source data, reviewed the calculations and retain responsibility for the interpretation. AI-generated output is not treated as independent evidence.
