# ADR-011 — Governed quarterly financial controlled write

Status: Approved and implemented for the governed quarterly materialization path.

## Decision

The fully validated and human-approved governed quarterly financial statement is
the second and only quantitative writer connected to the Controlled Intelligence
Write Boundary. Revenue, other income, total income and PAT are retained together
as one source-table `FACT`, with ticker, company, quarter, period start/end,
standalone/consolidated basis, INR-crore unit, source page, document hash,
governed-fact identity and human-review identity.

## Atomic scope

The reconciled core statement is one Fact rather than four independent writes.
This prevents a partial controlled state if one line conflicts. A differing
statement for the same company, period and basis is preserved as a conflict and
blocks governed quarterly materialization.

## Limits

Staged candidates, incomplete reporting-note review and failed six-check
assessments never reach the controlled boundary. No annual, balance-sheet,
cash-flow, derived-metric, AI, UI, EIP, portfolio or trading writer is connected.

