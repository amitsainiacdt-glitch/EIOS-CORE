# EIOS Pre-Inflection and Earliest Investable Point Architecture

Status: Approved architecture; implementation must proceed through governed checkpoints.

Permanent interpretation approved 2026-09-09: this is EIOS's causal-first, pre-operator path. It extends the existing architecture and does not establish a parallel engine. Reported financial recovery and widespread market recognition are post-EIP confirmation evidence, never mandatory prerequisites for identifying a possible EIP.

## 1. Objective

EIOS must detect credible changes in the causes of future earnings before those
changes become obvious in reported revenue, margins, profit, guidance, analyst
upgrades, or price breakouts.

The objective is not to predict exact market bottoms. It is to identify the
Earliest Investable Point (EIP): the first point at which independent causal
evidence makes a future business inflection credible while market recognition
and valuation still provide sufficient room for error and upside.

## 2. Architectural position

This capability extends the existing EIOS chain. It must not create a second
Observation, Evidence, Signal, Catalyst, Expectation Gap, Mispricing,
Opportunity, Committee, or portfolio architecture.

```text
Primary and secondary sources
        ↓
Existing Research Runtime
        ↓
Existing Observation + enriched document provenance
        ↓
Existing Evidence governance
        ↓
Temporal Evidence
        ↓
Sector/company causal leading-indicator interpretation
        ↓
Pre-Inflection assessment
        ↓
Evidence reliability + contradiction + kill tests
        ↓
Inflection-strength assessment
        ↓
Price Recognition Gate
        ↓
Existing Expectation Gap
        ↓
Earliest Investable Point state
        ↓
Existing Catalyst → Mispricing → Asymmetry → Opportunity chain
        ↓
Investment Committee
        ↓
Outcome Tracking → Learning Ledger → Signal Performance
```

Pre-Inflection is upstream intelligence. It is not an investment decision and
must never bypass the governed downstream chain.

## 3. Source coverage

The architecture must eventually support source-neutral adapters for:

- Exchange filings and announcements
- Regulators and government agencies
- Company investor relations and annual/quarterly disclosures
- Orders, tenders, awards, cancellations, and execution updates
- Industry associations and commodity/product data
- Competitor, supplier, customer, distributor, and channel commentary
- Credit, delinquency, collection, import/export, capacity, inventory, pricing,
  utilization, approval, and registration data
- Reputable news, research, and syndicated reporting
- Market price, volume, relative-performance, valuation, and consensus data

Connectors must feed the existing Research Runtime and Observation boundary.
They must not create Signals, Catalysts, or Opportunities directly.

Only confirmed public information may enter this pipeline. Confidential,
leaked, credential-gated, or unpublished price-sensitive information (UPSI)
must be rejected. Acquisition and extraction failures remain explicit coverage
gaps and must never be interpreted by Meta-Analysis as negative evidence.

## 4. Primary-source-ready provenance

Pre-Inflection quality depends on what EIOS knew, when it knew it, where it
came from, and whether apparently independent reports were actually copies of
one document.

The existing `ObservationProvenance` should be extended additively with:

- `published_at`: original publication time
- `filing_at`: formal filing or submission time
- `source_document_id`: stable source-native identifier
- `document_hash`: deterministic underlying-document identity
- `extraction_method`: descriptive acquisition method

All fields remain optional and source-neutral. Existing `retrieved_at`,
Observation timestamp, content fingerprint, document hash, and Observation
fingerprint retain distinct meanings.

Within-cycle deduplication may prefer strong supplied document identity when
available, while preserving current URL/content behavior otherwise. Cross-cycle
document reconciliation remains a later governed checkpoint.

## 5. Sector causal knowledge

Sector-specific indicator definitions are passive typed knowledge, not engine
logic and not UI rules. Each definition should describe:

- Indicator identity and sector applicability
- Economic variable represented
- Expected direction and lead time
- Causal link to revenue, margin, cash flow, or balance-sheet outcomes
- Applicable company archetypes
- Preferred primary and corroborating sources
- Independence groups to prevent double counting
- Expected persistence
- Known false-positive conditions
- Contradictions and kill tests
- Historical performance metadata when learning data exists

Examples include channel inventory in agrochemicals, product spreads and
feedstock costs in chemicals, tender/order activity in industrials, early DPD
migration for lenders, and imports/realizations/utilization for building
materials. These are configurable knowledge, not universal hardcoded rules.

Every Meta causal hypothesis must reference one or more enabled, versioned
indicator definitions from the causal-indicator registry. Unknown indicators
or indicators outside the assessment's sector scope fail the mandatory Meta
gate. The initial library covers tender-to-order conversion in industrials,
early credit stress for lenders, chemical spread recovery, and building
material utilization/realization breadth. This seed library is illustrative;
new sectors use the same validated contract rather than new engine logic.

## 6. Temporal Evidence

One observation is rarely sufficient. Temporal Evidence must reconstruct:

