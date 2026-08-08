# Retrospective exploratory analysis of historical music-campaign performance

## Executive summary

This report revisits surviving evidence from my work at Kashe Music Group / Santeri. The Meta Ads export is an important quantitative record, but it represents only one part of the campaign. I therefore analyse the later releases as a **resource-to-response system** rather than beginning with advertising metrics alone.

Throsby (2006) distinguishes labour, operating capital and human capital as inputs to artistic production, while Gander's (2015) recording-studio study shows how spatial and material arrangements help regulate tasks, roles, review and decision-making in temporary teams under uncertainty ([Throsby, 2006](https://doi.org/10.1007/s10824-005-9001-4); [Gander, 2015](https://doi.org/10.1108/MD-03-2014-0165)). Drawing on those concepts and the historical case, I distinguish creative/intellectual assets, specialist labour, technical/operating capital, financial capital, organisational capability, network resources, media channels and information resources.

Chronology matters. The four opening-act appearances involving Portable occurred in the earlier manager-led artist phase, before *Let's Fly Away* and before I took broad ownership of creative operations. They therefore establish pre-existing live experience and network access rather than outcomes of my later creative strategy.

*Let's Fly Away* marked the transition to broader creative ownership. Bunda represented a further increase in production intensity. The music video cost more than **NGN 5 million** according to my historical records/recollection and involved more than **30 people**, including specialist roles such as producer, director and costume/styling alongside scripted creative development. The video reached **230,000+ YouTube views** during its active release period according to my historical account. These facts describe production inputs and observed platform response rather than independently proving artistic quality or identifying what caused the response.

The surviving Meta workbook contains **126 campaign rows**, **NGN 1,029,228.11 spend** and **10,332,896 impressions**. Across **106 link-click rows**, it records **635,240 link clicks** from **NGN 907,409.25 spend**, giving a portfolio-weighted **NGN 1.43 CPC**, **6.53% derived CTR** and **NGN 93.30 CPM**. The distribution is much less uniform than those pooled values suggest: median campaign CPC is **NGN 19.81** and median derived CTR is **0.51%**. The two principal Bunda YouTube traffic rows and Pressure account for **94.32% of all link clicks** from **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**.

This is primarily a traffic-response dataset: 106 of 126 rows report link clicks, while every other recognised result type appears in only one to six rows. The unit is an exported campaign row rather than a unique creative asset, and the missing ad-level identifiers and creative metadata prevent creative-feature attribution.

Eighteen recognised rows whose surviving names explicitly contain `Bunda` provide a conservative lower-bound reconstruction. They record **NGN 450,035.75 spend**, **3,085,893 impressions**, **568,819 link clicks** across 15 link-click rows and **29,344 ThruPlays** across three video-view rows. Because some names are generic or truncated, I do not treat this as the complete Bunda Meta budget.

At the time, I believed that stronger content, paid distribution, organic engagement and offline promotion were combining into visible **market traction**, and that this visibility helped when I approached or negotiated with television, radio and event decision-makers. Some opportunities were actively negotiated and others arrived inbound. I did not test that belief. I now treat it as an **untested managerial hypothesis** with multiple plausible drivers and barriers rather than as a causal result.

The retrospective demonstrates a more disciplined way of using the surviving evidence. I separate resources from outcomes, pooled portfolio efficiency from typical campaign performance, paid-media response from total campaign return, and historical managerial interpretation from claims that would require controlled evidence.

## 1. Campaign resources and media architecture

For this case, the relevant resource domains are:

| Resource domain | Examples |
|---|---|
| **Creative/intellectual assets** | Song/master, visual concept, script, artwork, music video, visualiser, short-form edits, challenge concept |
| **Human capital and specialist labour** | Artist, producers, directors, camera/lighting crew, editors, styling/costume, performers, creators, managers and promotional personnel |
| **Technical/operating capital** | Studios/sets, locations, camera/lighting equipment, costumes/props, editing/post-production, transport/logistics |
| **Financial capital** | Production fees, labour, equipment/location, media spend, travel/logistics and offline promotion |
| **Organisational capability** | Budgeting, scheduling, briefing, approvals, coordination, release sequencing and campaign monitoring |
| **Network/relational resources** | Managers, promoters, radio/TV contacts, DJs/clubs, event organisers, collaborators and prior artist trajectory |
| **Media/channel resources** | Owned channels, paid advertising, earned publicity/word of mouth and offline/intermediated access |
| **Information resources** | Meta results, post/page response, audience messages, contact data and later analytical methods |

