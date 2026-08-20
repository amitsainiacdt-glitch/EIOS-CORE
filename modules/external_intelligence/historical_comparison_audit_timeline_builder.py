"""Build a chronological count-only timeline from typed audit records."""

from __future__ import annotations

from typing import Iterable

from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditRecord,
)
from modules.external_intelligence.historical_comparison_audit_timeline import (
    HistoricalComparisonAuditTimeline,
)
from modules.external_intelligence.historical_comparison_cycle_summarizer import (
    HistoricalComparisonCycleSummarizer,
)


class HistoricalComparisonAuditTimelineBuilder:
    """Group exact runtime timestamps into chronological cycle summaries."""

    def __init__(self, summarizer=None) -> None:
        self.summarizer = (
            summarizer
            if summarizer is not None
            else HistoricalComparisonCycleSummarizer()
        )

    def build(
        self,
        records: Iterable[HistoricalComparisonAuditRecord],
    ) -> HistoricalComparisonAuditTimeline:
        if records is None:
            raise ValueError("records must not be None")

        validated = []
        for record in records:
            if not isinstance(record, HistoricalComparisonAuditRecord):
                raise ValueError(
                    "records must contain HistoricalComparisonAuditRecord"
                )
            validated.append(record)

        cycle_times = set(record.recorded_at for record in validated)

        try:
            ordered_times = sorted(cycle_times)
        except TypeError as exc:
            raise ValueError(
                "audit cycle timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        return HistoricalComparisonAuditTimeline(
            cycles=tuple(
                self.summarizer.summarize(
                    validated,
                    recorded_at=recorded_at,
                )
                for recorded_at in ordered_times
            )
        )


__all__ = ["HistoricalComparisonAuditTimelineBuilder"]
