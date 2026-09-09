"""Governed pre-EIP comparison of market expectation and causal implication."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ExpectationGapDirection(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NO_CLEAR_GAP = "NO_CLEAR_GAP"


class ExpectationGapMateriality(str, Enum):
    IMMATERIAL = "IMMATERIAL"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    UNCERTAIN = "UNCERTAIN"


class FavorableMetricDirection(str, Enum):
    HIGHER = "HIGHER"
    LOWER = "LOWER"


@dataclass(frozen=True)
class GovernedExpectationMeasure:
    metric_id: str
    unit: str
    horizon_end: datetime
    value: float
    source_ids: tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class EIPExpectationGapAssessment:
    schema_version: int
    assessment_id: str
    causal_chain_id: str
    regime_assessment_id: str
    thesis_recognition_assessment_id: str
    market_expectation: GovernedExpectationMeasure
    causal_eios_expectation: GovernedExpectationMeasure
    favorable_direction: FavorableMetricDirection
    direction: ExpectationGapDirection
    materiality: ExpectationGapMateriality
    materiality_rationale: str
    assumptions: tuple[str, ...]
    contradictions: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class EIPExpectationGapResult:
    assessment_id: str
    metric_id: str
    unit: str
    horizon_end: datetime
    market_value: float
    eios_value: float
    absolute_gap: float
    relative_gap_percent: float | None
    direction: ExpectationGapDirection
    materiality: ExpectationGapMateriality
    eligible_for_eip_assembly: bool
    reason_codes: tuple[str, ...]
    non_authority_statement: str


__all__ = [
    "EIPExpectationGapAssessment", "EIPExpectationGapResult", "ExpectationGapDirection",
    "ExpectationGapMateriality", "FavorableMetricDirection", "GovernedExpectationMeasure",
]
