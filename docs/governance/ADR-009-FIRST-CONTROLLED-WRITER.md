# ADR-009 — First controlled production writer

Status: Approved and implemented for one path only.

## Decision

The human-approved public factual Observation commit service is the first and
only existing writer connected to the Controlled Intelligence Write Boundary.
It maps the exact reviewed proposal, review identity, source-document hash,
extraction identity, event time, statement posture and confidence to a verified
`FACT` command before the Observation is written.

## Preserved authority

Source admission, candidate validation, exact proposal reconstruction, human
approval, novelty protection, Observation provenance and the append-only public
commit audit remain authoritative. A controlled-write rejection blocks the
Observation and returns its immutable rejection receipt.

## Limits

Controlled records and receipts remain in memory at this checkpoint. No other
writer, dossier, UI, EIP, portfolio, collector, database or AI path is connected.
Durable controlled-record storage requires separate review.

