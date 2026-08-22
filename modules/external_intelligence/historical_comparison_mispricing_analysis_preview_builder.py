"""Run governed Mispricing analysis without persistence."""

import hashlib
import json
import math

from modules.external_intelligence.historical_comparison_mispricing_analysis_preview import HistoricalComparisonMispricingAnalysisPreview
from modules.external_intelligence.historical_comparison_mispricing_eligibility_preview_builder import HistoricalComparisonMispricingEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.external_intelligence.historical_comparison_valuation_snapshot_receipt import HistoricalComparisonValuationSnapshotReceipt
from modules.opportunity.expectation_gap_engine import ExpectationGapEngine
from modules.opportunity.mispricing_engine import MispricingEngine


class HistoricalComparisonMispricingAnalysisPreviewBuilder:
    def build(
        self, inputs, reviews, catalyst_assessment, catalyst_creation,
        gap_assessment, gap_creation, valuation, valuation_receipt, *, cmp,
        mispricing_assumptions=(), mispricing_invalidation_conditions=(), **kwargs,
    ):
        eligibility = HistoricalComparisonMispricingEligibilityPreviewBuilder().build(
            inputs, reviews, catalyst_assessment, catalyst_creation,
            gap_assessment, gap_creation, **kwargs,
        )
        if not eligibility.eligible:
            raise ValueError("Expectation Gap is not eligible for Mispricing analysis: " + "; ".join(eligibility.blockers))
        if not isinstance(valuation_receipt, HistoricalComparisonValuationSnapshotReceipt):
            raise ValueError("valuation_receipt must be a valuation snapshot receipt")
        HistoricalComparisonValuationSnapshotLedger.validate_valuation(valuation)
        valuation_fingerprint = HistoricalComparisonValuationSnapshotLedger.valuation_fingerprint(valuation)
        if (
            valuation_receipt.valuation_fingerprint, valuation_receipt.entity,
            valuation_receipt.intrinsic_value, valuation_receipt.fair_value,
            valuation_receipt.valuation_method, valuation_receipt.confidence,
            valuation_receipt.source,
        ) != (
            valuation_fingerprint, kwargs["company"], float(valuation.intrinsic_value),
            float(valuation.fair_value), valuation.valuation_method.strip(),
            float(valuation.confidence), valuation.source.strip(),
        ):
            raise ValueError("valuation receipt does not bind to the exact company valuation")
        if isinstance(cmp, bool) or not isinstance(cmp, (int, float)) or not math.isfinite(cmp) or cmp <= 0:
            raise ValueError("cmp must be a positive finite number")
        assumptions = self._texts(mispricing_assumptions, "mispricing_assumptions")
        invalidations = self._texts(mispricing_invalidation_conditions, "mispricing_invalidation_conditions")
        catalyst_keys = ("theme", "cluster_id", "catalyst_id", "trigger", "description", "economic_impact", "earnings_impact", "valuation_impact")
        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **{key: kwargs[key] for key in catalyst_keys}
        )
        gap_keys = ("gap_id", "company", "sector", "market_expectation", "eios_expectation", "market_earnings_expectation", "eios_earnings_expectation", "assumptions", "invalidation_conditions")
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **{key: kwargs[key] for key in gap_keys})
        if HistoricalComparisonExpectationGapCreationLedger.expectation_gap_fingerprint(gap) != eligibility.expectation_gap_fingerprint:
            raise ValueError("reconstructed Expectation Gap differs from its creation receipt")
        result = MispricingEngine().analyze(
            company=kwargs["company"], cmp=float(cmp), valuation=valuation,
            catalyst=catalyst, expectation_gap=gap,
            assumptions=list(assumptions), invalidation_conditions=list(invalidations),
        )
        valuation_receipt_fingerprint = self.valuation_receipt_fingerprint(valuation_receipt)
        values = {
            "eligibility_fingerprint": eligibility.eligibility_fingerprint,
            "valuation_fingerprint": valuation_fingerprint,
            "valuation_receipt_fingerprint": valuation_receipt_fingerprint,
            "gap_id": eligibility.gap_id,
            "expectation_gap_fingerprint": eligibility.expectation_gap_fingerprint,
            "catalyst_id": eligibility.catalyst_id,
            "catalyst_fingerprint": eligibility.catalyst_fingerprint,
            "company": result.company, "cmp": result.cmp,
            "intrinsic_value": result.intrinsic_value, "fair_value": result.fair_value,
            "valuation_upside": result.valuation_upside, "valuation_discount": result.valuation_discount,
            "catalyst_score": result.catalyst_score, "expectation_gap_score": result.expectation_gap_score,
            "expectation_difference": result.expectation_difference, "earnings_gap": result.earnings_gap,
            "market_recognition": result.market_recognition, "unrecognized_potential": result.unrecognized_potential,
            "mispricing_score": result.mispricing_score, "confidence": result.confidence,
            "valuation_support": result.valuation_support, "catalyst_support": result.catalyst_support,
            "expectation_support": result.expectation_support, "potential_mispricing": result.potential_mispricing,
            "evidence": tuple(result.evidence), "assumptions": tuple(result.assumptions),
            "disconfirming_evidence": tuple(result.disconfirming_evidence),
            "invalidation_conditions": tuple(result.invalidation_conditions),
            "reasons": tuple(result.reasons), "warnings": tuple(result.warnings),
            "signal_ids": eligibility.signal_ids, "promoted_signal_ids": eligibility.promoted_signal_ids,
        }
        canonical = {key: list(value) if isinstance(value, tuple) else value for key, value in values.items()}
        fingerprint = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return HistoricalComparisonMispricingAnalysisPreview(fingerprint, **values)

    @staticmethod
    def valuation_receipt_fingerprint(receipt):
        payload = {**receipt.__dict__, "recorded_at": receipt.recorded_at.isoformat()}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @staticmethod
    def _texts(values, name):
        if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
            raise ValueError(f"{name} must be a list")
        result = tuple(value.strip() for value in values if isinstance(value, str) and value.strip())
        if len(result) != len(values) or len({value.casefold() for value in result}) != len(result):
            raise ValueError(f"{name} must contain unique non-empty strings")
        return result


__all__ = ["HistoricalComparisonMispricingAnalysisPreviewBuilder"]
