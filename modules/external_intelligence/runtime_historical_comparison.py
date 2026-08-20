"""Typed result for opt-in runtime historical comparison."""

from __future__ import annotations

from dataclasses import dataclass

from modules.observation.historical_comparison import (
    HistoricalComparison,
)
from modules.observation.historical_observation_selector import (
    HistoricalObservationSelection,
)
from modules.observation.observation import Observation


@dataclass(frozen=True)
class RuntimeHistoricalComparison:
    """
    Preserves selection and optional comparison for one observation.
    """

    current_observation: Observation
    selection: HistoricalObservationSelection
    comparison: HistoricalComparison | None


__all__ = [
    "RuntimeHistoricalComparison",
]
