"""Passive structural preview consumed by mandatory Meta-Analysis."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class IndicatorEvidenceRelationship(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    CONTEXT_ONLY = "CONTEXT_ONLY"


@dataclass(frozen=True)
class TemporalIndicatorEvidenceLink:
    temporal_evidence_id: str
    indicator_id: str
    independence_group_id: str
    relationship: IndicatorEvidenceRelationship
    rationale: str


class TemporalIndicatorStructuralState(str, Enum):
    INSUFFICIENT = "INSUFFICIENT"
    FORMING = "FORMING"
    STRUCTURALLY_READY_FOR_META = "STRUCTURALLY_READY_FOR_META"
    CONTRADICTED = "CONTRADICTED"


@dataclass(frozen=True)
class TemporalLeadingIndicatorPreview:
    preview_fingerprint: str
    indicator_id: str
    indicator_version: int
    entity: str
    sector_id: str
    event_types: tuple[str, ...]
    temporal_evidence_ids: tuple[str, ...]
    observation_fingerprints: tuple[str, ...]
    supporting_count: int
    contradicting_count: int
    context_count: int
    independence_group_ids: tuple[str, ...]
    independence_group_count: int
    required_independence_groups: int
    persistent_observation_count: int
    required_persistent_observations: int
    observed_span_days: int
    expected_persistence_days: int
    earliest_event_at: datetime
    latest_event_at: datetime
    expected_lead_time_quarters: tuple[int, int]
    structural_state: TemporalIndicatorStructuralState
    reason_codes: tuple[str, ...]
    warnings: tuple[str, ...]
    meta_analysis_required: bool = True


__all__ = ["IndicatorEvidenceRelationship", "TemporalIndicatorEvidenceLink", "TemporalIndicatorStructuralState", "TemporalLeadingIndicatorPreview"]
