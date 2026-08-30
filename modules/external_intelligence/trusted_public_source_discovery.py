"""Read-only candidates discovered from an audited trusted public landing page."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrustedPublicDocumentCandidate:
    schema_version: int
    candidate_id: str
    source_id: str
    landing_acquisition_id: str
    landing_acquisition_fingerprint: str
    landing_document_hash: str
    url: str
    link_text: str
    document_type: str
    date_tokens: tuple[str, ...]
    matched_topics: tuple[str, ...]
    discovery_reasons: tuple[str, ...]
    relevance_tier: str
    candidate_fingerprint: str


@dataclass(frozen=True)
class TrustedPublicDiscoveryPreview:
    source_id: str
    landing_acquisition_id: str
    query_topics: tuple[str, ...]
    candidates: tuple[TrustedPublicDocumentCandidate, ...]
    rejected_link_count: int
    creates_evidence: bool = False
    creates_observation: bool = False


__all__ = ["TrustedPublicDocumentCandidate", "TrustedPublicDiscoveryPreview"]
