"""Immutable human Evidence assessment for an accepted historical review."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonEvidenceAssessment:
    """Persisted assessment metadata that is not itself Evidence."""

    schema_version: int
    candidate_id: str
    observation_fingerprint: str
    category: str
    direction: str
    strength: float
    confidence: float
    independent_confirmation: int
    is_primary_source: bool
    is_time_sensitive: bool
    assessor: str
    rationale: str
    assessed_at: datetime


__all__ = ["HistoricalComparisonEvidenceAssessment"]
