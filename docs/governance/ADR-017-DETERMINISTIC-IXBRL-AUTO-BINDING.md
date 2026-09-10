# ADR-017 — Deterministic iXBRL automatic column binding

Status: Approved and implemented with exception-only human routing.

## Decision

EIOS automatically binds an NSE iXBRL numeric column when either the filing has
exactly one numeric column or exactly one explicit column context matches the
filing's declared period start, period end and reporting basis. The assessment is
fingerprint-bound and reproducible; a changed candidate invalidates it.

Automatic binding remains `PROVISIONAL`. It produces only an exchange
corroboration candidate for subsequent issuer-PDF reconciliation, META checks and
human Fact approval. It never verifies its own financial Fact.

Multiple matches, no match, absent multi-column context and context-count
mismatch route to human review. The existing manual column decision ledger is
therefore an exception path, not the default workflow.

## Operational visibility

The automatic company-cycle summary separately reports total iXBRL candidates,
automatically bound candidates, human-review exceptions and parsing holds. This
allows automation coverage and failure rates to be measured without overstating
trusted-data coverage.

