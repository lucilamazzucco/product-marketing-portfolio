# Revolut Crypto — Customer Research & Segmentation

**Independent PMM case study | UK | Working hypotheses, not Revolut internal data**

## Research question
How might Revolut help existing customers who show interest in crypto understand the product, risks and costs, and make an informed decision about whether to use it?

## Segment definition: Crypto-Curious
An existing Revolut customer who has **never completed a crypto purchase** and has demonstrated **recent, observable interest** in crypto. Interest is not the same as purchase intent, financial suitability or permission to market.

### Illustrative event signals (last 30 days)
| Signal | Example event | Illustrative weight |
|---|---|---:|
| Visits crypto section | `crypto_section_view` | 1 |
| Views an asset detail page | `crypto_asset_view` | 2 |
| Visits crypto on 3 distinct days | Derived from dated visits | 3 |
| Adds an asset to a watchlist | `crypto_watchlist_add` | 4 |
| Completes educational content | `crypto_education_complete` | 4 |
| Starts crypto onboarding | `crypto_onboarding_start` | 5 |

**Illustrative scoring:** 0–3 = early/no observed interest; 4–7 = moderate; 8+ = high. Weights and cutoffs must be validated using real data; deduplicate repeat events and cap frequency. Do not treat the score as an eligibility or suitability decision. No internal event schema is available for this case.

## Metrics: identification vs success

**Segment identification / sizing**
- **Crypto-Curious users (30d):** distinct existing customers with zero completed crypto purchases and interest score >= an empirically validated threshold.
- **Crypto-Curious rate:** Crypto-Curious users / eligible existing Revolut customers with observable events in the period.
- **Signal mix:** share of segment with educational engagement, repeat visits, watchlist activity, etc.

**Experiment outcome (education-led discovery)**
- **Primary KPI:** incremental completion rate of educational content *with demonstrated comprehension* among eligible users exposed to the experiment versus control.
- **Secondary:** voluntary product exploration, informed onboarding completion where appropriate, comprehension of costs and risk, satisfaction.
- **Guardrails:** complaints, opt-outs, misunderstanding of risk, inappropriate targeting, onboarding pressure, and regulatory compliance.
- **Longer-term diagnostic:** first crypto purchase rate among eligible users, observed but not optimised in isolation; purchases are not necessarily desirable for every customer.

## Initial hypotheses to test
1. Some customers are interested in crypto but uncertain about how it works and what it costs.
2. Clear, balanced educational journeys may improve understanding and confidence in deciding whether crypto is appropriate.
3. Existing Revolut familiarity could lower discovery friction relative to signing up for a separate exchange; this is not yet validated.

## Research plan
1. Review UK consumer research and official competitor product pages; log source URLs, dates and limitations.
2. Interview 6–10 potential users across no-interest, crypto-curious and casual-investor groups; recruit beyond current crypto enthusiasts.
3. Validate behavioral clusters, thresholds and consent/eligibility criteria with internal data **if available**.
4. Test messaging and education experiences with comprehension and safety measures, not transaction volume alone.

## Research limitations
This portfolio project has no access to Revolut customer records, internal analytics, eligibility data or experiment outcomes. Segment thresholds, event names and campaign concepts are illustrative. Crypto carries risk; marketing must comply with applicable UK rules and financial promotion requirements.

## Product ecosystem
Revolut Crypto in the main app is the primary case focus. Revolut X is considered as a separate, advanced-trading offering relevant to a different set of user needs, not a default next step for every customer.
