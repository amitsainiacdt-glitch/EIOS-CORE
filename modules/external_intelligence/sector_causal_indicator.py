"""Passive, versioned sector causal-indicator knowledge contract."""

from dataclasses import dataclass
from enum import Enum


class CausalEffectDirection(str, Enum):
    SUPPORTIVE = "SUPPORTIVE"
    ADVERSE = "ADVERSE"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"


@dataclass(frozen=True)
class SectorCausalIndicatorDefinition:
    schema_version: int
    indicator_id: str
    version: int
    name: str
    sector_ids: tuple[str, ...]
    applicable_event_types: tuple[str, ...]
    economic_variable: str
    expected_direction: CausalEffectDirection
    lead_time_quarters_min: int
    lead_time_quarters_max: int
    causal_mechanism: str
    earnings_channels: tuple[str, ...]
    company_archetypes: tuple[str, ...]
    preferred_primary_source_types: tuple[str, ...]
    corroborating_source_types: tuple[str, ...]
    independence_group_template: str
    minimum_independence_groups: int
    minimum_persistent_observations: int
    expected_persistence_days: int
    known_false_positive_conditions: tuple[str, ...]
    contradiction_tests: tuple[str, ...]
    kill_tests: tuple[str, ...]
    enabled: bool = True
    required_upstream_indicator_ids: tuple[str, ...] = ()


__all__ = ["CausalEffectDirection", "SectorCausalIndicatorDefinition"]
