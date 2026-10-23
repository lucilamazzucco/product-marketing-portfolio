# Revolut Crypto — Crypto-Curious Customer Journey

**Independent Product Marketing portfolio case study**  
**Market:** United Kingdom  
**Status:** Hypothesis-driven framework — not based on Revolut internal customer data  
**Prepared:** October 2026  
**Updated:** 23 October 2026 — observed in-app disclosure at discovery

## Strategic question

How might Revolut help eligible existing customers who show interest in crypto understand the product, its costs and risks, and decide whether it meets their needs?

## Working segment definition

**Crypto-Curious:** An existing Revolut customer with no recorded crypto purchase who has demonstrated recent interest through appropriate, observable product interactions. Segment membership must not be equated with suitability to invest or permission to receive promotional communications.

**Illustrative eligibility rules (to validate):**
- No completed crypto purchase on Revolut as of the observation date.
- One or more relevant interest signals within a rolling 30-day window.
- Only permissioned and appropriately processed behavioural data.
- Apply relevant product eligibility, compliance, consent, and financial-promotion rules before any marketing action.

## Customer journey map

| Stage | Customer question / job | Illustrative observable events (proposed tracking) | Potential friction | PMM opportunity | Measurement |
|---|---|---|---|---|---|
| 1. Discover | “What is crypto, and can I explore it here?” | `crypto_hub_viewed`, `crypto_info_opened`, `crypto_execution_notice_shown` (proposed) | **Observed in one account on 23 October 2026:** a lengthy notice comparing Revolut app and Revolut X appeared immediately on entering Crypto, before any trade was attempted. Impact on users remains untested. | Evaluate plain-language explanations and information hierarchy while preserving all mandatory disclosures | Correct comprehension of execution, fees and risks; qualitative clarity |
| 2. Explore | “What would I be buying, and what does it cost?” | `crypto_asset_detail_viewed`, `crypto_fee_info_viewed`, `crypto_risk_info_viewed` | Confusing jargon, unclear fees, perceived complexity | Clear asset and pricing explanations; non-promotional learning paths | Fee/risk information engagement and comprehension |
| 3. Learn | “Do I understand the risks well enough to decide?” | `crypto_learning_started`, `crypto_learning_completed`, `knowledge_check_completed` | Educational gaps, fear of losses | Balanced education; clarify that losses are possible and protection may differ | **Primary experimental KPI:** risk-and-fee comprehension uplift vs. control |
| 4. Decide | “Is crypto appropriate for me?” | `crypto_eligibility_flow_started`, `crypto_onboarding_completed`, `crypto_onboarding_abandoned` | Lack of confidence or regulatory requirements misunderstood | Explain required steps without coaching users to pass assessments | Understanding of onboarding requirements; complaints and support contacts |
| 5. Optional first use | “If I choose to proceed, is the experience clear?” | `crypto_order_previewed`, `crypto_order_completed` | Surprising costs or order details | Transparent previews and clear transaction summaries | Successful order experience among independently eligible users; issues/refunds/complaints |
| 6. Ongoing relationship | “Where can I review my holdings and learn more?” | `crypto_portfolio_viewed`, `crypto_price_alert_set`, `crypto_learning_revisited` | Low ongoing clarity, avoidable support requests | Neutral portfolio education and self-service support | Customer understanding, support contacts and satisfaction |

**Note:** Event names and tracking availability are hypothetical. They are not assertions about Revolut's internal systems.

## Observed product evidence — execution-model notice (23 October 2026)

**Evidence type:** First-hand screenshots and participant-reported sequence from one Revolut app session, supplied voluntarily by the portfolio author. **Observed trigger:** the notice appeared immediately upon opening the Crypto section, before selecting an asset or attempting a transaction. Exact geography/account eligibility, display frequency, device/app version, and whether the notice is legally mandatory at this point are not independently verified.

**Visible information:** the notice distinguishes Revolut app over-the-counter execution (Revolut as counterparty, proprietary quoted prices, retail fee structure) from Revolut X order-book execution (Revolut as facilitator, maker/taker fee structure, partial fills and slippage possible); it also describes limitations and risks.

**Research interpretation, not an established defect:** detailed and technical comparison at the discovery stage *may* make it harder for crypto-curious visitors to identify which details matter to them. Equally, the notice may improve transparency and informed decisions. Both outcomes should be tested, not assumed.

**Working research question:** Can a balanced plain-language orientation and clearer information hierarchy improve comprehension of both execution models, total costs and risk—without obscuring, replacing, delaying, or reducing required disclosures?

