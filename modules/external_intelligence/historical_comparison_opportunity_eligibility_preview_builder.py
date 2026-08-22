"""Verify governed Mispricing before any Opportunity synthesis."""

import hashlib
import json

from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_mispricing_assessment_decision import HistoricalComparisonMispricingAssessmentDecision, HistoricalComparisonMispricingAssessmentDisposition
from modules.external_intelligence.historical_comparison_mispricing_creation_ledger import HistoricalComparisonMispricingCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_creation_receipt import HistoricalComparisonMispricingCreationReceipt
from modules.external_intelligence.historical_comparison_opportunity_eligibility_preview import HistoricalComparisonOpportunityEligibilityPreview
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.opportunity.expectation_gap_engine import ExpectationGapEngine
from modules.opportunity.mispricing_engine import MispricingEngine


class HistoricalComparisonOpportunityEligibilityPreviewBuilder:
    REQUIRED_INPUTS = (
        "company", "sector", "catalyst", "expectation_gap", "mispricing",
        "governed_asymmetry", "governed_opportunity_evidence_pack",
        "assumptions", "invalidation_conditions", "kill_switches",
    )

    def build(
        self, inputs, reviews, catalyst_assessment, catalyst_creation,
        gap_assessment, gap_creation, valuation, valuation_receipt,
        mispricing_assessment, mispricing_creation, *, cmp,
        mispricing_assumptions=(), mispricing_invalidation_conditions=(), **kwargs,
    ):
        if not isinstance(mispricing_assessment, HistoricalComparisonMispricingAssessmentDecision):
            raise ValueError("mispricing_assessment must be a Mispricing assessment")
        if not isinstance(mispricing_creation, HistoricalComparisonMispricingCreationReceipt):
            raise ValueError("mispricing_creation must be a Mispricing creation receipt")

        preview = HistoricalComparisonMispricingAnalysisPreviewBuilder().build(
            inputs, reviews, catalyst_assessment, catalyst_creation, gap_assessment,
            gap_creation, valuation, valuation_receipt, cmp=cmp,
            mispricing_assumptions=mispricing_assumptions,
            mispricing_invalidation_conditions=mispricing_invalidation_conditions,
            **kwargs,
        )
        assessment_fingerprint = HistoricalComparisonMispricingCreationLedger.assessment_fingerprint(mispricing_assessment)
        if (
            mispricing_assessment.analysis_fingerprint,
            mispricing_assessment.eligibility_fingerprint,
            mispricing_assessment.valuation_fingerprint,
            mispricing_assessment.valuation_receipt_fingerprint,
            mispricing_assessment.expectation_gap_fingerprint,
            mispricing_assessment.catalyst_fingerprint,
            mispricing_assessment.company,
            mispricing_assessment.potential_mispricing,
            mispricing_assessment.mispricing_score,
            mispricing_assessment.confidence,
            mispricing_assessment.signal_ids,
            mispricing_assessment.promoted_signal_ids,
        ) != (
            preview.analysis_fingerprint, preview.eligibility_fingerprint,
            preview.valuation_fingerprint, preview.valuation_receipt_fingerprint,
            preview.expectation_gap_fingerprint, preview.catalyst_fingerprint,
            preview.company, preview.potential_mispricing, preview.mispricing_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
        ):
            raise ValueError("Mispricing assessment does not bind to the exact analysis")

        catalyst_keys = ("theme", "cluster_id", "catalyst_id", "trigger", "description", "economic_impact", "earnings_impact", "valuation_impact")
        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **{key: kwargs[key] for key in catalyst_keys}
        )
        gap_keys = ("gap_id", "company", "sector", "market_expectation", "eios_expectation", "market_earnings_expectation", "eios_earnings_expectation", "assumptions", "invalidation_conditions")
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **{key: kwargs[key] for key in gap_keys})
        if HistoricalComparisonExpectationGapCreationLedger.expectation_gap_fingerprint(gap) != preview.expectation_gap_fingerprint:
            raise ValueError("reconstructed Expectation Gap differs from its creation receipt")
        mispricing = MispricingEngine().analyze(
            company=kwargs["company"], cmp=float(cmp), valuation=valuation,
            catalyst=catalyst, expectation_gap=gap,
            assumptions=list(mispricing_assumptions),
            invalidation_conditions=list(mispricing_invalidation_conditions),
        )
        mispricing_fingerprint = HistoricalComparisonMispricingCreationLedger.mispricing_fingerprint(mispricing)
        expected_creation = (
            preview.analysis_fingerprint, assessment_fingerprint,
            preview.eligibility_fingerprint, preview.valuation_fingerprint,
            preview.valuation_receipt_fingerprint, preview.gap_id,
            preview.expectation_gap_fingerprint, preview.catalyst_id,
            preview.catalyst_fingerprint, preview.company, preview.cmp,
            mispricing_fingerprint, preview.potential_mispricing,
            preview.mispricing_score, preview.confidence,
            preview.signal_ids, preview.promoted_signal_ids,
        )
        actual_creation = (
            mispricing_creation.analysis_fingerprint,
            mispricing_creation.assessment_fingerprint,
            mispricing_creation.eligibility_fingerprint,
            mispricing_creation.valuation_fingerprint,
            mispricing_creation.valuation_receipt_fingerprint,
            mispricing_creation.gap_id,
            mispricing_creation.expectation_gap_fingerprint,
            mispricing_creation.catalyst_id,
            mispricing_creation.catalyst_fingerprint,
            mispricing_creation.company, mispricing_creation.cmp,
            mispricing_creation.mispricing_fingerprint,
            mispricing_creation.potential_mispricing,
            mispricing_creation.mispricing_score,
            mispricing_creation.confidence,
            mispricing_creation.signal_ids,
            mispricing_creation.promoted_signal_ids,
        )
        if actual_creation != expected_creation:
            raise ValueError("Mispricing creation receipt does not bind to the exact approved analysis")

        blockers = []
        if mispricing_assessment.disposition != HistoricalComparisonMispricingAssessmentDisposition.APPROVED:
            blockers.append("Mispricing assessment is not Approved.")
        if not mispricing.potential_mispricing:
            blockers.append("Materialized result no longer identifies potential mispricing.")
        sector = kwargs.get("sector")
        if not isinstance(sector, str) or not sector.strip():
            blockers.append("Company sector is missing.")
            sector = ""
        else:
            sector = sector.strip()

        missing = (
            "governed_asymmetry",
            "governed_opportunity_evidence_pack",
            "opportunity_assumptions",
            "opportunity_invalidation_conditions",
            "opportunity_kill_switches",
        )
        blockers.extend((
            "A governed Asymmetry assessment and creation receipt are required.",
            "A governed Opportunity Evidence Pack and exact scoring provenance are required.",
            "Opportunity assumptions, invalidation conditions, and kill switches require explicit governed intake.",
        ))
        warnings = (
            "Opportunity synthesis is intentionally blocked until its remaining governed inputs exist.",
            "Asymmetry must be completed before Opportunity synthesis analysis.",
        )
        creation_fingerprint = self.creation_receipt_fingerprint(mispricing_creation)
        identity = {
            "mispricing_creation_receipt_fingerprint": creation_fingerprint,
            "mispricing_fingerprint": mispricing_fingerprint,
            "required_synthesis_inputs": self.REQUIRED_INPUTS,
            "missing_governed_inputs": missing,
            "blockers": blockers,
        }
        eligibility_fingerprint = hashlib.sha256(
            json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        return HistoricalComparisonOpportunityEligibilityPreview(
            eligibility_fingerprint, not blockers, preview.company, sector,
            mispricing_fingerprint, creation_fingerprint, assessment_fingerprint,
            preview.analysis_fingerprint, preview.eligibility_fingerprint,
            preview.valuation_fingerprint, preview.valuation_receipt_fingerprint,
            preview.gap_id, preview.expectation_gap_fingerprint,
            preview.catalyst_id, preview.catalyst_fingerprint,
            preview.potential_mispricing, preview.mispricing_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
            self.REQUIRED_INPUTS, missing, tuple(blockers), warnings,
        )

    @staticmethod
    def creation_receipt_fingerprint(receipt):
        if not isinstance(receipt, HistoricalComparisonMispricingCreationReceipt):
            raise ValueError("mispricing_creation must be a Mispricing creation receipt")
        payload = {
            **receipt.__dict__, "signal_ids": list(receipt.signal_ids),
            "promoted_signal_ids": list(receipt.promoted_signal_ids),
            "created_at": receipt.created_at.isoformat(),
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()


__all__ = ["HistoricalComparisonOpportunityEligibilityPreviewBuilder"]
