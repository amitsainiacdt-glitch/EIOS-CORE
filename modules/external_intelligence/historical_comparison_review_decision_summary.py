"""Immutable count-only summary of historical comparison review decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonReviewCount:
    """One deterministic label and count."""

    label: str
    count: int


@dataclass(frozen=True)
class HistoricalComparisonReviewDecisionSummary:
    """Operational review counts without financial interpretation."""

    candidate_count: int
    pending_count: int
    decided_count: int
    reviewed_count: int
    accepted_count: int
    rejected_count: int
    deferred_count: int
    by_entity: tuple[HistoricalComparisonReviewCount, ...]
    by_category: tuple[HistoricalComparisonReviewCount, ...]
    by_comparison_type: tuple[HistoricalComparisonReviewCount, ...]
    by_reviewer: tuple[HistoricalComparisonReviewCount, ...]
    by_review_date: tuple[HistoricalComparisonReviewCount, ...]
    unresolved_candidate_ids: tuple[str, ...]
    earliest_reviewed_at: datetime | None
    latest_reviewed_at: datetime | None


__all__ = [
    "HistoricalComparisonReviewCount",
    "HistoricalComparisonReviewDecisionSummary",
]
