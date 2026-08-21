"""Preview Evidence conversion eligibility without creating Evidence."""

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
from modules.external_intelligence.historical_comparison_evidence_conversion_preview_builder import (
    HistoricalComparisonEvidenceConversionPreviewBuilder,
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
            "Preview exact would-be Evidence fields after accepted review and "
            "human assessment. No Evidence is created."
        )
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--review-ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--assessment-ledger-path")
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
    }
    if any(not value for value in values.values()):
        print("Configuration error: all four source paths are required.")
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 4:
        print("Evidence conversion preview error: all source paths must differ.")
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
            candidate
            for candidate in reconciled
            if candidate.status == HistoricalComparisonReviewStatus.ACCEPTED
        )
        observations = ObservationPersistence(paths["observation"]).load()
        resolver = HistoricalComparisonAcceptedObservationResolver()
        resolved = tuple(
            resolver.resolve(candidate, observations) for candidate in accepted
        )
        eligibility = HistoricalComparisonEvidenceConversionPreviewBuilder().build(
            resolved,
            HistoricalComparisonEvidenceAssessmentLedger(
                paths["assessment"]
            ).read_all(),
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Evidence conversion preview error: {exc}")
        return 1

    for name, path in paths.items():
        if before[name] is not None and path.read_bytes() != before[name]:
            print(f"Evidence conversion preview error: {name} file changed.")
            return 1

    payload = {
        "schema_version": 1,
        "review_candidate_count": len(reconciled),
        "accepted_count": eligibility.accepted_count,
        "eligible_count": eligibility.eligible_count,
        "missing_assessment_candidate_ids": list(
            eligibility.missing_assessment_candidate_ids
        ),
        "conversion_previews": [
            _payload(preview) for preview in eligibility.eligible_previews
        ],
        "source_files_modified": False,
        "evidence_created": False,
        "financial_interpretation_performed": False,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        _print_text(payload)
    return 0


def _payload(preview) -> dict:
    return {
        "candidate_id": preview.candidate_id,
        "observation_fingerprint": preview.observation_fingerprint,
        "proposed_evidence_id": preview.proposed_evidence_id,
        "would_be_evidence_fields": {
            "statement": preview.statement,
            "source": preview.source,
            "category": preview.category,
            "direction": preview.direction,
            "strength": preview.strength,
            "confidence": preview.confidence,
            "independent_confirmation": preview.independent_confirmation,
            "is_primary_source": preview.is_primary_source,
            "is_time_sensitive": preview.is_time_sensitive,
            "notes": preview.notes,
        },
        "lineage": {
            "entity": preview.entity,
            "observation_title": preview.observation_title,
            "observation_timestamp": preview.observation_timestamp.isoformat(),
            "reviewer": preview.reviewer,
            "reviewed_at": preview.reviewed_at.isoformat(),
            "assessor": preview.assessor,
            "assessed_at": preview.assessed_at.isoformat(),
        },
    }


def _print_text(payload) -> None:
    print("EIOS HISTORICAL COMPARISON EVIDENCE CONVERSION PREVIEW")
    print(f"Review candidates: {payload['review_candidate_count']}")
    print(f"Accepted: {payload['accepted_count']}")
    print(f"Eligible: {payload['eligible_count']}")
    print(
        "Missing assessments: "
        f"{len(payload['missing_assessment_candidate_ids'])}"
    )
    for candidate_id in payload["missing_assessment_candidate_ids"]:
        print(f"  {candidate_id}")
    for preview in payload["conversion_previews"]:
        fields = preview["would_be_evidence_fields"]
        print("---")
        print(f"Candidate ID: {preview['candidate_id']}")
        print(f"Proposed Evidence ID: {preview['proposed_evidence_id']}")
        print(f"Direction: {fields['direction']}")
        print(f"Strength: {fields['strength']}")
        print(f"Confidence: {fields['confidence']}")
    print("No source files were modified.")
    print("No Evidence was created.")
    print("No financial interpretation was performed.")


if __name__ == "__main__":
    raise SystemExit(main())
