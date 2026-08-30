"""Passive, source-grounded fact candidate from one admitted public document."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicFactualCandidate:
    schema_version: int
    candidate_id: str
    event_type: str
    statement_posture: str
    subject_entity: str
    mentioned_entities: tuple[str, ...]
    explicit_amounts: tuple[str, ...]
    explicit_dates: tuple[str, ...]
    source_passage: str
    passage_start: int
    passage_end: int
    matched_triggers: tuple[str, ...]
    acquisition_id: str
    extraction_id: str
    source_url: str
    document_hash: str
    extracted_content_fingerprint: str
    extraction_method: str


@dataclass(frozen=True)
class PublicFactualCandidatePreview:
    acquisition_id: str
    extraction_id: str
    candidate_count: int
    candidates: tuple[PublicFactualCandidate, ...]
    warnings: tuple[str, ...]


__all__ = ["PublicFactualCandidate", "PublicFactualCandidatePreview"]
