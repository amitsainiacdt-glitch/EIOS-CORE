"""
EIOS
Everest Investment Operating System

Historical Comparison Model
===========================

Purpose
-------
Represents the comparison between a current observation and a
historical observation.

Architecture
------------

Current Observation
        +
Historical Observation
        ↓
HistoricalComparison

Design Principles
-----------------
- Passive typed data model only.
- Does not perform comparison logic.
- Does not modify Observation objects.
- Preserves both current and historical observations.
- Preserves provenance.
- Does not create Evidence.
- Does not create Signals.
- Does not create Catalysts.
- Does not perform valuation.
- Does not make investment decisions.

Important
---------
HistoricalComparison is distinct from ObservationNovelty.

ObservationNovelty asks:

    "Have I seen this observation before?"

HistoricalComparison asks:

    "How does the current observation differ from the
     historical observation?"
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from modules.observation.observation import Observation


class ComparisonType(str, Enum):
    """
    Type of historical comparison.
    """

    NO_CHANGE = "NO_CHANGE"

    INFORMATION_CHANGE = "INFORMATION_CHANGE"

    SOURCE_CHANGE = "SOURCE_CHANGE"


class ChangeDirection(str, Enum):
    """
    Direction of an identified information change.

    Direction remains UNKNOWN unless the existing observation
    data explicitly supports a directional conclusion.
    """

    UNKNOWN = "UNKNOWN"

    POSITIVE = "POSITIVE"

    NEGATIVE = "NEGATIVE"

    NEUTRAL = "NEUTRAL"


class Materiality(str, Enum):
    """
    Conservative materiality classification.

    The initial foundation does not infer financial materiality
    from arbitrary text.
    """

    UNKNOWN = "UNKNOWN"

    IMMATERIAL = "IMMATERIAL"

    MATERIAL = "MATERIAL"


@dataclass(frozen=True)
class HistoricalComparison:
    """
    Immutable comparison between two observations.
    """

    current_observation: Observation

    historical_observation: Observation

    comparison_type: ComparisonType

    change_detected: bool = False

    change_direction: ChangeDirection = (
        ChangeDirection.UNKNOWN
    )

    materiality: Materiality = (
        Materiality.UNKNOWN
    )

    delta: float | None = None

    provenance: str = ""


__all__ = [
    "HistoricalComparison",
    "ComparisonType",
    "ChangeDirection",
    "Materiality",
]