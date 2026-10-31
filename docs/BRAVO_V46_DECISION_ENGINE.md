# BRAVO EIOS v4.6 — experimental decision engine

This isolated module is a research prototype. It is not wired to the production EIOS pipeline, market data, trading, notifications, or the dashboard.

## Inputs and decisions
- Three dated, consistent-horizon bear/base/bull equity-value scenarios with probabilities summing to one.
- Current share price, independent causal evidence, diluted valuation reconciliation, funding credibility, governance and thesis-break gates.
- Evidence-gated ADD / WAIT / REJECT. ADD is **research only**; capital_authorized is always false.
- WAIT requires a concrete trigger and review date in operational use. The current function carries those fields but does not yet enforce their presence, so integration must validate them.
- REJECT can be reconsidered only on new material evidence. Caller is responsible for maintaining append-only history.

## Limitations
Expected terminal value annualisation is **not** an expected CAGR. Scenario probabilities are subjective until calibrated; dividend, dilution and liquidity effects must be embedded in scenario values. A three-point bear case does not bound tail loss. No live-market or historical backtest has been performed.

## Tests
Run from repository root: `python -m unittest discover -s tests -p 'test_bravo_v46.py'`.

## Before integration
Add source provenance, dated CMP and share-count validation, sector-specific modelling, tail-risk limits, WAIT expiry enforcement, audit logs, historical calibration and portfolio committee approval gates.
