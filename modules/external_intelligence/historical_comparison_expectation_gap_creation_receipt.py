"""Immutable receipt for one explicitly materialized governed Expectation Gap."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonExpectationGapCreationReceipt:
    schema_version: int
    analysis_fingerprint: str
    assessment_fingerprint: str
    eligibility_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    gap_id: str
    expectation_gap_fingerprint: str
    material_gap: bool
    positive_gap: bool
    negative_gap: bool
    gap_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    creator: str
    rationale: str
    created_at: datetime


__all__ = ["HistoricalComparisonExpectationGapCreationReceipt"]
