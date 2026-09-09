# Controlled Intelligence Write Boundary

Status: Checkpoint 1 implemented as a non-production reference boundary.

## Purpose

The boundary classifies every proposed intelligence record as exactly one of
`FACT`, `DERIVED_METRIC`, `INFERENCE`, or `DECISION`. It supplies actor,
authority, command, lifecycle, receipt, and fingerprint contracts before any
existing production writer is integrated.

## Authority

`modules.master_dossier.MasterDossier` is the proposed canonical dossier. This
checkpoint does not migrate it or change either existing dossier implementation.

Machine-originated facts are always stored as `PROVISIONAL`. AI cannot verify a
fact or create a decision. A governed decision requires a decision orchestrator
with explicit decision authority.

## Contracts

The passive contracts live in `modules/intelligence_write/contracts.py`:

- `InformationClass`
- `ActorOrigin`, `ActorType`, `OriginType`, and `AuthorityScope`
- `SourceReference`
- `WriteCommand` and `WriteOperation`
- `ClassifiedInformationRecord`
- `ValidationStatus`
- `WriteReceipt` and `WriteReceiptStatus`

The validation lifecycle is `PROVISIONAL`, `PENDING_REVIEW`, `VERIFIED`,
`CONFLICTED`, `REJECTED`, `SUPERSEDED`, and `STALE`.

## Reference service

`ControlledIntelligenceWriteService` is deliberately in memory. It proves:

1. operation/class/authority validation;
2. provisional machine facts;
3. exact-revision verification and supersession;
4. semantic duplicate and conflict handling;
5. conflict exclusion from trusted reads;
6. immutable accepted and rejected receipts;
7. deterministic request, record, and receipt fingerprints.

It is not connected to the Master Dossier, Observations, Temporal Evidence,
EIP, UI, collectors, portfolio, trading, or any AI provider.

## Future integration boundary

The first eligible production integration is the existing reviewed public
factual Observation commit path. That work requires a separate review and must
preserve its current admission, review, provenance, audit, and novelty gates.

