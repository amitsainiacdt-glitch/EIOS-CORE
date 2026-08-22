"""Run governed Expectation Gap analysis without persistence."""

from __future__ import annotations

import hashlib
import json
import math

from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview import (
    HistoricalComparisonExpectationGapAnalysisPreview,
)
from modules.external_intelligence.historical_comparison_expectation_gap_eligibility_preview_builder import (
    HistoricalComparisonExpectationGapEligibilityPreviewBuilder,
)
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import (
    HistoricalComparisonPromotedStageCatalystPreviewBuilder,
)
from modules.opportunity.expectation_gap_engine import ExpectationGapEngine


class HistoricalComparisonExpectationGapAnalysisPreviewBuilder:
    """Verify the governed Catalyst chain before invoking the existing engine."""

    def build(
        self,
        inputs,
        reviews,
        assessment,
        creation,
        *,
        theme: str,
        cluster_id: str,
        catalyst_id: str,
        trigger: str,
        description: str,
        economic_impact: str,
        earnings_impact: str,
        valuation_impact: str,
        gap_id: str,
        company: str,
        sector: str,
        market_expectation: float,
        eios_expectation: float,
        market_earnings_expectation: float,
        eios_earnings_expectation: float,
        assumptions=None,
        invalidation_conditions=None,
    ) -> HistoricalComparisonExpectationGapAnalysisPreview:
        engine_inputs = self._validated_inputs(
            gap_id=gap_id,
            company=company,
            sector=sector,
            market_expectation=market_expectation,
            eios_expectation=eios_expectation,
            market_earnings_expectation=market_earnings_expectation,
            eios_earnings_expectation=eios_earnings_expectation,
            assumptions=assumptions,
            invalidation_conditions=invalidation_conditions,
        )
        catalyst_kwargs = dict(
            theme=theme,
            cluster_id=cluster_id,
            catalyst_id=catalyst_id,
            trigger=trigger,
            description=description,
            economic_impact=economic_impact,
            earnings_impact=earnings_impact,
            valuation_impact=valuation_impact,
        )
        eligibility = HistoricalComparisonExpectationGapEligibilityPreviewBuilder().build(
            inputs, reviews, assessment, creation, **catalyst_kwargs
        )
        if not eligibility.eligible:
            raise ValueError(
                "Catalyst is not eligible for Expectation Gap analysis: "
                + "; ".join(eligibility.blockers)
            )

        _, catalyst = HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(
            inputs, reviews, **catalyst_kwargs
        )
        gap = ExpectationGapEngine().analyze(catalyst=catalyst, **engine_inputs)
        result = {
            "eligibility_fingerprint": eligibility.eligibility_fingerprint,
            "catalyst_id": eligibility.catalyst_id,
            "catalyst_fingerprint": eligibility.catalyst_fingerprint,
            "creation_receipt_fingerprint": eligibility.creation_receipt_fingerprint,
            "gap_id": gap.gap_id,
            "company": gap.company,
            "sector": gap.sector,
            "market_expectation": gap.market_expectation,
            "eios_expectation": gap.eios_expectation,
            "expectation_difference": gap.expectation_difference,
            "market_earnings_expectation": gap.market_earnings_expectation,
            "eios_earnings_expectation": gap.eios_earnings_expectation,
            "earnings_gap": gap.earnings_gap,
            "market_recognition": gap.market_recognition,
            "unrecognized_potential": gap.unrecognized_potential,
            "positive_gap": gap.positive_gap,
            "negative_gap": gap.negative_gap,
            "material_gap": gap.positive_gap or gap.negative_gap,
            "gap_score": gap.gap_score,
            "confidence": gap.confidence,
            "evidence": tuple(gap.evidence),
            "assumptions": tuple(gap.assumptions),
            "disconfirming_evidence": tuple(gap.disconfirming_evidence),
            "invalidation_conditions": tuple(gap.invalidation_conditions),
            "reasons": tuple(gap.reasons),
            "warnings": tuple(gap.warnings),
            "signal_ids": eligibility.signal_ids,
            "promoted_signal_ids": eligibility.promoted_signal_ids,
        }
        fingerprint_payload = {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in result.items()
        }
        analysis_fingerprint = hashlib.sha256(
            json.dumps(
                fingerprint_payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
        return HistoricalComparisonExpectationGapAnalysisPreview(
            analysis_fingerprint=analysis_fingerprint, **result
        )

    @staticmethod
    def _validated_inputs(**values):
        result = {}
        for name in ("gap_id", "company", "sector"):
            value = values[name]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
            result[name] = value.strip()
        for name in (
            "market_expectation",
            "eios_expectation",
            "market_earnings_expectation",
            "eios_earnings_expectation",
        ):
            value = values[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
            value = float(value)
            if not math.isfinite(value) or not 0.0 <= value <= 100.0:
                raise ValueError(f"{name} must be on the 0-100 scale")
            result[name] = value
        for name in ("assumptions", "invalidation_conditions"):
            value = values[name] or ()
            if isinstance(value, (str, bytes)) or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ValueError(f"{name} must contain non-empty strings")
            result[name] = [item.strip() for item in value]
        return result


__all__ = ["HistoricalComparisonExpectationGapAnalysisPreviewBuilder"]
