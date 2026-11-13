# FOX historical validation — predeclared 20-company pilot frame

**Created 2026-11-13. This is a 20-company sampling frame, NOT 20 verified historical events. Verified cases: 0.**

The 20 names were selected from existing FOX/BRAVO discussion and diverse industries as a **convenience pilot** to validate data ingestion and the research workflow. The sample is not random, is partly anchored to known companies, and therefore cannot be used to estimate universe-wide predictive accuracy. Some companies may have no eligible 2023–2024 event; they must remain missing, not be replaced after seeing outcomes.

## Protocol (freeze before data collection)
1. Within 2023-01-01 to 2024-10-31, find the **earliest qualifying company-specific exchange filing** for each ticker, per predefined FOX thresholds. If no filing qualifies, explicitly record `NO EVENT`. Do not cherry-pick the best later filing.
2. Record true exchange dissemination timestamp and evidence cutoff; if timestamp only inferred from a filename, keep unverified.
3. Cross-check the signal using only contemporaneously available independent filings. Preserve and report contradictory evidence and the initial computed FOX classification without viewing future price outcomes.
4. Independently certify split/bonus/rights adjustments, symbol and ISIN continuity, NSE/BSE source bhavcopy checksums, and relevant benchmark sessions.
5. Use the first *later* actual exchange trading session open, including special Sunday sessions. Net round-trip cost default 40 bps; report alternative costs and illiquid/price-limit cases.
6. Calculate 63/126/252 trading-session performance only where truly matured. Keep missing and censored records in denominator accounting; never treat censoring as zero return.
7. Compare false positives and misses using predeclared universe and relevant controls. Blind signal evaluation to future returns. Cluster overlapping events to avoid pretending each is independent.
8. Do not infer population win rate from this convenience sample. Advance to a much larger, unbiased frame that includes delistings and failed companies only after passing import QA.

**Important:** The names in the CSV are slots, not dated signals; no trading activity is authorised. Capital deployment = ₹0.
