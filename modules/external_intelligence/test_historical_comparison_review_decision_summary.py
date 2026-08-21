"""No-network validation for read-only review decision summaries."""

import io
import json
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence import (
    test_historical_comparison_audit_reader_summary as audit_test,
)
from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
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
from modules.external_intelligence.historical_comparison_review_decision_summarizer import (
    HistoricalComparisonReviewDecisionSummarizer,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)
from scripts.summarize_historical_comparison_review_decisions import (
    main as summary_main,
)


def _review(candidate, status, reviewer, minutes):
    return HistoricalComparisonReviewService().review(
        candidate,
        status=status,
        reviewer=reviewer,
        reason="Explicit operational review decision.",
        reviewed_at=candidate.recorded_at + timedelta(minutes=minutes),
    )


def validate_summary(candidate) -> None:
    second_observation = replace(
        candidate.current_observation,
        entity="Beta Corp",
        category="accounting",
    )
    candidates = (
        candidate,
        _review(replace(candidate, candidate_id="1" * 64), HistoricalComparisonReviewStatus.ACCEPTED, "Reviewer A", 1),
        _review(replace(candidate, candidate_id="2" * 64, current_observation=second_observation), HistoricalComparisonReviewStatus.REJECTED, "Reviewer B", 2),
        _review(replace(candidate, candidate_id="3" * 64), HistoricalComparisonReviewStatus.DEFERRED, "Reviewer A", 3),
        _review(replace(candidate, candidate_id="4" * 64), HistoricalComparisonReviewStatus.REVIEWED, "Reviewer A", 4),
    )
    summary = HistoricalComparisonReviewDecisionSummarizer().summarize(candidates)
    assert summary.candidate_count == 5
    assert summary.pending_count == 1
    assert summary.decided_count == 4
    assert summary.accepted_count == 1
    assert summary.rejected_count == 1
    assert summary.deferred_count == 1
    assert summary.reviewed_count == 1
    assert summary.unresolved_candidate_ids == (candidate.candidate_id,)
    assert [(item.label, item.count) for item in summary.by_reviewer] == [
        ("Reviewer A", 3), ("Reviewer B", 1)
    ]
    assert sum(item.count for item in summary.by_entity) == 5
    assert sum(item.count for item in summary.by_review_date) == 4
    assert summary.earliest_reviewed_at == candidates[1].reviewed_at
    assert summary.latest_reviewed_at == candidates[4].reviewed_at

    try:
        HistoricalComparisonReviewDecisionSummarizer().summarize([candidate, candidate])
        raise AssertionError("Duplicate candidate identity was summarized")
    except ValueError as exc:
        assert "unique" in str(exc).casefold()

    try:
        HistoricalComparisonReviewDecisionSummarizer().summarize([
            replace(candidate, reviewer="Unexpected reviewer")
        ])
        raise AssertionError("Pending review metadata was accepted")
    except ValueError as exc:
        assert "pending" in str(exc).casefold()


def validate_command(audit_path: Path, ledger_path: Path) -> None:
    candidate = HistoricalComparisonReviewCandidateBuilder().build(
        HistoricalComparisonAuditReader(audit_path).read_all()
    )[0]
    accepted = _review(candidate, HistoricalComparisonReviewStatus.ACCEPTED, "Human Reviewer", 5)
    HistoricalComparisonReviewDecisionLedger(ledger_path).record(accepted)
    audit_before = audit_path.read_bytes()
    ledger_before = ledger_path.read_bytes()

    output = io.StringIO()
    with redirect_stdout(output):
        result = summary_main([
            "--path", str(audit_path), "--ledger-path", str(ledger_path), "--json"
        ])
    assert result == 0
    payload = json.loads(output.getvalue())
    assert payload["candidate_count"] == 1
    assert payload["pending_count"] == 0
    assert payload["decided_count"] == 1
    assert payload["status_counts"]["ACCEPTED"] == 1
    assert payload["by_reviewer"] == [{"label": "Human Reviewer", "count": 1}]
    assert payload["unresolved_candidate_ids"] == []
    assert payload["source_files_modified"] is False
    assert payload["evidence_created"] is False
    assert payload["financial_interpretation_performed"] is False
    assert audit_path.read_bytes() == audit_before
    assert ledger_path.read_bytes() == ledger_before

    error_output = io.StringIO()
    with redirect_stdout(error_output):
        error = summary_main(["--path", str(audit_path), "--ledger-path", str(audit_path)])
    assert error == 1
    assert "must differ" in error_output.getvalue()


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        ledger_path = root / "decisions.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        validate_summary(candidate)
        validate_command(audit_path, ledger_path)
    print("HISTORICAL REVIEW DECISION SUMMARY: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
