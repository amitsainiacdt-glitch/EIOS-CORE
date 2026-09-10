# ADR-016 — Human binding of NSE iXBRL financial columns

Status: Approved and implemented as a review prerequisite.

## Decision

EIOS does not assume that the first numeric iXBRL column represents the current
quarter. Every staged NSE candidate produces a review document showing all
metric columns, filing identity, period metadata, source and candidate
fingerprint. A human must explicitly `SELECT` one zero-based column or record
`HOLD`/`REJECT` with reviewer identity, rationale and time.

The append-only decision is bound to the complete candidate fingerprint and has
its own receipt fingerprint. Duplicate decisions, tampering, changed candidates,
inconsistent metric-column counts and out-of-range selections fail closed.

## Result and authority

A valid selection produces a single-column exchange corroboration candidate for
the existing issuer-PDF quarterly review path. It remains non-approving and
cannot independently create a Fact, verdict, EIP, portfolio action or trade.