**Recommended validation:** 5–8 exploratory usability interviews across different familiarity levels, followed by a powered randomised comprehension experiment only if permitted by Legal/Compliance. Compare the current disclosure to an alternative with an explanatory overview *plus complete existing disclosure*. Include accessibility review. Do not optimise solely for dismissals, time-to-buy, or purchase conversion.

**Primary outcome:** percentage correctly answering pre-specified execution / fees / risk questions. **Guardrails:** no deterioration in understanding of losses, price uncertainty, or protections; complaint and support-contact trends. **Evidence limitation:** one observed screen is not evidence of prevalence or performance.

For the fuller analysis and draft alternative, see [`crypto-disclosure-ux-audit.md`](crypto-disclosure-ux-audit.md).

## Instrumentation proposal

For each event, an analytics team would define: canonical event name, timestamp, pseudonymous user ID, surface, country, app version, consent/eligibility flags, and event-specific properties. Avoid collecting sensitive data unnecessarily. Use aggregated reporting for public-facing case studies.

Example event specifications:

| Event | Trigger | Suggested properties |
|---|---|---|
| `crypto_hub_viewed` | Eligible customer opens the crypto hub | `entry_point`, `surface`, `country` |
| `crypto_fee_info_viewed` | Customer opens fee information | `asset_category`, `surface` |
| `crypto_learning_completed` | Customer completes a learning module | `module_id`, `completion_type` |
| `knowledge_check_completed` | Customer submits a neutral comprehension check | `module_id`, `score_band` (aggregate) |
| `crypto_onboarding_abandoned` | A defined onboarding session ends without completion | `stage`, `reason_if_volunteered` |

## Segment scoring: prototype, not production logic

A **Crypto Interest Score** may help prioritise research cohorts, but weights should be learned from evidence rather than assumed. A simpler, more explainable initial rule is:

- **Exploring:** at least one crypto hub or asset-information interaction in 30 days, no completed purchase.
- **Engaged explorer:** interactions on at least two distinct days, or an explicit learning/watchlist action, no completed purchase.
- **Onboarding explorer:** independently initiated onboarding, no completed purchase.

These cohorts can overlap; reporting should define whether a mutually exclusive hierarchy is required. Engagement signals do not indicate investment suitability.

## Illustrative experiment: Education-led discovery

**Research hypothesis:** Among eligible customers exploring Revolut Crypto, clearer and more balanced education improves understanding of risks, costs, and product mechanics compared with the current experience.

**Design:** Randomised control vs. alternative educational experience, subject to internal compliance/legal review, existing eligibility checks and accessibility standards. Do not bypass, shorten, or optimise around mandatory protections.

**Primary KPI:** Risk-and-fee comprehension uplift, defined as the difference in the percentage of evaluated participants who meet a pre-specified comprehension threshold between treatment and control.

**Secondary metrics:** Learning completion, fee-information engagement, customer-reported clarity, support-contact rate, optional onboarding completion among eligible users.

**Guardrails:** Complaint rate, misleading-impression reports, opt-outs, comprehension of loss risk, and negative customer outcomes. First-purchase conversion is diagnostic, **not** the sole success measure.

**Decision rule (proposed):** Advance only if the primary comprehension metric improves meaningfully and guardrails do not deteriorate. Exact minimum detectable effect, sample size and duration require baseline data.

## PMM decisions this research can support

1. Which user needs are under-served by the current explanatory and educational experience?
2. Which messaging resonates without minimising investment risk?
3. Which customer cohorts need further qualitative research before any campaign?
4. Which journey friction points belong to Product/UX rather than Marketing?
5. When, if ever, is Revolut X a relevant alternative for advanced user needs rather than a default next step?

## How this powers the future AI PMM Agent

**Inputs:** Approved public competitor pages, FCA research, product documentation, structured interview notes (with consent), and this journey framework.

**Workflow:** (1) Retrieve sources → (2) extract claims with URLs, dates, and geography → (3) map claims to journey stages → (4) flag evidence gaps and regulatory caveats → (5) draft prioritised PMM research questions and *hypothetical* experiments → (6) require human review before publication.

**Outputs:** Source-backed insight cards, segment-to-competitor comparisons, journey friction hypotheses, suggested research, experiment briefs, and explicit confidence/limitations.

**Do not claim:** Access to Revolut analytics, verified Revolut personas, actual experimentation outcomes, or a functioning autonomous agent until implemented and demonstrated.

## Next research questions

- How many Revolut UK customers enter each proposed exploratory cohort?
- What do existing customers understand about crypto costs and risk warnings?
- What makes people choose a finance app over Coinbase, eToro or Crypto.com?
- Which explanations improve comprehension without encouraging unsuitable investing?
- What role do trust, perceived simplicity and brand familiarity play, based on interviews rather than assumption?

---
*Independent educational case study; not affiliated with Revolut. Not investment advice.*
