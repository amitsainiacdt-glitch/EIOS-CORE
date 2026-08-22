"""Immutable human decision on one exact Expectation Gap analysis."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class HistoricalComparisonExpectationGapAssessmentDisposition(Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEFERRED = "Deferred"


@dataclass(frozen=True)
class HistoricalComparisonExpectationGapAssessmentDecision:
    schema_version: int
    analysis_fingerprint: str
    eligibility_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    creation_receipt_fingerprint: str
    gap_id: str
    material_gap: bool
    positive_gap: bool
    negative_gap: bool
    gap_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    disposition: HistoricalComparisonExpectationGapAssessmentDisposition
    conditions: tuple[str, ...]
    monitoring_requirements: tuple[str, ...]
    reviewer: str
    rationale: str
    reviewed_at: datetime


__all__ = [
    "HistoricalComparisonExpectationGapAssessmentDecision",
    "HistoricalComparisonExpectationGapAssessmentDisposition",
]
