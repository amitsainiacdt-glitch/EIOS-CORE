# Pre-Inflection Discovery Gate — initial integration (19 October 2026)

Module: `modules/discovery/pre_inflection.py`
Tests: `modules/discovery/test_pre_inflection.py`

## Purpose
Evidence-first, all-sector research triage. Detect causal changes before reported
revenue, EBITDA or PAT confirms the inflection. Do not anchor discovery on holdings
or previously studied names.

## Inputs
Supply point-in-time source-linked events, cash-earnings bridge, expectation gap,
contradictions, kill tests and researched price recognition. Scores are
subjective research priorities (not calibrated success probabilities).

## Safeguards
- No future-published evidence is considered valid at an earlier assessment date.
- Independent corroboration is mandatory for EIP promotion.
- Missing economics or kill tests block promotion.
- Material re-rating triggers Too Late; a broken thesis triggers Reject.
- Explained temporary imperfections do not block EIP; weak permanent economics do.
- Research classification never triggers capital deployment.
- Empty scans explicitly report no fresh high-conviction opportunity.

## Boundaries
This module is deterministic and has no source ingestion, scheduled scanning,
live quotations, historical calibration, or dashboard integration. It leaves
the existing long-term discovery and 10x registries untouched.

Run locally: `python -m unittest modules.discovery.test_pre_inflection`

## Next integration
1. Connect the existing neutral-discovery queue to evidence-led candidate dossiers.
2. Feed official exchange filings through a licensed, resilient ingestion adapter
   with stable tickers/ISIN, event IDs, deduplication and source archiving.
3. Add company-specific quantified cash earnings bridge and price recognition history.
4. Backtest point-in-time classifications and monitor false positives.
5. Wire gated research output into separate EIP and 10x research views.

Never treat this initial module alone as production investment intelligence.
