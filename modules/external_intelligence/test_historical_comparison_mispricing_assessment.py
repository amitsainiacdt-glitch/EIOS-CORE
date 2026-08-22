"""Offline validation for human governed Mispricing decisions."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_mispricing_assessment_ledger import HistoricalComparisonMispricingAssessmentLedger
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.external_intelligence.test_historical_comparison_expectation_gap_creation import setup
from modules.external_intelligence.test_historical_comparison_valuation_snapshot_ledger import valuation


def build(root):
    items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, kwargs = setup(root)
    _, gap_creation = HistoricalComparisonExpectationGapCreationLedger(root / "gap-creations.jsonl").materialize(
        items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, **kwargs,
        creator="Gap Steward", rationale="Explicit materialization.", created_at=datetime(2026, 8, 22, 11),
    )
    section = valuation()
    valuation_receipt = HistoricalComparisonValuationSnapshotLedger(root / "valuations.jsonl").record(
        section, entity="Entity A", recorder="Valuation Steward",
        rationale="Authoritative valuation captured.", recorded_at=datetime(2026, 8, 22, 12),
    )
    return HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
        items, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
        gap_creation, section, valuation_receipt, cmp=3500.0, **kwargs,
    )


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        preview = build(root)
        sources = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        ledger = HistoricalComparisonMispricingAssessmentLedger(root / "mispricing-decisions.jsonl")
        disposition = "Approved" if preview.potential_mispricing else "Deferred"
        decision = ledger.record(
            preview, disposition=disposition, conditions=["Valuation remains current"],
            monitoring_requirements=["Review quarterly"], reviewer="Mispricing Reviewer",
            rationale="Exact governed analysis reviewed.", reviewed_at=datetime(2026, 8, 22, 13),
        )
        assert decision.analysis_fingerprint == preview.analysis_fingerprint
        assert ledger.read_all() == (decision,)
        assert all(path.read_bytes() == value for path, value in sources.items())
        try:
            ledger.record(preview, disposition="Rejected", reviewer="Other", rationale="Duplicate.", reviewed_at=datetime(2026, 8, 23))
        except ValueError as exc:
            assert "already exists" in str(exc)
        else:
            raise AssertionError("duplicate decision accepted")
        weak = replace(preview, potential_mispricing=False)
        try:
            HistoricalComparisonMispricingAssessmentLedger(root / "weak.jsonl").record(
                weak, disposition="Approved", reviewer="Reviewer", rationale="Invalid approval.", reviewed_at=datetime(2026, 8, 22)
            )
        except ValueError as exc:
            assert "without potential" in str(exc)
        else:
            raise AssertionError("unsupported approval accepted")
        deferred = HistoricalComparisonMispricingAssessmentLedger(root / "deferred.jsonl").record(
            weak, disposition="Deferred", reviewer="Reviewer", rationale="More evidence required.", reviewed_at=datetime(2026, 8, 22)
        )
        assert deferred.disposition.value == "Deferred"
    print("HISTORICAL MISPRICING ASSESSMENT: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
