"""Record one human assessment without creating Evidence."""

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
            "Record an explicit human Evidence assessment for one accepted "
            "historical comparison. No Evidence is created."
        )
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--review-ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--assessment-ledger-path")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument(
        "--direction",
        required=True,
        choices=HistoricalComparisonEvidenceAssessmentLedger.DIRECTIONS,
    )
    parser.add_argument("--strength", required=True, type=float)
    parser.add_argument("--confidence", required=True, type=float)
    parser.add_argument(
        "--independent-confirmation", required=True, type=int
    )
    parser.add_argument(
        "--primary-source",
        action=argparse.BooleanOptionalAction,
        required=True,
    )
    parser.add_argument(
        "--time-sensitive",
        action=argparse.BooleanOptionalAction,
        required=True,
    )
    parser.add_argument("--assessor", required=True)
    parser.add_argument("--rationale", required=True)
    parser.add_argument("--assessed-at", required=True)
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
        print(
            "Configuration error: audit, review, observation, and Evidence "
            "assessment ledger paths are required."
        )
        return 1
    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 4:
        print("Evidence assessment error: all configured paths must differ.")
        return 1

    source_names = ("audit", "review", "observation")
    source_before = {
        name: paths[name].read_bytes() if paths[name].is_file() else None
        for name in source_names
    }
    try:
        assessed_at = datetime.fromisoformat(args.assessed_at)
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(paths["audit"]).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates,
            HistoricalComparisonReviewDecisionLedger(paths["review"]).read_all(),
        )
        matches = [
            candidate
            for candidate in reconciled
            if candidate.candidate_id == args.candidate_id.casefold()
        ]
        if len(matches) != 1:
            raise ValueError("candidate ID was not found uniquely")
        if matches[0].status != HistoricalComparisonReviewStatus.ACCEPTED:
            raise ValueError("candidate must have ACCEPTED status")
        preview = HistoricalComparisonAcceptedObservationResolver().resolve(
            matches[0],
            ObservationPersistence(paths["observation"]).load(),
        )
        assessment = HistoricalComparisonEvidenceAssessmentLedger(
            paths["assessment"]
        ).record(
            preview,
            category=args.category,
            direction=args.direction,
            strength=args.strength,
            confidence=args.confidence,
            independent_confirmation=args.independent_confirmation,
            is_primary_source=args.primary_source,
            is_time_sensitive=args.time_sensitive,
            assessor=args.assessor,
            rationale=args.rationale,
            assessed_at=assessed_at,
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Evidence assessment error: {exc}")
        return 1

    for name in source_names:
        path = paths[name]
        if source_before[name] is not None and path.read_bytes() != source_before[name]:
            print(f"Evidence assessment error: {name} source file changed.")
            return 1

    print(f"Recorded candidate: {assessment.candidate_id}")
    print(f"Observation fingerprint: {assessment.observation_fingerprint}")
    print(f"Direction: {assessment.direction}")
    print("Evidence assessment metadata was recorded.")
    print("No Evidence was created.")
    print("No financial interpretation was performed by EIOS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
