# FOX Corporate-Action Price History Engine (2026-11-13)

## What was implemented
- Research-only module `modules/validation/fox_corporate_actions.py`: `adjust_history(raw_bars, verified_events, review)`.
- Accepts NSE-origin ticker, 12-character ISIN, EQ or BE trading series, actual exchange trade-date sessions, raw open/close and source SHA256.
- Models split/bonus price factors across effective trading dates; handles historical-to-current share-base changes, checks unique dates, ISIN lineage and exceptional series transitions.
- **Fail closed** when source history is incomplete, event verification or required independent audit is missing, liquidity/BE settlement is unreviewed, or dividend/rights/demerger handling is unreviewed. Return `backtest_admissible=False` and list precise blockers. Adjusted numerical illustrations may be output with `verified_adjusted=False`, and MUST NOT be fed into FOX's historical-return reporting.
- Synthetic fixtures and regression tests: `modules/validation/test_fox_corporate_actions.py`.
- GitHub CI run [43457297699](https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43457297699): **68 tests PASS** (entire configured FOX suite, not full repository).

## Relationship to historical data
Raw observations from `modules/validation/fox_multiday_collect.py` map to `ObservedBar`. Contemporaneous actions require an independent exchange-source `CapitalEvent` with effective TRADE date, old/new ISIN, split or bonus factor and human-reviewed evidence. `ReviewAttestation` records time-window coverage and separate checks for actions, distributions, rights/demergers, ISIN/symbol, series/liquidity and original publication time.

**Caution:** the code only verifies schemas and internal consistency. A `reviewer_confirmed=True` flag or URL is not independent proof the underlying source is authentic or all actions have been found. This requires a genuine external audit before release for a performance backtest.

## Actual seven-session pilot assessment
The 2024-10-24 to 2024-11-05 NSE raw observations for twenty companies are genuine source data. They are **NOT yet a complete adjusted series**. The known V2RETAIL 2026-03-25 10:1 split (old ISIN INE945H01013, new INE945H01021) illustrates a factor of 0.1 for pre-split prices when normalising to post-split share count, but this is not necessarily a total-return calculation. Anup's April 2024 bonus predates the seven-session window; do not apply its factor AGAIN to October 2024 raw quotes. Additional actions, relevant dividends, rights and historical filings remain unverified.

**Historical cases admitted: 0.** No 63/126/252-session return series is yet complete; the 20-company list remains a data pilot, not an unbiased predictive validation.

## Remaining integration and data-quality work
1. Obtain 252+ continuous post-signal exchange sessions per company and contemporaneous filing timestamps.
2. Obtain/independently verify full corporate-action and distribution ledgers across each complete holding period.
3. Produce complete price-series audit report, with frozen source digests and explicit signoff.
4. Convert only `AuditResult.backtest_admissible=True` series to `fox_backtest.PriceBar`, with separate total-return and investable-execution policy.
5. Include delistings, failed recoveries, sector benchmarks, trading costs, non-trading dates and out-of-sample holdout.

No deployed EIOS API/dashboard connection or trading authority is implied. **Capital deployment ₹0.**
