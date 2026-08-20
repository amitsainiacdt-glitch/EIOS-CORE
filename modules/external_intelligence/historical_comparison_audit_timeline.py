"""Typed chronological timeline of comparison audit cycle summaries."""

from __future__ import annotations

from dataclasses import dataclass

from modules.external_intelligence.historical_comparison_cycle_summary import (
    HistoricalComparisonCycleSummary,
)


@dataclass(frozen=True)
class HistoricalComparisonAuditTimeline:
    """Immutable ordered collection of count-only cycle summaries."""

    cycles: tuple[HistoricalComparisonCycleSummary, ...]

    @property
    def cycle_count(self) -> int:
        return len(self.cycles)

    @property
    def record_count(self) -> int:
        return sum(cycle.record_count for cycle in self.cycles)


__all__ = ["HistoricalComparisonAuditTimeline"]
