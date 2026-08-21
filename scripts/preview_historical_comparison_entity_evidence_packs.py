"""Preview verified materialized EvidenceItems grouped by exact entity."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_resolver import (
    HistoricalComparisonAcceptedObservationResolver,
)
from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_evidence_assessment_ledger import (
    HistoricalComparisonEvidenceAssessmentLedger,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import (
    HistoricalComparisonEvidenceConversionReceiptLedger,
)
from modules.external_intelligence.historical_comparison_evidence_receipt_reconciler import (
    HistoricalComparisonEvidenceReceiptReconciler,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_candidate_builder import (
    HistoricalComparisonReviewCandidateBuilder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_reconciler import (
    HistoricalComparisonReviewReconciler,
)
from modules.observation.observation_persistence import ObservationPersistence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify materialization receipts and preview entity-scoped "
            "EvidenceItem collections without scoring."
        )
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--review-ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--assessment-ledger-path")
    parser.add_argument("--receipt-path")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    values = {
        "audit": args.audit_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH", ""
        ).strip(),
        "review": args.review_ledger_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH", ""
        ).strip(),
        "observation": args.observation_path or os.environ.get(
            "EIOS_OBSERVATION_PATH", ""
        ).strip(),
        "assessment": args.assessment_ledger_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_EVIDENCE_ASSESSMENT_LEDGER_PATH", ""
        ).strip(),
        "receipt": args.receipt_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_EVIDENCE_CONVERSION_RECEIPT_PATH", ""
        ).strip(),
    }
    if any(not value for value in values.values()):
        print("Configuration error: all five source paths are required.")
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 5:
        print("Entity Evidence pack preview error: all source paths must differ.")
        return 1
    before = {
        name: path.read_bytes() if path.is_file() else None
        for name, path in paths.items()
    }

    try:
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(paths["audit"]).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates,
            HistoricalComparisonReviewDecisionLedger(paths["review"]).read_all(),
        )
        accepted = tuple(
            item
            for item in reconciled
            if item.status == HistoricalComparisonReviewStatus.ACCEPTED
        )
        observations = ObservationPersistence(paths["observation"]).load()
        resolver = HistoricalComparisonAcceptedObservationResolver()
        previews = tuple(
            resolver.resolve(candidate, observations) for candidate in accepted
        )
        result = HistoricalComparisonEvidenceReceiptReconciler().reconcile(
            previews,
            HistoricalComparisonEvidenceAssessmentLedger(
                paths["assessment"]
            ).read_all(),
            HistoricalComparisonEvidenceConversionReceiptLedger(
                paths["receipt"]
            ).read_all(),
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Entity Evidence pack preview error: {exc}")
        return 1

    for name, path in paths.items():
        if before[name] is not None and path.read_bytes() != before[name]:
            print(f"Entity Evidence pack preview error: {name} file changed.")
            return 1

    payload = {
        "schema_version": 1,
        "accepted_count": result.accepted_count,
        "assessment_count": result.assessment_count,
        "receipt_count": result.receipt_count,
        "entity_pack_count": len(result.entity_packs),
        "entity_packs": [_pack_payload(pack) for pack in result.entity_packs],
        "source_files_modified": False,
        "new_evidence_created": False,
        "intelligence_published": False,
        "opportunity_scoring_performed": False,
        "financial_interpretation_performed": False,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        _print_text(payload)
    return 0


def _pack_payload(pack) -> dict:
    return {
        "entity": pack.entity,
        "materialized_count": pack.materialized_count,
        "supporting_evidence_ids": list(pack.supporting_evidence_ids),
        "contradictory_evidence_ids": list(pack.contradictory_evidence_ids),
        "missing_assessment_candidate_ids": list(
            pack.missing_assessment_candidate_ids
        ),
        "missing_receipt_candidate_ids": list(
            pack.missing_receipt_candidate_ids
        ),
        "receipts": [_receipt_payload(item) for item in pack.materialized_receipts],
    }


def _receipt_payload(item) -> dict:
    return {
        "candidate_id": item.candidate_id,
        "observation_fingerprint": item.observation_fingerprint,
        "evidence_id": item.evidence_id,
        "statement": item.statement,
        "source": item.source,
        "category": item.category,
        "direction": item.direction,
        "strength": item.strength,
        "confidence": item.confidence,
        "independent_confirmation": item.independent_confirmation,
        "is_primary_source": item.is_primary_source,
        "is_time_sensitive": item.is_time_sensitive,
        "notes": item.notes,
        "reviewer": item.reviewer,
        "reviewed_at": item.reviewed_at.isoformat(),
        "assessor": item.assessor,
        "assessed_at": item.assessed_at.isoformat(),
        "converter": item.converter,
        "converted_at": item.converted_at.isoformat(),
    }


def _print_text(payload) -> None:
    print("EIOS ENTITY-SCOPED MATERIALIZED EVIDENCE PACK PREVIEW")
    print(f"Accepted: {payload['accepted_count']}")
    print(f"Assessments: {payload['assessment_count']}")
    print(f"Receipts: {payload['receipt_count']}")
    for pack in payload["entity_packs"]:
        print("---")
        print(f"Entity: {pack['entity']}")
        print(f"Materialized: {pack['materialized_count']}")
        print(f"Supporting: {len(pack['supporting_evidence_ids'])}")
        print(f"Contradictory: {len(pack['contradictory_evidence_ids'])}")
        print(
            "Missing assessments: "
            f"{len(pack['missing_assessment_candidate_ids'])}"
        )
        print(
            "Missing receipts: "
            f"{len(pack['missing_receipt_candidate_ids'])}"
        )
    print("No source files were modified.")
    print("No new Evidence was created.")
    print("No Intelligence was published.")
    print("No Opportunity scoring was performed.")


if __name__ == "__main__":
    raise SystemExit(main())
