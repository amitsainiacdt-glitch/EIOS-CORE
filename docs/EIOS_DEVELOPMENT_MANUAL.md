# EIOS Development Manual
Version: 1.0
Status: Active
Owner: EIOS Engineering

---

# Purpose

This manual defines the permanent engineering process for developing the Everest Investment Operating System (EIOS).

It exists to ensure that every future module is built consistently, documented properly, and integrated without compromising architecture or quality.

This document governs how EIOS is developed.

---

# Core Development Philosophy

EIOS is not a stock screener.

EIOS is an institutional-grade Investment Operating System.

Every engineering decision must support:

- Evidence before opinion.
- Architecture before implementation.
- Long-term maintainability over short-term convenience.
- Explainability over black-box outputs.
- Modular design over tightly coupled code.
- One responsibility per module.
- One responsibility per Office.

---

# Development Lifecycle

Every sprint follows the same lifecycle.

## Phase 1 — Design

Before writing code:

- Review architecture.
- Challenge assumptions.
- Design interfaces.
- Review dependencies.
- Define responsibilities.
- Update blueprint if necessary.

No implementation begins until architecture is approved.

---

## Phase 2 — Implementation

Implementation rules:

- Build one subsystem at a time.
- Complete one capability before starting another.
- Never partially implement an Office.
- Prefer replacing complete files over fragmented patches.
- Avoid hardcoded company-specific logic.
- Reuse existing interfaces whenever possible.

---

## Phase 3 — Verification

Every sprint must successfully complete:

- Project builds successfully.
- python main.py executes without errors.
- New functionality verified.
- Existing functionality unaffected.
- Master Dossier updated correctly.

A sprint cannot proceed until verification succeeds.

---

## Phase 4 — Sprint Review

Before closing a sprint review:

- Was the objective achieved?
- Was architecture respected?
- Was technical debt introduced?
- Were better designs discovered?
- Are interfaces still clean?
- Is documentation affected?

Every lesson learned becomes part of project knowledge.

---

## Phase 5 — Sprint Closure

A sprint is complete only after:

✓ Code verified

✓ Architecture reviewed

✓ Documentation updated

✓ Project state updated

✓ Changelog updated

✓ Git commit completed

Only then may the next sprint begin.

---

# Sprint Closure Checklist

## Code

- All modules compile.
- Runtime verified.
- No integration failures.

---

## Architecture

Review:

- Architecture changes
- Design improvements
- Technical debt
- Dependency changes

---

## Documentation

Update when required:

PROJECT_STATE.md

CHANGELOG.md

ARCHITECTURE.md

ENGINEERING.md

PROJECT_BOOK.md

ROADMAP.md

---

## ADR Review

If a permanent architectural decision is made:

Create or update an Architecture Decision Record.

---

## Master Dossier Review

Confirm:

- Schema compatibility
- New outputs stored correctly
- Downstream compatibility

---

## Sprint Review

Record:

- Objective
- Deliverables
- Lessons Learned
- Technical Debt
- Risks
- Next Sprint

---

## Git

Commit only after Sprint Closure is complete.

---

# Engineering Principles

## Architecture First

Architecture precedes implementation.

Never solve architectural problems with code.

---

## Single Responsibility

Every Office has one responsibility.

Every module has one responsibility.

Every engine has one responsibility.

---

## Separation of Concerns

Research never performs valuation.

Valuation never makes investment decisions.

Decision Office never performs research.

Portfolio Office never performs valuation.

Monitoring Office never modifies evidence.

---

## Standard Interfaces

Every subsystem communicates through defined interfaces.

Examples:

Master Dossier

ValuationResult

DecisionResult

PortfolioResult

Never invent new interfaces unnecessarily.

---

## Extensibility

Every new module should plug into EIOS without requiring modification of existing modules.

Prefer extension over modification.

---

## Explainability

Every output must explain:

- Why?
- Based on what evidence?
- Under which assumptions?
- What could invalidate it?

No unexplained recommendation is acceptable.

---

# Documentation Policy

Documentation is maintained continuously.

Documentation is updated only after a sprint is complete.

Code and documentation must always remain synchronized.

---

# Architecture Decision Records (ADR)

Every permanent architectural decision must be documented.

Each ADR contains:

Decision

Reason

Alternatives Considered

Consequences

Status

---

# Coding Standards

Prefer:

- clear code
- readable code
- reusable code
- modular code

Avoid:

- duplicated logic
- hidden assumptions
- hardcoded values
- company-specific rules

---

# Repository Standards

Every release should improve:

Architecture

Documentation

Maintainability

Scalability

Explainability

Testing

Never sacrifice long-term quality for short-term speed.

---

# AI Collaboration Rules

The AI acts as:

- Software Architect
- Investment Systems Designer
- Code Reviewer
- Engineering Partner

The AI should:

Challenge assumptions.

Recommend better architecture.

Prevent technical debt.

Prefer scalable solutions.

Highlight risks before implementation.

Suggest documentation updates.

The AI should never blindly generate code if a better architectural solution exists.

---

# Definition of Done

A sprint is considered complete only when:

✓ Architecture approved

✓ Code implemented

✓ Integration verified

✓ Runtime tested

✓ Documentation updated

✓ Project state updated

✓ Changelog updated

✓ ADR updated (if required)

✓ Git commit completed

Until all conditions are satisfied, the sprint remains open.

---

# Permanent Engineering Principle

Build EIOS as if it will be maintained by an institutional engineering team for the next twenty years.

Every design decision should prioritize clarity, modularity, explainability, and long-term scalability over short-term convenience.