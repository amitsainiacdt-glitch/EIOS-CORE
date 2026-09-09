# ADR-010 — Durable Controlled Write Journal

Status: Approved and implemented for the first controlled writer.

## Decision

Controlled write receipts, newly created classified records and lifecycle-status
snapshots are stored in one append-only JSONL journal. Every entry has a
contiguous sequence, the prior entry fingerprint and its own SHA-256 fingerprint.
Embedded record and receipt fingerprints are independently verified on reload.

## Failure policy

Malformed JSON, missing entries, reordered entries, broken hash chains, changed
receipts, changed records, unknown status references and duplicate record
identities fail closed during service initialization.

## Scope

The journal is used only by the reviewed public factual Observation writer. It
does not migrate existing ledgers or connect another writer, dossier, UI, AI,
EIP, portfolio or trading path.

