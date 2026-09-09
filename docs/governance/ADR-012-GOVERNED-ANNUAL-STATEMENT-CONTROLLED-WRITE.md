# ADR-012 — Governed annual statement controlled write

Status: Approved and implemented as a guarded materialization boundary.

## Decision

Balance-sheet and cash-flow extraction outputs remain non-evidence review
candidates. A complete statement may become a verified quantitative `FACT` only
after a named human approves the deterministic fingerprint of that exact
statement. The approval retains its identity, rationale, confidence and time.

Each company, period, reporting basis and statement type has a separate semantic
identity. All reported lines are written atomically as one source-table Fact,
with INR-crore units, source URL, document hash and source pages. A conflicting
version is preserved by the Controlled Intelligence Write Service and blocks the
annual governed record and trusted downstream reads.

## Safety boundary

Arithmetic reconciliation and META/AI review cannot grant approval. Mixed-source
figures, altered fingerprints, unsupported statement types, missing provenance,
non-finite values and synthetic approval-shaped dictionaries fail closed. The
record has no verdict or trading authority.

## Migration and current data

No existing Coromandel review JSON is migrated or promoted. Its balance-sheet
and cash-flow histories remain `PENDING_META_REVIEW` with `creates_evidence=false`
until exact human review records are deliberately supplied. The new repository
is additive and does not change current UI or EIP behavior.

