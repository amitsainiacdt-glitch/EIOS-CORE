# Structured IMD rainfall extracts

- `imd_rainfall_2026-08-30_daily.json` and `_v2.json` are superseded parser-development artifacts and must not be used.
- `imd_rainfall_2026-08-30_daily_v3.json` is the current correctly record-isolated daily extract.
- `imd_rainfall_2026-08-30_weekly.json` and `_v2.json` are superseded label-parser artifacts.
- `imd_rainfall_2026-08-30_weekly_v3.json` carries the active official label `Weekly (20-08-2026 To 26-08-2026)`, but its 40 area/value tuples are identical to the daily view. It is blocked by `PERIOD_VIEW_DATA_COLLISION` and cannot serve as independent corroboration.
- `imd_rainfall_2026-08-30_monthly.json` and `_v2.json` are superseded period-label artifacts.
- `imd_rainfall_2026-08-30_monthly_v3.json` is the current monthly extract for 1-30 August 2026.
- `imd_rainfall_2026-08-30_cumulative.json` is the current cumulative extract for 1 June-30 August 2026.

- `pib_kharif_area_2026-08-21_v1.json` is a superseded live parser artifact because PIB rendered its crop table twice; it must not be used.
- `pib_kharif_area_2026-07-17_label_v1.json`, `pib_kharif_area_2026-08-07_label_v1.json`, `pib_kharif_area_2026-08-14_label_v1.json`, and `pib_kharif_area_2026-08-21_label_v1.json` are superseded pre-alias artifacts and must not be used for time-series joins.
- The corresponding files without `_label_v1` are the current duplicate-suppressed, canonical-label structured crop-area extracts.
- Files ending `_schema_v1.json` are superseded because reports before 21 August contained an additional final-area column; they must not be used for normal-area comparisons.
- `pib_kharif_area_timeline_2026-07-17_to_2026-08-21_schema_v1.json` is the corresponding blocked pre-correction timeline and must not be used.
- `pib_kharif_area_timeline_2026-07-17_to_2026-08-21.json` is the current consistency-passing four-date crop-progress timeline.

- `pib_fertilizer_market_2026-07-19.json` is the current hash-bound all-India Kharif requirement, availability, DBT-sales, and closing-stock extract.
- `pib_fertilizer_market_interpretation_2026-07-19.json` is its review-only balance interpretation; it confirms national availability above requirement but holds sales momentum and company impact.
- `pib_fertilizer_sales_yoy_2026-07-14.json` is the current hash-bound corresponding-period aggregate consumption comparison.
- `pib_state_fertilizer_2026-07-29_scope_v1.json` is superseded because the All India row was not yet explicitly separated from state scope.
- `pib_state_fertilizer_2026-07-29.json` is the current scope-labelled state-by-product balance extract.
- `pib_state_fertilizer_analysis_2026-07-29.json` is the review-only geographic balance analysis; its requirement gaps are not retail-shortage claims.
- `pib_foodgrain_buffer_2026-05-28.json` is a verified pre-monsoon Central Pool buffer baseline; it is stale for current August stock claims.
- The Consumer Affairs daily food-price extractor is ready, but no structured price artifact exists yet because all three governed live acquisitions failed or timed out. Indexed/displayed values must not be copied into this folder without a hash-bound acquisition receipt.
- No AGMARKNET/India OGD mandi artifact exists yet. The current OGD catalog verifies a sanctioned daily price dataset but requires an issued API key, and accessible metadata did not verify arrival quantity plus unit. Price-only data must not be represented as physical-arrival evidence.
- `india_kharif_2026_pre_inflection_readiness.json` is the current review-only end-to-end snapshot. Its live stage is `WEATHER_CROP_HINT_ONLY`, and the current causal-interpretation confidence ceiling is 10% and ineligible; it is not a sector transmission, company thesis, Signal, Catalyst, Opportunity, recommendation, or trade.
- `india_kharif_2026_evidence_queue.json` is the bounded information-gain research queue. All current actions are waiting because of backoff, access requirements, or deliberate company-research deferral; it authorizes no automatic external action.
