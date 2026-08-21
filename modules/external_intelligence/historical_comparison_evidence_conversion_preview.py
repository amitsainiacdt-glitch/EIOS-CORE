"""Immutable preview of fields eligible for later Evidence conversion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonEvidenceConversionPreview:
    """Would-be EvidenceItem fields plus preserved human lineage."""

    candidate_id: str
    observation_fingerprint: str
    proposed_evidence_id: str
    statement: str
    source: str
    category: str
    direction: str
    strength: float
    confidence: float
    independent_confirmation: int
    is_primary_source: bool
    is_time_sensitive: bool
    notes: str
    entity: str
    observation_title: str
    observation_timestamp: datetime
    reviewer: str
    reviewed_at: datetime
    assessor: str
    assessed_at: datetime


@dataclass(frozen=True)
class HistoricalComparisonEvidenceConversionEligibility:
    """Eligible projections and accepted candidates still lacking assessment."""

    accepted_count: int
    eligible_previews: tuple[HistoricalComparisonEvidenceConversionPreview, ...]
    missing_assessment_candidate_ids: tuple[str, ...]

    @property
    def eligible_count(self) -> int:
        return len(self.eligible_previews)


__all__ = [
    "HistoricalComparisonEvidenceConversionEligibility",
    "HistoricalComparisonEvidenceConversionPreview",
]
