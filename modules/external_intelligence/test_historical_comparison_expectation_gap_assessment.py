"""Offline validation for human Expectation Gap assessment decisions."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import HistoricalComparisonExpectationGapAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from modules.external_intelligence.test_historical_comparison_catalyst_creation import inputs


def build_preview(root):
    items, reviews, catalyst_kwargs, assessment = inputs(root)
    _, creation = HistoricalComparisonCatalystCreationLedger(root / "creations.jsonl").materialize(
        items, reviews, assessment, **catalyst_kwargs, creator="Catalyst Steward",
        rationale="Explicit materialization.", created_at=datetime(2026, 8, 22),
    )
    analysis_kwargs = dict(
        gap_id="GAP-001", company="Entity A", sector="Industrials",
        market_expectation=35, eios_expectation=70,
        market_earnings_expectation=40, eios_earnings_expectation=68,
        assumptions=["Demand persists."], invalidation_conditions=["Demand reverses."],
    )
    preview = HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
        items, reviews, assessment, creation, **catalyst_kwargs, **analysis_kwargs
    )
    return preview


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        preview = build_preview(root)
        sources = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        ledger = HistoricalComparisonExpectationGapAssessmentLedger(root / "gap-decisions.jsonl")
        with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", side_effect=AssertionError("Mispricing forbidden")):
            decision = ledger.record(
                preview, disposition="Approved", conditions=["Maintain corroboration"],
                monitoring_requirements=["Review quarterly"], reviewer="Gap Reviewer",
                rationale="The exact analysis supports a material gap.", reviewed_at=datetime(2026, 8, 22),
            )
        assert decision.analysis_fingerprint == preview.analysis_fingerprint
        assert ledger.read_all() == (decision,)
        assert all(path.read_bytes() == value for path, value in sources.items())
        try:
            ledger.record(preview, disposition="Deferred", reviewer="Other", rationale="Wait.", reviewed_at=datetime(2026, 8, 23))
        except ValueError as exc:
            assert "already exists" in str(exc)
        else:
            raise AssertionError("duplicate assessment accepted")

        weak = replace(preview, material_gap=False, positive_gap=False, negative_gap=False)
        try:
            HistoricalComparisonExpectationGapAssessmentLedger(root / "weak.jsonl").record(
                weak, disposition="Approved", reviewer="Reviewer", rationale="Invalid approval.", reviewed_at=datetime(2026, 8, 22)
            )
        except ValueError as exc:
            assert "non-material" in str(exc)
        else:
            raise AssertionError("non-material gap approval accepted")
        deferred = HistoricalComparisonExpectationGapAssessmentLedger(root / "deferred.jsonl").record(
            weak, disposition="Deferred", reviewer="Reviewer", rationale="More evidence required.", reviewed_at=datetime(2026, 8, 22)
        )
        assert deferred.disposition.value == "Deferred"
    print("HISTORICAL EXPECTATION GAP ASSESSMENT: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
