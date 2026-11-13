# FOX v4.8 — Research ADD underwriting and historical pilot (2026-11-13)

## Completed
- New standalone bounded-risk decision module `modules/decision/fox_add_engine.py`.
- Explicit classifications: EIP ADD / VALUE ADD / SPECIAL SITUATION ADD / WAIT / REJECT.
- Two leading signals, dated primary-source URL and price, conservative bear/base/bull diluted equity valuation, weighted expected value, 18% base annualised preference, 2:1 upside/downside preference, funding, cash conversion, governance, kill tests, fixed valuation-zone versions.
- Temporary bounded unresolved risks can produce a smaller **research-only** ADD provided their downside and falsifiable kill tests are documented.
- Price-only zone revisions blocked. Later dated fundamental changes require an evidenced version increment.
- `capital_deployment_rupees=0` is hard-coded in the decision output. Research allocation is not trade authorization.
- Regression tests: `modules/decision/test_fox_add_engine.py` (15 cases).
- Existing FOX GitHub Actions workflow expanded to include all validation and decision tests. **GitHub Actions run 43449580129 completed SUCCESS: 43 tests, OK**: https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43449580129

## Pilot20
- 20 ticker slots predeclared in `data/fox/pilot20_sampling_frame.csv` with a fixed 2023-01-01 through 2024-10-31 event-search interval.
- Protocol: `docs/FOX_PILOT20_PROTOCOL.md`. These are **company slots**, not verified events or successful signals.
- Current admissible cases: **0**. Historical 3/6/12-month return success rate: **not available**.
- The sample is deliberately labelled a convenience pilot, not an unbiased universe-wide backtest. No future-information cherry-picking and no silently replacing no-event cases.

## Open integration/quality gaps
1. Real historical NSE/BSE filing publication timestamps and adjusted bhavcopy price histories are missing; only admit audit-passed cases.
2. Admissibility flags require independent operator review and are not proof of authenticity on their own.
3. The new research evaluator is standalone and **not wired to /api/daily, website/dashboard, trading, or the morning workflow runtime**.
4. Run prospective blind calibration and separate market benchmarks, liquidity constraints, sector beta and downside false-positive analyses before judging investment predictiveness.
5. All examples in tests are synthetic; they do not constitute current recommendations.

**Capital deployment ₹0; no orders placed or authorised.**
