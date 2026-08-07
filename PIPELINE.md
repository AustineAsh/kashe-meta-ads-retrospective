# Reproducible analysis pipeline

This repository separates the computational work into explicit stages so that the published metrics and charts can be regenerated rather than recreated manually.

The historical workbook itself is restricted because one campaign name contains a phone number. The source filename and SHA-256 remain documented, while the public repository contains the redacted derivative and all downstream code. This preserves provenance without publishing the private value.

## Stages

1. **Source extraction — `scripts/xlsx_reader.py`**  
   A deliberately narrow reader extracts visible cell values from the fixed historical `.xlsx` export. It uses Python's ZIP/XML support because this project needs only one known worksheet; it is not presented as a general spreadsheet library.

2. **Targeted preparation — `scripts/prepare_data.py`**  
   This is not described as comprehensive data cleaning. The script verifies the source hash, locates the header from labels, checks that the duplicated campaign-name fields agree, verifies that the ranking fields contain no usable values, keeps every source campaign row, converts analysis fields into consistent values, redacts the historical WhatsApp number, and flags the four rows whose result type/results/cost-per-result fields are blank. It does not impute missing values, infer deleted creative characteristics or remove genuine extreme campaigns.

3. **Validation — `scripts/validate_data.py`**  
   The public CSV is checked for expected columns, row identifiers, privacy leakage, non-negative numeric values, reach/impression consistency, result-type flags and the arithmetic relationship between spend, results and exported cost per result. All 122 rows with recognised result types reconcile within `1e-6`. A semantic fingerprint also checks that the prepared public records match the verified private-source preparation independently of harmless CSV newline or numeric-format differences.

4. **Analysis — `scripts/analyse_campaigns.py`**  
   Result types are kept separate. The script calculates the published Meta KPIs, campaign-level distribution statistics, concentration and sensitivity analyses, the exact two-row Bunda traffic case, and a conservative lower-bound subset based only on surviving names that explicitly contain `Bunda`.

5. **Visualisation — `scripts/visualise_results.py`**  
   Five SVG charts are regenerated directly from the prepared CSV and analysis summary. The visualisations focus on the analytical questions in the report: CPC distribution, the spend/response relationship, concentration in top campaigns, and sensitivity of pooled CPC/CTR to Bunda and Pressure.

6. **Provenance manifest — `scripts/build_manifest.py`**  
   The manifest records the verified source hash, Python/Matplotlib versions and SHA-256 hashes of code and derived products.

7. **Orchestration — `scripts/run_pipeline.py`**  
   One command runs the stages in order. Locally, with the restricted workbook present, it regenerates everything from source. Public CI uses `--from-public-csv`, because the private workbook is intentionally not committed.

## Run locally from the verified workbook

Place the source at `data/private/30-01-23.xlsx`, then run:

```bash
python -m scripts.run_pipeline
```

## Rebuild the public products only

```bash
python -m scripts.run_pipeline --from-public-csv
```

## Tests

```bash
python -m unittest discover -s tests -v
```

Code-quality checks used in CI:

```bash
ruff check scripts tests
```

The tests include an end-to-end source-equivalence check. When the restricted workbook is present, `prepare_data.py` must produce the same structured campaign records as the committed public CSV. The comparison uses a semantic fingerprint rather than requiring byte-for-byte equality, so harmless differences in CSV line endings or numeric text formatting do not count as data differences. GitHub Actions also runs the tests and regenerates downstream products on every push or pull request.

## Why the pipeline is structured this way

The structure follows established reproducible-computing principles rather than treating the scripts as production software. The underlying preparation, validation, programming and visualisation practices are not new concepts for me; the newer learning in this project is the paid-social creative-performance domain and its Meta-specific measurement terminology. Wilson et al. (2014) recommend readable modular code, automated workflows, version control, tests and recording versions/provenance; Sandve et al. (2013) specifically recommend replacing manual data manipulation with executable transformations and retaining intermediate results. Wilkinson et al. (2016) additionally emphasise rich provenance and the continued accessibility of metadata even where source data cannot be made public. Trisovic et al. (2022) show empirically that missing dependencies, hard-coded paths and incomplete documentation are recurring barriers to re-executing published research code.

The visualisation layer follows Munzner's (2009) distinction between the domain question, data/operation abstraction and visual encoding: the charts were chosen only after defining what the analysis needed to compare. A highly skewed positive CPC distribution is shown on a logarithmic scale; ranking uses bars on a common baseline; and the spend/click scatter uses log scales because both variables span several orders of magnitude.

## References

- Wilson, G. et al. (2014). *Best Practices for Scientific Computing*. PLOS Biology, 12(1), e1001745. https://doi.org/10.1371/journal.pbio.1001745
- Sandve, G.K. et al. (2013). *Ten Simple Rules for Reproducible Computational Research*. PLOS Computational Biology, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
- Wilkinson, M.D. et al. (2016). *The FAIR Guiding Principles for scientific data management and stewardship*. Scientific Data, 3, 160018. https://doi.org/10.1038/sdata.2016.18
- Trisovic, A. et al. (2022). *A large-scale study on research code quality and execution*. Scientific Data, 9, 60. https://doi.org/10.1038/s41597-022-01143-6
- Munzner, T. (2009). *A Nested Model for Visualization Design and Validation*. IEEE Transactions on Visualization and Computer Graphics, 15(6), 921–928. https://doi.org/10.1109/TVCG.2009.111
- Wickham, H. (2014). *Tidy Data*. Journal of Statistical Software, 59(10), 1–23. https://doi.org/10.18637/jss.v059.i10
- Van den Broeck, J. et al. (2005). *Data Cleaning: Detecting, Diagnosing, and Editing Data Abnormalities*. PLOS Medicine, 2(10), e267. https://doi.org/10.1371/journal.pmed.0020267