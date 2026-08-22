"""Offline validation for explicit governed Expectation Gap creation."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import HistoricalComparisonExpectationGapAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.test_historical_comparison_catalyst_creation import inputs


def setup(root):
    items, reviews, catalyst_kwargs, catalyst_assessment = inputs(root)
    _, catalyst_creation = HistoricalComparisonCatalystCreationLedger(root / "catalyst-creations.jsonl").materialize(
        items, reviews, catalyst_assessment, **catalyst_kwargs, creator="Catalyst Steward",
        rationale="Explicit materialization.", created_at=datetime(2026, 8, 22, 9),
    )
    gap_kwargs = dict(gap_id="GAP-001", company="Entity A", sector="Industrials", market_expectation=35, eios_expectation=70, market_earnings_expectation=40, eios_earnings_expectation=68, assumptions=["Demand persists."], invalidation_conditions=["Demand reverses."])
    preview = HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(items, reviews, catalyst_assessment, catalyst_creation, **catalyst_kwargs, **gap_kwargs)
    assessment = HistoricalComparisonExpectationGapAssessmentLedger(root / "gap-assessments.jsonl").record(preview, disposition="Approved", reviewer="Gap Reviewer", rationale="Material gap approved.", reviewed_at=datetime(2026, 8, 22, 10))
    return items, reviews, catalyst_assessment, catalyst_creation, assessment, {**catalyst_kwargs, **gap_kwargs}


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        items, reviews, catalyst_assessment, catalyst_creation, assessment, kwargs = setup(root)
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        ledger = HistoricalComparisonExpectationGapCreationLedger(root / "gap-creations.jsonl")
        gap, receipt = ledger.materialize(items, reviews, catalyst_assessment, catalyst_creation, assessment, **kwargs, creator="Gap Steward", rationale="Explicit approved materialization.", created_at=datetime(2026, 8, 22, 11))
        assert gap.gap_id == receipt.gap_id and receipt.material_gap
        assert receipt.expectation_gap_fingerprint == ledger.expectation_gap_fingerprint(gap)
        assert ledger.read_all() == (receipt,)
        assert all(path.read_bytes() == value for path, value in before.items())
        class FailingBuilder:
            def build(self, *args, **kwargs): raise AssertionError("duplicate reached materializer")
        try:
            ledger.materialize(items, reviews, catalyst_assessment, catalyst_creation, assessment, **kwargs, creator="Other", rationale="Duplicate.", created_at=datetime(2026, 8, 22, 12), builder=FailingBuilder())
        except ValueError as exc:
            assert "already" in str(exc)
        else:
            raise AssertionError("duplicate materialization accepted")
        rejected = replace(assessment, disposition=assessment.disposition.__class__.REJECTED)
        try:
            HistoricalComparisonExpectationGapCreationLedger(root / "rejected.jsonl").materialize(items, reviews, catalyst_assessment, catalyst_creation, rejected, **kwargs, creator="Creator", rationale="Forbidden.", created_at=datetime(2026, 8, 22, 11))
        except ValueError as exc:
            assert "Approved" in str(exc)
        else:
            raise AssertionError("rejected assessment materialized")
    print("HISTORICAL EXPECTATION GAP CREATION: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
