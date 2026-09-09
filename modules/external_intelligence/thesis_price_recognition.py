"""Thesis-specific interpretation layered over the existing market snapshot."""

from dataclasses import dataclass
from enum import Enum


class FundamentalChangeIncorporation(str, Enum):
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    NOT_RECOGNIZED = "NOT_RECOGNIZED"
    LIMITED = "LIMITED"
    MATERIAL = "MATERIAL"
    MOST_OR_ALL = "MOST_OR_ALL"


class ThesisRecognitionDecision(str, Enum):
    HOLD_INSUFFICIENT_EVIDENCE = "HOLD_INSUFFICIENT_EVIDENCE"
    ALLOW_EIP_REVIEW = "ALLOW_EIP_REVIEW"
    VETO_TOO_LATE = "VETO_TOO_LATE"


@dataclass(frozen=True)
class ThesisPriceRecognitionAssessment:
    schema_version: int
    assessment_id: str
    causal_chain_id: str
    regime_assessment_id: str
    market_snapshot_id: str
    incorporation: FundamentalChangeIncorporation
    thesis_related_source_ids: tuple[str, ...]
    thesis_related_dimensions: tuple[str, ...]
    evidence_rationale: str
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class ThesisPriceRecognitionGateResult:
    decision: ThesisRecognitionDecision
    incorporation: FundamentalChangeIncorporation
    reason_codes: tuple[str, ...]
    assessment_id: str
    hard_veto: bool
    non_authority_statement: str


__all__ = [
    "FundamentalChangeIncorporation", "ThesisPriceRecognitionAssessment",
    "ThesisPriceRecognitionGateResult", "ThesisRecognitionDecision",
]
