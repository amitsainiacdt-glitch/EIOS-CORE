# ADR-019 — Issuer PDF and NSE iXBRL reconciliation bridge

Status: Approved and implemented for automatically bound NSE candidates.

## Decision

Before quarterly PDF extraction, EIOS reloads automatically bound NSE
corroborations from their complete three-file lineage: original candidate,
deterministic binding assessment and bound output. The binding is recalculated;
any changed or missing artifact fails closed.

For each issuer-PDF table, EIOS selects at most one exchange corroboration with
the same ticker, exact reporting-period end and standalone/consolidated basis.
That exact candidate is supplied to the existing unit/header and source-reading
reconciliation logic. No match results in no corroboration; multiple matches are
a conflict and stop that table's unattended processing.

## Authority and cadence

NSE corroboration remains provisional and cannot approve the issuer PDF or its
financial facts. The bridge becomes effective when the issuer PDF is processed
after the NSE candidate exists; a later retry/cycle may complete the pairing.
Governed META and human Fact approval remain downstream requirements.

