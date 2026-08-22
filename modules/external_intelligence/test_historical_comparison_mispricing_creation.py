"""Offline validation for explicit governed Mispricing materialization."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_mispricing_assessment_ledger import HistoricalComparisonMispricingAssessmentLedger
from modules.external_intelligence.historical_comparison_mispricing_creation_ledger import HistoricalComparisonMispricingCreationLedger
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.external_intelligence.test_historical_comparison_expectation_gap_creation import setup
from modules.external_intelligence.test_historical_comparison_valuation_snapshot_ledger import valuation
from modules.opportunity.mispricing_engine import MispricingEngine


_ORIGINAL_MISPRICING_ANALYZE = MispricingEngine.analyze


def qualifying_analysis(self, *args, **kwargs):
    result = _ORIGINAL_MISPRICING_ANALYZE(self, *args, **kwargs)
    result.catalyst_support = True
    result.potential_mispricing = True
    return result


def governed_chain(root):
    with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", new=qualifying_analysis):
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
    with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", new=qualifying_analysis):
        preview = HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
            items, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
            gap_creation, section, valuation_receipt, cmp=3500.0, **kwargs,
        )
    assessment = HistoricalComparisonMispricingAssessmentLedger(root / "mispricing-decisions.jsonl").record(
        preview, disposition="Approved", reviewer="Mispricing Reviewer",
        rationale="Exact governed analysis reviewed.", reviewed_at=datetime(2026, 8, 22, 13),
    )
    return items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, section, valuation_receipt, assessment, kwargs


def call(ledger, chain, **overrides):
    items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, section, valuation_receipt, assessment, kwargs = chain
    options = dict(cmp=3500.0, creator="Mispricing Steward", rationale="Explicit materialization.", created_at=datetime(2026, 8, 22, 14))
    options.update(overrides)
    with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", new=qualifying_analysis):
        return ledger.materialize(items, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, section, valuation_receipt, assessment, **kwargs, **options)


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        chain = governed_chain(root)
        before = {path: path.read_bytes() for path in root.glob("*.jsonl")}
        ledger = HistoricalComparisonMispricingCreationLedger(root / "mispricing-creations.jsonl")
        with patch("modules.opportunity.opportunity_synthesis_engine.OpportunitySynthesisEngine.analyze", side_effect=AssertionError("Opportunity synthesis forbidden")), patch("modules.valuation.valuation_engine.ValuationEngine.analyze", side_effect=AssertionError("valuation forbidden")):
            result, receipt = call(ledger, chain)
        assert result.potential_mispricing and receipt.potential_mispricing
        assert receipt.mispricing_fingerprint == ledger.mispricing_fingerprint(result)
        assert ledger.read_all() == (receipt,)
        assert all(path.read_bytes() == value for path, value in before.items())

        try:
            call(ledger, chain)
        except ValueError as exc:
            assert "already materialized" in str(exc)
        else:
            raise AssertionError("duplicate assessment consumption accepted")

        rejected = replace(chain[8], disposition=chain[8].disposition.REJECTED)
        rejected_chain = (*chain[:8], rejected, chain[9])
        with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", side_effect=AssertionError("engine must not run")):
            try:
                call(HistoricalComparisonMispricingCreationLedger(root / "rejected.jsonl"), rejected_chain)
            except ValueError as exc:
                assert "Approved" in str(exc)
            else:
                raise AssertionError("rejected assessment accepted")

        stale = replace(chain[8], valuation_fingerprint="0" * 64)
        stale_chain = (*chain[:8], stale, chain[9])
        class FailingBuilder:
            def build(self, *args, **kwargs):
                raise AssertionError("analysis reconstruction must not run")
        try:
            call(HistoricalComparisonMispricingCreationLedger(root / "stale.jsonl"), stale_chain, builder=FailingBuilder())
        except ValueError as exc:
            assert "does not bind" in str(exc)
        else:
            raise AssertionError("stale assessment accepted")

        try:
            call(HistoricalComparisonMispricingCreationLedger(root / "early.jsonl"), chain, created_at=datetime(2026, 8, 22, 12))
        except ValueError as exc:
            assert "precedes" in str(exc)
        else:
            raise AssertionError("early creation accepted")

        duplicate_identity = replace(chain[8], reviewer="Second Reviewer", rationale="Second exact approval.")
        duplicate_chain = (*chain[:8], duplicate_identity, chain[9])
        try:
            call(ledger, duplicate_chain)
        except ValueError as exc:
            assert "identity" in str(exc)
        else:
            raise AssertionError("duplicate Mispricing identity accepted")

        result_again, _ = call(HistoricalComparisonMispricingCreationLedger(root / "deterministic.jsonl"), duplicate_chain)
        assert ledger.mispricing_fingerprint(result) == ledger.mispricing_fingerprint(result_again)
    print("HISTORICAL MISPRICING CREATION: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
