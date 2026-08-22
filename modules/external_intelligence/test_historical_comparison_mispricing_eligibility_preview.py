"""Offline validation for governed Mispricing eligibility."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_eligibility_preview_builder import HistoricalComparisonMispricingEligibilityPreviewBuilder
from modules.external_intelligence.test_historical_comparison_expectation_gap_creation import setup


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, kwargs = setup(root)
        _, gap_creation = HistoricalComparisonExpectationGapCreationLedger(root / "gap-creations.jsonl").materialize(
            items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, **kwargs,
            creator="Gap Steward", rationale="Explicit materialization.", created_at=datetime(2026, 8, 22, 11),
        )
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", side_effect=AssertionError("Mispricing forbidden")):
            preview = HistoricalComparisonMispricingEligibilityPreviewBuilder().build(
                items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, **kwargs
            )
        assert preview.eligible and not preview.blockers
        assert preview.required_analysis_inputs == ("company", "cmp", "valuation")
        assert all(path.read_bytes() == value for path, value in before.items())
        stale = replace(gap_creation, expectation_gap_fingerprint="0" * 64)
        try:
            HistoricalComparisonMispricingEligibilityPreviewBuilder().build(
                items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, stale, **kwargs
            )
        except ValueError as exc:
            assert "does not bind" in str(exc)
        else:
            raise AssertionError("stale creation receipt accepted")
        rejected = replace(gap_assessment, disposition=gap_assessment.disposition.__class__.REJECTED)
        rejected_creation = replace(
            gap_creation,
            assessment_fingerprint=HistoricalComparisonExpectationGapCreationLedger.assessment_fingerprint(rejected),
        )
        blocked = HistoricalComparisonMispricingEligibilityPreviewBuilder().build(
            items, reviews, catalyst_assessment, catalyst_creation, rejected, rejected_creation, **kwargs
        )
        assert not blocked.eligible and "not Approved" in blocked.blockers[0]
    print("HISTORICAL MISPRICING ELIGIBILITY PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
