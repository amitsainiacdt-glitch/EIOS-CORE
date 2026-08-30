"""Read-only manifest for reviewing EIP inputs in the existing Evidence path."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EIPEvidenceReviewReference:
    temporal_evidence_id: str
    observation_fingerprint: str
    entity: str
    event_type: str
    statement_posture: str
    event_at: datetime
    known_at: datetime
    source_url: str
    observation_title: str
    observation_description: str


@dataclass(frozen=True)
class EIPEvidenceReviewCandidate:
    schema_version: int
    candidate_id: str
    candidate_fingerprint: str
    classification_id: str
    classification_fingerprint: str
    eip_review_id: str
    eip_stage: str
    pre_inflection_preview_id: str
    pre_inflection_fingerprint: str
    meta_assessment_id: str
    meta_assessment_fingerprint: str
    entity_scope: tuple[str, ...]
    sector_scope: tuple[str, ...]
    causal_indicator_ids: tuple[str, ...]
    evidence_references: tuple[EIPEvidenceReviewReference, ...]
    confirmation_requirements: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    requires_human_evidence_assessment: bool
    non_authority_statement: str


__all__ = ["EIPEvidenceReviewCandidate", "EIPEvidenceReviewReference"]
