# ARCHITECTURE DECISIONS

This document records major architectural decisions made during the development of EIOS.

Each decision includes:

- Context
- Decision
- Reason
- Consequences

Every major architectural change must be recorded here.

---

## ADR-001

Title

Repository First Development

Decision

The repository shall always be treated as the implementation source of truth.

Reason

Prevents architectural drift and ensures reproducible development.

---

## ADR-002

Title

Constitution First

Decision

Major capabilities shall be documented in the Constitution before implementation begins.

Reason

Architecture must drive implementation rather than implementation driving architecture.