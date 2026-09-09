"""Hard pre-EIP survivability gate; no general risk score or trade authority."""

import math
from dataclasses import dataclass

from modules.external_intelligence.causal_chain import CausalChainAssessment
from modules.external_intelligence.normalized_valuation import NormalizedValuationResult, NormalizedValuationRoom
from modules.external_intelligence.survivability import SurvivabilityAssessment, SurvivabilityDecision, SurvivabilityGateResult


@dataclass(frozen=True)
class SurvivabilityPolicy:
    clear_liquidity_coverage: float = 1.25
    veto_liquidity_coverage: float = 1.0
    clear_debt_to_ebitda: float = 4.0
    veto_debt_to_ebitda: float = 6.0
    clear_interest_coverage: float = 2.0
    veto_interest_coverage: float = 1.0
    maximum_contained_dilution_percent: float = 20.0


class SurvivabilityService:
    NON_AUTHORITY = "Pre-EIP survivability research; not a general credit rating, EIP, recommendation, position, or trade instruction."

    def __init__(self, policy=None):
        self.policy = policy or SurvivabilityPolicy()

    def evaluate(self, *, causal_chain, normalized_valuation, assessment):
        if not isinstance(causal_chain, CausalChainAssessment):
            raise ValueError("causal_chain must be CausalChainAssessment")
        if not isinstance(normalized_valuation, NormalizedValuationResult):
            raise ValueError("normalized_valuation must be NormalizedValuationResult")
        if not isinstance(assessment, SurvivabilityAssessment):
            raise ValueError("assessment must be SurvivabilityAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported survivability schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("survivability does not bind to causal chain")
        if assessment.normalized_valuation_assessment_id != normalized_valuation.assessment_id:
            raise ValueError("survivability does not bind to normalized valuation")
        if assessment.as_of.tzinfo is None:
            raise ValueError("survivability as_of must be timezone-aware")
        self._text(assessment.currency, "currency")
        if assessment.currency.casefold() != normalized_valuation.currency.casefold():
            raise ValueError("survivability and valuation currency mismatch")
        if not assessment.public_information_only:
            raise ValueError("survivability accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("survivability requires the canonical non-authority statement")
        self._texts(assessment.source_ids, "source_ids")
        self._texts(assessment.assumptions, "assumptions")
        self._texts(assessment.critical_governance_threats, "critical_governance_threats", allow_empty=True)
        self._text(assessment.uncertainty_statement, "uncertainty_statement")
        cash = self._nonnegative(assessment.cash_and_liquid_investments, "cash_and_liquid_investments")
        facilities = self._nonnegative(assessment.committed_undrawn_facilities, "committed_undrawn_facilities")
        burn = self._nonnegative(assessment.annual_cash_burn, "annual_cash_burn")
        debt_due = self._nonnegative(assessment.debt_due_within_thesis_horizon, "debt_due_within_thesis_horizon")
        debt = self._nonnegative(assessment.total_debt, "total_debt")
        ebitda = self._finite(assessment.normalized_ebitda, "normalized_ebitda")
        interest = self._nonnegative(assessment.interest_expense, "interest_expense")
        dilution = self._nonnegative(assessment.potential_dilution_percent, "potential_dilution_percent")
        if dilution > 100:
            raise ValueError("potential_dilution_percent cannot exceed 100")

        horizon = causal_chain.expected_lead_time_quarters[1]
        available = cash + facilities
        funding_need = debt_due + burn * horizon / 4.0
        liquidity = None if funding_need == 0 else available / funding_need
        leverage = None if ebitda <= 0 else debt / ebitda
        interest_cover = None if interest == 0 else ebitda / interest
        reasons = []
        hard = False
        if assessment.going_concern_warning:
            hard = True; reasons.append("GOING_CONCERN_WARNING")
        if assessment.unresolved_covenant_breach:
            hard = True; reasons.append("UNRESOLVED_COVENANT_BREACH")
        if assessment.critical_governance_threats:
            hard = True; reasons.append("CRITICAL_GOVERNANCE_THREAT")
        if ebitda <= 0 and debt > 0:
            hard = True; reasons.append("NON_POSITIVE_EBITDA_WITH_DEBT")
        if liquidity is not None and liquidity < self.policy.veto_liquidity_coverage:
            hard = True; reasons.append("LIQUIDITY_DOES_NOT_COVER_HORIZON_NEED")
        if leverage is not None and leverage > self.policy.veto_debt_to_ebitda:
            hard = True; reasons.append("LEVERAGE_EXCEEDS_VETO_LIMIT")
        if interest_cover is not None and interest_cover < self.policy.veto_interest_coverage:
            hard = True; reasons.append("INTEREST_COVERAGE_BELOW_VETO_LIMIT")
        if hard:
            decision = SurvivabilityDecision.VETO_SURVIVABILITY_FAILURE
        else:
            cautions = []
            if liquidity is not None and liquidity < self.policy.clear_liquidity_coverage: cautions.append("LIQUIDITY_MARGIN_THIN")
            if leverage is not None and leverage > self.policy.clear_debt_to_ebitda: cautions.append("LEVERAGE_ELEVATED")
            if interest_cover is not None and interest_cover < self.policy.clear_interest_coverage: cautions.append("INTEREST_COVERAGE_THIN")
            if dilution > self.policy.maximum_contained_dilution_percent: cautions.append("DILUTION_RISK_HIGH")
            reasons.extend(cautions)
            decision = SurvivabilityDecision.HOLD_INSUFFICIENT_MARGIN if cautions else (
                SurvivabilityDecision.CLEAR if debt == 0 and funding_need == 0 else SurvivabilityDecision.CONTAINED)
        if normalized_valuation.valuation_room != NormalizedValuationRoom.SUFFICIENT:
            reasons.append("NORMALIZED_VALUATION_NOT_ELIGIBLE")
        eligible = decision in (SurvivabilityDecision.CLEAR, SurvivabilityDecision.CONTAINED) and normalized_valuation.eligible_for_eip_assembly
        return SurvivabilityGateResult(
            assessment.assessment_id, horizon, available, funding_need, liquidity, leverage,
            interest_cover, dilution, decision, hard, eligible, tuple(reasons), self.NON_AUTHORITY)

    @staticmethod
    def _finite(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return float(value)

    @classmethod
    def _nonnegative(cls, value, name):
        result = cls._finite(value, name)
        if result < 0:
            raise ValueError(f"{name} must be non-negative")
        return result

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


__all__ = ["SurvivabilityPolicy", "SurvivabilityService"]
