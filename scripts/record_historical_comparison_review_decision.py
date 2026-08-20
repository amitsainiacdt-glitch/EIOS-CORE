"""Explicitly record one human review decision without creating Evidence."""

import argparse
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence import (
    historical_comparison_review_candidate_builder as candidate_builder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)


HistoricalComparisonReviewCandidateBuilder = (
    candidate_builder.HistoricalComparisonReviewCandidateBuilder
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Record one explicit review decision. No Evidence is created."
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--ledger-path")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument(
        "--status",
        required=True,
        choices=[
            status.value
            for status in HistoricalComparisonReviewStatus
            if status != HistoricalComparisonReviewStatus.PENDING
        ],
    )
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--reviewed-at", required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    audit_value = args.audit_path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH",
        "",
    ).strip()
    ledger_value = args.ledger_path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH",
        "",
    ).strip()
    if not audit_value or not ledger_value:
        print("Configuration error: audit and review-ledger paths are required.")
        return 1

    audit_path = Path(audit_value)
    ledger_path = Path(ledger_value)
    if audit_path.resolve() == ledger_path.resolve():
        print("Configuration error: audit and review ledger must be separate.")
        return 1

    try:
        reviewed_at = datetime.fromisoformat(args.reviewed_at)
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )
        matches = [
            candidate
            for candidate in candidates
            if candidate.candidate_id == args.candidate_id
        ]
        if len(matches) != 1:
            raise ValueError("candidate ID was not found uniquely")
        reviewed = HistoricalComparisonReviewService().review(
            matches[0],
            status=HistoricalComparisonReviewStatus(args.status),
            reviewer=args.reviewer,
            reason=args.reason,
            reviewed_at=reviewed_at,
        )
        decision = HistoricalComparisonReviewDecisionLedger(
            ledger_path
        ).record(reviewed)
    except ValueError as exc:
        print(f"Review decision error: {exc}")
        return 1

    print(f"Recorded candidate: {decision.candidate_id}")
    print(f"Status: {decision.status.value}")
    print("No Evidence was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
