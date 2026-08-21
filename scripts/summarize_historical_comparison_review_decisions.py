"""Summarize reconciled historical comparison review decisions read-only."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_review_candidate_builder import (
    HistoricalComparisonReviewCandidateBuilder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_decision_summarizer import (
    HistoricalComparisonReviewDecisionSummarizer,
)
from modules.external_intelligence.historical_comparison_review_reconciler import (
    HistoricalComparisonReviewReconciler,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize explicit historical comparison review decisions. "
            "No source files are modified and no Evidence is created."
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
        "--ledger-path",
        help=(
            "Review ledger path. Defaults to "
            "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit stable machine-readable JSON.",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    audit_value = args.path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH", ""
    ).strip()
    ledger_value = args.ledger_path or os.environ.get(
        "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH", ""
    ).strip()
    if not audit_value or not ledger_value:
        print(
            "Configuration error: provide audit and ledger paths through "
            "--path/--ledger-path or their EIOS environment variables."
        )
        return 1

    audit_path = Path(audit_value)
    ledger_path = Path(ledger_value)
    if audit_path.resolve() == ledger_path.resolve():
        print("Review summary error: audit and ledger paths must differ.")
        return 1

    audit_before = audit_path.read_bytes() if audit_path.is_file() else None
    ledger_before = ledger_path.read_bytes() if ledger_path.is_file() else None
    try:
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates,
            HistoricalComparisonReviewDecisionLedger(ledger_path).read_all(),
        )
        summary = HistoricalComparisonReviewDecisionSummarizer().summarize(
            reconciled
        )
    except ValueError as exc:
        print(f"Review summary error: {exc}")
        return 1

    if audit_before is not None and audit_path.read_bytes() != audit_before:
        print("Review summary error: audit file changed during reading.")
        return 1
    if ledger_before is not None and ledger_path.read_bytes() != ledger_before:
        print("Review summary error: decision ledger changed during reading.")
        return 1

    if args.json:
        print(json.dumps(_payload(summary), sort_keys=True))
    else:
        _print_text(summary)
    return 0


def _payload(summary) -> dict:
    return {
        "schema_version": 1,
        "candidate_count": summary.candidate_count,
        "pending_count": summary.pending_count,
        "decided_count": summary.decided_count,
        "status_counts": {
            "REVIEWED": summary.reviewed_count,
            "ACCEPTED": summary.accepted_count,
            "REJECTED": summary.rejected_count,
            "DEFERRED": summary.deferred_count,
        },
        "by_entity": _count_payload(summary.by_entity),
        "by_category": _count_payload(summary.by_category),
        "by_comparison_type": _count_payload(summary.by_comparison_type),
        "by_reviewer": _count_payload(summary.by_reviewer),
        "by_review_date": _count_payload(summary.by_review_date),
        "unresolved_candidate_ids": list(summary.unresolved_candidate_ids),
        "earliest_reviewed_at": _time(summary.earliest_reviewed_at),
        "latest_reviewed_at": _time(summary.latest_reviewed_at),
        "source_files_modified": False,
        "evidence_created": False,
        "financial_interpretation_performed": False,
    }


def _count_payload(counts) -> list[dict]:
    return [{"label": item.label, "count": item.count} for item in counts]


def _time(value) -> str | None:
    return value.isoformat() if value is not None else None


def _print_text(summary) -> None:
    print("EIOS HISTORICAL COMPARISON REVIEW DECISION SUMMARY")
    print(f"Candidates: {summary.candidate_count}")
    print(f"Pending: {summary.pending_count}")
    print(f"Decided: {summary.decided_count}")
    print(f"Reviewed: {summary.reviewed_count}")
    print(f"Accepted: {summary.accepted_count}")
    print(f"Rejected: {summary.rejected_count}")
    print(f"Deferred: {summary.deferred_count}")
    for label, values in (
        ("Entities", summary.by_entity),
        ("Categories", summary.by_category),
        ("Comparison types", summary.by_comparison_type),
        ("Reviewers", summary.by_reviewer),
        ("Review dates", summary.by_review_date),
    ):
        print(f"{label}:")
        for item in values:
            print(f"  {item.label}: {item.count}")
    print(f"Unresolved candidate IDs: {len(summary.unresolved_candidate_ids)}")
    for candidate_id in summary.unresolved_candidate_ids:
        print(f"  {candidate_id}")
    print(f"Earliest review: {_time(summary.earliest_reviewed_at) or '-'}")
    print(f"Latest review: {_time(summary.latest_reviewed_at) or '-'}")
    print("No source files were modified.")
    print("No Evidence was created.")
    print("No financial interpretation was performed.")


if __name__ == "__main__":
    raise SystemExit(main())
