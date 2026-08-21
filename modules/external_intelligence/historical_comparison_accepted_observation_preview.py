"""Immutable preview of an accepted review candidate's source observation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonAcceptedObservationPreview:
    """Exact resolved facts awaiting a separate Evidence assessment."""

    candidate_id: str
    audit_recorded_at: datetime
    reviewer: str
    review_reason: str
    reviewed_at: datetime
    title: str
    description: str
    source: str
    category: str
    entity: str
    confidence: float
    timestamp: datetime
    cycle_id: str | None
    job_id: str | None
    research_intent: str | None
    retrieved_at: datetime | None
    source_url: str | None
    source_domain: str | None
    source_type: str | None
    content_fingerprint: str


__all__ = ["HistoricalComparisonAcceptedObservationPreview"]
