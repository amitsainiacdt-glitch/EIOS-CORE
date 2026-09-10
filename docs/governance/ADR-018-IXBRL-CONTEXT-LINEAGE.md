# ADR-018 — iXBRL context lineage for automatic period binding

Status: Approved and implemented in the NSE iXBRL parser.

## Decision

EIOS reads each numeric fact's `contextRef` and the corresponding XBRL context
period (`startDate`/`endDate` or `instant`). Explicit dimension members are used
to identify standalone or consolidated basis when present. Context sequences
must agree across every extracted financial metric before column contexts are
emitted.

Dates are normalized only for deterministic comparison, allowing standard ISO
XBRL dates to match the filing's displayed date format. Exactly one matching
period-and-basis context enables provisional automatic binding. Missing,
inconsistent or duplicated context lineage remains an exception for review.

## Authority

Context parsing proves column lineage, not financial truth. The bound output
remains provisional exchange corroboration and must still pass issuer-document
reconciliation, META validation and governed approval.

