"""A deterministic bundle of factual proposals awaiting human decisions."""

from dataclasses import dataclass

from modules.external_intelligence.public_factual_observation_proposal import PublicFactualObservationProposal


@dataclass(frozen=True)
class DeferredPublicFactualCandidate:
    candidate_id: str
    event_type: str
    statement_posture: str
    source_passage: str
    validation_decision: str
    reason_codes: tuple[str, ...]
    requires_corroboration: bool


@dataclass(frozen=True)
class PublicFactualObservationReviewPackage:
    schema_version: int
    package_id: str
    package_fingerprint: str
    acquisition_id: str
    extraction_id: str
    document_hash: str
    source_url: str
    proposals: tuple[PublicFactualObservationProposal, ...]
    deferred_candidates: tuple[DeferredPublicFactualCandidate, ...]
    excluded_candidate_ids: tuple[str, ...]
    package_status: str
    requires_human_review: bool = True
    creates_observation: bool = False


__all__ = ["DeferredPublicFactualCandidate", "PublicFactualObservationReviewPackage"]
