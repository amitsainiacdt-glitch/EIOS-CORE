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

## First integrated writer

The existing reviewed public factual Observation commit path is the first and
only connected writer. `PublicFactualControlledWriteAdapter` maps the already
validated and human-approved proposal to an event-shaped `FACT`. A rejected or
conflicted controlled write blocks Observation creation. The existing admission,
review, provenance, audit and novelty gates remain in force.

Controlled records and receipts are returned with the commit result and stored
in a dedicated append-only JSONL journal beside the existing public commit audit
ledger. Journal entries are sequence-checked and hash-chained; embedded receipt
and record fingerprints are verified during reload. Corruption, truncation or a
broken chain prevents the service from starting with untrusted state.

Existing Observation and audit persistence remain unchanged. Controlled-write
persistence is currently used only by the explicitly connected reviewed public
event and governed quarterly-financial paths.

## First quantitative financial writer

`GovernedQuarterlyFinancialRepository` now sends its fully reconciled,
human-approved core income statement through the same durable boundary before
materialization. Revenue, other income, total income and PAT remain one atomic
source-table Fact keyed by ticker, period end and accounting basis. This avoids
partial acceptance of a quarterly statement.

The existing governed company Fact, six financial checks, reporting-note
clearance, source hash/page binding and duplicate-candidate protection remain
mandatory. A controlled conflict prevents the governed quarterly record from
being written.
