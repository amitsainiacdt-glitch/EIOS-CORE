"""Typed read model for one historical comparison audit record."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from modules.observation.historical_comparison import (
    ChangeDirection,
    ComparisonType,
    Materiality,
)
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


@dataclass(frozen=True)
class HistoricalComparisonAuditObservation:
    """Stable observation reference preserved in an audit record."""

    title: str
    entity: str
    category: str
    timestamp: datetime
    source: str
    job_id: str | None
    research_intent: str | None
    content_fingerprint: str | None


@dataclass(frozen=True)
class HistoricalComparisonAuditRecord:
    """Validated schema-version-one historical comparison audit record."""

    schema_version: int
    recorded_at: datetime
    current_observation: HistoricalComparisonAuditObservation
    historical_observation: (
        HistoricalComparisonAuditObservation | None
    )
    selection_basis: HistoricalSelectionBasis | None
    eligible_count: int
    selection_reason: str
    comparison_type: ComparisonType | None
    change_detected: bool | None
    change_direction: ChangeDirection | None
    materiality: Materiality | None
    delta: float | None
    comparison_provenance: str | None


__all__ = [
    "HistoricalComparisonAuditObservation",
    "HistoricalComparisonAuditRecord",
]