- First-known, published, filing, and retrieval times
- Direction and persistence across observations
- Acceleration, deceleration, stabilization, and reversal
- Independent confirmation versus syndication
- Sector confirmation versus company-specific confirmation
- Causal distance from earnings
- Evidence freshness and decay
- Contradictions and missing expected confirmation

Temporal calculations belong in engines. Typed models remain passive and the
repository layer owns persistence.

## 7. Meta-Analysis capability

The Meta-Analysis Engine is a mandatory read-only intelligence layer that looks across
companies, sectors, sources, and time without making investment decisions.

No reviewed Temporal Evidence may advance to Pre-Inflection assessment,
Catalyst interpretation, EIP classification, or Opportunity analysis without
an assessment bound to the exact Temporal Evidence and Observation
fingerprints. A missing or incomplete Meta assessment fails closed.

It should be able to detect:

- Several weak indicators forming one coherent causal chain
- Supplier/customer/competitor evidence that leads a target company
- Tender activity preceding orders and orders preceding execution/revenue
- Regulatory approvals, registrations, duties, shutdowns, or policy changes
  that alter future economics
- Inventory, pricing, spread, utilization, or credit trends that conflict with
  currently reported financial results
- Sector breadth: isolated company noise versus industry-wide change
- Cross-sector transmission, such as commodity cost changes benefiting one
  value-chain segment while hurting another
- Evidence that should have appeared but has not appeared
- Repeated narratives that trace back to one original document
- Emerging catalyst clusters not captured by a single observation

Meta-analysis produces governed candidate interpretations and research gaps.
It does not publish Signals or Opportunities automatically.

Every Meta assessment must explicitly document source independence,
contradictions, missing expected evidence, acquisition/extraction coverage
gaps, causal hypotheses, uncertainty, and its lack of investment-decision
authority. At least two genuine independence groups are required before the
mandatory gate can mark evidence ready for Pre-Inflection review. Insufficient,
contradicted, single-source, or high-contradiction cases remain held for
research. Confidential or UPSI inputs are prohibited.

Meta must also record syndication findings, cross-company/cross-sector
transmission findings, open research gaps, and one explicit result for every
kill test defined by each cited causal indicator. A triggered or unresolved
kill test holds the case; incomplete kill-test coverage blocks it. Meta binds
to deterministic indicator-preview fingerprints so changes to persistence,
independence assignments, relationships, or rationales invalidate stale
assessments.

Mandatory gate states are:

- `BLOCKED`: Meta is absent, incomplete, non-public, stale, or bound to the
  wrong evidence.
- `HOLD_FOR_RESEARCH`: Meta is complete but support, independence, causal
  coherence, or contradiction burden is not ready.
- `READY_FOR_PRE_INFLECTION`: Meta is complete, source-bound, independently
  supported, causally explicit, and within the permitted contradiction burden.

`READY_FOR_PRE_INFLECTION` is permission to perform the next governed review;
it is not a Signal, Catalyst, Opportunity, recommendation, or trade decision.

## 8. Bounded catalyst-research agents

Agents are controlled research roles operating through the existing context
and repository boundaries. They are not autonomous investors.

Recommended roles:

1. Primary Source Scout
   - Finds filings, orders, tenders, approvals, registrations, and official data.
2. Sector Causal Analyst
   - Maps new evidence to the relevant sector causal model.
3. Company Transmission Analyst
   - Explains how sector evidence may reach company revenue, margins, cash flow,
     balance sheet, or competitive position.
4. Contradiction and Kill-Test Agent
   - Searches specifically for disconfirming evidence and structural risks.
5. Independence and Syndication Auditor
   - Determines whether apparent confirmations are genuinely independent.
6. Catalyst Cluster Analyst
   - Groups governed Signals into candidate Catalyst mechanisms using the
     existing Catalyst architecture.
7. Price Recognition Analyst
   - Evaluates how much of the inferred fundamental change is already reflected.
8. Meta-Analysis Coordinator
   - Combines bounded outputs, identifies missing research, and proposes a
     governed pre-inflection assessment for human review.

Every agent output must preserve input fingerprints, source provenance,
assumptions, contradictions, uncertainty, and explicit non-authority. Agents
cannot write downstream ledgers except through their dedicated governed command.

## 9. Inflection-strength assessment

Until sufficient outcome history exists, EIOS must avoid fake probability
precision. Initial output should be ordinal and explainable:

- Weak
- Emerging
- Credible
- Strong

The assessment should expose separately:

- Independent indicator count and breadth
- Direction, magnitude, and persistence
- Source reliability
- Causal proximity to earnings
- Sector and company confirmation
- Contradiction burden
- Evidence gaps
- Confidence and uncertainty
- Expected 2–4 quarter horizon

Calibrated numerical probabilities may be introduced only after the Learning
Ledger establishes defensible historical performance.

## 10. Price Recognition Gate

Fundamental inflection strength and market recognition are independent axes.
The gate should evaluate:

