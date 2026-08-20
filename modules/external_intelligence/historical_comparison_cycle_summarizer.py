"""Count-only summarization for one historical comparison audit cycle."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditRecord,
)
from modules.external_intelligence.historical_comparison_cycle_summary import (
    HistoricalComparisonCycleSummary,
)
from modules.observation.historical_comparison import ComparisonType
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


class HistoricalComparisonCycleSummarizer:
    """Summarize explicit audit facts without inferring importance."""

    def summarize(
        self,
        records: Iterable[HistoricalComparisonAuditRecord],
        *,
        recorded_at: datetime,
    ) -> HistoricalComparisonCycleSummary:
        if records is None:
            raise ValueError("records must not be None")

        if not isinstance(recorded_at, datetime):
            raise ValueError("recorded_at must be a datetime")

        cycle_records = []
        for record in records:
            if not isinstance(record, HistoricalComparisonAuditRecord):
                raise ValueError(
                    "records must contain HistoricalComparisonAuditRecord"
                )
            if record.recorded_at == recorded_at:
                cycle_records.append(record)

        selected_count = sum(
            record.historical_observation is not None
            for record in cycle_records
        )
        ambiguous_count = sum(
            record.historical_observation is None
            and record.eligible_count > 0
            for record in cycle_records
        )
        no_match_count = sum(
            record.historical_observation is None
            and record.eligible_count == 0
            for record in cycle_records
        )

        return HistoricalComparisonCycleSummary(
            recorded_at=recorded_at,
            record_count=len(cycle_records),
            selected_count=selected_count,
            no_match_count=no_match_count,
            ambiguous_count=ambiguous_count,
            comparison_count=sum(
                record.comparison_type is not None
                for record in cycle_records
            ),
            change_detected_count=sum(
                record.change_detected is True
                for record in cycle_records
            ),
            job_id_selection_count=self._count_basis(
                cycle_records,
                HistoricalSelectionBasis.JOB_ID,
            ),
            research_intent_selection_count=self._count_basis(
                cycle_records,
                HistoricalSelectionBasis.RESEARCH_INTENT,
            ),
            legacy_selection_count=self._count_basis(
                cycle_records,
                HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY,
            ),
            no_change_comparison_count=self._count_comparison(
                cycle_records,
                ComparisonType.NO_CHANGE,
            ),
            information_change_comparison_count=(
                self._count_comparison(
                    cycle_records,
                    ComparisonType.INFORMATION_CHANGE,
                )
            ),
            source_change_comparison_count=self._count_comparison(
                cycle_records,
                ComparisonType.SOURCE_CHANGE,
            ),
        )

    @staticmethod
    def _count_basis(records, basis) -> int:
        return sum(
            record.selection_basis == basis
            for record in records
        )

    @staticmethod
    def _count_comparison(records, comparison_type) -> int:
        return sum(
            record.comparison_type == comparison_type
            for record in records
        )


__all__ = ["HistoricalComparisonCycleSummarizer"]
