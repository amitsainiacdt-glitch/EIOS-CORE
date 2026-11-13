# FOX raw NSE multi-session validation — 2026-11-13

**Result: 3 official raw NSE sessions acquired, 57 matched pilot ticker/session rows, 19/20 distinct tickers matched, zero identifier conflicts. Not an adjusted-return backtest.**

- GitHub Actions collection: https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43452558495 — success.
- Collection artifact ID: 14052935388; named `fox-nse-multiday-pilot`; temporary artifact retention ~30 days.
- Trading sessions: 2024-10-28, 2024-10-29, 2024-10-30.
- Official NSE source URLs generated via `BhavCopy_NSE_CM_0_0_0_YYYYMMDD_F_0000.csv.zip`.
- ZIP SHA256 2024-10-28: `d7864c97d02bdbbcf25c7d33cdaa3bf1575808ebaa3d5b64a25b9cff05320c37`.
- ZIP SHA256 2024-10-29: `c3ad7971fc38c210c8dcbb26ee754b2ea894e1885d1db9ca07bdea9943e7ef7f`.
- ZIP SHA256 2024-10-30: `f77cb6942f893fdc2c7e91f071388106beeec278796da7829a9ab50422ff25ac`.
- All 19 matched tickers were present on all three dates (57 raw OHLC pairs) with the same ISIN across these dates. `V2RETAIL` missing; listing/symbol history remains unresolved.
- Example raw NSE EQ prices: ANUP close ₹2,740.55 (28 Oct), ₹3,148.85 (29 Oct), ₹3,110.60 (30 Oct); IRMENERGY ₹384.60, ₹385.00, ₹394.40 respectively.
- Explicit caveat: raw data have NOT been certified as adjusted for splits/bonus/rights; verify corporate-action history before computing long-horizon returns. A short three-session move is NOT a FOX historical investment outcome.
- Existing event timestamps remain unverified and no pilot company has a completed dated historical ADD decision. Backtest-admissible cases are **0**.
- New pipeline code: `modules/validation/fox_multiday_collect.py` and tests. GitHub CI rerun https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43452738009 passed following a synthetic fixture correction. Prior run 43452457169 failed one newly added fixture test; preserve failure in audit trail.
- Collection rejects unexpected archives, missing ISIN and missing sessions without inventing prices. No actual trade authorization is created.

Next: trace corporate actions and historical original filings for an older eligible event, collect 63/126/252 later sessions where available, then benchmark and test false positives. **Capital deployment ₹0.**
