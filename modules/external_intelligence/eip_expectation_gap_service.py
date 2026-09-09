"""Validates and calculates a source-backed pre-EIP Expectation Gap."""

import math

from modules.external_intelligence.causal_chain import CausalChainAssessment
from modules.external_intelligence.change_regime import ChangeRegimeAssessment
from modules.external_intelligence.eip_expectation_gap import (
    EIPExpectationGapAssessment, EIPExpectationGapResult, ExpectationGapDirection,
    ExpectationGapMateriality, FavorableMetricDirection, GovernedExpectationMeasure,
)
from modules.external_intelligence.thesis_price_recognition import ThesisPriceRecognitionGateResult, ThesisRecognitionDecision


class EIPExpectationGapService:
    NON_AUTHORITY = "Research-stage Expectation Gap; not an EIP, valuation conclusion, recommendation, position, or trade instruction."

    def evaluate(self, *, causal_chain, regime_assessment, recognition_gate, assessment):
        if not isinstance(causal_chain, CausalChainAssessment):
            raise ValueError("causal_chain must be CausalChainAssessment")
        if not isinstance(regime_assessment, ChangeRegimeAssessment):
            raise ValueError("regime_assessment must be ChangeRegimeAssessment")
        if not isinstance(recognition_gate, ThesisPriceRecognitionGateResult):
            raise ValueError("recognition_gate must be ThesisPriceRecognitionGateResult")
        if not isinstance(assessment, EIPExpectationGapAssessment):
            raise ValueError("assessment must be EIPExpectationGapAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported EIP Expectation Gap schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("Expectation Gap does not bind to causal chain")
        if assessment.regime_assessment_id != regime_assessment.assessment_id or regime_assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("Expectation Gap does not bind to regime assessment")
        if assessment.thesis_recognition_assessment_id != recognition_gate.assessment_id:
            raise ValueError("Expectation Gap does not bind to thesis recognition")
        if not assessment.public_information_only:
            raise ValueError("Expectation Gap accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("Expectation Gap requires the canonical non-authority statement")
        if not isinstance(assessment.favorable_direction, FavorableMetricDirection):
            raise ValueError("favorable metric direction is invalid")
        if not isinstance(assessment.direction, ExpectationGapDirection):
            raise ValueError("Expectation Gap direction is invalid")
        if not isinstance(assessment.materiality, ExpectationGapMateriality):
            raise ValueError("Expectation Gap materiality is invalid")
        market = self._measure(assessment.market_expectation, "market_expectation")
        eios = self._measure(assessment.causal_eios_expectation, "causal_eios_expectation")
        if (market.metric_id.casefold(), market.unit.casefold(), market.horizon_end) != (
                eios.metric_id.casefold(), eios.unit.casefold(), eios.horizon_end):
            raise ValueError("market and EIOS expectations must use the same metric, unit, and horizon")
        self._texts(assessment.assumptions, "assumptions")
        self._texts(assessment.contradictions, "contradictions", allow_empty=True)
        self._texts(assessment.invalidation_conditions, "invalidation_conditions")
        self._text(assessment.materiality_rationale, "materiality_rationale")
        self._text(assessment.uncertainty_statement, "uncertainty_statement")

        raw_gap = eios.value - market.value
        favorable_gap = raw_gap if assessment.favorable_direction == FavorableMetricDirection.HIGHER else -raw_gap
        calculated_direction = (ExpectationGapDirection.POSITIVE if favorable_gap > 0 else
                                ExpectationGapDirection.NEGATIVE if favorable_gap < 0 else
                                ExpectationGapDirection.NO_CLEAR_GAP)
        if assessment.direction != calculated_direction:
            raise ValueError("declared Expectation Gap direction disagrees with comparable values")
        if calculated_direction == ExpectationGapDirection.NO_CLEAR_GAP and assessment.materiality != ExpectationGapMateriality.IMMATERIAL:
            raise ValueError("equal expectations must be immaterial")
        relative = None if market.value == 0 else raw_gap / abs(market.value) * 100.0
        reasons = []
        eligible = True
        if recognition_gate.decision != ThesisRecognitionDecision.ALLOW_EIP_REVIEW:
            eligible = False; reasons.append("PRICE_RECOGNITION_DID_NOT_ALLOW_EIP_REVIEW")
        if calculated_direction != ExpectationGapDirection.POSITIVE:
            eligible = False; reasons.append("POSITIVE_EXPECTATION_GAP_NOT_ESTABLISHED")
        if assessment.materiality in (ExpectationGapMateriality.IMMATERIAL, ExpectationGapMateriality.UNCERTAIN):
            eligible = False; reasons.append("MATERIAL_EXPECTATION_GAP_NOT_ESTABLISHED")
        return EIPExpectationGapResult(
            assessment.assessment_id, market.metric_id, market.unit, market.horizon_end,
            market.value, eios.value, raw_gap, relative, calculated_direction,
            assessment.materiality, eligible, tuple(reasons), self.NON_AUTHORITY,
        )

    @classmethod
    def _measure(cls, value, name):
        if not isinstance(value, GovernedExpectationMeasure):
            raise ValueError(f"{name} must be GovernedExpectationMeasure")
        cls._text(value.metric_id, f"{name}.metric_id")
        cls._text(value.unit, f"{name}.unit")
        if value.horizon_end.tzinfo is None:
            raise ValueError(f"{name}.horizon_end must be timezone-aware")
        if isinstance(value.value, bool) or not isinstance(value.value, (int, float)) or not math.isfinite(value.value):
            raise ValueError(f"{name}.value must be finite")
        cls._texts(value.source_ids, f"{name}.source_ids")
        cls._text(value.explanation, f"{name}.explanation")
        return value

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name, *, allow_empty=False):
        if not isinstance(values, tuple):
            raise ValueError(f"{name} must be a tuple")
        result = tuple(cls._text(value, name) for value in values)
        if not allow_empty and not result:
            raise ValueError(f"{name} must not be empty")
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result


__all__ = ["EIPExpectationGapService"]
