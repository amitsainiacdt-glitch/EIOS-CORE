# ADR-020 — Delayed exchange reconciliation retry queue

Status: Approved and implemented in the automatic company cycle.

## Decision

An issuer quarterly PDF with no exact NSE corroboration is placed in an
append-only retry ledger. The request binds ticker, company, workspace-relative
archive path, PDF SHA-256 and official source URL. Scheduling is idempotent for
the same ticker, document and source.

When a newly staged, automatically bound NSE filing becomes available, EIOS
retries pending PDFs for that ticker immediately. The preserved PDF hash is
verified before execution and the bound NSE lineage is independently reverified.
The retry is marked `RECONCILED` only when the quarterly intake reports at least
one exact ticker/period/basis match. Otherwise it remains waiting or is held.

## Audit and limits

Every state transition is appended with attempt count, timestamp and receipt
fingerprint. Changed PDFs, path escape, tampered ledger entries and processing
failures fail closed. Retry completion means source reconciliation only; META and
human Fact approval remain mandatory.

