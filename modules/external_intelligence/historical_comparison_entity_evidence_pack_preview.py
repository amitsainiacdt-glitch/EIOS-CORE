"""Immutable entity-scoped preview of materialized historical EvidenceItems."""

from __future__ import annotations

from dataclasses import dataclass

from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import (
    HistoricalComparisonEvidenceConversionReceipt,
)


@dataclass(frozen=True)
class HistoricalComparisonEntityEvidencePackPreview:
    """Verified receipts and operational workflow gaps for one exact entity."""

    entity: str
    materialized_receipts: tuple[
        HistoricalComparisonEvidenceConversionReceipt, ...
    ]
    supporting_evidence_ids: tuple[str, ...]
    contradictory_evidence_ids: tuple[str, ...]
    missing_assessment_candidate_ids: tuple[str, ...]
    missing_receipt_candidate_ids: tuple[str, ...]

    @property
    def materialized_count(self) -> int:
        return len(self.materialized_receipts)


@dataclass(frozen=True)
class HistoricalComparisonEvidencePackPreviewResult:
    accepted_count: int
    assessment_count: int
    receipt_count: int
    entity_packs: tuple[HistoricalComparisonEntityEvidencePackPreview, ...]


__all__ = [
    "HistoricalComparisonEntityEvidencePackPreview",
    "HistoricalComparisonEvidencePackPreviewResult",
]
