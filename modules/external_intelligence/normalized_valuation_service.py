"""Calculates transparent normalized scenarios without price-history shortcuts."""

import math
from dataclasses import dataclass

from modules.external_intelligence.eip_expectation_gap import EIPExpectationGapResult
from modules.external_intelligence.normalized_valuation import (
    NormalizedOperatingScenario, NormalizedScenarioKind, NormalizedScenarioResult,
    NormalizedValuationAssessment, NormalizedValuationResult, NormalizedValuationRoom,
)


@dataclass(frozen=True)
class NormalizedValuationPolicy:
    minimum_reasonable_upside_percent: float = 20.0


class NormalizedValuationService:
    NON_AUTHORITY = "Normalized scenario research; not intrinsic-value certainty, an EIP, recommendation, position, or trade instruction."
    REQUIRED_SCENARIOS = tuple(NormalizedScenarioKind)

    def __init__(self, policy=None):
        self.policy = policy or NormalizedValuationPolicy()
        if not math.isfinite(self.policy.minimum_reasonable_upside_percent) or self.policy.minimum_reasonable_upside_percent < 0:
            raise ValueError("minimum reasonable upside policy is invalid")

    def evaluate(self, *, expectation_gap, assessment):
        if not isinstance(expectation_gap, EIPExpectationGapResult):
            raise ValueError("expectation_gap must be EIPExpectationGapResult")
        if not isinstance(assessment, NormalizedValuationAssessment):
            raise ValueError("assessment must be NormalizedValuationAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported normalized-valuation schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.expectation_gap_assessment_id != expectation_gap.assessment_id:
            raise ValueError("normalized valuation does not bind to Expectation Gap")
        self._text(assessment.currency, "currency")
        if not assessment.public_information_only:
            raise ValueError("normalized valuation accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("normalized valuation requires the canonical non-authority statement")
        current_price = self._positive(assessment.current_price, "current_price")
        self._texts(assessment.current_price_source_ids, "current_price_source_ids")
        net_debt = self._finite(assessment.net_debt, "net_debt")
        shares = self._positive(assessment.shares_outstanding, "shares_outstanding")
        self._texts(assessment.assumptions, "assumptions")
        self._text(assessment.uncertainty_statement, "uncertainty_statement")
        if not isinstance(assessment.scenarios, tuple) or tuple(item.kind for item in assessment.scenarios) != self.REQUIRED_SCENARIOS:
            raise ValueError("valuation must contain current/trough, reasonable recovery, and strong normalization in order")

        results = tuple(self._scenario(item, current_price, net_debt, shares) for item in assessment.scenarios)
        ebitda_values = tuple(item.normalized_ebitda for item in results)
        if not (ebitda_values[0] <= ebitda_values[1] <= ebitda_values[2]):
            raise ValueError("normalized EBITDA must not decline across stronger scenarios")
        reasonable = results[1]
        reasons = []
        if not expectation_gap.eligible_for_eip_assembly:
            room = NormalizedValuationRoom.NOT_ASSESSABLE
            reasons.append("EXPECTATION_GAP_NOT_ELIGIBLE")
        elif reasonable.upside_downside_percent < self.policy.minimum_reasonable_upside_percent:
            room = NormalizedValuationRoom.INSUFFICIENT
            reasons.append("REASONABLE_RECOVERY_VALUATION_ROOM_INSUFFICIENT")
        else:
            room = NormalizedValuationRoom.SUFFICIENT
        return NormalizedValuationResult(
            assessment.assessment_id, assessment.currency, current_price, results, room,
            room == NormalizedValuationRoom.SUFFICIENT, tuple(reasons), self.NON_AUTHORITY,
        )

    def _scenario(self, item, current_price, net_debt, shares):
        if not isinstance(item, NormalizedOperatingScenario):
            raise ValueError("scenarios must contain NormalizedOperatingScenario values")
        if not isinstance(item.kind, NormalizedScenarioKind):
            raise ValueError("scenario kind is invalid")
        revenue = self._positive(item.revenue, "scenario revenue")
        margin = self._finite(item.ebitda_margin_percent, "EBITDA margin")
        if not 0 <= margin <= 100:
            raise ValueError("EBITDA margin must be between zero and 100")
        multiple = self._positive(item.ev_to_ebitda_multiple, "EV/EBITDA multiple")
        self._texts(item.assumption_source_ids, "scenario assumption_source_ids")
        self._text(item.rationale, "scenario rationale")
        ebitda = revenue * margin / 100.0
        enterprise = ebitda * multiple
        equity = enterprise - net_debt
        per_share = equity / shares
        upside = (per_share / current_price - 1.0) * 100.0
        return NormalizedScenarioResult(item.kind, revenue, margin, ebitda, multiple, enterprise, equity, per_share, upside)

    @staticmethod
    def _finite(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return float(value)

    @classmethod
    def _positive(cls, value, name):
        result = cls._finite(value, name)
        if result <= 0:
            raise ValueError(f"{name} must be positive")
        return result

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, tuple) or not values:
            raise ValueError(f"{name} must be a non-empty tuple")
        result = tuple(cls._text(value, name) for value in values)
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result


__all__ = ["NormalizedValuationPolicy", "NormalizedValuationService"]
