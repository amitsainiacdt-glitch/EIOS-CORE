# ARCHITECTURE DECISIONS

This document records major architectural decisions made during the development of EIOS.

Each decision includes:

- Context
- Decision
- Reason
- Consequences

---

## ADR-002 — Causal-first Pre-Operator detection extends the existing EIP path

Date: 2026-09-09

Status: Approved

### Context

Conventional research often waits for improving reported results, guidance, consensus or price momentum. That may identify a good business after informed market participants have already recognized the change. EIOS already contains Temporal Evidence, sector causal indicators, Mandatory Meta, contradiction and kill-test governance, Pre-Inflection assessment, Price Recognition, EIP classification and the downstream Opportunity architecture. A parallel architecture would duplicate these controls and create inconsistent authority.

### Decision

EIOS will search for public root-cause change and sector/company-specific causal leading indicators before requiring reported financial confirmation. The permanent order is causal evidence, independent corroboration, Pre-Inflection assessment, a hard Price Recognition review, governed Expectation Gap, normalized valuation, survivability and EIP review. Later revenue, EBITDA, PAT, guidance, analyst, consensus and price confirmation belongs after the potential EIP and may support Scale, Hold or Kill monitoring.

This capability will extend the existing Pre-Inflection/EIP and Opportunity modules through additive, fingerprint-bound contracts. It will not create a second Observation, Evidence, Signal, Catalyst, Opportunity, committee or portfolio architecture. Business quality, causal evidence, evidence quality, inflection strength, contradictions, Price Recognition, Expectation Gap, valuation, survivability, kill tests and final classification remain separate. Price recognition, serious contradictions and survivability may veto advancement.

Discovery must not favor current holdings or previously discussed companies. `No qualifying opportunity` remains a correct output. Learning remains prospective, auditable and non-self-modifying.

### Reason

This preserves early detection without weakening evidence quality, explainability, governance or compatibility with the existing investment process.

### Consequences

- Reported financial recovery and widespread recognition cannot be EIP prerequisites.
- The existing Price Recognition gate must be strengthened to compare recognition with the specific expected fundamental change.
- A governed Expectation Gap, normalized valuation scenario and survivability assessment must bind into EIP before implementation is considered complete.
- The system must add explicit causal-chain and change-regime contracts without one giant score.
- Existing repositories remain readable; new fields and contracts must be additive and versioned.
- Implementation proceeds through documented, offline-testable, fail-closed checkpoints.

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
