# Methodology

## 1. Analytical purpose

This is a **retrospective exploratory analysis** of a historical Meta Ads export. I use the surviving data to answer four related questions:

1. What paid-media activity and scale can be reconstructed from the source records?
2. How did recorded performance vary within genuinely comparable result types?
3. Which campaigns materially shaped the account-level aggregates?
4. What additional information would be required to move from descriptive diagnosis to stronger creative-effect or commercial conclusions?

The analysis also serves an evidential purpose: it provides a transparent source trail for statements in my CV and cover letter about having run paid advertising and used campaign-performance information in creative and promotional decision-making.

## 2. Conceptual basis: measure the decision, not simply the available number

The methodology starts from the idea that advertising metrics have meaning in relation to an objective. Li, Larimo and Leonidou (2021) conceptualise social-media marketing strategy around drivers, inputs, throughputs and outputs, and show that firms use social media for different strategic objectives. Their social-monitoring perspective is particularly relevant because it treats customer behaviour data as an information resource that organisations can acquire, interpret and respond to. The authors also identify the selection of appropriate performance metrics as an important research problem ([Li et al., 2021](https://doi.org/10.1007/s11747-020-00733-3)).

Yousef, Dietrich and Rundle-Thiele (2021) make the measurement progression more explicit in a Facebook advertising experiment. They distinguish exposure/connection from interaction and then measure an action beyond Facebook through website form submissions. Importantly, their comparison of creative appeals used controlled A/B testing rather than inferring creative effects from unrelated campaign results ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

I synthesise those ideas into five measurement layers for this retrospective. This is my analytical structure, not a model reproduced verbatim from either source:

| Layer | Primary question | Measures relevant to the present data |
|---|---|---|
| **Delivery** | At what scale and cost was advertising served? | Spend, impressions, reach, CPM, impressions/reach |
| **Attention** | Did the creative retain enough attention to progress? | 3-second video plays, ThruPlay and other retention measures where available |
| **Traffic response** | Did exposure produce the intended click response and at what cost? | Link clicks, derived CTR, CPC |
| **Downstream action** | What occurred after or beyond the initial response? | Messaging conversations, leads; landing-page and purchase outcomes if available |
| **Commercial value** | Did those actions create sufficient economic value? | Revenue, AOV, CPA/CAC, ROAS and profit-related measures if available |

This structure determines how the result types are interpreted. It also avoids treating unlike outcomes as though they were measurements of the same thing.

Current practice sources support the same objective-led orientation. Nielsen (2025) argues that abundant marketing metrics do not automatically produce clarity and that KPIs become useful when they are aligned with business priorities and interpreted in context. IAB UK's 2026 Measurement Hub similarly presents different measurement strategies according to the objective and places outcomes measurement, standards and consistency within its current industry agenda ([Nielsen, 2025](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/); [IAB UK, 2026](https://www.iabuk.com/measurement)). I use these sources as sector context, while the analytical claims about this case come from the historical dataset itself.

## 3. Data sources and unit of analysis

The principal source is the `raw-data` sheet in the historical workbook `30-01-23.xlsx`. A separate Meta account screenshot records an account-level spent amount of **NGN 1,492,844.45** and is used only to contextualise the coverage of the campaign export.

The public repository does not contain the unmodified workbook because one historical campaign name includes a WhatsApp phone number. Instead, `data/meta_campaign_export_sanitized.csv` preserves the campaign-level performance fields while redacting that number. The original file hashes and evidence chain are documented in `PROVENANCE.md`.

The unit of analysis is a **source campaign row**. The workbook contains **126 rows but 96 distinct campaign-name strings**. Campaign and ad IDs are not available, so repeated names cannot be deduplicated reliably. I therefore preserve every source row and use `campaign_row_id` as the stable analytical identifier.

## 4. Verification and data-quality checks

Before the current analysis was written, I re-read the raw-data sheet and recalculated the numerical relationships rather than relying on the earlier repository summary.

The workbook contains 126 campaign rows. **122 rows have recognisable result types** and four contain an ambiguous result type/value (`2`). For every one of the 122 recognisable rows, recalculating `amount spent / results` reproduces the exported `cost per result` value within `1e-6`; the maximum absolute floating-point difference is approximately `4.95e-09`. This gives a strong internal arithmetic check on the recognised performance records.

The four ambiguous rows are retained in the sanitised dataset with `data_quality_flag = ambiguous_result_type`, but excluded from comparisons by result type because their outcome cannot be interpreted reliably. Together they account for only **NGN 126.39 spend** and **462 impressions**.

The two duplicated campaign-name columns in the source workbook agree across all 126 rows. The quality, engagement-rate and conversion-rate ranking columns contain `-` on every row, so they provide no usable information for the analysis.

The source also repeats the same reporting start and end dates across campaign rows. I treat those as an **export/reporting window**, not as evidence of each campaign's individual active dates. This means time-series creative-fatigue analysis cannot be reconstructed from this file.

## 5. Derived measures

The source export supplies spend, impressions, reach, result type, number of results and exported cost per result. Where the components allow it, I derive additional descriptive measures:

- **CPC / weighted cost per link click** = `total link-campaign spend / total link clicks`
- **Derived link CTR** = `link clicks / impressions × 100`
- **CPM** = `spend / impressions × 1,000`
- **Individual-row impressions/reach ratio** = `impressions / reach`
- **Result/impression rate** = `results / impressions × 100`

Grouped cost-per-result calculations are **weighted** using total spend divided by total results. I do not average campaign-level CPCs because doing so would give every row equal influence regardless of volume.

For distributions, I also report campaign-level medians. This is important because a weighted portfolio KPI answers a different question from a typical row. The former describes what happened across total spend/results; the latter helps reveal whether the pooled figure is being dominated by a small number of campaigns.

Where quartiles are reported, the Python implementation uses `statistics.quantiles(..., method="exclusive")`. The convention is named because alternative percentile definitions can yield slightly different quartile values without any change in the underlying data.

## 6. Analytical procedures

### 6.1 Result-type separation

I first group rows by their recorded result type. Link clicks, Facebook likes, messaging conversations, post engagements, ThruPlays, three-second video plays and leads are analysed separately. This follows from the conceptual measurement map: each is evidence about a different type or stage of response.

### 6.2 Distribution before interpretation

The link-click group is the largest comparable set, so I calculate both portfolio-weighted KPIs and campaign-level distribution statistics. When the weighted CPC and median CPC diverged substantially, I investigated the contribution of high-volume rows rather than treating the pooled KPI as representative of all campaigns.

### 6.3 Concentration analysis

Rows are ranked by recorded link clicks. I calculate what share of total link clicks, spend and impressions is accounted for by the leading campaigns. This identifies whether the account-wide response is broadly distributed or concentrated in a small number of cases.

### 6.4 Sensitivity analysis

Because the two Bunda rows dominate link-click volume, I recalculate the pooled link metrics after excluding them. I then repeat the calculation after excluding the unusually strong Pressure row. The purpose is not to discard successful campaigns, but to test how dependent the headline account metric is on them.

### 6.5 Cross-metric interpretation

For high-performing cases, I examine CPC alongside CPM and CTR. CPC alone cannot tell me whether a low cost per click came from low media-delivery cost, high response to the impressions received, or both. Comparing the three allows a more useful descriptive interpretation of efficiency.

## 7. Why this remains exploratory rather than explanatory

The analysis can identify **where performance differs** because the result metrics are preserved. It cannot reliably identify **why** a campaign differed because most of the explanatory variables needed for that question are missing: complete creative assets, hook/angle/format labels, audience, placement, device, budget strategy, campaign-specific timing and controlled test assignments.

This is a methodological boundary rather than a blanket caution against interpretation. I still make deductions that the data support. For example, when Bunda has a higher CPM than the overall link group but a much lower CPC, I can infer arithmetically that unusually cheap impression delivery is not sufficient to explain the low CPC and that the higher recorded click rate is central to the result. What I cannot infer from the available file is which specific creative, audience or delivery feature caused that response rate.

Yousef et al. (2021) demonstrate the stronger design needed for creative-effect inference: their advertisements were deliberately constructed as comparable variants, exposure was controlled through Facebook's A/B testing tool, and platform engagement was connected with a downstream website action. Their charity/environment context is different from this music-promotion case, so I use the study for methodological reasoning rather than performance benchmarking ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

## 8. Video and downstream-measurement boundaries

Six campaign rows use `ThruPlay` as the result type, while one different row uses `3-second video plays`. These can be analysed within their own groups. I do **not** calculate a combined historical hold/retention rate by dividing one group by the other because the numerator and denominator do not refer to the same creatives or campaign rows.

The downstream-action layer is also incomplete. Messaging conversations are available and one campaign row records a lead, but the dataset lacks consistent landing-page views, purchases and conversion values. Consequently, commercial measures such as purchase conversion rate, CPA/CAC, AOV and ROAS cannot be reconstructed from the surviving export.

## 9. Reproducibility

`analysis/retrospective_analysis.py` reads the public sanitised CSV, reproduces the descriptive metrics and concentration/sensitivity calculations, and writes `analysis/summary.json`. The repository charts are generated from the same sanitised data.

The script and narrative deliberately distinguish **source-recorded measures** from **derived calculations**. The numerical outputs have been re-run against the historical source workbook and reviewed before publication.

## References

Li, F., Larimo, J. and Leonidou, L.C. (2021) ‘Social media marketing strategy: definition, conceptualization, taxonomy, validation, and future agenda’, *Journal of the Academy of Marketing Science*, 49, pp. 51–70. [https://doi.org/10.1007/s11747-020-00733-3](https://doi.org/10.1007/s11747-020-00733-3).

Yousef, M., Dietrich, T. and Rundle-Thiele, S. (2021) ‘Social Advertising Effectiveness in Driving Action: A Study of Positive, Negative and Coactive Appeals on Social Media’, *International Journal of Environmental Research and Public Health*, 18(11), 5954. [https://doi.org/10.3390/ijerph18115954](https://doi.org/10.3390/ijerph18115954).

Nielsen (2025) ‘Why strategy matters more than tools for measurement in marketing’. [https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/).

IAB UK (2026) ‘Measurement hub’. [https://www.iabuk.com/measurement](https://www.iabuk.com/measurement).