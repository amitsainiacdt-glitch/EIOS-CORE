# FOX initial historical-event queue — NOT VALIDATED

This is a seed research queue, **not a backtest dataset**. Publication timestamps in the first three rows have been parsed from filenames as *unverified hints*. They are not established exchange publication times. Missing official adjusted OHLCV prices must not be guessed. All rows have `price_adjustments_verified=no` and therefore **zero rows are admissible** for investment-performance evaluation.

Verify the exact filing/publication time against the exchange; obtain corporate-action-adjusted NSE/BSE open/close series for at least 252 trading sessions *after* the earliest permissible entry; ensure the full signal set was public at the observation time; preserve the original no-lookahead filing archive; capture sector/beta benchmarks. Include failed/delisted firms, not just recent winners.

Input queue: `data/fox/initial_case_queue.csv`. Audit code: `modules/validation/fox_data_audit.py`.

**No calibrated hit rate is currently established. No live order authority. Capital deployment ₹0.**
