# DOCUMENTATION_STANDARDS.md

# EIOS Documentation Standards

Version: 1.0

Status: Active

---

# Purpose

This document defines the standards governing all documentation within the Everest Investment Operating System (EIOS).

Its objectives are to:

- Maintain consistency.
- Prevent documentation drift.
- Preserve institutional knowledge.
- Ensure long-term maintainability.
- Synchronize documentation with implementation.

Documentation is considered a first-class component of the software.

No capability is complete until its documentation has been updated.

---

# Documentation Philosophy

Documentation exists to explain:

- Why something exists.
- What it does.
- How it works.
- How it should evolve.

Documentation must never become a historical archive of outdated ideas.

It must always represent the current architecture.

---

# Documentation Hierarchy

The repository is divided into five documentation layers.

## Layer 1

Repository Root

Purpose

Executive Dashboard

Contains

- README.md
- PROJECT_STATE.md
- ROADMAP.md
- CHANGELOG.md

Audience

Everyone

---

## Layer 2

constitution/

Purpose

Permanent institutional principles.

Changes

Rare.

Examples

- Constitution
- Engineering Laws
- Architecture Principles

---

## Layer 3

strategy/

Purpose

Long-term execution.

Examples

- Master Execution Plan
- Manhattan Project
- Success Metrics

---

## Layer 4

docs/

Purpose

Engineering documentation.

Contains

Architecture

Governance

Academies

Engines

Knowledge

Research

Validation

Models

Releases

---

## Layer 5

Source Code

Purpose

Implementation.

Documentation explains implementation.

Implementation must never replace documentation.

---

# Naming Convention

Use

UPPER_CASE.md

for institutional documents.

Example

PROJECT_STATE.md

ROADMAP.md

CHANGELOG.md

Use

Title_Case.md

only when documenting specific subjects.

---

# Document Structure

Every major document should follow this order.

1. Purpose

2. Scope

3. Definitions

4. Current State

5. Details

6. References

7. Revision History

---

# Update Policy

PROJECT_STATE.md

Every sprint

ROADMAP.md

Every release

CHANGELOG.md

Every release

DECISION_LOG.md

Whenever architecture changes

Architecture Documents

Only when architecture changes

Constitution

Only by deliberate institutional decision

---

# Documentation Ownership

Every document has one owner.

Every contributor may suggest changes.

Major documents require architectural review before modification.

---

# Cross Referencing

Do not duplicate information.

Instead reference the authoritative document.

Example

PROJECT_STATE.md references ROADMAP.md.

ROADMAP.md references EXECUTION_PLAN.md.

Architecture documents reference DECISION_LOG.md.

---

# Writing Style

Documentation should be

Clear

Objective

Precise

Maintainable

Avoid

Marketing language

Personal opinions

Temporary notes

Conversation history

---

# Engineering Rule

Documentation is part of the architecture.

Implementation is incomplete until documentation has been updated.

---

# Quality Checklist

Every major document should answer

Why?

What?

How?

Current Status?

Future Direction?

Dependencies?

Owner?

Last Updated?

---

# Institutional Principle

Documentation is the institutional memory of EIOS.

Software may evolve.

Programming languages may change.

Architecture may improve.

Documentation preserves understanding.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 04-Aug-2026 | Initial documentation standards established |