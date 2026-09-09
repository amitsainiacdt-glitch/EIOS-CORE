"""Explicit operating scenarios for normalized pre-EIP valuation research."""

from dataclasses import dataclass
from enum import Enum


class NormalizedScenarioKind(str, Enum):
    CURRENT_TROUGH = "CURRENT_TROUGH"
    REASONABLE_RECOVERY = "REASONABLE_RECOVERY"
    STRONG_NORMALIZATION = "STRONG_NORMALIZATION"


class NormalizedValuationRoom(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"
    NOT_ASSESSABLE = "NOT_ASSESSABLE"


@dataclass(frozen=True)
class NormalizedOperatingScenario:
    kind: NormalizedScenarioKind
    revenue: float
    ebitda_margin_percent: float
    ev_to_ebitda_multiple: float
    assumption_source_ids: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class NormalizedValuationAssessment:
    schema_version: int
    assessment_id: str
    expectation_gap_assessment_id: str
    currency: str
    current_price: float
    current_price_source_ids: tuple[str, ...]
    net_debt: float
    shares_outstanding: float
    scenarios: tuple[NormalizedOperatingScenario, ...]
    assumptions: tuple[str, ...]
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class NormalizedScenarioResult:
    kind: NormalizedScenarioKind
    revenue: float
    ebitda_margin_percent: float
    normalized_ebitda: float
    ev_to_ebitda_multiple: float
    enterprise_value: float
    equity_value: float
    value_per_share: float
    upside_downside_percent: float


@dataclass(frozen=True)
class NormalizedValuationResult:
    assessment_id: str
    currency: str
    current_price: float
    scenarios: tuple[NormalizedScenarioResult, ...]
    valuation_room: NormalizedValuationRoom
    eligible_for_eip_assembly: bool
    reason_codes: tuple[str, ...]
    non_authority_statement: str


__all__ = [
    "NormalizedOperatingScenario", "NormalizedScenarioKind", "NormalizedScenarioResult",
    "NormalizedValuationAssessment", "NormalizedValuationResult", "NormalizedValuationRoom",
]
