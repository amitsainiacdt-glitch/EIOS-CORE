"""Passive proposal for turning one validated public fact into an Observation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFactualObservationProposal:
    schema_version: int
    proposal_id: str
    proposal_fingerprint: str
    candidate_id: str
    title: str
    description: str
    entity: str
    category: str
    source_url: str
    event_type: str
    statement_posture: str
    acquisition_id: str
    extraction_id: str
    document_hash: str
    extracted_content_fingerprint: str
    extraction_method: str
    explicit_amounts: tuple[str, ...]
    explicit_dates: tuple[str, ...]
    requires_human_review: bool = True


__all__ = ["PublicFactualObservationProposal"]
