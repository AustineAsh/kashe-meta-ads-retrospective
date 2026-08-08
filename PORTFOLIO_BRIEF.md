# Portfolio brief: from campaign delivery to evidence-led creative testing

## Purpose

This project revisits a campaign I helped deliver before completing my formal IT and postgraduate data training. It demonstrates two connected capabilities:

1. practical experience coordinating creative work, contributors and paid promotion; and
2. the ability to return to incomplete historical evidence, reconstruct it carefully, test what can be verified and state what the data cannot support.

It is evidence of development and methodological discipline, not a claim that I was already working as a specialist creative analyst.

## My historical role

At Kashe Music Group I moved from artist activity into broader creative and operational responsibility. I helped coordinate release assets and contributors, managed parts of digital promotion, worked with creators and partners, monitored response and used that information in ongoing campaign decisions and outreach. During the paid-growth phase, I grew the Facebook page audience from launch to around 5,000 in just over a month before it plateaued. I also used click-to-WhatsApp campaigns to build a direct audience contact list for closer engagement, while the Bunda music video reached 230,000+ YouTube views during its active release period.

The later Bunda campaign involved a larger production and promotional resource bundle. The Meta workbook records paid delivery and platform response, including 3,977 attributed Facebook likes and 86 messaging conversations across the relevant rows. The complete Facebook growth timeline, later use of WhatsApp contacts, YouTube total, production scale, chronology and offline activity come from my historical account and are therefore reported separately from workbook-derived claims.

## Evidence recovered

- 126 Meta campaign rows across several result types.
- NGN 1,029,228.11 recorded spend and 10,332,896 impressions.
- 106 comparable link-click rows with 635,240 clicks.
- A source-verified, phone-redacted public dataset and an automated validation report.
- Reproducible KPI tables, sensitivity analysis and five visualisations.

The public data is weighted heavily toward traffic campaigns: 106 of 126 rows report link clicks. The remaining result types have between one and six rows each, so they are retained as descriptive evidence rather than used for broad cross-objective conclusions.

## Main findings

The link-click portfolio appears efficient when viewed only through pooled metrics: **NGN 1.43 weighted CPC** and **6.53% derived CTR**. That summary is dominated by three campaign rows. Two Bunda YouTube traffic rows and one Pressure row account for **94.32% of link clicks**, despite representing **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**.

Without the two Bunda traffic rows, weighted CPC rises to **NGN 7.42** and derived CTR falls to **0.98%**. Removing Pressure as well leaves **NGN 14.02 CPC** and **0.52% CTR**. The decision lesson is that a portfolio average should not be treated as the expected result of a typical creative or campaign row.

The strongest recorded traffic response cannot be attributed to a particular hook, format, angle, creator or audience. Those variables were not preserved consistently, and platform delivery also depends on objective, targeting, budget, duration and creative. The historical export supports descriptive comparison, not a causal creative-performance claim.

## How I would communicate the result

**Finding:** response was unusually concentrated in three rows.

**Implication:** use those rows to generate creative hypotheses, not as proof that one remembered feature caused performance.

**Action:** recover the underlying assets where possible, code their observable features using a predefined taxonomy, and test the most commercially useful hypotheses prospectively.

**Risk:** optimising only for inexpensive clicks could improve a platform metric without improving purchases, contribution margin or customer value.

## Proposed next-campaign design

This is a prospective design for a future campaign. It was not applied retrospectively to the historical data.

### 1. Define the decision and outcome

- State the decision the test must inform, such as which opening hook should be developed into the next production batch.
- Select one primary commercial KPI before launch, such as cost per purchase or contribution margin per impression.
- Retain diagnostic measures such as thumb-stop/hold measures, click-through rate and landing-page conversion, but do not substitute them for the primary outcome.

### 2. Create a stable creative taxonomy

For every asset, preserve:

- creative and version ID;
- hook and opening visual;
- format and duration;
- angle or customer problem addressed;
- creator/talent and delivery style;
- product, offer, CTA and landing page;
- production date and cost; and
- approval status and source file.

For every delivery cell, preserve objective, optimisation event, audience, placement, geography, budget, schedule and attribution setting. Meta describes objective, targeting, budget, duration and creative as connected inputs to ad-auction performance, so these conditions must be retained before creative differences can be interpreted responsibly.

### 3. Use a controlled comparison where attribution matters

- Form one testable hypothesis and nominate the focal creative factor.
- Keep the remaining test conditions as comparable as the platform and business context allow.
- Randomly allocate exposure through an appropriate platform experiment rather than comparing unrelated historical rows.
- Pre-specify the analysis window, exclusions, decision rule and minimum effect worth detecting.
- Estimate sample requirements from baseline conversion, the minimum detectable effect and chosen error/power thresholds; report uncertainty as well as the point estimate.
- Avoid repeatedly stopping and restarting based only on an early favourable result.

Meta recommends A/B testing for learning about Reels creative and placements. Statistical design still depends on the outcome and experiment type; work on Facebook lift studies likewise shows that significance, power and required sample size need explicit treatment rather than a generic traffic threshold.

### 4. Connect platform response to business value

- Validate campaign and conversion tracking before launch.
- Carry stable IDs into analytics, order and customer records where lawful and technically feasible.
- Reconcile spend, platform conversions and downstream outcomes.
- Segment results only where the design and sample support it; label exploratory subgroup findings as hypotheses.

### 5. Turn the result into the next brief

The reporting output should contain the decision, hypothesis, test conditions, data-quality checks, result with uncertainty, commercial interpretation, limitations and the next creative action. A creator brief should translate the finding into observable changes while preserving what still needs to be tested.

## Evidence boundary

The historical analysis can establish recorded spend, delivery, platform results, arithmetic consistency, concentration and sensitivity. It cannot recover deleted creative variables, validate Meta's original attribution independently, establish total return on production investment or prove why later media and live opportunities occurred.

That boundary is part of the project: reliable analysis requires saying when the available evidence is not capable of answering the business question.

## Sources informing the proposed design

- Meta for Business, *The ad auction explained*: https://www.facebook.com/business/ads/ad-auction
- Meta for Business, *Facebook and Instagram Reels ads*: https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- Liu, C.H.B., Bettaney, E.M. and Chamberlain, B.P. (2018), *Designing Experiments to Measure Incrementality on Facebook*: https://arxiv.org/abs/1806.02588
