# Future campaign measurement plan

## Research question

How should a future Kashe music campaign be designed so that its creative,
delivery, audience, cost and downstream outcomes can be analysed more
credibly than the historical Meta export, without imposing an enterprise-level
measurement system on a small campaign?

## Evidence matrix

| Source | Type and reading depth | Evidence used | Implication for the next campaign |
|---|---|---|---|
| This repository's methodology and exploratory report | Primary case evidence; relevant limitations and future-work sections read in full | The historical export lacks stable ad-level identifiers, creative and delivery metadata, reliable dates, a complete cost ledger and downstream value measures | Build the prospective data structure around these known gaps rather than collecting more platform metrics without context |
| Meta, Ads Manager campaign structure and Conversions API guidance | Official platform guidance; relevant indexed guidance reviewed, with current pages checked on 22 August 2026 | Objective sits at campaign level; audience, placement, budget and schedule sit at ad-set level; creative sits at ad level. Pixel and Conversions API events can support later-journey measurement, but do not override privacy requirements | Preserve identifiers and settings at all three levels. Use website or CRM events only when proportionate, technically verified and lawfully collected |
| Google Analytics, custom campaign URLs and recommended events | Official product guidance; both pages read in full | Consistent UTM values identify referring campaigns and creative variants; recommended events cover actions such as sign-up, lead generation and purchase; events should be verified after setup | Use a controlled naming and tagging dictionary, select events that match the real campaign journey and test them before launch |
| Spotify for Artists, audience segments and release engagement | Official platform guidance; both pages read in full | Spotify distinguishes active and programmed listeners and reports the proportion of the pre-release active audience engaging with a release over its first 28 days | Record pre-launch and post-launch Spotify snapshots as contextual evidence of fan development, while avoiding unsupported claims that a Meta click caused a stream |
| ICO, direct-marketing and electronic-mail guidance | UK regulator; relevant consent, tracking and record-keeping sections read | Tracking pixels and electronic marketing can engage PECR and data-protection duties. Consent must be specific and informed where required, recorded, and easy to withdraw | Treat fan contact collection as an owned relationship with a consent record and withdrawal route, not merely as a campaign result |
| IAB and IAB Europe, 2025 incrementality guidelines | Industry guidance; pages 2-7 read in detail, acknowledgements not used | Attribution describes observed credit; a causal claim requires a credible counterfactual, bias control and enough signal. Experiments offer stronger causal evidence but can be costly and vulnerable to contamination or insufficient data | Do not make a controlled test mandatory for the first prospective campaign. Establish clean measurement first and add causal testing when feasibility and decision value justify it |

## Synthesis

**Fact:** the retrospective can locate unusually strong platform response, but
it cannot connect that response reliably to a unique creative treatment,
delivery configuration, listener action or commercial return.

**Inference:** the immediate capability gap is measurement design and evidence
preservation, not another retrospective calculation. A future campaign will be
more informative if the decision, identifiers, event definitions, costs and
review windows are agreed before launch.

**Recommendation:** run the next campaign as a prospective measurement case
study. Use the minimum viable design below. Treat platform attribution and
Spotify movement as evidence of observed association. Reserve causal language
for a properly designed comparison with a credible counterfactual and adequate
signal.

## Minimum viable design

### 1. Plan the evidence before launch

Create a one-page campaign brief containing:

- the decision the campaign is intended to inform;
- one primary outcome, such as new active listeners, consented fan sign-ups,
  qualified enquiries, ticket or merchandise sales, depending on the real
  campaign purpose;
- supporting funnel measures from spend and impressions through landing-page
  and outbound-platform actions;
- the total budget, reporting currency, campaign dates and one consistent time
  zone;
- a pre-campaign baseline and fixed reporting checkpoints;
- the conditions for continuing, changing or stopping the campaign; and
- the owner of each data source and final decision.

For a release campaign, take a baseline snapshot immediately before launch,
review platform delivery during the campaign, close the primary outcome window
at 28 days, and schedule at least one later retention review. The 28-day point
aligns with Spotify's release-engagement and active-audience reporting, but it
does not prove attribution from external advertising.

### 2. Instrument the journey

