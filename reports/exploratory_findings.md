# Exploratory findings

## 1. Verification status and dataset footprint

The source workbook was re-read from its raw-data sheet and the calculations were re-run independently of the earlier written summary.

The export contains **126 campaign rows**, of which **122 have recognized result types** and **4 contain an ambiguous result type (`2`)**. Across all 126 rows it records:

- **NGN 1,029,228.11 spend**;
- **10,332,896 impressions**;
- **8,630,892 summed campaign-level reach**.

The reach figure is not interpreted as unique people because the same person can be reached by multiple campaigns.

As an arithmetic integrity check, **all 122 recognized rows reconcile**: `amount spent / results` reproduces the exported cost-per-result value to normal floating-point precision. The four ambiguous rows do not contain a usable result type and are excluded from result-type summaries.

A separate Meta account screenshot records **NGN 1,492,844.45 spent at account level**. The workbook therefore captures about **68.94%** of that account-level spend, leaving **NGN 463,616.34 (31.06%)** outside this export. The spreadsheet should consequently be treated as a surviving subset rather than the complete account history.

## 2. Link-click campaigns

There are **106** recognized link-click campaign rows, recording:

- **635,240 link clicks**;
- **NGN 907,409.25 spend**;
- **9,725,211 impressions**;
- **8,073,807 summed campaign reach**.

Derived grouped KPIs are:

- **NGN 1.43 weighted CPC** (`spend / link clicks`);
- **6.53% implied link CTR** (`link clicks / impressions`);
- **NGN 93.30 weighted CPM** (`spend / impressions × 1,000`);
- **1.20 impressions per summed campaign reach** (`impressions / summed reach`).

The grouped figures are strongly influenced by a few very large, high-performing rows. The **median campaign-level CPC is NGN 19.81**, while the weighted CPC is only NGN 1.43. Median campaign-level implied CTR is **0.51%** and median campaign CPM is **NGN 90.74**.

Using Python's `statistics.quantiles(..., method="exclusive")`, the sample first and third quartiles for campaign-level CPC are **NGN 12.88** and **NGN 36.06**. The observed range is **NGN 0.29 to NGN 397.11**.

This dispersion shows that campaign outcomes differed substantially. It does **not** establish why they differed.

## 3. Performance concentration

The top three link-click rows by recorded clicks are:

1. `Bunda Youtube – official`;
2. `Bunda Youtube`;
3. `Post: "Feel the beats, feel the 'Pressure.' Now..."`.

Together they generated **599,178 link clicks**, or **94.32% of all link clicks**, from **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**.

This concentration matters when interpreting account-wide averages: a small number of rows materially lower the weighted CPC and raise the weighted CTR.

## 4. Bunda YouTube traffic rows

The two rows explicitly named `Bunda Youtube – official` and `Bunda Youtube` record:

- **565,764 link clicks**;
- **2,613,269 impressions**;
- **1,619,607 summed campaign reach**;
- **NGN 391,913.64 spend**.

Derived KPIs are:

- **NGN 0.69 weighted CPC**;
- **21.65% implied link CTR**;
- **NGN 149.97 weighted CPM**;
- **1.61 impressions per summed campaign reach**.

The two rows account for **89.06% of all link clicks**, **43.19% of link-campaign spend**, **38.08% of total export spend**, and **26.87% of link-campaign impressions**.

A useful descriptive point is that Bunda's low CPC was **not** driven by unusually cheap impressions: its combined CPM was higher than the overall link-campaign CPM. The low CPC is arithmetically associated with the much higher link-click rate. That remains a descriptive relationship, not proof that a particular creative element caused it.

If the two Bunda rows are excluded, the remaining 104 link-click rows record **69,476 clicks from NGN 515,495.61 spend**, producing **NGN 7.42 weighted CPC** and **0.98% implied link CTR**. If the unusually strong `Pressure` row is also excluded, the remaining 103 rows produce **NGN 14.02 weighted CPC** and **0.52% implied link CTR**.

These sensitivity checks demonstrate how much the headline aggregate is driven by a few high-volume rows.

The outcome recorded in this dataset is a **Meta link click**. No inference is made from these clicks to YouTube views, watch time, subscriptions, revenue or downstream industry opportunities.

