# Retrospective exploratory analysis of historical Meta Ads performance

## Executive summary

This report revisits a surviving Meta Ads export from my work at Kashe Music Group / Santeri. Its first purpose is analytical: to examine the historical campaign data using the stronger data-analysis and research discipline I have developed since the campaigns were run. Its second purpose is evidential: to show the surviving basis for statements in my CV and cover letter about running paid media and using campaign-performance information to inform creative and promotional decisions.

The analysis starts from the role that measurement serves. Li, Larimo and Leonidou (2021) describe social media as having developed from a promotional tool into a source of marketing intelligence through which firms can observe customer behaviour, interpret information and respond. They also show that social-media strategies can pursue different objectives, so their outputs and appropriate performance measures are not interchangeable ([Li et al., 2021](https://doi.org/10.1007/s11747-020-00733-3)). Yousef, Dietrich and Rundle-Thiele (2021) make a related distinction in an experimental Facebook study between exposure or connection, interaction with advertising, and action beyond the platform; their design connected platform metrics to a website behaviour rather than treating engagement as the final outcome ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)). I use these ideas to organise the historical data into five analytical layers: **delivery, attention, traffic response, downstream action and commercial value**. This five-layer map is my synthesis for this retrospective, rather than a framework stated verbatim by either study.

The source workbook contains **126 campaign rows** and **NGN 1,029,228.11** of recorded campaign spend. Of the 126 rows, 122 have recognisable result types and all 122 reproduce the exported cost-per-result value when `amount spent / results` is recalculated to normal floating-point precision. The export records **10,332,896 impressions**. A separate Meta account screenshot records **NGN 1,492,844.45 spent at account level**, so the workbook represents about **68.94%** of that figure and is treated as a surviving subset of the account history rather than the complete account record.

Traffic response is the strongest reconstructable layer. Across **106 link-click rows**, the export records **635,240 link clicks** from **9,725,211 impressions** and **NGN 907,409.25 spend**. This gives a portfolio-weighted **NGN 1.43 CPC**, **6.53% derived link CTR** and **NGN 93.30 CPM**. Those pooled values are not representative of a typical campaign row: median campaign CPC is **NGN 19.81** and median derived CTR is **0.51%**. The difference led me to examine concentration. The two Bunda YouTube traffic rows and one Pressure row generated **94.32% of all recorded link clicks** while accounting for **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**. I therefore interpret the very low portfolio-weighted CPC primarily as the result of a small number of unusually high-response campaigns rather than consistently similar performance across the account.

The two Bunda traffic rows are the clearest example. Together they produced **565,764 Meta link clicks** from **2,613,269 impressions** and **NGN 391,913.64 spend**, giving a weighted **NGN 0.69 CPC**, **21.65% derived link CTR** and **NGN 149.97 CPM**. Their CPM was higher than the NGN 93.30 pooled CPM of all link-click rows, while their CPC was substantially lower. Within the metrics available, the low CPC is therefore explained arithmetically by the much higher recorded click rate rather than unusually cheap impression delivery. A sensitivity check strengthens that interpretation: removing Bunda reduces pooled link CTR from 6.53% to **0.98%** and increases CPC from NGN 1.43 to **NGN 7.42**; removing the Pressure row as well leaves the remaining 103 link-click rows at **0.52% CTR** and **NGN 14.02 CPC**.

The export also preserves evidence from other objectives: **3,977 attributed Facebook likes**, **86 messaging conversations started**, **58,112 ThruPlays** and **12,859 post engagements** in their respective campaign groups. These measures answer different questions and are analysed separately. The data are much weaker for downstream conversion and commercial value: there is only one lead-form result and no reliable purchase, revenue, AOV, CPA/CAC or ROAS data. The retrospective can consequently explain the scale, response and distribution of the surviving paid-social activity, but it cannot reconstruct a complete ecommerce conversion funnel or identify which hook, creator, format or audience caused a performance difference. That distinction determines the scope of the conclusions rather than being added as a generic disclaimer.

## 1. From social-media activity to marketing intelligence

The starting concept is not the individual KPI but the decision that the information is meant to support. Li et al. (2021) argue that the role of social media has expanded beyond being a communication channel: customer behaviour on social platforms can also become an information resource for marketing decisions. Their social-monitoring strategy is especially relevant to this retrospective because it describes firms using behavioural data to listen, learn and react, supported by capabilities for acquiring, interpreting and responding to information ([Li et al., 2021](https://doi.org/10.1007/s11747-020-00733-3)).

That distinction reflects how I remember using Meta at the time. I was not running a formal creative-analytics programme or a controlled experimentation system. I was producing and promoting content, looking at the performance information available in Meta and using those signals to judge which posts and approaches appeared to be attracting stronger audience response. This retrospective does not rewrite that historical practice as something more mature than it was. Instead, it uses the surviving data to examine what those performance signals actually looked like and what I can now infer from them more systematically.

Li et al. also show why objectives matter. Their framework distinguishes strategic uses of social media ranging from promotion and selling to content, monitoring and relationship management, while their empirical validation found that different strategies emphasised different objectives and engagement behaviours. In their future-research agenda, the authors identify appropriate performance metrics as a priority and distinguish performance in terms of effectiveness, efficiency and adaptiveness. I take from this that a metric should not be treated as intrinsically meaningful: its value depends on the objective and the decision it is capable of informing.

Current sector material points in the same direction. Nielsen's 2025 measurement article argues that marketing teams can accumulate impressions, clicks, engagement, conversions and spend without necessarily gaining clarity; it places emphasis on aligning KPIs with business priorities and interpreting patterns in context before using them to make resource-allocation decisions ([Nielsen, 2025](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/)). IAB UK's current Measurement Hub similarly positions measurement strategy as something selected according to the objective and frames outcomes measurement, standards, consistency, transparency and trust as active industry priorities ([IAB UK, 2026](https://www.iabuk.com/measurement)). These are sector perspectives rather than substitutes for peer-reviewed evidence, but they show that objective-led measurement remains a practical concern in contemporary advertising.

## 2. A measurement map for this retrospective

Yousef et al. (2021) provide a useful empirical bridge from concepts to measurement. Building on a multi-actor engagement framework, they distinguish **connection** (including reach and impressions), **interaction** (including clicks and engagement), loyalty and advocacy, and then extend the analysis to a behavioural action beyond Facebook. Their experiment controlled three Facebook advertisements through A/B testing and linked platform metrics to website form submissions. The study therefore demonstrates two things that matter here: performance can be observed at different stages, and a stronger claim about what creative produced an effect requires a design that makes the alternatives genuinely comparable ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

Drawing on that distinction, Li et al.'s objective-led strategy perspective, and the present data structure, I use the following analytical map. This is **my synthesis** for interpreting the export:

| Layer | Decision question | Examples of relevant measures | Coverage in this export |
|---|---|---|---|
| **Delivery** | At what scale and cost was advertising delivered? | Spend, impressions, reach, CPM, frequency | Strong, although reach overlaps across campaigns |
| **Attention** | Did the delivered creative hold enough attention to progress? | 3-second views, ThruPlay, retention/watch metrics | Partial and inconsistent across rows |
| **Traffic response** | Did exposure produce the intended click response, and at what cost? | Link clicks, CTR, CPC | Strongest comparable layer |
| **Downstream action** | What happened after or beyond the initial platform response? | Landing-page views, messages, leads, purchases, conversion rate | Partial: messaging is present; only one lead-form result |
| **Commercial value** | Did those actions create sufficient economic value? | Revenue, AOV, CPA/CAC, ROAS, profit contribution | Not present |

The practical benefit of this map is that it prevents unlike metrics from being collapsed into a single idea of “performance”. An impression describes delivery. A click describes a response. A purchase would describe a later action, while ROAS would connect that action to economic value. The historical export contains substantial evidence for the first and third layers, some evidence for attention and direct conversation, and little evidence for the commercial end of the chain.

## 3. Source data, unit of analysis and integrity checks

The source is a historical Meta Ads workbook supplied from the advertising account. The public repository contains a sanitised campaign-level derivative because one campaign name in the original workbook included a historical WhatsApp phone number. No performance values are changed by that redaction.

Each row is treated as a **campaign row**, not automatically as a unique campaign. The workbook contains **126 rows but 96 distinct campaign-name strings**, and it does not preserve the campaign/ad IDs needed to resolve repeated names reliably. I therefore retain each source row and assign `campaign_row_id` as a stable analytical identifier rather than deduplicating by name.

The integrity checks produced a strong result. Of 126 rows, **122 have recognisable result types**, and all 122 satisfy the arithmetic relationship between results, spend and the exported cost-per-result value to within normal floating-point precision. The maximum absolute difference when I recalculate `amount spent / results` is approximately `4.95e-09`. Four rows contain an ambiguous result type/value (`2`) and are retained for transparency but excluded from result-type comparisons. Together those four rows represent only **NGN 126.39 spend** and **462 impressions**, so their exclusion does not materially drive the main findings.

Across all rows, the workbook records **NGN 1,029,228.11 spend**, **10,332,896 impressions** and **8,630,892 summed campaign-level reach**. The separate account screenshot records **NGN 1,492,844.45 spent**. I therefore interpret the workbook as a partial surviving export: it contains about 68.94% of the account-level spend shown in the screenshot and leaves approximately **NGN 463,616.34** outside the available campaign file.

The summed reach value is retained because it is useful for inspecting individual rows and delivery ratios, but it is not used as a count of distinct people across the portfolio. The same person can appear in the reach of more than one campaign, so summing campaign reach does not deduplicate audiences. The more stable export-wide scale measure for this analysis is therefore the **10.33 million recorded impressions**.

## 4. Delivery: scale and cost of exposure

Delivery measures answer the first question in the measurement map: how much advertising was served and what did that delivery cost? Across the full export, **10,332,896 impressions** were recorded from **NGN 1,029,228.11** spend, producing a derived portfolio CPM of approximately **NGN 99.61**.

That figure is useful for describing the cost of delivering the historical advertising inventory represented by the file. It does not, by itself, tell me whether the creative persuaded people to act. This is where the distinction in Yousef et al. (2021) between connection/exposure and interaction becomes analytically useful: delivery establishes the opportunity for response; the next layer asks what response was recorded.

## 5. Traffic response: the pooled account result hides a highly uneven distribution

The most complete comparable group consists of the **106 rows whose recorded result type is Link clicks**. Together these rows record:

| Measure | Result |
|---|---:|
| Spend | **NGN 907,409.25** |
| Impressions | **9,725,211** |
| Link clicks | **635,240** |
| Weighted CPC | **NGN 1.43** |
| Derived link CTR | **6.53%** |
| Derived CPM | **NGN 93.30** |

If I stopped at those pooled KPIs, the account would appear to have produced a fairly uniform story of high click response at very low cost. The campaign distribution shows otherwise. The **median campaign-level CPC is NGN 19.81**, around fourteen times the weighted CPC, while the **median campaign-level derived CTR is 0.51%**, far below the pooled 6.53% rate. The campaign-level CPC values range from approximately **NGN 0.29 to NGN 397.11**.

This difference changed the analytical question. Rather than asking only “what was the account CPC?”, I asked **which rows are determining that aggregate?** The answer is unusually concentrated. The three largest link-click rows by clicks are `Bunda Youtube – official`, `Bunda Youtube`, and the Pressure post. Together they generated **599,178 clicks**, or **94.32% of all link clicks**, while using **44.27% of link-campaign spend** and receiving **28.00% of link-campaign impressions**.

I therefore interpret the NGN 1.43 weighted CPC and 6.53% pooled CTR as valid portfolio statistics but poor descriptions of a typical campaign row. The medians tell me more about the centre of the campaign distribution, while the weighted figures tell me what happened to the advertising portfolio as a whole. Reporting both is more informative because it makes the concentration visible instead of allowing a small number of high-volume campaigns to define the apparent norm.

## 6. Bunda and Pressure: what the outliers tell me

The two rows explicitly labelled `Bunda Youtube – official` and `Bunda Youtube` record:

| Bunda traffic measure | Result |
|---|---:|
| Meta link clicks | **565,764** |
| Impressions | **2,613,269** |
| Spend | **NGN 391,913.64** |
| Weighted CPC | **NGN 0.69** |
| Derived link CTR | **21.65%** |
| Derived CPM | **NGN 149.97** |

These two rows alone account for **89.06% of all link clicks**, **43.19% of link-campaign spend** and **26.87% of link-campaign impressions**.

The relationship between CPM, CTR and CPC is especially informative. Bunda's combined **NGN 149.97 CPM is higher** than the **NGN 93.30 CPM** across all link-click rows, yet its **NGN 0.69 CPC is much lower** than the pooled NGN 1.43 and the median campaign CPC of NGN 19.81. On the available data, unusually cheap impression delivery cannot explain that low CPC. Arithmetically, it is the exceptionally high rate of recorded clicks relative to impressions that offsets the higher delivery cost.

The Pressure row reinforces the point. It records **33,414 link clicks from 110,215 impressions and NGN 9,825 spend**, equivalent to a derived **30.32% link CTR**, **NGN 0.29 CPC** and **NGN 89.14 CPM**. Pressure therefore combines a delivery cost close to the link-campaign average with an unusually high response rate.

I tested how sensitive the portfolio result is to these outliers. Removing the two Bunda rows leaves **69,476 clicks** and raises weighted CPC to **NGN 7.42**, while derived CTR falls to **0.98%**. Removing Pressure as well leaves 103 link-click rows at **NGN 14.02 weighted CPC** and **0.52% derived CTR**. The sensitivity analysis strengthens my interpretation that Bunda and Pressure were not simply larger versions of typical campaign performance; they materially change the shape of the portfolio result.

The missing creative and targeting metadata determines where that interpretation must stop. Many original posts have since been deleted or disabled, and the export does not preserve a reliable common taxonomy of hook, angle, creator, CTA, placement, audience and campaign-specific timing. I can identify **where** exceptional performance appears in the data, but this file alone cannot identify **which underlying creative or delivery variable produced it**. Yousef et al.'s controlled experiment illustrates the additional design needed for that stronger conclusion: comparable alternatives, controlled exposure and an outcome defined beyond the initial platform signal ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

## 7. Audience growth and direct conversation: different objectives, different evidence

Two `Promoting Santeri` rows use **Facebook likes** as their result type. Together they record **3,977 attributed likes** from **NGN 73,259.03 spend** and **39,504 impressions**, producing a weighted **NGN 18.42 cost per attributed like**. These rows provide direct historical evidence that paid promotion contributed materially to audience growth during the period in which the Facebook page was being developed. They do not reconstruct the complete follower time series, so I continue to treat the recollected growth from roughly 0 to 5,000 followers within four months as a historical account rather than a figure reproduced from this export.

Two other rows use **messaging conversations started** as the result type. Together they record **86 conversations** from **NGN 10,769.04 spend**, a weighted **NGN 125.22 per conversation**. The larger click-to-WhatsApp campaign produced **78 conversations from NGN 8,460.63**, or **NGN 108.47 per conversation**.

This is analytically different from a click objective. It records movement from advertising exposure into direct two-way conversation. Li et al. (2021) distinguish simple promotion from more interactive uses of social media in which firms learn from and respond to customer behaviour. I would not retrospectively label this small-business practice a formal social-CRM system, but the campaign-to-WhatsApp process did move beyond one-way promotion: I personally engaged the incoming contacts and retained contacts for later promotion. In the context of this portfolio, the messaging rows therefore support the historical account of using paid media not only to generate visibility but also to build direct audience relationships.

## 8. Attention and engagement: useful signals, but not a common video funnel

The export contains additional groups reported under different objectives. Six rows record **58,112 ThruPlays** from **NGN 20,596.01 spend**, producing a weighted **NGN 0.35 cost per ThruPlay**. Four rows record **12,859 post engagements** from **NGN 15,606.98 spend**, or approximately **NGN 1.21 per engagement**. One separate row records **3,233 three-second video plays from 12,144 impressions**, a derived **26.62% three-second-view/impression rate** and approximately **NGN 0.14 per three-second play**.

These measures are relevant to the attention and interaction layers, but the way they were exported prevents me from building a consistent video-retention sequence. The three-second plays and ThruPlays were not recorded for the same set of campaign rows. Calculating a “hold rate” by dividing one group by the other would therefore manufacture a denominator relationship that does not exist in the source data. I retain the component results and analyse them within their own groups instead.

## 9. What the retrospective establishes about my historical working practice

The numerical analysis and the historical account answer slightly different questions. The export establishes that I was running real paid-social activity at meaningful scale and that campaign outcomes varied substantially. My historical account explains how I used the information available to me: I compared Meta performance across posts and campaigns, learned which approaches appeared to be gaining stronger response, and used that information when planning later content and promotion.

The retrospective adds analytical discipline that I did not apply formally at the time. In particular, it reveals that the headline account metrics are dominated by a small number of outliers; separates delivery cost from response efficiency; uses sensitivity checks to test how dependent the pooled result is on Bunda and Pressure; and separates objectives instead of treating all result types as comparable. That is the most important development from my earlier practice. I am not presenting the historical campaigns as if they were designed by the analyst I am now becoming; I am showing how later analytical training allows me to interrogate the work more rigorously.

This also explains why the repository is useful as evidence for my CV and cover letter. The claim is not simply that I had access to Meta Ads Manager. The source data show sustained campaign activity, substantial delivery and response volumes, audience-growth activity and direct-response messaging. The retrospective then demonstrates how I now convert those records into a structured performance analysis.

## 10. What a contemporary ecommerce creative analysis would add

The current sector direction reinforces the distinction between reporting activity and measuring outcomes. Nielsen (2025) argues that measurement becomes useful when KPIs are linked to business priorities and interpreted in context, while IAB UK's current Measurement Hub foregrounds outcomes measurement and provides different measurement approaches according to the objective ([Nielsen, 2025](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/); [IAB UK, 2026](https://www.iabuk.com/measurement)).

For a contemporary ecommerce creative-analysis environment, I would therefore extend this dataset in two directions.

First, I would create a **creative taxonomy** that makes the content analytically comparable: hook, format, angle, creator, CTA, duration, placement and other relevant characteristics. Those labels would be joined to campaign/ad IDs, audience and delivery metadata. This would allow questions such as whether particular creative approaches are repeatedly associated with stronger early attention, click response or conversion performance.

Second, I would connect those upstream creative measures to **downstream outcomes**: landing-page views, add-to-cart, checkout, purchase conversion, CPA/CAC, revenue, AOV and ROAS or another appropriate profitability measure. The decision question then changes from “which ad received the strongest response?” to “which creative approach produced the most commercially valuable response at an acceptable acquisition cost?”

Where the objective is causal learning rather than exploratory diagnosis, I would also require a test design that supports the claim. Yousef et al. (2021) controlled exposure across creative variants and connected Facebook behaviour to an external website action. Their setting was environmental/charity advertising rather than ecommerce, so I do not use their performance values as benchmarks for these campaigns; I use the study methodologically to show why controlled comparison and downstream outcomes matter when attributing an effect to creative ([Yousef et al., 2021](https://doi.org/10.3390/ijerph18115954)).

## 11. Conclusion

The surviving data support a more substantial account of my historical Meta experience than a simple statement that I ran social ads. The workbook documents over **NGN 1.02 million** of campaign-level spend and **10.33 million impressions**, while separate account evidence shows about **NGN 1.49 million spent**. It records **635,240 link clicks**, with the majority concentrated in the two Bunda traffic campaigns and the Pressure row, as well as audience-growth, messaging, video and engagement outcomes.

The main analytical finding is not the pooled CPC or CTR alone. It is the **distribution behind them**. The very low weighted CPC is largely produced by three unusually high-response rows. Bunda is particularly notable because its low CPC occurs despite a higher-than-average CPM, making the recorded response rate central to understanding its efficiency. The sensitivity analysis confirms that removing those outliers materially changes the portfolio result.

Taken together, the data and literature support my interpretation that the most defensible use of this historical export is **exploratory performance analysis**: establishing what was delivered, where response concentrated, how efficiency differed and which cases merit deeper creative investigation. The missing historical assets and downstream commercial data prevent the stronger explanatory question from being answered retrospectively. That boundary does not weaken the evidence of the work performed; it defines what the surviving evidence can responsibly support.

## References

Li, F., Larimo, J. and Leonidou, L.C. (2021) ‘Social media marketing strategy: definition, conceptualization, taxonomy, validation, and future agenda’, *Journal of the Academy of Marketing Science*, 49, pp. 51–70. [https://doi.org/10.1007/s11747-020-00733-3](https://doi.org/10.1007/s11747-020-00733-3).

Yousef, M., Dietrich, T. and Rundle-Thiele, S. (2021) ‘Social Advertising Effectiveness in Driving Action: A Study of Positive, Negative and Coactive Appeals on Social Media’, *International Journal of Environmental Research and Public Health*, 18(11), 5954. [https://doi.org/10.3390/ijerph18115954](https://doi.org/10.3390/ijerph18115954).

Nielsen (2025) ‘Why strategy matters more than tools for measurement in marketing’, November 2025. [https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/](https://www.nielsen.com/insights/2025/why-strategy-matters-more-than-tools-roi/).

IAB UK (2026) ‘Measurement hub’. [https://www.iabuk.com/measurement](https://www.iabuk.com/measurement).