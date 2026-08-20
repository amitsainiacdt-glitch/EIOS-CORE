"""Conservative count-only summary of one comparison audit cycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonCycleSummary:
    """Aggregate operational counts without financial interpretation."""

    recorded_at: datetime
    record_count: int
    selected_count: int
    no_match_count: int
    ambiguous_count: int
    comparison_count: int
    change_detected_count: int
    job_id_selection_count: int
    research_intent_selection_count: int
    legacy_selection_count: int
    no_change_comparison_count: int
    information_change_comparison_count: int
    source_change_comparison_count: int


__all__ = ["HistoricalComparisonCycleSummary"]
