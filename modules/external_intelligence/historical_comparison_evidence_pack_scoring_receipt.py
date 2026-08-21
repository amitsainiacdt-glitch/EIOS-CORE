"""Immutable receipt for an explicit entity Evidence pack score."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonEvidencePackScoringReceipt:
    schema_version: int
    pack_fingerprint: str
    entity: str
    supporting_evidence_ids: tuple[str, ...]
    contradictory_evidence_ids: tuple[str, ...]
    evidence_score: float
    confidence: float
    sufficiently_supported: bool
    evidence_gaps: tuple[str, ...]
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    warnings: tuple[str, ...]
    analyst: str
    analyzed_at: datetime


__all__ = ["HistoricalComparisonEvidencePackScoringReceipt"]
