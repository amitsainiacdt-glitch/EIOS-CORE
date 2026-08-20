"""Read-only exact-match filtering for typed comparison audit records."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable

from modules.external_intelligence.historical_comparison_audit_filter import (
    HistoricalComparisonAuditFilter,
)
from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditRecord,
)
from modules.observation.historical_comparison import ComparisonType
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


class HistoricalComparisonAuditFilterEngine:
    """Filter validated records without altering source data or meaning."""

    def filter(
        self,
        records: Iterable[HistoricalComparisonAuditRecord],
        criteria: HistoricalComparisonAuditFilter,
    ) -> tuple[HistoricalComparisonAuditRecord, ...]:
        if records is None:
            raise ValueError("records must not be None")

        if not isinstance(criteria, HistoricalComparisonAuditFilter):
            raise ValueError(
                "criteria must be a HistoricalComparisonAuditFilter"
            )

        self._validate_criteria(criteria)
        selected = []

        for record in records:
            if not isinstance(record, HistoricalComparisonAuditRecord):
                raise ValueError(
                    "records must contain HistoricalComparisonAuditRecord"
                )

            if self._matches(record, criteria):
                selected.append(record)

        return tuple(selected)

    @classmethod
    def _matches(cls, record, criteria) -> bool:
        current = record.current_observation

        if not cls._text_matches(current.entity, criteria.entity):
            return False
        if not cls._text_matches(current.category, criteria.category):
            return False
        if not cls._text_matches(current.job_id, criteria.job_id):
            return False
        if not cls._text_matches(
            current.research_intent,
            criteria.research_intent,
        ):
            return False
        if (
            criteria.selection_basis is not None
            and record.selection_basis != criteria.selection_basis
        ):
            return False
        if (
            criteria.comparison_type is not None
            and record.comparison_type != criteria.comparison_type
        ):
            return False

        try:
            if (
                criteria.recorded_from is not None
                and record.recorded_at < criteria.recorded_from
            ):
                return False
            if (
                criteria.recorded_to is not None
                and record.recorded_at > criteria.recorded_to
            ):
                return False
        except TypeError as exc:
            raise ValueError(
                "audit record and filter timestamps must use a "
                "consistent timezone-awareness policy"
            ) from exc

        return True

    @classmethod
    def _text_matches(cls, value, expected) -> bool:
        if expected is None:
            return True
        return cls._normalize(value) == cls._normalize(expected)

    @staticmethod
    def _normalize(value) -> str:
        if value is None:
            return ""
        return re.sub(r"\s+", " ", str(value).strip()).casefold()

    @classmethod
    def _validate_criteria(cls, criteria) -> None:
        for name in (
            "entity",
            "category",
            "job_id",
            "research_intent",
        ):
            value = getattr(criteria, name)
            if value is not None:
                if not isinstance(value, str):
                    raise ValueError(f"{name} filter must be a string")
                if not cls._normalize(value):
                    raise ValueError(f"{name} filter must not be empty")

        for name in ("recorded_from", "recorded_to"):
            value = getattr(criteria, name)
            if value is not None and not isinstance(value, datetime):
                raise ValueError(f"{name} filter must be a datetime")

        if (
            criteria.selection_basis is not None
            and not isinstance(
                criteria.selection_basis,
                HistoricalSelectionBasis,
            )
        ):
            raise ValueError("selection_basis filter is invalid")

        if (
            criteria.comparison_type is not None
            and not isinstance(criteria.comparison_type, ComparisonType)
        ):
            raise ValueError("comparison_type filter is invalid")

        try:
            if (
                criteria.recorded_from is not None
                and criteria.recorded_to is not None
                and criteria.recorded_from > criteria.recorded_to
            ):
                raise ValueError(
                    "recorded_from must not be later than recorded_to"
                )
        except TypeError as exc:
            raise ValueError(
                "filter bounds must use a consistent "
                "timezone-awareness policy"
            ) from exc


__all__ = ["HistoricalComparisonAuditFilterEngine"]
