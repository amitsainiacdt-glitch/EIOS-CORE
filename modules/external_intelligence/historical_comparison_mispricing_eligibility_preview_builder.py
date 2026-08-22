"""Verify a governed Expectation Gap before any Mispricing analysis."""

import hashlib
import json

from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview_builder import HistoricalComparisonExpectationGapAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_decision import HistoricalComparisonExpectationGapAssessmentDecision, HistoricalComparisonExpectationGapAssessmentDisposition
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_expectation_gap_creation_receipt import HistoricalComparisonExpectationGapCreationReceipt
from modules.external_intelligence.historical_comparison_mispricing_eligibility_preview import HistoricalComparisonMispricingEligibilityPreview
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.opportunity.expectation_gap_engine import ExpectationGapEngine


class HistoricalComparisonMispricingEligibilityPreviewBuilder:
    REQUIRED_INPUTS = ("company", "cmp", "valuation")

    def build(self, inputs, reviews, catalyst_assessment, catalyst_creation, gap_assessment, gap_creation, **kwargs):
        if not isinstance(gap_assessment, HistoricalComparisonExpectationGapAssessmentDecision):
            raise ValueError("gap_assessment must be an Expectation Gap assessment")
        if not isinstance(gap_creation, HistoricalComparisonExpectationGapCreationReceipt):
            raise ValueError("gap_creation must be an Expectation Gap creation receipt")
        preview = HistoricalComparisonExpectationGapAnalysisPreviewBuilder().build(
            inputs, reviews, catalyst_assessment, catalyst_creation, **kwargs
        )
        assessment_fingerprint = HistoricalComparisonExpectationGapCreationLedger.assessment_fingerprint(gap_assessment)
        if (
            gap_assessment.analysis_fingerprint, gap_assessment.eligibility_fingerprint,
            gap_assessment.catalyst_id, gap_assessment.catalyst_fingerprint,
            gap_assessment.gap_id, gap_assessment.material_gap, gap_assessment.positive_gap,
            gap_assessment.negative_gap, gap_assessment.gap_score, gap_assessment.confidence,
            gap_assessment.signal_ids, gap_assessment.promoted_signal_ids,
        ) != (
            preview.analysis_fingerprint, preview.eligibility_fingerprint, preview.catalyst_id,
            preview.catalyst_fingerprint, preview.gap_id, preview.material_gap,
            preview.positive_gap, preview.negative_gap, preview.gap_score, preview.confidence,
            preview.signal_ids, preview.promoted_signal_ids,
        ):
            raise ValueError("Expectation Gap assessment does not bind to the exact analysis")
        catalyst_keys = ("theme", "cluster_id", "catalyst_id", "trigger", "description", "economic_impact", "earnings_impact", "valuation_impact")
        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **{key: kwargs[key] for key in catalyst_keys}
        )
        gap_keys = ("gap_id", "company", "sector", "market_expectation", "eios_expectation", "market_earnings_expectation", "eios_earnings_expectation", "assumptions", "invalidation_conditions")
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **{key: kwargs[key] for key in gap_keys})
        gap_fingerprint = HistoricalComparisonExpectationGapCreationLedger.expectation_gap_fingerprint(gap)
        if (
            gap_creation.analysis_fingerprint, gap_creation.assessment_fingerprint,
            gap_creation.eligibility_fingerprint, gap_creation.catalyst_id,
            gap_creation.catalyst_fingerprint, gap_creation.gap_id,
            gap_creation.expectation_gap_fingerprint, gap_creation.material_gap,
            gap_creation.positive_gap, gap_creation.negative_gap, gap_creation.gap_score,
            gap_creation.confidence, gap_creation.signal_ids, gap_creation.promoted_signal_ids,
        ) != (
            preview.analysis_fingerprint, assessment_fingerprint, preview.eligibility_fingerprint,
            preview.catalyst_id, preview.catalyst_fingerprint, preview.gap_id, gap_fingerprint,
            preview.material_gap, preview.positive_gap, preview.negative_gap, preview.gap_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
        ):
            raise ValueError("Expectation Gap creation receipt does not bind to the exact approved analysis")
        blockers = []
        if gap_assessment.disposition != HistoricalComparisonExpectationGapAssessmentDisposition.APPROVED:
            blockers.append("Expectation Gap assessment is not Approved.")
        if not preview.material_gap:
            blockers.append("Expectation Gap is no longer material.")
        warnings = tuple(preview.warnings)
        receipt_fingerprint = self.creation_receipt_fingerprint(gap_creation)
        identity = {
            "gap_creation_receipt_fingerprint": receipt_fingerprint,
            "expectation_gap_fingerprint": gap_fingerprint,
            "required_analysis_inputs": self.REQUIRED_INPUTS,
        }
        eligibility_fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return HistoricalComparisonMispricingEligibilityPreview(
            eligibility_fingerprint, not blockers, preview.gap_id, gap_fingerprint,
            receipt_fingerprint, assessment_fingerprint, preview.analysis_fingerprint,
            preview.catalyst_id, preview.catalyst_fingerprint, preview.material_gap,
            preview.positive_gap, preview.negative_gap, preview.gap_score, preview.confidence,
            preview.signal_ids, preview.promoted_signal_ids, self.REQUIRED_INPUTS,
            tuple(blockers), warnings,
        )

    @staticmethod
    def creation_receipt_fingerprint(receipt):
        if not isinstance(receipt, HistoricalComparisonExpectationGapCreationReceipt):
            raise ValueError("gap_creation must be an Expectation Gap creation receipt")
        payload = {**receipt.__dict__, "signal_ids": list(receipt.signal_ids), "promoted_signal_ids": list(receipt.promoted_signal_ids), "created_at": receipt.created_at.isoformat()}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


__all__ = ["HistoricalComparisonMispricingEligibilityPreviewBuilder"]
