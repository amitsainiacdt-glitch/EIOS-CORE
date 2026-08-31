# EIOS Pre-Inflection Live Research Runbook

## Purpose

This runbook covers the governed public-information path from an early external hint to a prospectively testable research hypothesis. It does not authorize investment decisions, positions, or trades.

## Current live case

Case: `INDIA-KHARIF-2026`

Current stage: `WEATHER_CROP_HINT_ONLY`

Current causal-interpretation confidence ceiling: `10% — ineligible`

What is verified:

- official rainfall period records;
- four-date Kharif crop-area progression;
- national and state/product fertilizer balance;
- comparable aggregate fertilizer consumption;
- pre-monsoon foodgrain buffer baseline;
- explicit contradiction and freshness controls.

What blocks sector transmission:

- no governed observed soil-moisture or crop-condition record;
- current reservoir storage is not verified and mapped to crop geography;
- current official output-price bytes were not captured;
- maize mandi arrival quantity and unit are not verified.

Company work is deliberately deferred until sector transmission is ready.

## Required analytical path

1. Acquire only an allowlisted public source and retain every success or failure receipt.
2. Bind extraction to the exact acquired document hash.
3. Validate the source-specific schema, units, identities, row counts, and reconciliations.
4. Keep structured facts review-only; do not create a production Observation automatically.
5. Test freshness, geographic scope, comparable periods, independence, contradictions, and kill tests.
6. Run Mandatory Meta and obtain an append-only human authorization.
7. Assemble sector, company, and catalyst readiness without treating one as another.
8. Calculate the evidence-confidence ceiling.
9. Freeze a hypothesis only through the authorized freezing service and append it to the hash-chained hypothesis ledger.
10. Resolve it once against a later authoritative public outcome, append the resolution, calibrate the complete declared cohort, and monitor calibration drift.

## Live refresh commands

Run from the repository root with Python UTF-8 output enabled on Windows.

```powershell
$env:PYTHONUTF8='1'
python -m scripts.assess_india_kharif_pre_inflection_readiness --output data/live_cases/india_kharif_2026/structured/india_kharif_2026_pre_inflection_readiness.json
python -m scripts.build_india_kharif_evidence_queue --output data/live_cases/india_kharif_2026/structured/india_kharif_2026_evidence_queue.json
```

These commands perform local deterministic assessment only. They do not authorize or initiate external acquisition.

## Core verification commands

```powershell
$env:PYTHONUTF8='1'
python -m modules.external_intelligence.test_pre_inflection_prospective_lifecycle
python -m modules.external_intelligence.test_mandatory_meta_analysis_gate
python -m modules.external_intelligence.test_public_source_schema_drift
python -m modules.external_intelligence.test_evidence_confidence_ceiling
python -m modules.external_intelligence.test_evidence_acquisition_queue
python -m modules.external_intelligence.test_pre_inflection_case_readiness
python -m modules.external_intelligence.test_pre_inflection_hypothesis_freezing_service
python -m modules.external_intelligence.test_pre_inflection_hypothesis_ledger
python -m modules.external_intelligence.test_pre_inflection_resolution_ledger
python -m modules.external_intelligence.test_pre_inflection_calibration
python -m modules.external_intelligence.test_pre_inflection_calibration_drift
```

Production Observation integrity:

```powershell
python -c "import json; assert len(json.load(open('data/observations.json',encoding='utf-8')))==46; print('PASS')"
```

## Human authority points

Human review is mandatory for:

- promotion of a factual proposal into a production Observation;
- Mandatory Meta authorization;
- Pre-Inflection review;
- formal hypothesis freezing;
- interpretation of a company exposure or catalyst;
- any later Opportunity, recommendation, position, or trade decision.

## Fail-closed rules

- Do not bypass login, API-key, signed-client, CAPTCHA, or protected-inspection boundaries.
- Do not copy indexed or displayed numbers into structured data without captured hash-bound source bytes.
- Do not infer physical supply from price alone or production loss from mandi arrivals alone.
- Do not infer company earnings from sector exposure, revenue share, order value, or an announcement alone.
- Do not call an event surprising or unpriced without a public expectation baseline.
- Do not freeze hint-only cases or confidence above the evidence ceiling.
- Do not remove failed hypotheses, inconclusive outcomes, or unsuccessful source attempts from their declared cohorts or ledgers.

## Principal live artifacts

- `data/live_cases/india_kharif_2026/acquisitions.jsonl`
- `data/live_cases/india_kharif_2026/extractions.jsonl`
- `data/live_cases/india_kharif_2026/structured/README.md`
- `data/live_cases/india_kharif_2026/structured/india_kharif_2026_pre_inflection_readiness.json`
- `data/live_cases/india_kharif_2026/structured/india_kharif_2026_evidence_queue.json`

## Current next evidence priority

Wait for an eligible sanctioned route. In information-value order, the unresolved needs are current crop-mapped reservoir storage, observed soil/crop condition, maize mandi price plus verified arrivals, and current official output prices. Issuer and catalyst research remains deferred.
