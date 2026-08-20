"""Typed criteria for read-only historical comparison audit filtering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from modules.observation.historical_comparison import ComparisonType
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


@dataclass(frozen=True)
class HistoricalComparisonAuditFilter:
    """Optional exact-match provenance and runtime bounds."""

    entity: str | None = None
    category: str | None = None
    job_id: str | None = None
    research_intent: str | None = None
    selection_basis: HistoricalSelectionBasis | None = None
    comparison_type: ComparisonType | None = None
    recorded_from: datetime | None = None
    recorded_to: datetime | None = None


__all__ = ["HistoricalComparisonAuditFilter"]
