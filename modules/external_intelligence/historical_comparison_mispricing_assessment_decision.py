"""Immutable human decision on one exact governed Mispricing analysis."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class HistoricalComparisonMispricingAssessmentDisposition(Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEFERRED = "Deferred"


@dataclass(frozen=True)
class HistoricalComparisonMispricingAssessmentDecision:
    schema_version: int
    analysis_fingerprint: str
    eligibility_fingerprint: str
    valuation_fingerprint: str
    valuation_receipt_fingerprint: str
    expectation_gap_fingerprint: str
    catalyst_fingerprint: str
    company: str
    potential_mispricing: bool
    mispricing_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    disposition: HistoricalComparisonMispricingAssessmentDisposition
    conditions: tuple[str, ...]
    monitoring_requirements: tuple[str, ...]
    reviewer: str
    rationale: str
    reviewed_at: datetime


__all__ = [
    "HistoricalComparisonMispricingAssessmentDecision",
    "HistoricalComparisonMispricingAssessmentDisposition",
]
