"""Passive typed results for read-only cross-cycle document reconciliation."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrossCycleDocumentGroup:
    identity_kind: str
    identity_fingerprint: str
    document_hash: str | None
    source_domain: str | None
    source_document_id: str | None
    cycle_ids: tuple[str, ...]
    observation_fingerprints: tuple[str, ...]
    source_urls: tuple[str, ...]
    earliest_published_at: datetime | None
    earliest_filing_at: datetime | None
    earliest_retrieved_at: datetime | None
    latest_retrieved_at: datetime | None


@dataclass(frozen=True)
class CrossCycleDocumentReconciliationPreview:
    preview_fingerprint: str
    total_observations: int
    strong_identity_observations: int
    reconciled_group_count: int
    reconciled_observation_count: int
    unmatched_strong_identity_count: int
    missing_strong_identity_count: int
    groups: tuple[CrossCycleDocumentGroup, ...]
    warnings: tuple[str, ...]


__all__ = [
    "CrossCycleDocumentGroup",
    "CrossCycleDocumentReconciliationPreview",
]
