"""List human-review candidates with optional decision reconciliation."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence import (
    historical_comparison_review_candidate_builder as candidate_builder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_reconciler import (
    HistoricalComparisonReviewReconciler,
)


HistoricalComparisonReviewCandidateBuilder = (
    candidate_builder.HistoricalComparisonReviewCandidateBuilder
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "List explicit historical changes and review status. "
            "No decisions are persisted or published."
        )
    )
    parser.add_argument(
        "--path",
        help=(
            "Audit JSON Lines path. Defaults to "
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit stable machine-readable JSON.",
    )
    parser.add_argument(
        "--ledger-path",
        help=(
            "Optional review decision ledger. Defaults to "
            "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH."
        ),
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    path_value = (
        args.path
        or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH",
            "",
        ).strip()
    )

    if not path_value:
        print(
            "Configuration error: provide --path or set "
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH."
        )
        return 1

    path = Path(path_value)
    ledger_value = (
        args.ledger_path
        or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH",
            "",
        ).strip()
    )
    ledger_path = Path(ledger_value) if ledger_value else None
    if ledger_path is not None and path.resolve() == ledger_path.resolve():
        print("Review candidate error: audit and ledger paths must differ.")
        return 1
    before = path.read_bytes() if path.is_file() else None
    ledger_before = (
        ledger_path.read_bytes()
        if ledger_path is not None and ledger_path.is_file()
        else None
    )

    try:
        records = HistoricalComparisonAuditReader(path).read_all()
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            records
        )
        if ledger_path is not None:
            candidates = HistoricalComparisonReviewReconciler().reconcile(
                candidates,
                HistoricalComparisonReviewDecisionLedger(
                    ledger_path
                ).read_all(),
            )
    except ValueError as exc:
        print(f"Review candidate error: {exc}")
        return 1

    if before is not None and path.read_bytes() != before:
        print("Review candidate error: audit file changed during reading.")
        return 1
    if (
        ledger_before is not None
        and ledger_path.read_bytes() != ledger_before
    ):
        print("Review candidate error: decision ledger changed during reading.")
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "candidate_count": len(candidates),
                    "pending_count": sum(
                        not candidate.reviewed
                        for candidate in candidates
                    ),
                    "decided_count": sum(
                        candidate.reviewed
                        for candidate in candidates
                    ),
                    "candidates": [
                        _candidate_payload(candidate)
                        for candidate in candidates
                    ],
                    "evidence_created": False,
                    "financial_interpretation_performed": False,
                },
                sort_keys=True,
            )
        )
        return 0

    print("EIOS HISTORICAL COMPARISON REVIEW CANDIDATES")
    print(f"Candidates: {len(candidates)}")
    print(
        "Pending: "
        f"{sum(not candidate.reviewed for candidate in candidates)}"
    )
    print(
        "Decided: "
        f"{sum(candidate.reviewed for candidate in candidates)}"
    )
    for candidate in candidates:
        print("---")
        print(f"Candidate ID: {candidate.candidate_id}")
        print(f"Recorded at: {candidate.recorded_at.isoformat()}")
        print(f"Entity: {candidate.current_observation.entity}")
        print(f"Current: {candidate.current_observation.title}")
        print(f"Historical: {candidate.historical_observation.title}")
        print(f"Comparison type: {candidate.comparison_type.value}")
        print(f"Status: {candidate.status.value}")
    print("No Evidence was created.")
    print("No financial interpretation was performed.")
    return 0


def _candidate_payload(candidate) -> dict:
    return {
        "candidate_id": candidate.candidate_id,
        "recorded_at": candidate.recorded_at.isoformat(),
        "entity": candidate.current_observation.entity,
        "category": candidate.current_observation.category,
        "job_id": candidate.current_observation.job_id,
        "research_intent": (
            candidate.current_observation.research_intent
        ),
        "current_title": candidate.current_observation.title,
        "current_fingerprint": (
            candidate.current_observation.content_fingerprint
        ),
        "historical_title": candidate.historical_observation.title,
        "historical_fingerprint": (
            candidate.historical_observation.content_fingerprint
        ),
        "selection_basis": (
            candidate.selection_basis.value
            if candidate.selection_basis is not None
            else None
        ),
        "comparison_type": candidate.comparison_type.value,
        "change_direction": candidate.change_direction.value,
        "materiality": candidate.materiality.value,
        "delta": candidate.delta,
        "comparison_provenance": candidate.comparison_provenance,
        "status": candidate.status.value,
        "reviewer": candidate.reviewer,
        "reviewed_at": (
            candidate.reviewed_at.isoformat()
            if candidate.reviewed_at is not None
            else None
        ),
        "review_reason": candidate.review_reason,
    }


if __name__ == "__main__":
    raise SystemExit(main())
