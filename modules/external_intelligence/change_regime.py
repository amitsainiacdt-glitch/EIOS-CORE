"""Passive change-regime classification for a validated causal chain."""

from dataclasses import dataclass
from enum import Enum


class ChangeRegime(str, Enum):
    STRUCTURAL = "STRUCTURAL"
    CYCLICAL = "CYCLICAL"
    TEMPORARY_DISRUPTION = "TEMPORARY_DISRUPTION"
    SEASONAL_EFFECT = "SEASONAL_EFFECT"
    STATISTICAL_NOISE = "STATISTICAL_NOISE"
    SPECULATIVE_NARRATIVE = "SPECULATIVE_NARRATIVE"


class RegimeConfidence(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


@dataclass(frozen=True)
class ChangeRegimeAssessment:
    schema_version: int
    assessment_id: str
    causal_chain_id: str
    regime: ChangeRegime
    confidence: RegimeConfidence
    input_temporal_evidence_ids: tuple[str, ...]
    classification_basis: tuple[str, ...]
    alternative_explanations: tuple[str, ...]
    distinguishing_tests: tuple[str, ...]
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


__all__ = ["ChangeRegime", "ChangeRegimeAssessment", "RegimeConfidence"]
