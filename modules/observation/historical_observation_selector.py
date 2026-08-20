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
- The uniquely most recent eligible observation is selected.
- A tie at the most recent timestamp is treated as ambiguous.
- Title, description, source, confidence, and financial meaning are
  not used to infer comparability.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .observation import Observation


@dataclass(frozen=True)
class HistoricalObservationSelection:
    """Auditable result of historical candidate selection."""

    current_observation: Observation
    selected_observation: Observation | None
    eligible_count: int
    reason: str


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

        eligible = []

        for candidate in observations:
            if candidate is None or candidate is current_observation:
                continue

            if not isinstance(candidate, Observation):
                continue

            if not isinstance(candidate.timestamp, datetime):
                continue

            try:
                if candidate.timestamp >= current_observation.timestamp:
                    continue
            except TypeError:
                # Naive and timezone-aware timestamps cannot be
                # ordered safely without an explicit timezone policy.
                continue

            if self._normalize(candidate.entity) != current_entity:
                continue

            if self._normalize(candidate.category) != current_category:
                continue

            eligible.append(candidate)

        if not eligible:
            return HistoricalObservationSelection(
                current_observation=current_observation,
                selected_observation=None,
                eligible_count=0,
                reason=(
                    "No strictly earlier observation matches "
                    "the current entity and category."
                ),
            )

        latest_timestamp = max(
            candidate.timestamp
            for candidate in eligible
        )

        latest_candidates = [
            candidate
            for candidate in eligible
            if candidate.timestamp == latest_timestamp
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
            )

        return HistoricalObservationSelection(
            current_observation=current_observation,
            selected_observation=latest_candidates[0],
            eligible_count=len(eligible),
            reason=(
                "Selected the uniquely most recent strictly earlier "
                "observation with matching entity and category."
            ),
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


__all__ = [
    "HistoricalObservationSelection",
    "HistoricalObservationSelector",
]
