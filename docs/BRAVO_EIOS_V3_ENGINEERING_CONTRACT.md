# BRAVO EIOS — Alpha Discovery v3: Audited Engineering Contract

**Status:** Proposed, version-controlled research/engineering specification. **Supersedes UNO EIOS v2 and EIOS Alpha**. BRAVO is the single active research-method name. Not deployed. Release 3 prerequisite remains in force according to the repository README.

## Mission and success criteria
Find 1–2 genuinely overlooked Indian listed-equity opportunities where independently observable causal events indicate a plausible cash-earnings/ROCE improvement within 2–4 quarters, while current **fully diluted** valuation creates favorable downside-adjusted asymmetry. A no-ADD result is valid; measure discovery quality, not number of picks.

## Audit findings corrected from UNO v2
1. **No point-in-time control:** backtests could use earnings revisions, share counts or filings unavailable on the discovery date. Add published_at, observed_at, effective_at and ingestion_at; immutable raw-source snapshots; prohibit information newer than the decision timestamp.
2. **No ownership attribution:** order books in SPVs/JVs, gross project values and acquisitions could be valued as 100% attributable profits. Normalize attributable share, cancellations, funding responsibility, stage and execution probability.
3. **No explicit data confidence threshold:** add evidence grades primary/independent corroborated/management-only/unverified and block research ADD on stale quotes, unverified dilution or material contradictory facts.
4. **Valuation could overstate future earnings:** handle cyclically high margins, subsidies, commodity pass-through, corporate restructurings, exceptional gains, treasury income, minority interests, options/warrants/convertibles and capitalized costs.
5. **Cash quality could be misclassified:** reconcile PAT -> CFO -> maintenance capex -> free cash flow, with billed/unbilled receivables, retention money, advances, milestone certification, subsidies and debt repayment schedule; test *why and when* temporary absorption reverses.
6. **Missing portfolio/cockpit safeguards:** append-only research events and explicit approval boundary; no trading instructions or automatic status changes from monitoring.
7. **No sector-neutral ranking:** compare industry-specific economics and working-capital patterns, separate structural changes from recoveries due to commodity prices or base effects.
8. **Unclear test of execution:** require fixture-based unit tests, historical replay, shadow-mode comparison against current system, fail-safe missing-data behavior and documented deployment checklist before considering production.

## Independent discovery: two simultaneous tracks
A. **Causal first:** commissionings, dispatches, customer approvals, new tenders/contracts, order-to-revenue conversion, pricing/spreads, supply constraints, inventory, trade data, regulatory change, credit availability, capacity retirement and operational turnarounds.
B. **Quality dislocation:** robust economics or credible temporary recoveries at depressed normalized valuation; include boring, cyclical, under-covered small/midcap sectors, not only fashionable themes.
Start from dated NSE/BSE active-list universe; record coverage by sector, liquidity, market cap, missing filings and known exclusions. Never seed from holdings, old research registry or screenshots. Deduplicate by ISIN and corporate-action lineage.

## Evidence hierarchy and audit trail
Primary: NSE/BSE issuer filings and audited reports; government/tender portals; regulator and rating-agency releases. Corroborate using customers, suppliers, commodity/trade statistics and reputable reporting. Screens and social media are discovery-only.
Each evidence item: {source_uri, issuer, captured_at, published_at, period_covered, primary_grade, raw_snapshot_hash, company_id, event_type, claim, contradictons, reviewer_notes}. New events should not resend unchanged old findings. Never say 'verified' when only snippets or management assertions exist.

## Financial bridge: required for ADD
- Specific causal event -> units/capacity/orders realized -> timing -> incremental revenue -> gross profit/EBITDA -> taxes/interest/depreciation -> **attributable diluted EPS** -> working capital and maintenance/growth capex -> sustainable incremental ROCE/FCF.
- Explicit probabilities, deadlines, funding sources and 2–4-quarter lead horizon.
- Model bear/base/bull **with probability-weighted and unweighted downside**, price recognition, balance sheet stress and competitor response. Scenario numbers are assumptions, not targets.
- Distinguish base earnings from peak-margin windfalls; use normalized earnings and enterprise value appropriately for leverage. Do not rely on a single P/E.
- Live/dated price: official exchange when available; independently reconfirm price at analysis time. Missing or stale price means **WAIT pending quote**, not ADD.

## Explainable imperfections
Weak margins, low utilization, negative CFO, capex debt and poor quarters can qualify if the cash/margin recovery bridge is independently supportable and valuation compensates. No blanket rejection for two negative CFO years. However, opaque unbilled receivables, weak collections with no funding path, undisclosed guarantees, repeat dilution without incremental returns or material governance failures block ADD.

## Strict classifications (research only)
- **ADD**: independent causal evidence AND plausible incremental attributable FCF/ROCE AND sustainable funding/governance AND sufficient current price asymmetry. A research ADD is inclusion in research folder, NEVER a purchase instruction.
- **WAIT**: concrete missing evidence with numeric/time-bounded upgrade and rejection triggers, responsible source, next review date.
- **REJECT**: structural failure, confirmed thesis break or poor reward/risk without a realistic measurable repair; remove from active priority until new material evidence.
Record reason, timestamp, previous classification, reviewer and overrides. If only an initial screen has been done, default WAIT (preliminary), never call it fully audited.

## Persisted registries
Keep EIP (timing) and 10x (long-duration structural) as separate axes. Folder action ADD/UPGRADE/DOWNGRADE/REMOVE/NO CHANGE never changes capital deployment. Use append-only event sourcing; retain conflicting evidence and prior verdicts. No automatic merge to cockpit.

