"""Explicitly create one EvidenceItem and append its conversion receipt."""

from __future__ import annotations

import argparse
import os
from datetime import datetime
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
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import (
    HistoricalComparisonEvidenceConversionReceiptLedger,
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
            "Explicitly materialize one assessed accepted comparison as an "
            "EvidenceItem. No Intelligence is published."
        )
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--review-ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--assessment-ledger-path")
    parser.add_argument("--receipt-path")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--converter", required=True)
    parser.add_argument("--converted-at", required=True)
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
        print("Configuration error: all five paths are required.")
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 5:
        print("Evidence materialization error: all configured paths must differ.")
        return 1
    source_names = ("audit", "review", "observation", "assessment")
    source_before = {
        name: paths[name].read_bytes() if paths[name].is_file() else None
        for name in source_names
    }

    try:
        converted_at = datetime.fromisoformat(args.converted_at)
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
        previews = tuple(
            resolver.resolve(candidate, observations) for candidate in accepted
        )
        assessments = HistoricalComparisonEvidenceAssessmentLedger(
            paths["assessment"]
        ).read_all()
        eligibility = HistoricalComparisonEvidenceConversionPreviewBuilder().build(
            previews, assessments
        )
        candidate_id = args.candidate_id.casefold()
        eligible = [
            item
            for item in eligibility.eligible_previews
            if item.candidate_id == candidate_id
        ]
        preview_matches = [
            item for item in previews if item.candidate_id == candidate_id
        ]
        assessment_matches = [
            item for item in assessments if item.candidate_id == candidate_id
        ]
        if len(eligible) != 1 or len(preview_matches) != 1 or len(assessment_matches) != 1:
            raise ValueError(
                "candidate is not uniquely eligible for Evidence conversion"
            )
        evidence, receipt = HistoricalComparisonEvidenceConversionReceiptLedger(
            paths["receipt"]
        ).materialize(
            preview_matches[0],
            assessment_matches[0],
            converter=args.converter,
            converted_at=converted_at,
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Evidence materialization error: {exc}")
        return 1

    for name in source_names:
        path = paths[name]
        if source_before[name] is not None and path.read_bytes() != source_before[name]:
            print(f"Evidence materialization error: {name} source file changed.")
            return 1

    print(f"Created EvidenceItem: {evidence.evidence_id}")
    print(f"Candidate: {receipt.candidate_id}")
    print(f"Direction: {evidence.direction}")
    print("Conversion receipt appended.")
    print("No Intelligence was published.")
    print("No Opportunity was scored.")
    print("No valuation or investment decision was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
