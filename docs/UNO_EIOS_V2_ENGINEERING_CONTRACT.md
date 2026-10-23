# UNO EIOS — Alpha Discovery v2: Engineering Contract

Status: PROPOSED; implementation gated by completion of Release 3. This document does **not** indicate deployment or a live trading signal.

## Purpose
Replace the ineffective ratio-led candidate funnel with independently sourced, testable 2–4-quarter business inflection discovery, without changing the portfolio or auto-trading.

## Five required upgrades

### U1. Independent and dual-track discovery
Run two complementary scans across an explicitly logged NSE/BSE universe: **causal early inflection** (orders, tenders, commissioning, customer approvals, dispatches, utilization, policy, inventory and spreads) and **quality under distressed pricing** (normalized ROCE, earnings resilience, capital structure and deep drawdown). Do not seed screens from holdings, screenshots or previous watchlists. Deduplicate by NSE/BSE identifiers. Record coverage, exclusions, query provenance, time of capture and screening denominators. No claim of complete all-market coverage without actual census.

### U2. Price and valuation protection
For each shortlisted company record a timestamped, independently checked NSE/BSE price (or label 'stale quote'), diluted shares, market cap, debt and cash, normalized EBITDA/PAT, minority interest, other income, exceptional items, subsidies, acquisitions, related-party exposure, capitalized costs, working capital and estimated maintenance/growth capex. Compute bear/base/bull scenarios from explicit assumptions with downside at current price; never equate a fall from a peak with undervaluation. Evidence source and retrieval time required for every number.

### U3. Explainable imperfection
Cash-flow deficits, low utilization, leverage and margin compression are not automatic rejections. Require a causal bridge (why temporary; how it reverses; when; cash required; independent proof). Reject persistent unbilled-revenue accumulation without a verified billing/collections path, unfinanceable capex, recurring dilution without returns, or material governance breaches. Distinguish confirmed fact, management estimate and inference.

### U4. One strict research classification
Exactly one of ADD / WAIT / REJECT. ADD requires independently corroborated causal change, defensible normalized earnings, funded business plan, acceptable governance and asymmetric valuation **before** full market recognition. WAIT requires measurable upgrade and rejection triggers, responsible next evidence source and a review date. REJECT removes from active research unless a material new fact changes the thesis. No 'research ADD' based on good ratios alone. Folder actions (EIP, 10x) separate from classification and from capital deployment.

### U5. Performance audit
Append-only event ledger with company/ticker, discovery timestamp, price, sources, thesis version, contradictons, causal level, confidence calibration, baseline index/sector benchmark, expected trigger date, verdict and committee decision. At 3/6/12 months compute benchmark-adjusted returns, hit rate, false ADDs, missed names and whether the forecast causal event occurred. Preserve superseded decisions; never overwrite history.

## Daily pipeline and review
1. Capture universe and new, dated official or corroborated external leading evidence.
2. Deduplicate already-seen events and verify provenance.
3. Link event to financial drivers expected within 2–4 quarters, with explicit uncertainty.
4. Run early financial-risk and governance screen.
5. Validate current price and price recognition; model downside before costly deep dive.
6. Rank a small set for forensic research and deliver at most 1–2 high-quality actionable discoveries.
7. Apply ADD / WAIT / REJECT and record explicit no-discovery outcome if no candidate qualifies.
8. Proposed registry/cockpit modifications require investment committee review and express user approval.

## API/data contract (proposed)
Candidate: {ticker, exchange, sector, theme, discovery_date, source_ids, causal_event, event_date, causal_level, financial_bridge, forward_quarters, risks, contradictions, kill_tests, quote_value, quote_time, diluted_shares, normalizations, valuation_cases, recognition_state, classification, classification_reason, add_trigger, reject_trigger, next_review_date, eip_folder_action, ten_x_folder_action, committee_review_required, capital_deployment_state}.
capital_deployment_state MUST equal "NO NEW CAPITAL DEPLOYMENT" for research monitoring output.

## Acceptance tests before rollout
- Universe is independent of portfolios and old watchlists; coverage metrics are exposed.
- Stale/missing prices block price-based ADD.
- One-time profits and metal-price pass-through do not masquerade as organic acceleration.
- Two-year negative CFO alone does not force REJECT if a verifiable collectible-asset bridge exists.
- Weak orders-to-cash conversion and unbilled contract assets trigger explicit tests.
- Identical filings across feeds produce one event, not repeated alerts.
- Historical decisions and original sources remain retrievable.
- No research finding modifies a position, portfolio verdict or cockpit automatically.
- Every WAIT has date-stamped measurable catalysts; every ADD has valuation/downside proof.
- Backtests show false-positive and missed-winner counts, with survivorship and look-ahead bias checks.

## Release sequencing
Release 3 remains prerequisite per repository README. Following Release 3, implement and test the pipeline behind a feature flag; perform historical replay and shadow-run before any production cutover. Do not publish or deploy without explicit approval.