## Monitoring and performance
Quarterly causal-event scorecard; 3/6/12 month realized returns vs Nifty 500 and sector benchmark, adjustment for splits/dividends/delistings, missed winners and false research ADDs. Use historical investable universe and point-in-time data; explicitly test survivorship, restatements and look-ahead bias. Distinguish signal accuracy, market timing and portfolio implementation.
Publish research-only outcomes even when zero candidates qualify; alerts only for genuinely new material information.

## Required safety/permission contract
`capital_deployment_state` is always **NO NEW CAPITAL DEPLOYMENT** in monitoring. Any change to allocation, previous verdict, position size, or deployed cockpit requires **committee review and user's explicit approval**. The code must not contain autonomous brokerage actions.

## Release plan and tests
Release 3 completion -> data/schema interfaces -> ingestion provenance -> causal mapping and normalized financial bridge -> valuations -> decision rules -> immutable ledger -> fixture-based tests -> historical replay -> shadow operation -> user review -> optional controlled deployment.
Before enabling production, assert:
- no old watchlist or holdings leakage into discovery input;
- exact quote time and diluted denominator;
- early record not contaminated by newer filings;
- metal-price pass-through and exceptional income cannot masquerade as organic unit growth;
- SPV/JV order attribution correct;
- receivable bridge can tolerate temporary cash absorption but demands collectability evidence;
- missing data blocks ADD;
- one filing = one new event despite multiple vendors;
- WAIT has triggers and date, REJECT has material restart condition;
- no automatic position, cockpit or capital changes.


## Remediation package R1–R5 — observed shortcomings (23 October 2026)
These controls are **mandatory acceptance criteria**, not claims that a scanning service currently exists.

### R1. Proactive causal discovery rather than backward-looking ratios
- Build dated sector-first event feeds for tenders awarded/cancelled, commissioning, dispatches, new customer approvals, government procurement, inventories, pricing spreads, rating triggers, export/import data and supplier/customer disclosures.
- Derive the candidate universe **from events**, then join to company identifiers; run an independent valuation-dislocation track separately. An opportunity discovered from an old watchlist must be marked 'portfolio-sourced' and cannot count toward the independent-discovery hit rate.
- For each causal signal record a 2–4-quarter time-to-P&L bridge and leading KPI; distinguish signed order from LOI, commissioned from commercially utilized, and installed capacity from delivered revenue.
- Test: synthetic dated commissioning event identifies an otherwise unscreened listed company; a press announcement without corroboration is flagged unverified.

### R2. Independent corroboration and contradictions
- A research ADD must have primary documentation AND independent corroboration for its key business inflection, or an explicit documented exception reviewed by a human committee.
- Triangulate customer, supplier, rating, regulator, industry and trade sources. Store negative and contradictory data with original evidence timestamp. Do not count two articles copying one company announcement as independent evidence.
- Test: duplicated syndicated media cannot raise evidence confidence; a subsequent order cancellation automatically opens a high-priority thesis review without silently changing the verdict.

### R3. Probability-weighted upside/downside and capital efficiency
- Require scenario drivers (volume, realizations, contribution margin, working-capital intensity, interest, tax, diluted shares), explicit probabilities adding to 100%, bear-case financing runway and per-share outcomes.
- Compare expected upside to probability-weighted downside and realistic failure/illiquidity loss; stress margins and multiple together under a market selloff. Show impact of all SPV/JV ownership and capital calls.
- Test: a high-ROCE low-P/E firm with poor downside-adjusted asymmetry is never auto-ADD; missing diluted share count or current quote blocks an ADD.

### R4. Temporary versus structural weakness adjudication
- For every adverse cash-flow, margin, leverage or utilization measure, require: mechanical driver, historical comparables, independently verifiable reversal catalyst, timing, funding need, threshold and thesis kill test.
- Report two separate outcomes: 'operating impairment' and 'temporary investment/working-capital absorption'. Do not reject purely on two years negative CFO; equally, do not assume every receivable is collectible.
- Test: healthy milestone receivables with customer-backed payment terms may remain eligible for ADD; undisputed aged unbilled revenue without a collectible milestone path blocks ADD.

### R5. Real outcome tracking and anti-self-congratulation
- Freeze each research call's company, timestamped price, methodology version, causal thesis, expected financial KPI, downside scenarios and benchmark before future information is available.
- At 3/6/12 months compute sector/Nifty 500-adjusted returns, forecast KPI attainment, hit rate, false ADD, missed-winner rate, and drawdown; include delisted names and adjust for corporate actions.
- Publish a quarterly calibration report including number screened, independently found, rejected, promoted and later falsified. No claims of superior performance without out-of-sample evidence.
- Test: evaluation cannot update the original verdict or read a filing dated after the decision; aggregate performance includes failures.

### Mandatory adversarial review (red team)
Before *every* proposed research ADD, construct the strongest plausible bear case and request evidence that could disprove the thesis. Require an independent contradiction review on competitive response, execution funding, promoter/governance, accounting, market recognition and hidden customer concentration. Log both bull and bear evidence, sign-off and next invalidation trigger. Research committee approval is needed for overrides; a machine-generated ADD does not affect deployed cockpits or portfolios.

### Implementation / release guardrails
Implementation should be staged after the repository's Release 3 prerequisite: event collectors -> provenance/normalization -> contradiction engine -> probabilistic bridge -> decision gates -> evaluation ledger -> shadow run. New collectors need licensing/rate-limit compliance and missing-data failure behavior. Live automation must not be claimed until connectors, scheduled ingestion, replay tests, and operational monitoring have actually passed acceptance.

**Capital Deployment State: NO NEW CAPITAL DEPLOYMENT**
