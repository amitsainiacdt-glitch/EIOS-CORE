"""Immutable human decision on one exact Signal validation result."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class HistoricalComparisonSignalValidationDisposition(Enum):
    APPROVED="Approved"
    REJECTED="Rejected"
    DEFERRED="Deferred"

@dataclass(frozen=True)
class HistoricalComparisonSignalValidationDecision:
    schema_version:int
    validation_fingerprint:str
    signal_fingerprint:str
    signal_id:str
    governed_input_fingerprint:str
    evidence_id:str
    disposition:HistoricalComparisonSignalValidationDisposition
    conditions:tuple[str,...]
    monitoring_requirements:tuple[str,...]
    reviewer:str
    rationale:str
    reviewed_at:datetime

__all__=["HistoricalComparisonSignalValidationDecision","HistoricalComparisonSignalValidationDisposition"]