Lovett and Staelin (2016) distinguish paid, earned and owned media in an entertainment setting ([Lovett & Staelin, 2016](https://doi.org/10.1287/mksc.2015.0961)). I use that classification for the digital campaign and keep radio/TV, DJs/clubs, live activity and other relationship-mediated promotion as a separate practical layer because any particular activity may be paid, earned or network-driven.

## 2. Chronology and the historical hypothesis

The earlier manager-led phase matters because the artist did not begin the later campaign from zero. Existing live experience and networks were already present. *Let's Fly Away* then marked the transition to broader creative ownership, while Bunda materially increased the financial, human and production resources committed.

My working assumption at the time can now be expressed as:

`resource configuration → campaign execution → exposure/engagement → visible traction → perceived market signal → gatekeeper interest/negotiation leverage → media/live opportunities`

That chain was not tested. Existing relationships, prior live history, song characteristics, production intensity, paid reach, organic word of mouth, direct outreach, offline promotion, algorithms, timing and gatekeeper preferences could all have contributed. Polak and Schaap's interviews with 20 formally trained Dutch early- to mid-career musicians provide limited context for this uncertainty: most participants knew about platform-optimisation practices, but only a handful reported using them explicitly. The sample omitted several major genres, including rap/hip-hop, so I use the study only to show that platform awareness does not translate into one uniform production response ([Polak & Schaap, 2025](https://doi.org/10.1177/14614448241243095)).

## 3. Data preparation and verification

The quantitative source is the `Raw Data Report` sheet of `30-01-23.xlsx`. The preparation is deliberately **targeted rather than comprehensive data cleaning** because the historical export was already broadly tabular.

Each record remains a campaign row from that export. Seventeen campaign-name strings recur, but stable campaign/ad IDs are absent, so repeated names cannot safely be classified as duplicate records and are preserved.

The reproducible preparation stage verifies the workbook hash, locates the header, checks the duplicated campaign-name columns, verifies fields before omitting them, preserves all 126 rows, converts the relevant analysis values and redacts the historical WhatsApp phone number from one campaign name. Repeated campaign names are retained because the file does not preserve the stable campaign/ad IDs needed to decide whether they are duplicates.

Four rows have **blank result type, blank Results and blank Cost per result fields**. They are preserved and flagged `missing_result_type` rather than repaired. An earlier manual inspection had described these records as result type `2`; end-to-end reproduction with the XLSX shared strings resolved correctly showed that the corresponding shared-string entry is empty. This correction does not change the published result-type KPIs because those rows were already excluded from result-type summaries. They account for only **NGN 126.39 spend** and **462 impressions**.

For all **122 rows with recognised result types**, recalculating `amount spent / results` reproduces Meta's exported cost per result within normal floating-point precision. This supports the internal consistency of the transferred numerical fields; it does not independently validate Meta's historical attribution system.

## 4. Paid-social delivery and traffic response

The 106 link-click rows provide the largest comparable group:

| Measure | Result |
|---|---:|
| Spend | **NGN 907,409.25** |
| Impressions | **9,725,211** |
| Link clicks | **635,240** |
| Weighted CPC | **NGN 1.43** |
| Derived link CTR | **6.53%** |
| Derived CPM | **NGN 93.30** |

The pooled figures hide a highly concentrated distribution. The **median campaign CPC is NGN 19.81** and the **median derived CTR is 0.51%**. CPC ranges from approximately **NGN 0.29 to NGN 397.11**.

The two principal Bunda YouTube traffic rows and Pressure generated **599,178 clicks**, or **94.32% of all link clicks**, from **44.27% of link-campaign spend** and **28.00% of link-campaign impressions**. I therefore use the weighted result as a portfolio statistic, not as the normal performance of an individual campaign row.

## 5. Bunda and Pressure: interpreting the high-response cases

The two rows labelled `Bunda Youtube – official` and `Bunda Youtube` record **565,764 Meta link clicks**, **2,613,269 impressions** and **NGN 391,913.64 spend**, giving **NGN 0.69 weighted CPC**, **21.65% derived CTR** and **NGN 149.97 CPM**.

Their CPM is higher than the NGN 93.30 pooled CPM across link-click rows, yet their CPC is much lower. The low CPC is therefore not explained by unusually cheap impression delivery. Arithmetically, the high rate of clicks relative to impressions is central to the result.

Pressure records **33,414 clicks from 110,215 impressions and NGN 9,825 spend**, equivalent to **30.32% derived CTR**, **NGN 0.29 CPC** and approximately **NGN 89.14 CPM**.

Sensitivity analysis confirms how strongly those cases affect the portfolio. Removing the two Bunda YouTube rows increases weighted CPC to **NGN 7.42** and reduces derived CTR to **0.98%**. Removing Pressure as well leaves 103 rows at **NGN 14.02 CPC** and **0.52% CTR**.

These calculations identify where unusually strong response occurred. They do not identify which hook, format, audience, placement or other factor produced it because those explanatory variables are not consistently preserved.

## 6. Other objectives and direct audience development

Two `Promoting Santeri` rows record **3,977 attributed Facebook likes** from **NGN 73,259.03 spend**, or **NGN 18.42 per attributed like**. In my historical account, the Facebook page audience grew from launch to around **5,000 in just over a month** while the paid-growth campaigns were active, before plateauing. The attributed likes partly corroborate that activity but do not independently establish the full page total or exact interval.

Two messaging rows record **86 conversations started** from **NGN 10,769.04 spend**; the larger click-to-WhatsApp campaign produced **78 conversations from NGN 8,460.63**. I personally engaged incoming contacts and retained contacts for later promotion, using the feature as a direct audience contact list for closer communication rather than treating the conversations as one-off responses. The workbook records the conversations, while the retention and later use of contacts form part of my historical operating account.

Six rows record **58,112 ThruPlays** from **NGN 20,596.01 spend**, while one separate row records **3,233 three-second video plays**. Because those measures are not recorded for the same campaign rows, I do not manufacture a historical retention/hold rate by dividing one group by the other.

## 7. Resource efficiency versus total campaign return

The Meta file supports **paid-media efficiency** calculations because spend and the corresponding platform result are recorded together. It does not support a total campaign ROI.

For Bunda, I can identify more than **NGN 5 million** of author-reported video-production expenditure and **NGN 450,035.75** of explicitly Bunda-labelled Meta spend, before other digital and offline work is added. A defensible conclusion is therefore that Bunda used a substantially larger and more specialised resource bundle, and that parts of its Meta distribution achieved unusually efficient traffic response.

What cannot be reconstructed is whether the **complete** production, media, offline and labour resource bundle produced an economically efficient return. That would require a fuller cost ledger linked to revenue, profit, attributable bookings, audience lifetime value or another defined strategic outcome.

## 8. What I would test now

A future campaign analysis would collect the missing explanatory variables before launch: stable campaign/ad IDs, hook/format/angle/creator/CTA labels, production costs by workstream, audience and placement, campaign-specific dates, organic versus paid response, and downstream events such as streams, follows, direct enquiries, bookings, conversion value and revenue.

The question could then move from **where did performance differ?** to **which resource and creative configurations produced the most valuable response, through which channel, at what cost, and with what degree of confidence?** Where causal conclusions matter, controlled comparisons should be designed rather than inferred retrospectively from unrelated campaign rows.

## 9. Conclusion

The historical work combined creative production, specialist labour, technical resources, financial commitment, coordination, professional networks, paid media, owned content, organic response and offline/intermediated promotion. Bunda was the clearest scale-up, with more than NGN 5 million of author-reported video expenditure and at least NGN 450,035.75 of explicitly identifiable Meta spend in the surviving export.

The Meta records also show that paid-social response was unusually concentrated. Bunda and Pressure materially shape the portfolio averages, and Bunda's low CPC occurred despite higher-than-average CPM, making its recorded click rate central to its observed media efficiency.

The later media/live opportunities belong to the historical trajectory, but my original explanation for them remains a hypothesis. The strongest use of the surviving evidence is therefore exploratory: document the resources and activity, identify where response concentrated, quantify paid-media efficiency, and show what a better-designed future measurement system would need in order to test the drivers and barriers I could only infer at the time.

## References

Gander, J.M. (2015) 'Situating creative production: recording studios and the making of a pop song', *Management Decision*, 53(4), pp. 843–856. https://doi.org/10.1108/MD-03-2014-0165

Lovett, M.J. and Staelin, R. (2016) 'The role of paid, earned, and owned media in building entertainment brands: reminding, informing, and enhancing enjoyment', *Marketing Science*, 35(1), pp. 142–157. https://doi.org/10.1287/mksc.2015.0961

Polak, N. and Schaap, J. (2025) 'Write, record, optimize? How musicians reflect on music optimization strategies in the creative production process', *New Media & Society*, 27(8), pp. 4773–4789. First published online in 2024. https://doi.org/10.1177/14614448241243095

Throsby, D. (2006) 'An artistic production function: theory and an application to Australian visual artists', *Journal of Cultural Economics*, 30, pp. 1–14. https://doi.org/10.1007/s10824-005-9001-4
