# Kashe Music Group / Santeri: Retrospective Creative Campaign Analysis

> **Verification status:** The historical campaigns and source data relate to work I personally carried out. I reviewed the source workbook and the analysis. The quantitative workflow now reproduces the public dataset, validation checks, KPI tables and visualisations from the verified workbook in one pipeline. ChatGPT assisted with code development, literature discovery and substantial drafting of the explanatory text. I retain responsibility for the published interpretation.

This repository revisits surviving evidence from my work at **Kashe Music Group / Santeri**. It has two connected purposes: to analyse the historical campaigns using the stronger analytical discipline I developed later, and to provide a transparent evidence trail for paid-media and creative-campaign statements in my CV and cover letter.

The only surviving public artist account is the [Santeri Facebook page](https://www.facebook.com/therealsanteri).

## Executive summary

The campaign cannot be understood from Meta metrics alone. Creative production consumes and coordinates several forms of resource before an advertisement is delivered. Throsby (2006) distinguishes inputs such as labour, operating capital and human capital in artistic production, while Gander (2015) shows how music production depends on temporarily assembled specialist teams, material resources, knowledge and organisational coordination ([Throsby, 2006](https://doi.org/10.1007/s10824-005-9001-4); [Gander, 2015](https://doi.org/10.1108/MD-03-2014-0165)). I use those concepts to organise this case into **creative/intellectual assets, specialist human capital, technical/operating capital, financial capital, organisational capability, network resources, media channels and information resources**.

Chronology matters. Before *Let's Fly Away*, I was in a **manager-led artist-development phase**. Four opening-act appearances involving Portable occurred then, two at shows he organised and two at third-party shows where he was also booked. I was not directing creative operations for those events. They are baseline evidence of an existing artist trajectory and network access, not outcomes of the later social-media strategy.

*Let's Fly Away* marked my transition to broad creative ownership. *Bunda* represented a further increase in **production intensity and resource commitment**. The music video cost more than **NGN 5 million** according to my historical records/recollection and involved more than **30 people**, including specialist roles such as producer, director and costume/styling alongside scripted creative development. I treat those facts as evidence of production inputs and specialisation rather than as an objective measure of artistic quality.

The surviving Meta workbook documents **126 campaign rows**, **NGN 1,029,228.11 spend** and **10,332,896 impressions**. A separate account screenshot records **NGN 1,492,844.45 spent**, so the workbook is a partial historical export rather than a complete lifetime account record.

Across the **106 link-click rows**, the file records **635,240 link clicks** from **9,725,211 impressions** and **NGN 907,409.25 spend**, producing a portfolio-weighted **NGN 1.43 CPC**, **6.53% derived CTR** and **NGN 93.30 CPM**. Those pooled values hide a highly concentrated distribution: median campaign CPC is **NGN 19.81** and median derived CTR is **0.51%**. The two principal Bunda YouTube traffic rows and Pressure generated **94.32% of all link clicks** from **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**.

Eighteen rows whose surviving campaign names explicitly contain `Bunda` provide a conservative lower bound for clearly identifiable Bunda Meta activity. They record **NGN 450,035.75 spend** and **3,085,893 impressions**. Fifteen are link-click rows with **568,819 clicks** and three are ThruPlay rows with **29,344 ThruPlays**. Because generic or truncated names may also relate to Bunda, this is a lower-bound subset rather than a complete Bunda advertising total.

At the time, I believed that the culmination of stronger content, paid distribution, organic engagement and offline promotion was creating visible **market traction**, and that this helped during outreach and negotiation for television, radio and live opportunities. Some opportunities were actively negotiated and others arrived inbound. I now treat that belief as an **untested managerial hypothesis**, not an established causal result. Pre-existing relationships, production value, song characteristics, paid reach, organic word of mouth, offline promotion, timing, algorithms and gatekeeper preferences are all plausible drivers that I did not isolate.

The reproducible workflow does not change that evidential boundary. It makes the **data handling and descriptive calculations auditable**: the original workbook can be transformed into the sanitised public CSV, validated, analysed and visualised with one command, while the original private workbook remains uncommitted because it contains a historical phone number.

## Reproducible workflow

The first version of this repository reproduced the analysis from the public CSV, while the earlier Excel-to-CSV preparation was documented rather than coded. That gap is now closed.

The pipeline is separated into explicit stages:

1. `scripts/xlsx_reader.py` — reads the known historical XLSX export.
2. `scripts/prepare_data.py` — performs **targeted data preparation**: verifies the workbook hash, locates the header, checks duplicated fields, verifies fields before dropping them, converts relevant values, redacts the historical WhatsApp number and flags four rows whose result fields are blank.
3. `scripts/validate_data.py` — checks schema, numeric constraints, privacy redaction and cost-per-result arithmetic.
4. `scripts/analyse_campaigns.py` — calculates the published KPIs, distributions, concentration/sensitivity analysis and the conservative Bunda-name subset.
5. `scripts/visualise_results.py` — generates five deterministic SVG figures from the prepared data.
6. `scripts/build_manifest.py` — records code/product hashes and runtime versions.
7. `scripts/run_pipeline.py` — runs the complete workflow in order.

This is **not presented as comprehensive data cleaning**. The source export was already broadly tabular. The preparation stage is deliberately conservative: preserve the historical records, verify what can be verified, flag uncertainty instead of guessing, and make the transformations reproducible.

See **[PIPELINE.md](PIPELINE.md)** for the run instructions and **[TECHNICAL_AUDIT.md](TECHNICAL_AUDIT.md)** for the code/product assessment.

## Repository guide

- **[Full exploratory report](reports/exploratory_findings.md)** — resource model, chronology, historical hypothesis, Meta analysis and implications.
- **[Methodology](METHODOLOGY.md)** — conceptual basis, evidence types, data preparation/validation and analytical rules.
- **[Pipeline](PIPELINE.md)** — end-to-end reproducibility and commands.
- **[Technical audit](TECHNICAL_AUDIT.md)** — assessment of the scripts and outputs against reproducible-computing and visualisation literature.
- **[Sanitised campaign data](data/meta_campaign_export_sanitized.csv)** — generated public derivative of the restricted workbook.
- **[Analysis summary](analysis/summary.json)** — machine-readable KPI outputs.
- **[Validation report](analysis/validation_report.json)** — automated data checks.
- **[Provenance](PROVENANCE.md)** — evidence chain, source handling and contextual evidence boundaries.

![Distribution of campaign cost per link click](assets/01_link_click_cost_distribution.svg)

![Spend versus link clicks](assets/02_spend_vs_link_clicks.svg)

![Top campaigns by link clicks](assets/03_top_link_click_campaigns.svg)

![CPC sensitivity analysis](assets/04_cpc_sensitivity.svg)

![CTR sensitivity analysis](assets/05_ctr_sensitivity.svg)

## Run the pipeline

With the verified private workbook placed at `data/private/30-01-23.xlsx`:

```bash
python -m scripts.run_pipeline
```

To rebuild the public products without the private workbook:

```bash
python -m scripts.run_pipeline --from-public-csv
```

Tests:

```bash
python -m unittest discover -s tests -v
```

## AI assistance and author responsibility

The underlying historical advertising, music-release activity and source data relate to work I personally carried out. **ChatGPT did not participate in the original campaigns.**

I reviewed the historical source material, the data preparation decisions, the calculations and the analytical interpretation. ChatGPT was used subsequently to assist with reproducible Python code, re-run/cross-check calculations, identify relevant literature and draft substantial portions of the repository prose. The numerical Meta claims have been checked against the source data; author-reported production and chronology context is labelled separately from workbook evidence; AI-generated prose is not treated as independent evidence.

I retain responsibility for the final interpretation and for distinguishing source-recorded metrics, derived calculations, author-reported historical context and external research.
