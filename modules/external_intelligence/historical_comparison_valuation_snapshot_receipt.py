"""Immutable receipt for one governed authoritative valuation snapshot."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonValuationSnapshotReceipt:
    schema_version: int
    entity: str
    valuation_fingerprint: str
    intrinsic_value: float
    fair_value: float
    valuation_method: str
    confidence: float
    source: str
    recorder: str
    rationale: str
    recorded_at: datetime


__all__ = ["HistoricalComparisonValuationSnapshotReceipt"]
