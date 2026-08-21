"""No-network validation for candidate and decision reconciliation."""

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
from modules.external_intelligence.historical_comparison_review_reconciler import (
    HistoricalComparisonReviewReconciler,
)
from modules.external_intelligence.historical_comparison_review_service import (
    HistoricalComparisonReviewService,
)
from scripts.list_historical_comparison_review_candidates import main as list_main


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        ledger_path = root / "decisions.jsonl"
        audit_test.write_records(audit_path)
        candidate = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(audit_path).read_all()
        )[0]
        accepted = HistoricalComparisonReviewService().review(
            candidate,
            status=HistoricalComparisonReviewStatus.ACCEPTED,
            reviewer="Human Reviewer",
            reason="Explicit decision only.",
            reviewed_at=candidate.recorded_at + timedelta(minutes=5),
        )
        decision = HistoricalComparisonReviewDecisionLedger(
            ledger_path
        ).record(accepted)
        audit_before = audit_path.read_bytes()
        ledger_before = ledger_path.read_bytes()

        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            [candidate],
            [decision],
        )
        assert reconciled[0].status == HistoricalComparisonReviewStatus.ACCEPTED
        assert reconciled[0].reviewer == "Human Reviewer"
        assert candidate.status == HistoricalComparisonReviewStatus.PENDING

        unknown = replace(decision, candidate_id="0" * 64)
        try:
            HistoricalComparisonReviewReconciler().reconcile(
                [candidate],
                [unknown],
            )
            raise AssertionError("Unknown decision candidate was accepted")
        except ValueError as exc:
            assert "unknown" in str(exc).casefold()

        output = io.StringIO()
        with redirect_stdout(output):
            result = list_main(
                [
                    "--path",
                    str(audit_path),
                    "--ledger-path",
                    str(ledger_path),
                    "--json",
                ]
            )
        assert result == 0
        payload = json.loads(output.getvalue())
        assert payload["candidate_count"] == 1
        assert payload["pending_count"] == 0
        assert payload["decided_count"] == 1
        assert payload["candidates"][0]["status"] == "ACCEPTED"
        assert payload["candidates"][0]["reviewer"] == "Human Reviewer"
        assert payload["candidates"][0]["review_reason"] == (
            "Explicit decision only."
        )
        assert payload["evidence_created"] is False
        assert audit_path.read_bytes() == audit_before
        assert ledger_path.read_bytes() == ledger_before

    print(
        "HISTORICAL COMPARISON REVIEW RECONCILIATION: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
