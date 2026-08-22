"""Offline validation for governed read-only Mispricing analysis."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.external_intelligence.test_historical_comparison_expectation_gap_creation import setup
from modules.external_intelligence.test_historical_comparison_valuation_snapshot_ledger import valuation


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
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
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        preview = HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
            items, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
            gap_creation, section, valuation_receipt, cmp=3500.0,
            mispricing_assumptions=["Valuation remains valid."],
            mispricing_invalidation_conditions=["Valuation deteriorates."], **kwargs,
        )
        assert preview.company == "Entity A" and preview.valuation_support
        assert len(preview.analysis_fingerprint) == 64
        assert all(path.read_bytes() == value for path, value in before.items())
        stale = replace(valuation_receipt, valuation_fingerprint="0" * 64)
        with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", side_effect=AssertionError("engine must not run for stale valuation")):
            try:
                HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
                    items, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
                    gap_creation, section, stale, cmp=3500.0, **kwargs,
                )
            except ValueError as exc:
                assert "does not bind" in str(exc)
            else:
                raise AssertionError("stale valuation receipt accepted")
        try:
            HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
                items, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
                gap_creation, section, valuation_receipt, cmp=0, **kwargs,
            )
        except ValueError as exc:
            assert "positive" in str(exc)
        else:
            raise AssertionError("invalid current price accepted")
    print("HISTORICAL MISPRICING ANALYSIS PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
