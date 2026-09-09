"""Source-backed ability-to-survive assessment for the pre-EIP horizon."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SurvivabilityDecision(str, Enum):
    CLEAR = "CLEAR"
    CONTAINED = "CONTAINED"
    HOLD_INSUFFICIENT_MARGIN = "HOLD_INSUFFICIENT_MARGIN"
    VETO_SURVIVABILITY_FAILURE = "VETO_SURVIVABILITY_FAILURE"


@dataclass(frozen=True)
class SurvivabilityAssessment:
    schema_version: int
    assessment_id: str
    causal_chain_id: str
    normalized_valuation_assessment_id: str
    as_of: datetime
    currency: str
    cash_and_liquid_investments: float
    committed_undrawn_facilities: float
    annual_cash_burn: float
    debt_due_within_thesis_horizon: float
    total_debt: float
    normalized_ebitda: float
    interest_expense: float
    potential_dilution_percent: float
    unresolved_covenant_breach: bool
    going_concern_warning: bool
    critical_governance_threats: tuple[str, ...]
    source_ids: tuple[str, ...]
    assumptions: tuple[str, ...]
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class SurvivabilityGateResult:
    assessment_id: str
    thesis_horizon_quarters: int
    available_liquidity: float
    horizon_funding_need: float
    liquidity_coverage_ratio: float | None
    debt_to_normalized_ebitda: float | None
    normalized_ebitda_to_interest: float | None
    potential_dilution_percent: float
    decision: SurvivabilityDecision
    hard_veto: bool
    eligible_for_eip_assembly: bool
    reason_codes: tuple[str, ...]
    non_authority_statement: str


__all__ = ["SurvivabilityAssessment", "SurvivabilityDecision", "SurvivabilityGateResult"]
