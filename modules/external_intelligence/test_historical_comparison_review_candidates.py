"""No-network validation for historical comparison review candidates."""

import io
import json
from contextlib import redirect_stdout
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence import (
    historical_comparison_review_candidate_builder as candidate_builder,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)
from modules.external_intelligence import (
    test_historical_comparison_audit_reader_summary as audit_test,
)
from scripts.list_historical_comparison_review_candidates import (
    main as list_main,
)


HistoricalComparisonReviewCandidateBuilder = (
    candidate_builder.HistoricalComparisonReviewCandidateBuilder
)
write_records = audit_test.write_records


def validate_candidates(path: Path):
    before = path.read_bytes()
    records = HistoricalComparisonAuditReader(path).read_all()
    builder = HistoricalComparisonReviewCandidateBuilder()
    candidates = builder.build(records)

    assert len(candidates) == 1
    candidate = candidates[0]
    assert len(candidate.candidate_id) == 64
    assert candidate.status == HistoricalComparisonReviewStatus.PENDING
    assert candidate.reviewed is False
    assert candidate.current_observation.title == "Selected current"
    assert candidate.historical_observation.title == "Selected historical"
    assert builder.build(records)[0].candidate_id == candidate.candidate_id

    try:
        builder.build([records[0], records[0]])
        raise AssertionError("Duplicate candidate identity was accepted")
    except ValueError as exc:
        assert "duplicate" in str(exc).casefold()

    assert path.read_bytes() == before
    return candidate


def validate_review(candidate) -> None:
    service = HistoricalComparisonReviewService()
    reviewed_at = candidate.recorded_at + timedelta(minutes=5)

    for status in (
        HistoricalComparisonReviewStatus.REVIEWED,
        HistoricalComparisonReviewStatus.ACCEPTED,
        HistoricalComparisonReviewStatus.REJECTED,
        HistoricalComparisonReviewStatus.DEFERRED,
    ):
        reviewed = service.review(
            candidate,
            status=status,
            reviewer="Human Reviewer",
            reason="Explicit human disposition.",
            reviewed_at=reviewed_at,
        )
        assert reviewed.status == status
        assert reviewed.reviewed is True
        assert reviewed.reviewer == "Human Reviewer"
        assert candidate.status == HistoricalComparisonReviewStatus.PENDING

    accepted = service.review(
        candidate,
        status=HistoricalComparisonReviewStatus.ACCEPTED,
        reviewer="Human Reviewer",
        reason="Reviewed only; no Evidence conversion.",
        reviewed_at=reviewed_at,
    )
    try:
        service.review(
            accepted,
            status=HistoricalComparisonReviewStatus.REJECTED,
            reviewer="Second Reviewer",
            reason="Attempted second disposition.",
            reviewed_at=reviewed_at,
        )
        raise AssertionError("Already reviewed candidate was changed")
    except ValueError as exc:
        assert "already" in str(exc).casefold()

    try:
        service.review(
            candidate,
            status=HistoricalComparisonReviewStatus.ACCEPTED,
            reviewer="Human Reviewer",
            reason="Invalid early review.",
            reviewed_at=candidate.recorded_at - timedelta(seconds=1),
        )
        raise AssertionError("Review predating audit record was accepted")
    except ValueError as exc:
        assert "precede" in str(exc).casefold()


def validate_command(path: Path) -> None:
    before = path.read_bytes()
    output = io.StringIO()
    with redirect_stdout(output):
        result = list_main(["--path", str(path), "--json"])

    assert result == 0
    payload = json.loads(output.getvalue())
    assert payload["candidate_count"] == 1
    assert payload["candidates"][0]["status"] == "PENDING"
    assert payload["evidence_created"] is False
    assert payload["financial_interpretation_performed"] is False
    assert path.read_bytes() == before


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "historical.jsonl"
        write_records(path)
        candidate = validate_candidates(path)
        validate_review(candidate)
        validate_command(path)

    print(
        "HISTORICAL COMPARISON REVIEW CANDIDATES: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
