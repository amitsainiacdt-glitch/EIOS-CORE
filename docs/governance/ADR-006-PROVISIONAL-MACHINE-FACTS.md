# ADR-006 — Provisional machine-originated facts

Status: Approved and enforced by the reference service.

## Decision

Facts proposed by extraction services, research jobs, or AI models are always
initially `PROVISIONAL`. Confidence and source naming cannot independently make
them trusted. AI cannot verify a fact, including one it proposed.

## Consequences

Fact verification requires an authorized actor, the exact prior record identity,
and its current fingerprint. Stale or self-verifying requests fail closed.

