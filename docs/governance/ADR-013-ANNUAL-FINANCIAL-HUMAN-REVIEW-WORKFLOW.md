# ADR-013 — Annual financial human-review workflow

Status: Approved and implemented for annual statement review and display projection.

## Decision

Annual balance-sheet and cash-flow packs are converted into a deterministic,
period-by-period queue. Each item exposes its company, reporting basis, figure
count, source URL, document hash, pages and exact statement fingerprint. A human
may record `APPROVE`, `HOLD` or `REJECT`; no automatic process chooses a decision.

Decisions are append-only, unique per exact statement and protected by a receipt
fingerprint. Tampering, duplicate decisions, invalid confidence and changed
statements fail closed. Approval immediately invokes the governed annual
materialization boundary; Hold and Reject create no financial Fact.

## Reader projection

Receipt-bound governed annual records may fill otherwise missing presentation
cells and are labelled `VERIFIED_HUMAN_REVIEWED`. They take precedence over amber
pending-review candidates but never overwrite an existing financial-history
value. This projection does not mutate or expand the analysis engine's inputs.

## Limits

The workflow is a domain service, not yet an interactive UI screen. It does not
approve existing Coromandel records, connect AI, alter EIP authority, create a
verdict or authorize trading.