## 5. Selected individual link-click examples

| Campaign | Link clicks | Spend (NGN) | Implied CTR | CPC (NGN) | CPM (NGN) |
|---|---:|---:|---:|---:|---:|
| Post: "Feel the beats, feel the 'Pressure.' Now..." | 33,414 | 9,825.00 | 30.32% | 0.29 | 89.14 |
| Bunda Youtube – official | 480,589 | 294,600.87 | 22.86% | 0.61 | 140.11 |
| Bunda Youtube | 85,175 | 97,312.77 | 16.68% | 1.14 | 190.58 |
| DJ Khoded Valid Concert II | 8,213 | 12,919.39 | 16.73% | 1.57 | 263.25 |
| Instagram post: Bunda Baddie @ceebee__... | 1,500 | 5,999.84 | 6.67% | 4.00 | 266.60 |
| Instagram post: Join the #BundaDanceChallenge... | 154 | 17,659.03 | 0.50% | 114.67 | 577.58 |

The purpose of this table is to show the range of outcomes among rows sharing the same result type. Without consistent creative metadata, audience, placement, timing and test design, it should not be used to infer causal creative effects.

## 6. Audience-growth campaigns

Two `Promoting Santeri` rows use `Facebook likes` as the result type. Together they record:

- **3,977 attributed Facebook likes**;
- **NGN 73,259.03 spend**;
- **39,504 impressions**;
- **NGN 18.42 weighted cost per attributed like**.

This supports the historical account that paid promotion materially contributed to audience growth. It does not recreate a follower time series or establish the full source of page growth.

## 7. Messaging campaigns

Two rows record **86 messaging conversations started** from **NGN 10,769.04 spend**, giving a weighted **NGN 125.22 per conversation**.

The larger of the two generated **78 conversations from NGN 8,460.63**, or **NGN 108.47 per conversation**.

One campaign name included a direct WhatsApp URL and phone number in the original workbook. That phone number is redacted in the public dataset.

## 8. Video and engagement outcomes

The export also contains smaller groups with other optimization goals:

- **58,112 ThruPlays** across 6 rows from **NGN 20,596.01 spend**, or **NGN 0.35 weighted cost per ThruPlay**. ThruPlays equal **12.48% of impressions** across those six rows as a derived descriptive rate.
- **12,859 post engagements** across 4 rows from **NGN 15,606.98 spend**, or **NGN 1.21 weighted cost per engagement**.
- One row records **3,233 three-second video plays from 12,144 impressions**, giving a derived **26.62% three-second-view/impression rate** and **NGN 0.14 cost per three-second play**.
- One lead-form row records **1 lead at NGN 1,009.17**. A single observation is not sufficient for meaningful performance inference.

A conventional video `hold rate` cannot be reconstructed reliably because the three-second-view and ThruPlay metrics were not recorded for the same set of creatives/campaign rows.

## 9. What the dataset cannot calculate

For an ecommerce creative-analysis role, important downstream KPIs would normally include landing-page views, outbound CTR, purchase conversion rate, cost per acquisition, conversion value/revenue, return on ad spend, average order value and related customer-economics metrics. Those fields are absent here.

The export also lacks reliable creative-element labels (hook, angle, format, creator, CTA), campaign/ad IDs, audience, placement, device, campaign-specific active dates and controlled-test assignments. The quality, engagement-rate and conversion-rate ranking columns in the original workbook are blank (`-`) for every row.

Therefore, this repository can demonstrate historical paid-media activity and provide descriptive performance analysis, but it cannot retrospectively answer the stronger causal question: **which creative element drove conversions?**

## 10. What I would analyse differently with complete historical data

With complete assets and account metadata, I would build a creative taxonomy (hook, format, creator, angle, CTA, duration, platform/placement), join it to delivery and conversion data, define comparable test cells, and evaluate both upstream creative diagnostics and downstream commercial outcomes.

For video, that would include consistent three-second-view, retention/ThruPlay and click metrics. For ecommerce, the main outcome layer would include conversion rate, CPA/CAC, revenue/conversion value and ROAS. Where genuine randomized or otherwise well-controlled tests existed, uncertainty, effect sizes and statistical significance could be assessed. Where they did not, conclusions would remain observational.
