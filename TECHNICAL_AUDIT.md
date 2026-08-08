# Technical assessment of the analysis pipeline

## Scope

This is a small portfolio analysis pipeline, not a production advertising platform. I am applying data preparation, validation, programming, testing and visualisation practices that are already part of my software-engineering, IT and postgraduate data training. The newer learning in this project is the **paid-social and creative-performance domain**: how Meta advertising metrics are interpreted, how creative-performance questions are framed, and what stronger attribution or test designs would be needed.

The assessment below therefore asks whether the computational work is sufficiently transparent, repeatable and proportionate to the historical dataset. It does not treat additional engineering complexity as an objective in itself.

## Assessment approach

I used established computational-research and software guidance as the benchmark rather than inventing a checklist after writing the code. Wilson et al. (2014) recommend readable programs, modularisation, automated workflows, version control and tests. Sandve et al. (2013) emphasise executable workflows rather than manual data manipulation and recording the information required to rerun an analysis. Wilkinson et al. (2016) extend the provenance requirement through the FAIR principles, including rich metadata and provenance even where access to the underlying data is restricted. Trisovic et al. (2022) provide empirical evidence that missing dependencies, hard-coded paths, missing files, incomplete code and inadequate environment capture are recurring barriers when published research code is re-executed.

For the structure of the public campaign table, Wickham's (2014) tidy-data formulation provides a useful vocabulary: variables as columns and observations as rows. I use that idea only to describe the tabular structure; this source export was already broadly rectangular and did not require substantial reshaping. For data cleaning, Van den Broeck et al. (2005) are useful mainly because they distinguish screening and diagnosis from automatic editing, and distinguish genuine extreme observations from errors. That is relevant to preserving Bunda and Pressure rather than deleting them because they are unusual.

For visualisation I use Munzner's (2009) nested model as a design check: start with the domain question and data, then choose the abstraction and visual encoding. This supports using a distribution view for CPC dispersion, a scatter plot for the spend-response relationship, common-baseline bars for ranking and direct scenario bars for sensitivity analysis.

## Findings

| Area | Assessment | Evidence in this repository | Remaining limitation |
|---|---|---|---|
| **Source-to-output reproducibility** | Strong for this portfolio scale | `python -m scripts.run_pipeline` recreates the public CSV, validation, analysis tables, JSON summaries and charts from the verified workbook when the private source is available. | Public CI cannot rerun the private Excel-to-CSV stage because the workbook contains a historical phone number and is intentionally not committed. |
| **Data preparation** | Appropriate and deliberately narrow | Source hash check, label-based header discovery, duplicate-field comparison, verification before dropping empty/uninformative fields, phone redaction, preservation of every source row and explicit quality flags. | It is not comprehensive data cleaning and is not presented as such. The source is a historical platform export, so unavailable metadata cannot be reconstructed. |
| **Data validation** | Strong internal consistency checks | Schema, sequential row IDs, privacy scan, numeric/range checks, reach/impression relationship, flag consistency, cost-per-result reconciliation and a semantic fingerprint linking the public structured records to the verified private-source preparation. All 122 recognised rows reproduce Meta's exported cost per result within `1e-6`. | Internal consistency cannot independently validate Meta's historical measurement or attribution system. |
| **Code organisation** | Good for a small analysis | Preparation, validation, analysis, visualisation, provenance and orchestration are separate modules; repeated dataset calculations are centralised in `campaign_data.py`. | The custom XLSX reader is intentionally narrow and should not be treated as a general spreadsheet parser. A maintained spreadsheet library would be preferable if the source format became more varied. |
| **Testing** | Good portfolio-level coverage | Unit tests cover XLSX coordinates and redaction; dataset tests cover quality flags, headline KPIs, concentration and sensitivity claims; integration tests rerun the public pipeline; manifest completeness, canonical text products and repeated-run hashes are checked; with the private source present, the preparation output and committed public records must have the same semantic fingerprint. | Tests are focused on the known export and published claims rather than exhaustive property-based testing. |
| **Code readability/consistency** | Strengthened | Modular functions, type annotations, descriptive names and Ruff error/style lint checks in CI. | Passing automated style checks is not evidence that the analytical logic is correct; logic is checked separately through tests and source reconciliation. |
| **Dependency capture** | Good, not fully hermetic | Matplotlib and Ruff versions are pinned, CI declares Python 3.14, and the run manifest records Python/Matplotlib versions and hashes of code/products. | The complete execution environment is not containerised or locked to a Python patch version and OS image, so this is reproducible rather than bit-for-bit environment preservation. |
| **Provenance** | Strong | Original source SHA-256, public-derivative hash, preparation summary, semantic source-equivalence fingerprint and complete run manifest link source, public evidence, code and outputs. The screenshot is structurally checked before it is hashed. | The restricted source cannot be independently downloaded from the public repository. |
| **Visualisation** | Appropriate to the analytical questions | CPC distribution uses logarithmic spacing because values are highly skewed; spend/click scatter is log-log; ranking uses horizontal bars; sensitivity figures compare the same KPI under explicit exclusions. | The figures are descriptive. They do not supply missing causal variables or downstream commercial outcomes. |
| **Deterministic public outputs** | Strong within the declared environment | SVG metadata is stabilised; JSON/SVG files use canonical LF endings; two consecutive builds must produce identical product hashes; the manifest fails on missing products; CI fails if committed outputs drift. The earlier Windows/Linux difference was traced to line endings and corrected. | Matplotlib/runtime or font changes outside the pinned dependency and declared Python line could still affect future render details if the environment changes. |

