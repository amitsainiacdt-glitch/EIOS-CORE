# FOX first authenticated raw NSE price snapshot — 2024-10-30

- Execution date: 2026-11-13
- Runner: GitHub Actions run **43450286264** (SUCCESS): https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43450286264
- Archived artifact ID: **14048604579**, name `fox-nse-raw-` (input date default was 2024-10-30); 30-day retention.
- Official source URL: https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_20241030_F_0000.csv.zip
- Source ZIP SHA-256: `f77cb6942f893fdc2c7e91f071388106beeec278796da7829a9ab50422ff25ac`
- Validated schema and trade date: **2024-10-30**. Total **2,850** records; **1,911** EQ records.
- Pilot ticker raw price match: **19/20**; missing `V2RETAIL`, requiring separate symbol/listing timeline investigation.
- Confirmed raw examples (NOT split-adjusted): ANUP NSE EQ ISIN INE294Z01018 open ₹3,148.00 close ₹3,110.60; IRMENERGY ISIN INE07U701015 open ₹385.00 close ₹394.40.

## Crucial limitations

These are authenticated **raw** NSE daily prices (not independently adjusted for subsequent corporate actions). A single day is insufficient for any 63/126/252-session historical return. The publication timestamp of each company's relevant 2023–24 event is still unverified. Neither an original buy-zone nor an investment signal is established by the daily price snapshot.

**Backtest-ready events: 0. Do not calculate historical FOX hit rates from this result.** The raw ZIP is retained in GitHub Actions artifacts temporarily; keep its hash in the evidence ledger. The importer and artifact workflow are not connected to production.

## Next operations

1. Select each pilot's earliest eligible event in the frozen 2023-01-01 through 2024-10-31 interval using contemporaneously available sources.
2. Independently verify exchange dissemination timestamp and ISO date, including after-hours and special trading sessions.
3. Download requisite series of official daily bhavcopies and verify ISIN/symbol continuity, corporate actions, and benchmark prices.
4. Produce 63/126/252-session outcomes only with adequate history; include failed and delisted businesses and do not silently replace no-event cases.
5. Record signed-off data-quality evidence before setting `price_adjustments_verified=yes`.

Capital deployment ₹0; no trades.
