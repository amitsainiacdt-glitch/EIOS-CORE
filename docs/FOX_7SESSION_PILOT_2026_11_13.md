# FOX 7-session NSE historical pilot — 2026-11-13

## Actual completed data import
- Official GitHub Actions collection run: https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43456119007 (SUCCESS).
- Seven sessions (2024-10-24, 25, 28, 29, 30, Nov 4, 5) retrieved directly from NSE UDiFF daily ZIP archives. No failed days.
- Source ZIP SHA256 stored individually in the GitHub Actions artifact manifest; artifact 14053608553.
- **140 raw ticker/date price observations, 20/20 pilot tickers**, with zero ISIN conflicts *within this seven-session period*. EQ: 19 names; BE: V2RETAIL.
- V2RETAIL historical 2024 BE ISIN: INE945H01013. Its current filed post-split ISIN: INE945H01021. No automatic cross-date continuity or backtest clearance is claimed.
- Selected example: V2 Retail raw close 2024-10-30 ₹1,104.85; indicative mechanically split-normalised value ₹110.485 on post-March-2026 share basis. This is NOT total shareholder return.
- V2 Retail 10:1 split effective for trading 2026-03-25 as NSE circular https://nsearchives.nseindia.com/content/circulars/CML73355.pdf; company record date 2026-03-26: https://nsearchives.nseindia.com/corporate/V2RETAIL_11032026163855_SE_Record_Date_Intimation.pdf. Thus **effective trading date and record date differ**. Historical-price adjustment is not complete without further corporate-action and dividend review.
- Prior Anup 1:1 April 2024 bonus confirmed by FY25 annual report https://nsearchives.nseindia.com/annual_reports/AR_27134_ANUP_2024_2025_A_28072025174227.pdf. Its event precedes October 2024 quotes; further actions must still be checked.

## Quality gates still blocked
These 140 are **raw** prices, not individually certified corporate-action-adjusted 63/126/252-session series. Exchange original filing times, contemporaneous inflection values, liquidity/BE settlement limits and full forward history are incomplete. Therefore **admissible historical ADD cases remain 0**, and no FOX predictive win rate can be claimed.

## Code/test status
- Multi-session importer updated for EQ and BE, saving trading series explicitly.
- BE-series regression case added, and literal-newline syntax fix committed.
- GitHub CI validation run https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43456053693 succeeded: **56 tests passed**, including the new V2RETAIL BE-series regression case (confirmed from job logs). 
- No production deployment and no trading authority. Capital deployment ₹0.
