# Methodology

## 1. Analytical purpose

This repository is a **retrospective exploratory analysis** of a historical music-release and promotion programme for Kashe Music Group / Santeri. The Meta Ads workbook is the principal quantitative dataset, but paid social is treated as one observable part of a wider creative campaign.

The analysis asks what resources were committed, how media was deployed, what paid-social outcomes can be reconstructed, where performance was concentrated, and what additional data would be required to test the historical assumptions I made about market traction, gatekeeper interest and downstream opportunities.

The repository also serves an evidential purpose by providing a transparent source trail for statements in my CV and cover letter concerning creative campaign management, paid media, audience development and performance-informed decision-making.

## 2. Creative production as a resource system

Throsby (2006) distinguishes artistic-production inputs including labour, operating capital and human capital. Gander (2015) provides a music-specific organisational perspective in which production brings together specialist people, material resources, knowledge and temporary project relationships under uncertainty ([Throsby, 2006](https://doi.org/10.1007/s10824-005-9001-4); [Gander, 2015](https://doi.org/10.1108/MD-03-2014-0165)).

Drawing on those concepts and the historical case, I use eight resource domains: **creative/intellectual assets; human capital and specialist labour; physical/technical/operating capital; financial capital; organisational/managerial capability; network/relational resources; media/channel resources; and information/analytical resources**. This is my resource map for this case rather than a taxonomy reproduced from either study.

The report distinguishes **production intensity** from **creative quality**. Expenditure, team size and specialist roles are evidence that more financial, human and operating resources entered a project. They do not independently prove that the resulting creative was artistically superior.

## 3. Media deployment and chronology

Lovett and Staelin (2016) distinguish paid, earned and owned media in an entertainment setting ([Lovett & Staelin, 2016](https://doi.org/10.1287/mksc.2015.0961)). I use those categories for the digital campaign and retain **offline/intermediated promotion** separately because radio, television, DJs/clubs and live activity may be paid, earned or relationship-mediated depending on the activity.

Chronology is used as a control against retrospective over-attribution. The four Portable opening appearances occurred in the earlier manager-led artist phase, before *Let's Fly Away* and before I took broad creative-operations ownership. *Let's Fly Away* marks the transition to broad creative ownership; Bunda represents a later increase in production and promotional resources.

## 4. Historical managerial hypothesis

During the later period, I worked with an informal assumption that the combined campaign was creating visible market traction and that this visibility helped when approaching or negotiating with radio, television and event decision-makers. Some opportunities were negotiated outbound and others arrived inbound.

I did not test that assumption at the time. It is therefore represented as a hypothesis:

`resource configuration → campaign execution → exposure/engagement → visible traction → perceived market signal → gatekeeper interest/negotiation leverage → media/live opportunities`

The surviving evidence does not observe or control every link. Candidate drivers include creative/production inputs, song characteristics, paid distribution, organic response, pre-existing networks, direct outreach, offline promotion, algorithms and timing. Candidate barriers include saturation, weak audience fit, opaque platform mechanisms, gatekeeper criteria unrelated to social engagement, incomplete attribution and failure of online response to convert into durable fandom or commercial value.

## 5. Quantitative source and evidence types

The principal quantitative source is the `Raw Data Report` sheet of `30-01-23.xlsx`. A separate Meta screenshot records **NGN 1,492,844.45** spent at account level and is used to contextualise workbook coverage.

The project distinguishes four evidence types:

1. **workbook-recorded evidence** — values directly exported from Meta;
2. **derived measures** — calculations such as CTR, CPM, medians and concentration shares;
3. **author-reported historical context** — production cost, team size, chronology and broader promotional activity not contained in the workbook; and
4. **external research/sector evidence** — used to define concepts or establish contextual plausibility, not to overwrite the historical source data.

## 6. Targeted data preparation, not comprehensive cleaning

The source export was already broadly rectangular, so the task did not require comprehensive cleaning or substantial reshaping. The preparation stage is deliberately conservative: preserve the historical records, verify what can be verified, sanitise the one privacy-sensitive value and make the transformation reproducible.

`scripts/prepare_data.py` begins from the original workbook rather than from a manually prepared CSV. It verifies the expected SHA-256, finds the header from the source labels and checks the duplicated campaign-name columns before removing redundancy. It verifies that the quality, engagement-rate and conversion-rate ranking fields contain no usable values and that `Results (initial)` is blank before leaving those fields out of the public table.

All **126 campaign rows are preserved**. Repeated campaign names are not treated as duplicates because stable campaign/ad IDs are absent and a repeated name could represent a copy, separate run or related activity. Each row receives `campaign_row_id` and retains its original Excel row number for traceability.

One campaign name contains a historical WhatsApp phone number. The public transformation performs **redaction**, removing only the phone digits while preserving the campaign's analytical values.

Four source rows have **blank result type, blank Results and blank Cost per result fields**. They are not repaired or imputed. They are preserved with `data_quality_flag = missing_result_type` and excluded only from analyses that require a known result type. An earlier manual inspection had described these records as result type `2`; the end-to-end XLSX reader corrected that interpretation by resolving the workbook's shared strings properly.

The numerical preparation is limited to consistent data types/serialisation. Genuine extreme campaigns such as Bunda and Pressure are retained. They are later investigated through distributions and sensitivity analysis rather than removed as errors.

Van den Broeck et al. (2005) are useful here because they distinguish data screening/diagnosis from automatic editing and emphasise the difference between a genuine extreme observation and a faulty value ([Van den Broeck et al., 2005](https://doi.org/10.1371/journal.pmed.0020267)). Wickham's (2014) tidy-data terminology is relevant only at the structural level: variables are represented as columns and campaign observations as rows; the original export did not require major tidying ([Wickham, 2014](https://doi.org/10.18637/jss.v059.i10)).

## 7. Automated validation

`scripts/validate_data.py` checks the prepared public table before analysis. The checks cover:

- expected schema and sequential row identifiers;
- uniqueness of source Excel row references;
- absence of a WhatsApp phone number in published campaign names;
- numeric conversion and non-negative values;
- non-positive impressions/results where they should not occur;
- reach greater than impressions as a review condition;
- consistency between known/blank result types and the quality flag; and
- independent recalculation of Meta's exported `cost per result` as `amount spent / results`.

All **122 rows with recognised result types** reproduce the exported cost-per-result value within `1e-6`; the maximum absolute floating-point difference is approximately `4.95e-09`. This is an **internal consistency check**, not independent validation of Meta's historical measurement/attribution system.

## 8. Derived measures and analytical procedures

Result types are analysed separately. A Facebook like, link click, ThruPlay, messaging conversation and lead represent different objectives and are not pooled into a single result total.

Where the components exist, the analysis derives:

- **weighted CPC** = total link-campaign spend / total link clicks;
- **derived link CTR** = link clicks / impressions × 100;
- **CPM** = spend / impressions × 1,000;
- **row-level impressions/reach ratio** = impressions / reach; and
- **result/impression rate** = results / impressions × 100.

For link-click rows I report both portfolio-weighted KPIs and campaign-level medians. Their divergence led to a **concentration analysis** and then a **sensitivity analysis** excluding the two principal Bunda YouTube traffic rows and then Pressure. CPC is interpreted alongside CTR and CPM so that response efficiency is not confused with cheap media delivery.

The broader Bunda reconstruction uses only recognised rows whose surviving campaign name explicitly contains `Bunda`. It is labelled a **lower bound** because generic/truncated names may omit other Bunda-related activity.

## 9. Visualisation design

The visualisations are selected after defining the analytical question rather than because a particular chart type is available. Munzner's (2009) nested model distinguishes the domain problem, data/task abstraction, visual encoding and algorithmic implementation; mistakes at an upstream level cannot be repaired merely by a technically correct chart ([Munzner, 2009](https://doi.org/10.1109/TVCG.2009.111)).

The pipeline therefore generates:

- a logarithmically spaced CPC distribution because CPC spans several orders of magnitude;
- a log-log spend-versus-link-click scatter to examine the relationship over a highly skewed range;
- a horizontal common-baseline bar chart for the top link-click rows; and
- direct CPC and CTR scenario bars for the sensitivity analysis.

The figures are descriptive. They do not supply missing creative variables or causal identification.

## 10. Reproducibility and provenance

The computational workflow is split into preparation, validation, analysis, visualisation and provenance stages and is orchestrated by `scripts/run_pipeline.py`. `analysis/run_manifest.json` records runtime versions and hashes of code/configuration and generated products.

Wilson et al. (2014) recommend readable modular code, automation, version control and testing in scientific computing; Sandve et al. (2013) similarly emphasise executable transformations and retaining what is needed to reproduce a result. Wilkinson et al. (2016) extend that logic to rich provenance and reusable metadata even where source data cannot be openly shared. Trisovic et al. (2022), examining more than 2,000 replication packages, identify missing dependencies, hard-coded paths and insufficient documentation as recurring barriers to re-execution ([Wilson et al., 2014](https://doi.org/10.1371/journal.pbio.1001745); [Sandve et al., 2013](https://doi.org/10.1371/journal.pcbi.1003285); [Wilkinson et al., 2016](https://doi.org/10.1038/sdata.2016.18); [Trisovic et al., 2022](https://doi.org/10.1038/s41597-022-01143-6)).

The public GitHub Actions workflow compiles and lints the code, runs the tests, rebuilds public products from the sanitised CSV and fails if committed outputs drift. The private workbook is deliberately excluded, so the Excel-to-CSV stage can only be rerun in an authorised local environment with the verified source present.

## 11. Interpretation boundary

Reproducibility makes the transformation and calculations inspectable; it does not make the historical data explanatory. Deleted creative assets, audience/placement variables, campaign-specific dates, controlled test assignments and consistent downstream commercial outcomes are missing. The analysis can therefore establish where response concentrated and how paid-media efficiency differed, but not which creative element or marketing channel caused the wider career outcomes.

Likewise, Meta CPC or CTR cannot be used as a return measure for the more than NGN 5 million author-reported Bunda video investment. A total resource-productivity or ROI analysis would require a fuller cost ledger linked to revenue, profit, attributable bookings or another defined strategic outcome.

## 12. Reproduction

Full local pipeline with the verified workbook:

```bash
python -m scripts.run_pipeline
```

Public rebuild from the sanitised CSV:

```bash
python -m scripts.run_pipeline --from-public-csv
```

Tests:

```bash
python -m unittest discover -s tests -v
```

See [PIPELINE.md](PIPELINE.md) for the stage-by-stage workflow and [TECHNICAL_AUDIT.md](TECHNICAL_AUDIT.md) for the script/product assessment.

## References

Gander, J.M. (2015) 'Situating creative production: recording studios and the making of a pop song', *Management Decision*, 53(4), pp. 843–856. https://doi.org/10.1108/MD-03-2014-0165

Lovett, M.J. and Staelin, R. (2016) 'The role of paid, earned, and owned media in building entertainment brands: reminding, informing, and enhancing enjoyment', *Marketing Science*, 35(1), pp. 142–157. https://doi.org/10.1287/mksc.2015.0961

Throsby, D. (2006) 'An artistic production function: theory and an application to Australian visual artists', *Journal of Cultural Economics*, 30, pp. 1–14. https://doi.org/10.1007/s10824-005-9001-4

Van den Broeck, J. et al. (2005) 'Data Cleaning: Detecting, Diagnosing, and Editing Data Abnormalities', *PLOS Medicine*, 2(10), e267. https://doi.org/10.1371/journal.pmed.0020267

Wickham, H. (2014) 'Tidy Data', *Journal of Statistical Software*, 59(10), pp. 1–23. https://doi.org/10.18637/jss.v059.i10

Wilson, G. et al. (2014) 'Best Practices for Scientific Computing', *PLOS Biology*, 12(1), e1001745. https://doi.org/10.1371/journal.pbio.1001745

Sandve, G.K. et al. (2013) 'Ten Simple Rules for Reproducible Computational Research', *PLOS Computational Biology*, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285

Wilkinson, M.D. et al. (2016) 'The FAIR Guiding Principles for scientific data management and stewardship', *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18

Trisovic, A. et al. (2022) 'A large-scale study on research code quality and execution', *Scientific Data*, 9, 60. https://doi.org/10.1038/s41597-022-01143-6

Munzner, T. (2009) 'A Nested Model for Visualization Design and Validation', *IEEE Transactions on Visualization and Computer Graphics*, 15(6), pp. 921–928. https://doi.org/10.1109/TVCG.2009.111
