"""Offline validation for governed read-only Expectation Gap analysis."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import (
    HistoricalComparisonCatalystCreationLedger,
)
from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import (
    HistoricalComparisonExpectationGapAnalysisPreviewBuilder,
)
from modules.external_intelligence.test_historical_comparison_catalyst_creation import inputs


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        items, reviews, catalyst_kwargs, assessment = inputs(root)
        _, creation = HistoricalComparisonCatalystCreationLedger(
            root / "creations.jsonl"
        ).materialize(
            items,
            reviews,
            assessment,
            **catalyst_kwargs,
            creator="Catalyst Steward",
            rationale="Explicit materialization.",
            created_at=datetime(2026, 8, 22),
        )
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        analysis_kwargs = dict(
            gap_id="GAP-001",
            company="Entity A",
            sector="Industrials",
            market_expectation=35,
            eios_expectation=70,
            market_earnings_expectation=40,
            eios_earnings_expectation=68,
            assumptions=["Current demand persists."],
            invalidation_conditions=["Demand reverses."],
        )
        preview = HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
            items,
            reviews,
            assessment,
            creation,
            **catalyst_kwargs,
            **analysis_kwargs,
        )
        assert preview.material_gap and preview.positive_gap and not preview.negative_gap
        assert preview.expectation_difference == 35.0 and preview.earnings_gap == 28.0
        assert len(preview.analysis_fingerprint) == 64
        assert all(path.read_bytes() == value for path, value in before.items())

        stale = replace(creation, catalyst_fingerprint="0" * 64)
        with patch(
            "modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",
            side_effect=AssertionError("engine must not run for stale provenance"),
        ):
            try:
                HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
                    items,
                    reviews,
                    assessment,
                    stale,
                    **catalyst_kwargs,
                    **analysis_kwargs,
                )
            except ValueError as exc:
                assert "does not bind" in str(exc)
            else:
                raise AssertionError("stale Catalyst receipt accepted")

        invalid = dict(analysis_kwargs, market_expectation=101)
        try:
            HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
                items,
                reviews,
                assessment,
                creation,
                **catalyst_kwargs,
                **invalid,
            )
        except ValueError as exc:
            assert "0-100" in str(exc)
        else:
            raise AssertionError("out-of-range expectation accepted")

    print("HISTORICAL EXPECTATION GAP ANALYSIS PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