Maintain a campaign register with one row per ad and fields for:

- platform campaign, ad-set and ad IDs;
- objective, optimisation event and attribution setting;
- audience definition, geography, placement, schedule, budget and bid setting;
- creative ID and version, asset link, hook, angle, format, duration, creator,
  call to action and music excerpt;
- lowercase, consistently governed `utm_source`, `utm_medium`,
  `utm_campaign`, `utm_id` and `utm_content` values;
- paid, owned, earned or offline channel label;
- production, creator, media, agency and offline costs; and
- every material change, including date, reason and decision-maker.

Send traffic through a campaign landing or smart-link page where this fits the
audience journey. Measure only useful events, for example landing-page view,
outbound music-platform click, consented sign-up, lead, booking or purchase.
Use GA4 recommended events where they match. Add Meta Pixel or Conversions API
only when the expected value justifies the setup and the privacy controls are
in place. Verify events in test and real-time views before spending.

Keep personal information out of URLs and analytics parameters. If collecting
email, WhatsApp or other direct-contact details, record what the person agreed
to, when and how; explain the intended communication; and provide a practical
way to withdraw. Apply the law relevant to the campaign's operating and target
markets rather than assuming UK guidance covers every territory.

### 3. Run, preserve and review

- Freeze the brief, taxonomy and event dictionary before launch.
- Test every tagged destination and conversion event on desktop and mobile.
- Preserve raw exports and platform screenshots at each checkpoint rather than
  relying on a final dashboard view that may later change.
- Log budget, targeting, creative, schedule and optimisation changes when they
  occur.
- Reconcile media invoices and production costs with the campaign register.
- Report platform delivery, website or smart-link behaviour, owned actions,
  Spotify audience movement and commercial outcomes as separate evidence
  layers.
- Label each conclusion as descriptive, attributed by a platform, or causal.
- Record missing data and unexpected implementation changes before drawing the
  final conclusion.

## When to add a controlled test

A controlled comparison becomes useful when there is a decision worth
isolating, such as whether one hook or call to action improves a defined
downstream outcome. Before running it:

1. define the treatment, outcome and comparison group;
2. check that the budget and expected event volume can produce a useful read;
3. keep non-focal delivery conditions as comparable as the platform allows;
4. pre-set the duration, decision rule and handling of in-flight changes; and
5. report uncertainty and contamination risks.

If these conditions cannot be met, use the campaign as a descriptive learning
cycle and do not present the result as proof that one creative caused the
difference.

## Practical outputs to preserve

At the end of the campaign, the case-study folder should contain:

- campaign brief and measurement map;
- data dictionary, naming convention and UTM register;
- creative register and asset archive;
- consent and privacy wording, without publishing personal records;
- dated raw exports and a change log;
- production and media cost ledger;
- reproducible preparation and analysis scripts;
- executive dashboard and technical appendix; and
- a short lessons log separating findings, limitations and next decisions.

## Confidence and review trigger

Confidence is high that this plan addresses the specific evidence losses found
in the retrospective because the case gaps align with current official
guidance on campaign structure, tagging, event collection and privacy.
Confidence is moderate on the exact primary outcome and reporting cadence,
because those depend on the release, available budget, destination platforms
and commercial objective.

The plan should be revised when a real campaign brief, budget, target market,
landing path and available platform access are known. Those details may justify
removing parts of the instrumentation or adding a controlled comparison.

## Sources

- https://www.facebook.com/business/help/AboutConversionsAPI
- https://www.facebook.com/help/messenger-app/621956575422138/
- https://support.google.com/analytics/answer/10917952?hl=en-uk
- https://support.google.com/analytics/answer/9267735?hl=en
- https://support.spotify.com/na-en/artists/article/audience-segments-on-spotify/
- https://support.spotify.com/us/artists/article/understanding-release-engagement/
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/direct-marketing-guidance/plan-direct-marketing/
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/how-do-we-comply-with-the-pecr-electronic-mail-marketing-rules/
- https://www.iab.com/wp-content/uploads/2025/11/IAB_and_IAB_Europe_Guidelines_Incremental_Measurement_Commerce_Media_November_2025.pdf
