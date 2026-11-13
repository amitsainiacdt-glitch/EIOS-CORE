# FOX timestamp-safe historical validation (research only)

This module backtests **INVESTIGATE/NO NEW INFLECTION/REJECT** signals, not investment ADDs. It does not fetch data, place trades or assert predictive performance.

## Inputs

events.csv: `event_id,ticker,published_at_ist,source_url,action,evidence_cutoff_ist,sector,control_group`. Use exchange primary-source URL and UTC-offset-aware publication/evidence timestamps.

prices.csv and optional benchmarks.csv: `ticker,session,open,close,verified_adjusted`. Prices must reflect verified corporate-action-adjusted OHLCV from real exchange trading sessions; do NOT mark placeholders verified. Optional benchmark ticker NIFTY500.

## Usage

```bash
python -m unittest modules.validation.test_fox_backtest -v
python -m modules.validation.fox_backtest --events events.csv --prices prices.csv --benchmarks benchmarks.csv --as-of-session 2026-11-13 --output fox_report.json
```

## Honest limitations

- Conservative entry on first available trading session strictly after filing publication day; avoids same-session lookahead, including after-hours news.
- Horizons are 63/126/252 *trading sessions*. Unavailable future outcomes are **censored**, not losses.
- Round-trip cost default 40 bps; impact, tax, liquidity and price limit effects need separate modelling.
- Benchmarks compare only exactly aligned entry and exit sessions.
- Adjustment flags and URL syntax are checked; authenticity of sources, adjusted prices, report-time reliability and survivorship must be independently audited.
- Production deployment, complete historical data ingestion, 100+ representative cases, held-out testing and risk-adjusted ADD model remain outstanding.
- No trades, no capital deployment. Research capital = ₹0.
