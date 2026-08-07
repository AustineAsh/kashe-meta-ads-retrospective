# Kashe Music Group / Santeri: Retrospective Creative Campaign Analysis

> **Verification status:** The historical campaigns and source data relate to work I personally carried out. I reviewed the source workbook and the analysis. The quantitative calculations were re-run directly against the raw-data sheet and cross-checked with ChatGPT assistance. All **122 rows with recognisable Meta result types** reconcile their exported cost-per-result values to `spend / results` within normal floating-point precision. ChatGPT assisted with reproducible code, literature discovery/structuring and substantial drafting of the explanatory text. I retain responsibility for the published interpretation.

This repository examines surviving evidence from my work at **Kashe Music Group / Santeri**. It has two purposes: to analyse the historical campaigns using the stronger analytical discipline I developed later, and to provide a transparent evidence trail for paid-media and creative-campaign statements in my CV and cover letter.

The only surviving public artist account is the [Santeri Facebook page](https://www.facebook.com/therealsanteri).

## Executive summary

The campaign cannot be understood from Meta metrics alone. Creative production itself consumes resources. Throsby (2006) distinguishes inputs such as labour, physical/operating capital and human capital in artistic production, while Gander's (2015) music-production study shows the importance of temporarily assembled specialist teams, material resources, knowledge and organisational coordination ([Throsby, 2006](https://doi.org/10.1007/s10824-005-9001-4); [Gander, 2015](https://doi.org/10.1108/MD-03-2014-0165)). I use those concepts to organise this case into **creative/intellectual assets, specialist human capital, technical/operating capital, financial capital, organisational capability, network resources, media channels and information resources**.

Chronology matters. Before *Let's Fly Away*, I was in a **manager-led artist-development phase**. Four opening-act appearances involving Portable occurred then, two at shows he organised and two at third-party shows where he was also booked. I was not directing creative operations for those events. They are therefore baseline evidence of an existing artist trajectory and network access, not outcomes of the later social-media strategy.

*Let's Fly Away* marked my transition to broad creative ownership. *Bunda* was a further step-change in **production intensity and resource commitment**. The music video cost more than **NGN 5 million** according to my historical production records/recollection and involved a professional set of more than **30 people**, including specialist roles such as producer, director and costume/styling together with scripted creative development. I treat those facts as evidence of production inputs and specialisation rather than as an objective measure of artistic quality.

The surviving Meta data provide a documented paid-media layer. **Eighteen rows whose surviving names explicitly contain Bunda** record **NGN 450,035.75 spend** and **3,085,893 impressions**. Fifteen are link-click rows, recording **568,819 clicks from NGN 438,522.79 spend**, while three record **29,344 ThruPlays from NGN 11,512.96 spend**. Because some other exported names are generic or truncated, these 18 rows are a **lower-bound identifiable Bunda subset**, not a complete Bunda advertising total. Combining the author-reported video-production cost with only this explicit Meta subset identifies more than **NGN 5.45 million** of production and Meta expenditure before other digital and traditional/offline promotion is included.

The campaign also used a broader media mix. Lovett and Staelin (2016) distinguish **paid media** (advertising), **earned media** (word of mouth, social-media buzz and publicity) and **owned media** (brand-generated content/channels) in an entertainment setting ([Lovett & Staelin, 2016](https://doi.org/10.1287/mksc.2015.0961)). For this case, owned media included artist accounts and creative assets; paid media included Meta, X and Google advertising; earned media included organic sharing, discussion and unsolicited interest. I separately describe radio/TV outreach, DJs/clubs, live activity and other traditional promotion as **offline/intermediated promotion**, because those channels can be paid, earned or relationship-driven depending on the activity.

At the time, I believed that the culmination of stronger content, paid distribution, organic engagement and offline promotion created visible **market traction**, and that this helped during outreach and negotiation for television, radio and live opportunities. Some opportunities were negotiated outbound and others came inbound. I now treat that belief as an **untested managerial hypothesis**, not a result. Pre-existing artist relationships, production value, song characteristics, paid reach, organic word of mouth, offline promotion, timing, algorithms and gatekeeper preferences are all plausible drivers that were never isolated.

A Nigerian radio study makes one part of that hypothesis plausible without proving my case. Okolie and Onwuegbuna (2024) interviewed **16 Port Harcourt radio stations** and found that social-media responses, direct artist contact and artist online platforms featured in their reported popularity/programming environment ([Okolie & Onwuegbuna, 2024](https://www.researchgate.net/publication/380345560_Evolving_Trends_in_Radio_Popularization_of_Nigerian_Urban_Music)). Polak and Schaap (2024), from interviews with professional musicians, provide a complementary reason for caution: platform success is difficult for artists to interpret and can feel like a black box ([Polak & Schaap, 2024](https://doi.org/10.1177/14614448241243095)).

Within that wider resource system, the Meta export allows a narrower performance question to be answered rigorously. Across **126 campaign rows**, it records **NGN 1,029,228.11 spend** and **10,332,896 impressions**. A separate account screenshot records **NGN 1,492,844.45 spent**, so the workbook is a partial historical export.

Across the **106 link-click rows**, the export records **635,240 link clicks** from **9,725,211 impressions** and **NGN 907,409.25 spend**, producing a portfolio-weighted **NGN 1.43 CPC**, **6.53% derived CTR** and **NGN 93.30 CPM**. Those pooled values hide a highly concentrated distribution: median campaign CPC is **NGN 19.81** and median derived CTR is **0.51%**. The two principal Bunda YouTube traffic rows and Pressure generated **94.32% of all link clicks** from **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**.

The distinction matters for **resource efficiency**. Meta supports defensible paid-media efficiency measures such as CPC, CPM and cost per platform result. It does **not** support a total campaign ROI because the complete production/offline cost base and a common downstream value measure are missing. The strongest conclusion is therefore that Bunda was substantially more resource-intensive than the earlier work and that parts of its paid-social distribution achieved unusually efficient traffic response; the total economic return on the wider campaign cannot be reconstructed from the surviving evidence.

## Repository guide

- **[Full exploratory report](reports/exploratory_findings.md)**: resource model, chronology, historical hypothesis, Meta analysis, drivers/barriers and implications.
- **[Methodology](METHODOLOGY.md)**: conceptual basis, evidence types, verification procedures, formulas and analytical rules.
- **[Sanitised campaign data](data/meta_campaign_export_sanitized.csv)**: public campaign-level derivative of the historical Meta export.
- **[Reproducible analysis](analysis/retrospective_analysis.py)**: Python used to reproduce the quantitative analysis.
- **[Machine-readable summary](analysis/summary.json)**: verified KPI outputs.
- **[Provenance](PROVENANCE.md)**: source/evidence chain and file hashes.

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

The underlying historical advertising, music-release activity and source data relate to work I personally carried out. **ChatGPT did not participate in the original campaigns.**

I reviewed the historical source material and analytical interpretation. ChatGPT was used subsequently to re-run/cross-check calculations, assist with reproducible Python code, discover and structure relevant literature, and draft substantial portions of the repository prose. The numerical Meta claims have been checked against the source data; author-reported production/chronology context is labelled separately from workbook evidence; AI-generated prose is not treated as independent evidence.

I retain responsibility for the final interpretation and for distinguishing source-recorded metrics, derived calculations, author-reported historical context and external research.