# CEO dashboard research and design decisions

## Question

How should the existing retrospective be presented so that a time-constrained
executive can identify the main finding, understand its business significance
and decide what to do next without being misled by gaps in the historical data?

## Evidence matrix

| Source | Source judgement and reading depth | What it supports | Design decision |
|---|---|---|---|
| Microsoft Learn, *Tips for designing a great Power BI dashboard* | Official product guidance; relevant page read in full | Dashboards should reflect audience decisions, tell the story on one screen, place the highest-level information first and remove non-essential content | The first tab is a single decision brief. It leads with the finding and uses four contextual KPI cards rather than a general analytics workspace |
| Tableau Help, *Best Practices for Effective Dashboards* | Official product guidance; short page read in full | The most important view belongs in the upper-left area and two or three views are usually enough | The executive tab contains two charts: concentration and sensitivity. Detailed rows sit in a separate tab |
| Streamlit documentation, metrics and layout containers | Official technical documentation; relevant API and layout sections read in full | Metric cards, columns, tabs and expanders support a concise overview with secondary detail separated from the first view | Streamlit is used for a reproducible Python interface; responsive columns hold the KPIs and charts, while tabs contain due-diligence detail |
| UK Government Analysis Function, visualisation formatting guidance | Official analytical communication guidance; relevant formatting sections read in full | Clear charts remove decoration, use light grids, horizontal labels, direct labelling and restrained colour | The charts use horizontal bars, direct values, light gridlines, no 3D effects, no gauges and no decorative background images |
| Storytelling with Data, executive-summary and recommendation guidance | Specialist practitioner source; both web articles read in full | A summary title should state the takeaway, the communication should make the intended insight explicit, and the recommendation position should fit the audience | The headline states the concentration finding. The decision follows immediately because the dashboard is designed for a time-constrained executive |
| HBR, *How to Brief a Senior Executive* | Reputable management source; accessible article introduction and summary read, not the full paywalled article | Executive briefings require complex material to be compressed to the time available | Method detail is not removed, but it is placed behind the decision view |

## Synthesis

**Fact:** the published analysis shows that three link-click rows generated
94.32% of recorded link clicks from 44.27% of link-campaign spend and 28.00% of
link-campaign impressions. Removing those rows changes weighted CPC from NGN
1.43 to NGN 14.02 and derived CTR from 6.53% to 0.52%.

**Inference:** the pooled link metrics are dominated by exceptional rows and
should not be presented as the expected performance of a typical campaign.

**Recommendation:** use the leading rows to define creative hypotheses, recover
the underlying assets and delivery settings, then run a prospective test tied
to a commercial outcome. The dashboard therefore leads with concentration,
sensitivity and the next decision rather than a catalogue of all available
metrics.

The template image search was used only for visual pattern sampling. Several
commercial examples were dense and gauge-heavy, so official guidance on
clarity, comparison and limited views took precedence. No template was copied.

## Boundaries and confidence

Confidence is high that the dashboard structure is appropriate for this
dataset and audience because the official dashboard sources agree on audience,
hierarchy and restraint, and the design follows the repository's validated
analysis. Confidence is lower on whether a specific CEO would prefer more or
less detail; direct user testing with one or two executives could change the
ordering or wording.

Targets, trend arrows, ROAS and date controls are intentionally absent. Adding
them would require a reliable reporting period, comparison period, business
target and downstream revenue or profit data, none of which is preserved in
the public export.

## Sources

- https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips
- https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm
- https://docs.streamlit.io/develop/api-reference/data/st.metric
- https://docs.streamlit.io/develop/concepts/design/layouts-and-containers
- https://analysisfunction.civilservice.gov.uk/support/communicating-analysis/introduction-to-data-visualisation-e-learning/data-visualisation-e-learning-module-4-general-formatting-rules/
- https://www.storytellingwithdata.com/blog/2022/1/14/executive-summary-slides
- https://www.storytellingwithdata.com/blog/should-i-begin-or-end-with-my-recommendation
- https://hbr.org/2020/11/how-to-brief-a-senior-executive
