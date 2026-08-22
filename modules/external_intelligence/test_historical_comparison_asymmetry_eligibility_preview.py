"""Offline validation for governed Asymmetry eligibility."""

from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_asymmetry_eligibility_preview_builder import HistoricalComparisonAsymmetryEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_mispricing_creation_ledger import HistoricalComparisonMispricingCreationLedger
from modules.external_intelligence.test_historical_comparison_mispricing_creation import call, governed_chain, qualifying_analysis


def build(builder, chain, creation):
    items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, section, valuation_receipt, assessment, kwargs = chain
    with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", new=qualifying_analysis):
        return builder.build(
            items, reviews, catalyst_assessment, catalyst_creation,
            gap_assessment, gap_creation, section, valuation_receipt,
            assessment, creation, cmp=3500.0, **kwargs,
        )


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        chain = governed_chain(root)
        _, creation = call(HistoricalComparisonMispricingCreationLedger(root / "mispricing-creations.jsonl"), chain)
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        builder = HistoricalComparisonAsymmetryEligibilityPreviewBuilder()
        with patch("modules.opportunity.asymmetry_engine.AsymmetryEngine.analyze", side_effect=AssertionError("Asymmetry forbidden")), patch("modules.opportunity.opportunity_synthesis_engine.OpportunitySynthesisEngine.analyze", side_effect=AssertionError("Opportunity synthesis forbidden")):
            preview = build(builder, chain, creation)
            second = build(builder, chain, creation)
        assert preview.eligible and not preview.blockers
        assert preview.eligibility_fingerprint == second.eligibility_fingerprint
        assert preview.mispricing_fingerprint == creation.mispricing_fingerprint
        assert preview.required_analysis_inputs == (
            "company", "scenarios", "assumptions",
            "invalidation_conditions", "disconfirming_evidence",
        )
        assert all(path.read_bytes() == value for path, value in before.items())

        stale = replace(creation, assessment_fingerprint="0" * 64)
        with patch("modules.opportunity.asymmetry_engine.AsymmetryEngine.analyze", side_effect=AssertionError("Asymmetry forbidden")):
            try:
                build(builder, chain, stale)
            except ValueError as exc:
                assert "does not bind" in str(exc)
            else:
                raise AssertionError("stale Mispricing creation receipt accepted")
    print("HISTORICAL ASYMMETRY ELIGIBILITY PREVIEW: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
