"""Immutable human-review candidate for an explicit historical change."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditObservation,
)
from modules.observation.historical_comparison import (
    ChangeDirection,
    ComparisonType,
    Materiality,
)
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


class HistoricalComparisonReviewStatus(str, Enum):
    """Explicit human-review disposition without downstream meaning."""

    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True)
class HistoricalComparisonReviewCandidate:
    """Preserved audit facts awaiting or recording human review."""

    candidate_id: str
    recorded_at: datetime
    current_observation: HistoricalComparisonAuditObservation
    historical_observation: HistoricalComparisonAuditObservation
    selection_basis: HistoricalSelectionBasis | None
    comparison_type: ComparisonType
    change_direction: ChangeDirection
    materiality: Materiality
    delta: float | None
    comparison_provenance: str
    status: HistoricalComparisonReviewStatus = (
        HistoricalComparisonReviewStatus.PENDING
    )
    reviewer: str | None = None
    reviewed_at: datetime | None = None
    review_reason: str | None = None

    @property
    def reviewed(self) -> bool:
        return self.status != HistoricalComparisonReviewStatus.PENDING


__all__ = [
    "HistoricalComparisonReviewCandidate",
    "HistoricalComparisonReviewStatus",
]
