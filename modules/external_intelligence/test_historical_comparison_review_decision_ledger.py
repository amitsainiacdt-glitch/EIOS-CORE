"""No-network validation for the explicit review decision ledger."""

import io
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
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)
from modules.external_intelligence import (
    test_historical_comparison_audit_reader_summary as audit_test,
)
from scripts.record_historical_comparison_review_decision import main as record_main


HistoricalComparisonReviewCandidateBuilder = (
    candidate_builder.HistoricalComparisonReviewCandidateBuilder
)
write_records = audit_test.write_records


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "historical.jsonl"
        ledger_path = root / "decisions.jsonl"
        write_records(audit_path)
        audit_before = audit_path.read_bytes()

        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        reviewed_at = candidate.recorded_at + timedelta(minutes=5)
        accepted = HistoricalComparisonReviewService().review(
            candidate,
            status=HistoricalComparisonReviewStatus.ACCEPTED,
            reviewer="Human Reviewer",
            reason="Explicit acceptance without Evidence conversion.",
            reviewed_at=reviewed_at,
        )
        ledger = HistoricalComparisonReviewDecisionLedger(ledger_path)
        decision = ledger.record(accepted)
        assert decision.candidate_id == candidate.candidate_id
        assert decision.status == HistoricalComparisonReviewStatus.ACCEPTED
        assert ledger.read_all() == (decision,)
        ledger_before = ledger_path.read_bytes()

        conflicting = HistoricalComparisonReviewService().review(
            candidate,
            status=HistoricalComparisonReviewStatus.REJECTED,
            reviewer="Second Reviewer",
            reason="Conflicting disposition must be rejected.",
            reviewed_at=reviewed_at,
        )
        try:
            ledger.record(conflicting)
            raise AssertionError("Conflicting decision was persisted")
        except ValueError as exc:
            assert "already exists" in str(exc).casefold()
        assert ledger_path.read_bytes() == ledger_before
        assert audit_path.read_bytes() == audit_before

        command_ledger = root / "command-decisions.jsonl"
        output = io.StringIO()
        with redirect_stdout(output):
            result = record_main(
                [
                    "--audit-path",
                    str(audit_path),
                    "--ledger-path",
                    str(command_ledger),
                    "--candidate-id",
                    candidate.candidate_id,
                    "--status",
                    "DEFERRED",
                    "--reviewer",
                    "Human Reviewer",
                    "--reason",
                    "Await more information.",
                    "--reviewed-at",
                    reviewed_at.isoformat(),
                ]
            )
        assert result == 0
        assert "No Evidence was created." in output.getvalue()
        stored = HistoricalComparisonReviewDecisionLedger(
            command_ledger
        ).read_all()
        assert stored[0].status == HistoricalComparisonReviewStatus.DEFERRED
        assert audit_path.read_bytes() == audit_before

    print(
        "HISTORICAL COMPARISON REVIEW DECISION LEDGER: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
