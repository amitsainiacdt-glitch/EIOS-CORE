# ADR-004 — Immutable information classification

Status: Approved and implemented as passive contracts.

## Decision

Every controlled intelligence record has exactly one immutable class:
`FACT`, `DERIVED_METRIC`, `INFERENCE`, or `DECISION`. Operation-specific schemas
prevent one class from masquerading as another. Reclassification requires a new
record and an explicit prior-version relationship.

## Consequences

Facts require sources. Derived metrics require formulas and input record IDs.
Inferences require supporting records, mechanism, and uncertainty. Decisions
require an input packet fingerprint and reason codes.

