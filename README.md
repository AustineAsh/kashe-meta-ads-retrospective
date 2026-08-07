# Kashe Music Group Meta Ads — Retrospective Creative Performance Analysis

> **Verification status:** The historical campaigns and source data relate to work I personally carried out. I have reviewed the source workbook and the analysis. The calculations were subsequently re-run directly against the raw-data sheet for additional diligence and cross-checked with ChatGPT assistance. All **122 rows with recognisable result types** reconcile their exported cost-per-result values to `spend / results` within normal floating-point precision. ChatGPT assisted with reproducible code, literature-supported analytical structuring and substantial drafting of the explanatory text. I retain responsibility for the published interpretation.

This repository is a retrospective analysis of surviving Meta Ads data from my work at **Kashe Music Group / Santeri**. It has two connected purposes: to examine the campaigns using the analytical discipline I developed after the original work, and to provide a transparent evidence trail for paid-media and creative-performance statements in my CV and cover letter.

The only surviving public artist account is the [Santeri Facebook page](https://www.facebook.com/therealsanteri).

## Executive summary

The analysis is organised around the purpose of measurement rather than around whichever metrics happened to survive in the export. Li, Larimo and Leonidou (2021) describe social media as both a marketing channel and a source of customer-behaviour information that firms can interpret and use in marketing decisions; they also show that objectives differ across social-media strategies and identify appropriate performance measurement as an important research problem ([Li et al., 2021](https://doi.org/10.1007/s11747-020-00733-3)). Yousef, Dietrich and Rundle-Thiele (2021) distinguish exposure, interaction and action in an experimental Facebook study and connect platform engagement with an external website behaviour ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)). Drawing on those ideas, I analyse the historical export across **delivery, attention, traffic response, downstream action and commercial value**. This five-layer structure is my synthesis for the case.

The surviving workbook contains **126 campaign rows**, **NGN 1,029,228.11 campaign spend** and **10,332,896 impressions**. A separate account screenshot records **NGN 1,492,844.45 spent**, indicating that the workbook is a partial historical export rather than a complete lifetime account record.

The strongest comparable set is the **106 link-click rows**. They record **635,240 link clicks** from **9,725,211 impressions** and **NGN 907,409.25 spend**, producing a portfolio-weighted **NGN 1.43 CPC**, **6.53% derived link CTR** and **NGN 93.30 CPM**. However, the median campaign-level CPC is **NGN 19.81** and median campaign-level derived CTR is **0.51%**. I therefore do not treat the pooled result as typical campaign performance.

The distribution explains the difference. The two Bunda YouTube traffic rows and the Pressure row produced **94.32% of all recorded link clicks** while using **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**. Bunda alone records **565,764 Meta link clicks from 2,613,269 impressions** at a weighted **NGN 0.69 CPC** and **21.65% derived link CTR**. Its CPM was higher than the overall link-campaign CPM, so the unusually low CPC is associated with the much higher recorded click rate rather than unusually cheap impression delivery. Removing Bunda reduces pooled link CTR to **0.98%** and raises CPC to **NGN 7.42**; removing Pressure as well leaves the remaining 103 rows at **0.52% CTR** and **NGN 14.02 CPC**.

The export also records **3,977 attributed Facebook likes**, **86 messaging conversations started**, **58,112 ThruPlays** and **12,859 post engagements** within their respective campaign groups. These measures answer different questions, so they are analysed separately rather than combined into a single performance total.

## What I infer from the retrospective

At the time, I used Meta performance information pragmatically: I compared how posts and campaigns were responding and used those signals when deciding what to promote and how to approach later creative activity. The retrospective shows that the differences I was seeing were substantial, but it also reveals something I did not formally analyse then: the headline account metrics were dominated by a small number of unusually high-response campaigns.

That is the main analytical development demonstrated here. I now separate portfolio-weighted and typical campaign performance, test how sensitive the aggregate is to outliers, distinguish delivery cost from response efficiency, and keep different campaign objectives analytically separate.

Current industry thinking reinforces the importance of that context. Nielsen (2025) argues that marketing measurement can produce many numbers without clarity unless KPIs are connected to business priorities and interpreted in context, while IAB UK's current Measurement Hub organises measurement approaches around objectives and outcomes ([Nielsen, 2025](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/); [IAB UK, 2026](https://www.iabuk.com/measurement)).

## Scope of the evidence

The surviving data are strongest for **delivery and traffic response**, partial for **attention and direct action**, and weak for **commercial value**. Many original posts are no longer available, and the export does not preserve a complete creative taxonomy, audience/placement detail, campaign-specific timing, purchases or revenue. I can therefore identify where exceptional performance appears and how it affects the portfolio result, but I cannot retrospectively isolate which hook, creator, format, audience or delivery variable caused the difference.

That boundary follows from the research question. Yousef et al. (2021), for example, used deliberately comparable creative variants, controlled exposure through Facebook A/B testing and measured a behaviour beyond the platform. I use that study as a methodological reference for what a stronger creative-effect claim would require, not as a benchmark for these music campaigns ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

## Repository guide

- **[Full exploratory report](reports/exploratory_findings.md)** — concepts, literature, sector context, findings and my interpretation.
- **[Methodology](METHODOLOGY.md)** — measurement model, data verification, formulas, comparison rules and analytical procedures.
- **[Sanitised campaign data](data/meta_campaign_export_sanitized.csv)** — public campaign-level derivative of the historical export.
- **[Reproducible analysis](analysis/retrospective_analysis.py)** — Python used to reproduce the descriptive analysis.
- **[Machine-readable summary](analysis/summary.json)** — verified KPI outputs.
- **[Provenance](PROVENANCE.md)** — source/evidence chain and file hashes.

![Distribution of campaign cost per link click](assets/01_link_click_cost_distribution.svg)

![Spend versus link clicks](assets/02_spend_vs_link_clicks.svg)

![Top campaigns by link clicks](assets/03_top_link_click_campaigns.svg)

## Reproduce the analysis

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analysis/retrospective_analysis.py
```

## AI assistance and author responsibility

The underlying historical advertising activity and source data relate to work I personally carried out. **ChatGPT did not participate in the original campaigns.**

I reviewed the source export and analysis. ChatGPT was used afterwards to re-run and cross-check calculations, assist with reproducible Python code, discover and structure relevant literature, and draft substantial portions of the repository prose. The numerical claims are checked against the source data; AI-generated prose is not treated as independent evidence.

I retain responsibility for the final interpretation, the distinction between source-recorded and derived metrics, and the evidence boundaries stated in this repository.