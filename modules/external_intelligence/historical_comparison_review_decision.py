"""Immutable persisted decision for one historical review candidate."""

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)


@dataclass(frozen=True)
class HistoricalComparisonReviewDecision:
    schema_version: int
    candidate_id: str
    status: HistoricalComparisonReviewStatus
    reviewer: str
    reason: str
    reviewed_at: datetime


__all__ = ["HistoricalComparisonReviewDecision"]
