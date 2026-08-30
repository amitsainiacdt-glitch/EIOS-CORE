"""Passive temporal representation of reviewed public factual Observations."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PublicTemporalEvidenceRecord:
    schema_version: int
    temporal_evidence_id: str
    observation_fingerprint: str
    entity: str
    event_type: str
    statement_posture: str
    event_at: datetime
    known_at: datetime
    time_basis: str
    source_url: str
    document_hash: str
    candidate_id: str
    proposal_id: str
    review_id: str
    observation_title: str
    observation_description: str


@dataclass(frozen=True)
class PublicTemporalEvidenceSeries:
    entity: str
    event_type: str
    record_count: int
    asserted_count: int
    negated_count: int
    uncertain_count: int
    first_event_at: datetime
    latest_event_at: datetime
    records: tuple[PublicTemporalEvidenceRecord, ...]
    warnings: tuple[str, ...]


__all__ = ["PublicTemporalEvidenceRecord", "PublicTemporalEvidenceSeries"]
