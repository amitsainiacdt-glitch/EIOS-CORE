"""Deterministic maximum confidence permitted by evidence quality."""

from dataclasses import dataclass
from enum import Enum


class EvidenceDirectness(str,Enum):
    DIRECT="DIRECT"
    PROXY="PROXY"
    INFERRED="INFERRED"


@dataclass(frozen=True)
class EvidenceConfidenceInputs:
    primary_authority: bool
    age_days: int
    maximum_age_days: int
    directness: EvidenceDirectness
    geography_exact_match: bool
    period_comparable: bool
    schema_compatible: bool
    hash_bound_lineage: bool
    independent_source_group_count: int
    unresolved_material_contradictions: int
    missing_critical_layers: int


@dataclass(frozen=True)
class EvidenceConfidenceCeiling:
    maximum_confidence_percent: int
    confidence_eligible: bool
    reason_codes: tuple[str,...]
    non_authority_statement: str="Confidence ceiling only; it does not estimate probability, expected return, or position size."


def calculate_evidence_confidence_ceiling(inputs):
    if not isinstance(inputs,EvidenceConfidenceInputs): raise ValueError("evidence confidence inputs are required")
    if inputs.age_days<0 or inputs.maximum_age_days<0 or inputs.independent_source_group_count<0 or inputs.unresolved_material_contradictions<0 or inputs.missing_critical_layers<0: raise ValueError("confidence inputs must be non-negative")
    directness=inputs.directness if isinstance(inputs.directness,EvidenceDirectness) else EvidenceDirectness(inputs.directness)
    score=95; reasons=[]; eligible=True
    if not inputs.primary_authority: score-=20; reasons.append("NON_PRIMARY_SOURCE")
    if inputs.age_days>inputs.maximum_age_days: score-=25; reasons.append("STALE_EVIDENCE")
    elif inputs.maximum_age_days and inputs.age_days>0.75*inputs.maximum_age_days: score-=8; reasons.append("NEAR_FRESHNESS_LIMIT")
    if directness==EvidenceDirectness.PROXY: score-=15; reasons.append("PROXY_EVIDENCE")
    elif directness==EvidenceDirectness.INFERRED: score-=30; reasons.append("INFERRED_EVIDENCE")
    if not inputs.geography_exact_match: score-=15; reasons.append("GEOGRAPHY_MISMATCH")
    if not inputs.period_comparable: score-=15; reasons.append("PERIOD_NOT_COMPARABLE")
    if not inputs.schema_compatible: score-=35; reasons.append("SCHEMA_NOT_COMPATIBLE"); eligible=False
    if not inputs.hash_bound_lineage: score-=35; reasons.append("LINEAGE_NOT_HASH_BOUND"); eligible=False
    if inputs.independent_source_group_count<2: score-=20; reasons.append("INDEPENDENT_SUPPORT_INSUFFICIENT")
    score-=min(15*inputs.unresolved_material_contradictions,30)
    if inputs.unresolved_material_contradictions: reasons.append("MATERIAL_CONTRADICTIONS_UNRESOLVED")
    score-=min(20*inputs.missing_critical_layers,40)
    if inputs.missing_critical_layers: reasons.append("CRITICAL_EVIDENCE_LAYERS_MISSING")
    ceiling=max(5,min(95,score))
    if ceiling<50: eligible=False; reasons.append("EVIDENCE_CEILING_BELOW_RESEARCH_THRESHOLD")
    return EvidenceConfidenceCeiling(ceiling,eligible,tuple(dict.fromkeys(reasons)))


__all__=["EvidenceDirectness","EvidenceConfidenceInputs","EvidenceConfidenceCeiling","calculate_evidence_confidence_ceiling"]
