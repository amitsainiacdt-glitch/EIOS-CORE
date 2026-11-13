# FOX October 2024 raw NSE historical pilot — audited 2026-11-13

## Verified data collection
- Official exchange NSE UDiFF 21 explicitly selected trading sessions in October 2024 (1, 3–4, 7–11, 14–18, 21–25, 28–30). Excludes 2 October holiday and dates after 30 October.
- GitHub Actions collector run [43464283968](https://github.com/amitsainiacdt-glitch/EIOS-CORE/actions/runs/43464283968): **SUCCESS**.
- Artifact ID `14057841136`, temporary retention ~30 days; source ZIP archives with per-session SHA-256 and an archive+coverage manifest.
- External artifact digest: `sha256:7819abdb297354ff53ee781dd5ec6272889278a039e952bebec1708c99067121`.
- Downloaded archive manually inspected: `history_manifest.json` indicates `RAW_COMPLETE`, 21 source sessions, **420 raw ticker-session rows**, 20/20 pilot names, zero failed downloads. Every pilot name had prices for each selected date and no observed ISIN or BE/EQ series change *within these dates*.
- BE-series V2RETAIL preserved as BE (not misclassified as EQ).
- Raw October source data were not marked adjusted. No returns from synthetic observations.

## Verification limitations
- The October data are one month, **not** a continuous 63/126/252-session post-signal history.
- No research signal from 2023–24 has a fully validated exchange dissemination timestamp and contemporaneous FOX decision model.
- Exact corporate-action, distributions, demerger/rights, symbol lineage and execution/liquidity evidence across a full holding horizon remains unverified. One-month ISIN continuity is not proof of multi-year continuity.
- Sample is intentionally twenty familiar/diverse company slots (convenience sampling) rather than unbiased all-sector performance testing.
- Historical FOX prediction success and research ADD win rate: **not measurable (0 admissible cases)**.
- Archive artifacts are time-limited and require private durable provenance storage or documented lawful archival access before reproducible production backtesting.

## Implementation
- `modules/validation/fox_history_collect.py` collects raw dates in bounded batches, detects failed sources, records company coverage and refuses to infer missing sessions as market holidays.
- `modules/validation/fox_history_quality.py` independently audits gaps and series/ISIN changes; it never certifies a raw series as a backtest return.
- `modules/validation/fox_corporate_actions.py` requires explicit verified adjustments and external review.

Next: obtain a longer historical window, identify first qualifying point-in-time event and reconcile corporate actions plus total-return benchmark before scoring. **Capital deployment ₹0. No trades.**