## Changes made after the assessment

The first version of the repository could reproduce the analysis from the public CSV, but the Excel-to-CSV transformation was only documented. I corrected that gap by adding a dedicated source-preparation stage and one orchestration command for the complete workflow.

I also separated shared calculations into `campaign_data.py` so the analysis and chart stages do not maintain competing implementations of the same KPI logic. An earlier duplicate row-level KPI helper in `analyse_campaigns.py` was removed during this audit. This is a small example of Wilson et al.'s (2014) recommendation to avoid duplication and keep one authoritative implementation of repeated logic.

A second issue emerged when source-to-public equivalence was tested more strictly. Nine legacy public campaign names had converted embedded line breaks into spaces. Their performance values were unchanged, but the records were not textually equivalent to the verified preparation. I regenerated the public CSV from the verified source-derived records and added a semantic fingerprint check that compares structured values rather than fragile byte-level CSV formatting. The current public fingerprint matches the verified private-source fingerprint.

The public CI now compiles the modules, runs tests, lints code with Ruff, rebuilds all public products and fails if regenerated outputs differ from the committed files. The evidence manifest also rejects a truncated or structurally corrupt PNG rather than accepting its filename and hash as proof that it is readable. GitHub's current Python Actions guidance recommends `setup-python` for consistent runner behaviour and provides Ruff as an example lint/format step.

## Overall judgement

For a portfolio-scale retrospective analysis, the pipeline is now **end-to-end reproducible from the restricted source in a local authorised environment and reproducible from the sanitised public dataset in GitHub Actions**. The strongest features are preservation of source rows, explicit handling of uncertainty, internal arithmetic validation, source/public semantic equivalence, separation of unlike result types, automated regeneration and provenance hashes.

The most important technical limitation is intentional: the project uses a small custom XLSX reader tailored to one known historical export rather than a general spreadsheet-ingestion layer. That keeps the dependency surface small but makes the source reader unsuitable for arbitrary workbooks. If this became a recurring production workflow, I would replace that component with a maintained spreadsheet ingestion library, define a versioned input schema and strengthen environment locking and test coverage.

The computational reproducibility of the workflow should also be distinguished from the validity of the marketing interpretation. Re-running code can demonstrate that the same transformations and calculations produce the same outputs; it cannot recover deleted creative variables, establish causality or independently validate the platform's historical attribution. That distinction is important in this retrospective.

## References

- Wilson, G. et al. (2014). *Best Practices for Scientific Computing*. **PLOS Biology**, 12(1), e1001745. https://doi.org/10.1371/journal.pbio.1001745
- Sandve, G.K. et al. (2013). *Ten Simple Rules for Reproducible Computational Research*. **PLOS Computational Biology**, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
- Wilkinson, M.D. et al. (2016). *The FAIR Guiding Principles for scientific data management and stewardship*. **Scientific Data**, 3, 160018. https://doi.org/10.1038/sdata.2016.18
- Trisovic, A. et al. (2022). *A large-scale study on research code quality and execution*. **Scientific Data**, 9, 60. https://doi.org/10.1038/s41597-022-01143-6
- Wickham, H. (2014). *Tidy Data*. **Journal of Statistical Software**, 59(10), 1–23. https://doi.org/10.18637/jss.v059.i10
- Van den Broeck, J. et al. (2005). *Data Cleaning: Detecting, Diagnosing, and Editing Data Abnormalities*. **PLOS Medicine**, 2(10), e267. https://doi.org/10.1371/journal.pmed.0020267
- Munzner, T. (2009). *A Nested Model for Visualization Design and Validation*. **IEEE Transactions on Visualization and Computer Graphics**, 15(6), 921–928. https://doi.org/10.1109/TVCG.2009.111
- GitHub Docs (current). *Building and testing Python*. https://docs.github.com/en/actions/tutorials/build-and-test-code/python