- Price relative to pre-inflection levels
- 1/3/6/12-month and sector-relative performance
- 52-week position and abnormal volume
- Valuation rerating and remaining valuation gap
- Price reactions following identified evidence
- Analyst, consensus, media, and institutional recognition when available

Recognition states:

- Unrecognized
- Early Recognition
- Partially Recognized
- Fully Recognized / Potentially Too Late

A small price rise is not automatic rejection. The gate estimates how much of
the potential fundamental change is reflected, with evidence and uncertainty.

## 11. Earliest Investable Point states

- Stage 0 — Deterioration
- Stage 1 — Possible Bottoming
- Stage 2 — Pre-Inflection
- Stage 3 — Earliest Investable Point
- Stage 4 — Early Confirmation
- Stage 5 — Consensus Recovery / Potentially Too Late

Stage 3 cannot be triggered by one numeric threshold. It requires governed
evidence that independent causal indicators are sufficiently credible,
contradictions and kill tests are tolerable, balance-sheet/governance risks are
explicit, and recognition remains low enough to preserve asymmetry.

Stages 2–4 are research and Opportunity states, not automatic buy decisions.

## 12. False-positive protection

The architecture must distinguish temporary bounces from durable inflections.
Protection includes:

- Minimum independent-source and independence-group support
- Persistence and causal sequencing
- Explicit contradiction searches
- Structural deterioration and balance-sheet kill tests
- Management-claim corroboration
- Document syndication detection
- Historical comparison
- Expiry, decay, and reversal rules
- Human review at governed promotion boundaries

## 13. Required explanation

Every assessment must answer in plain language:

- What is changing?
- Why now?
- Which evidence leads earnings, and by how long?
- Is the evidence independent and persistent?
- What contradicts the thesis?
- Why has the market not fully priced it?
- What would confirm it?
- What would invalidate it?
- Why is the current stage appropriate?

## 14. Implementation sequence

Implementation should use small, backward-compatible checkpoints:

1. Primary-source-ready Observation provenance and document identity
2. Cross-cycle document reconciliation preview
3. Source-neutral acquisition and document-extraction boundary
4. Temporal Evidence typed foundation and repository
5. Sector causal-indicator knowledge contract
6. Temporal leading-indicator interpretation preview
7. Mandatory Meta-Analysis contract and fail-closed gate
8. Contradiction, independence, and kill-test governance
9. Pre-Inflection assessment and human review
10. Price Recognition Gate
11. EIP classification and human review
12. Integration with existing Catalyst/Mispricing/Asymmetry/Opportunity path
13. Outcome Tracking, Learning Ledger, and performance calibration

Each checkpoint must fail closed, preserve existing production data, remain
offline-testable, update `PROJECT_STATE.md`, and avoid downstream actions until
explicitly governed.

## 15. First implementation checkpoint

The first code checkpoint is limited to the existing Observation spine:

- Add optional document timing and identity fields to `ObservationProvenance`
- Preserve legacy loading and timezone semantics
- Allow `ExternalObservationAdapter` to accept supplied source-neutral metadata
- Extend within-cycle deduplication only when strong document identity is given
- Preserve existing URL/content behavior and cross-cycle semantics
- Add focused no-network tests using temporary files

It explicitly excludes connectors, scraping, PDF/OCR, new event taxonomies,
pre-inflection scoring, Price Recognition, EIP, alerts, UI, and portfolio logic.

The original first checkpoint above is complete and retained as implementation history. The next additive sequence is: structured five-link causal chain; change-regime classification; thesis-specific Price Recognition veto; governed Expectation Gap binding; normalized valuation scenarios; survivability veto; unified fingerprint-bound EIP decision packet; reader-facing classification; post-EIP Scale/Hold/Kill monitoring; anti-anchoring discovery controls; and auditable indicator-performance learning.

## 16. Agriculture-climate transmission extension

Agriculture conclusions must never be inferred from an all-India rainfall
headline alone. The existing causal-indicator and mandatory Meta architecture
must combine weather timing and dry-spell persistence with crop stage, soil
moisture, vegetation condition, sowing, irrigation, reservoirs, groundwater,
fertilizer timing and mix, crop switching, policy intervention, supply-chain
conditions, rural demand, and global fertilizer inputs.

Dependency-aware indicators fail closed when an asserted downstream mechanism
omits its configured prerequisites. In particular, rainfall-to-fertilizer
analysis requires the agricultural-drought composite, crop-stage stress,
irrigation shield, application timing, and nutrient-mix substitution. A food
price or processor-margin conclusion must retain satellite crop confirmation,
government buffer/trade intervention, and supply-chain amplification as
separate mechanisms and kill tests.

Company transmission requires public, dated exposure records for crops,
geographies, products, customer types, and irrigation dependence. Unknown or
undisclosed exposure remains explicit and cannot be replaced by an inferred
revenue percentage. This extension remains inside mandatory Meta and creates no
automatic Evidence, Signal, Catalyst, Opportunity, recommendation, or trade.
