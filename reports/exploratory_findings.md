# Exploratory findings

## 1. Dataset footprint

The export contains **126 campaign rows**. Across all rows it records **NGN 1,029,228.11** spend and **10,332,896 impressions**. The sum of campaign-level reach is **8,630,892**, but this is not interpreted as unique people because reach can overlap between campaigns.

Four campaign rows have an ambiguous result type (`2`). Their cost-per-result fields also fail reconciliation against spend/results, so they are excluded from result-type summaries while remaining visible in the public CSV.

## 2. Link-click campaigns

There are **106** recognized link-click campaign rows, recording **635,240 link clicks**, **NGN 907,409.25 spend**, and **9,725,211 impressions**.

The grouped weighted cost per link click is **NGN 1.43**. Campaign-level cost per link click is highly dispersed: the median is **NGN 19.81**, while the observed range is **NGN 0.29 to NGN 397.11**.

This variation is evidence that campaigns performed differently on the exported outcome. It is **not evidence of why** they performed differently.

## 3. Bunda YouTube traffic rows

The two rows explicitly named `Bunda Youtube – official` and `Bunda Youtube` record **565,764 link clicks**, **2,613,269 impressions**, and **NGN 391,913.64 spend**, producing a weighted **NGN 0.69 per link click**.

These campaigns account for about **89.1%** of all link clicks in the export while accounting for about **38.1%** of recorded spend.

The outcome is a Meta link click. No inference is made from those clicks to YouTube views, watch time, subscriptions, revenue or downstream industry opportunities.

## 4. Audience-growth campaigns

Two `Promoting Santeri` rows use `Facebook likes` as the result type. Together they record **3,977 attributed Facebook likes** from **NGN 73,259.03 spend**, a weighted cost of **NGN 18.42 per attributed like**.

This supports the historical account that paid promotion materially contributed to audience growth. It does not recreate a follower time series or establish the full source of page growth.

## 5. Messaging campaigns

Two campaigns record **86 messaging conversations started** from **NGN 10,769.04 spend**, a weighted **NGN 125.22 per conversation**.

One campaign name included a direct WhatsApp URL and phone number in the original workbook. That phone number is redacted in the public dataset.

## 6. Selected comparable examples

All examples below use `Link clicks` as the result type, making cost-per-result comparison more defensible than comparison across different campaign objectives.

| Campaign | Link clicks | Spend (NGN) | Cost/link click (NGN) |
|---|---:|---:|---:|
| Post: "Feel the beats, feel the 'Pressure.' Now..." | 33,414 | 9,825.00 | 0.29 |
| Bunda Youtube – official | 480,589 | 294,600.87 | 0.61 |
| Bunda Youtube | 85,175 | 97,312.77 | 1.14 |
| Instagram post: Bunda Baddie @ceebee__... | 1,500 | 5,999.84 | 4.00 |
| Instagram post: Join the #BundaDanceChallenge... | 154 | 17,659.03 | 114.67 |

The table demonstrates large observed variation. It does not identify the causal role of creative, audience, placement, timing or budget because those controls are absent.

## 7. What I would analyse differently with complete historical data

If the deleted creative assets and campaign-level settings were recoverable, a stronger analysis would first build a creative taxonomy (hook, format, creator, angle, CTA, duration, platform/placement), join it to spend and delivery metadata, define comparable tests, and only then assess whether observed differences remain after accounting for audience, placement, timing, budget and objective. Where controlled experiments existed, confidence intervals or appropriate hypothesis tests could be used. Where they did not, results would remain observational.
