"""
EIOS
Everest Investment Operating System

Historical Observation Selector
================================

Selects a conservative historical candidate for an explicit
current Observation.

Selection Policy
----------------
- Entity and category must match after conservative normalization.
- A candidate must have a timestamp strictly earlier than current.
- Exact provenance job ID matches are preferred.
- Matching research intent is used when no job ID match exists.
- Provenance-free legacy candidates are the final fallback.
- Conflicting populated job IDs are never comparable.
- The uniquely most recent eligible observation is selected.
- A tie at the most recent timestamp is treated as ambiguous.
- Title, description, source, confidence, and financial meaning are
  not used to infer comparability.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable

from .observation import Observation


class HistoricalSelectionBasis(str, Enum):
    """Provenance boundary used to select historical candidates."""

    JOB_ID = "JOB_ID"
    RESEARCH_INTENT = "RESEARCH_INTENT"
    LEGACY_ENTITY_CATEGORY = "LEGACY_ENTITY_CATEGORY"


@dataclass(frozen=True)
class HistoricalObservationSelection:
    """Auditable result of historical candidate selection."""

    current_observation: Observation
    selected_observation: Observation | None
    eligible_count: int
    reason: str
    selection_basis: HistoricalSelectionBasis | None = None


class HistoricalObservationSelector:
    """Select one unambiguous prior observation when possible."""

    def select(
        self,
        current_observation: Observation,
        observations: Iterable[Observation],
    ) -> HistoricalObservationSelection:
        if not isinstance(current_observation, Observation):
            raise ValueError(
                "current_observation must be an Observation"
            )

        if not isinstance(
            current_observation.timestamp,
            datetime,
        ):
            raise ValueError(
                "current_observation timestamp must be a datetime"
            )

        if observations is None:
            raise ValueError(
                "observations must not be None"
            )

        current_entity = self._normalize(
            current_observation.entity
        )
        current_category = self._normalize(
            current_observation.category
        )

        if not current_entity or not current_category:
            return HistoricalObservationSelection(
                current_observation=current_observation,
                selected_observation=None,
                eligible_count=0,
                reason=(
                    "Current entity and category are required for "
                    "historical selection."
                ),
            )

        job_matches = []
        intent_matches = []
        legacy_matches = []

        current_job_id = self._provenance_value(
            current_observation,
            "job_id",
        )
        current_intent = self._provenance_value(
            current_observation,
            "research_intent",
        )

        for candidate in observations:
            if candidate is None or candidate is current_observation:
                continue

            if not isinstance(candidate, Observation):
                continue

            if not isinstance(candidate.timestamp, datetime):
                continue

            if self._as_utc(candidate.timestamp) >= self._as_utc(
                current_observation.timestamp
            ):
                continue

            if self._normalize(candidate.entity) != current_entity:
                continue

            if self._normalize(candidate.category) != current_category:
                continue

            candidate_job_id = self._provenance_value(
                candidate,
                "job_id",
            )
            candidate_intent = self._provenance_value(
                candidate,
                "research_intent",
            )

            if (
                current_job_id
                and candidate_job_id
                and current_job_id != candidate_job_id
            ):
                continue

            if (
                current_job_id
                and candidate_job_id == current_job_id
            ):
                job_matches.append(candidate)
                continue

            if (
                current_intent
                and candidate_intent == current_intent
            ):
                intent_matches.append(candidate)
                continue

            if candidate.provenance is None:
                legacy_matches.append(candidate)

        eligible, selection_basis = self._preferred_candidates(
            job_matches=job_matches,
            intent_matches=intent_matches,
            legacy_matches=legacy_matches,
        )

        if not eligible:
            return HistoricalObservationSelection(
                current_observation=current_observation,
                selected_observation=None,
                eligible_count=0,
                reason=(
                    "No strictly earlier observation matches "
                    "the current entity, category, and provenance "
                    "selection policy."
                ),
            )

        latest_timestamp = max(
            self._as_utc(candidate.timestamp)
            for candidate in eligible
        )

        latest_candidates = [
            candidate
            for candidate in eligible
            if self._as_utc(candidate.timestamp) == latest_timestamp
        ]

        if len(latest_candidates) != 1:
            return HistoricalObservationSelection(
                current_observation=current_observation,
                selected_observation=None,
                eligible_count=len(eligible),
                reason=(
                    "Historical selection is ambiguous because "
                    "multiple latest candidates share a timestamp."
                ),
                selection_basis=selection_basis,
            )

        return HistoricalObservationSelection(
            current_observation=current_observation,
            selected_observation=latest_candidates[0],
            eligible_count=len(eligible),
            reason=(
                "Selected the uniquely most recent strictly earlier "
                "observation from the preferred provenance boundary."
            ),
            selection_basis=selection_basis,
        )

    @staticmethod
    def _preferred_candidates(
        *,
        job_matches: list[Observation],
        intent_matches: list[Observation],
        legacy_matches: list[Observation],
    ) -> tuple[
        list[Observation],
        HistoricalSelectionBasis | None,
    ]:
        if job_matches:
            return job_matches, HistoricalSelectionBasis.JOB_ID

        if intent_matches:
            return (
                intent_matches,
                HistoricalSelectionBasis.RESEARCH_INTENT,
            )

        if legacy_matches:
            return (
                legacy_matches,
                HistoricalSelectionBasis.LEGACY_ENTITY_CATEGORY,
            )

        return [], None

    @classmethod
    def _provenance_value(
        cls,
        observation: Observation,
        field: str,
    ) -> str:
        provenance = observation.provenance

        if provenance is None:
            return ""

        return cls._normalize(
            getattr(provenance, field, None)
        )

    @staticmethod
    def _normalize(value: str | None) -> str:
        if value is None:
            return ""

        return re.sub(
            r"\s+",
            " ",
            str(value).strip(),
        ).casefold()

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        """Normalize for ordering without mutating persisted models."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


__all__ = [
    "HistoricalObservationSelection",
    "HistoricalObservationSelector",
    "HistoricalSelectionBasis",
]
