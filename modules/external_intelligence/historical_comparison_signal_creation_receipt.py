"""Immutable receipt for one explicitly created historical-comparison Signal."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class HistoricalComparisonSignalCreationReceipt:
    schema_version: int
    governed_input_fingerprint: str
    pack_fingerprint: str
    evidence_id: str
    signal_id: str
    signal_fingerprint: str
    title: str
    domain: str
    signal_type: str
    direction: str
    stage: str
    horizon: str
    creator: str
    created_at: datetime

__all__ = ["HistoricalComparisonSignalCreationReceipt"]
