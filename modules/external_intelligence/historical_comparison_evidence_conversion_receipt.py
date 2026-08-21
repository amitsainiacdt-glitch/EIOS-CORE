"""Immutable receipt for one explicit EvidenceItem materialization."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonEvidenceConversionReceipt:
    schema_version: int
    candidate_id: str
    observation_fingerprint: str
    evidence_id: str
    statement: str
    source: str
    category: str
    direction: str
    strength: float
    confidence: float
    independent_confirmation: int
    is_primary_source: bool
    is_time_sensitive: bool
    notes: str
    reviewer: str
    reviewed_at: datetime
    assessor: str
    assessed_at: datetime
    converter: str
    converted_at: datetime


__all__ = ["HistoricalComparisonEvidenceConversionReceipt"]
