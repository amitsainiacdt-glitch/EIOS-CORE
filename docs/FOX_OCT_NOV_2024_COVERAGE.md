# FOX October–November 2024 Official NSE raw-history checkpoint

**Audit date:** 2026-11-13. **Status:** Raw data collected; research backtest NOT admissible.

## Collection provenance

- October archive run [43464283968](https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43464283968): 21 actual trading sessions, 420 raw ticker/session observations.
- November archive run [43473206092](https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43473206092): SUCCESS. 19 actual trading sessions, 380 raw ticker/session observations.
- November artifact ID `14061372894`, 30-day retention (expires approximately 2026-12-13), artifact SHA256 `853792348986f5b93da84bf72e2c293c26b0a8515a91b8218cb3ea00d6f3ca73`.
- October artifact ID `14057841136`; artifact SHA256 `7819abdb297354ff53ee781dd5ec6272889278a039e952bebec1708c99067121`.
- The combination was inspected from both original downloaded GitHub Actions artifact ZIPs; 800 unique (ticker, session) pairs, 40 unique exchange trading sessions, 20 pilot companies, zero duplicate records, zero missing ticker sessions, and no observed ticker-level ISIN/series transition **within these two months**.
- November includes Friday 2024-11-01 **Muhurat** trading session. NSE calendar official source: https://nsearchives.nseindia.com/content/circulars/CMTR59722.pdf.
- 2024-11-15 Guru Nanak Jayanti and 2024-11-20 Maharashtra election were closed equity sessions. NSE election circular: https://nsearchives.nseindia.com/content/circulars/CMTR64960.pdf.
- Both month manifests report `RAW_COMPLETE`. They are not proof of full corporate-action or trading-return adjustment.

## Interpretation and constraints

No historical FOX research ADD has been independently reconstructed from an original contemporaneous filing and a verified dated, diluted valuation. No 63/126/252-session post-entry investment histories have been adjudicated. The 40-session collection remains a **raw exchange-data pilot**, not a winner/loser backtest.

- Raw OHLC is NOT corporate-action-adjusted, total-return-adjusted or guaranteed tradeable at observed open (notably BE).
- Official archive retrieval and hash validation do not certify every dividend, bonus, split, rights, demerger or delisting.
- Must reconcile the full event window, original NSE announcement timestamp, first permissible trading session, costs, liquidity and benchmarks.
- Forty trading sessions is insufficient for the 63/126/252-session return horizons.
- Historical pilot is 20 predeclared convenience-selected company slots, not an unbiased random sample, and cannot support a population hit-rate claim.

**Current backtest-admissible events = 0. Capital deployment = ₹0. No trades.**

## Next acceptance milestones

1. Find the earliest eligible predeclared 2023–2024 event for each pilot company, strictly from evidence available at that time; retain NO EVENT where applicable.
2. Verify exact exchange dissemination timestamps (not inferred solely from filenames) and contemporaneous source contents.
3. Collect at least 252 actual subsequent exchange sessions per candidate and source-backed corporate-action/total-return evidence.
4. Require independently reviewed, point-in-time fully diluted valuation and scenario downside before assigning retrospective ADD.
5. Measure all outcomes including failures, out-of-sample controls, costs and missed opportunities. Do not report predictive skill in advance.

The combined CSV `FOX_Oct_Nov_2024_800_raw_prices.csv` is available as a generated conversation artifact; archive ZIPs are preserved temporarily as GitHub Actions artifacts. Persist long-term lawful copies separately if reproducibility is required.
