"""Immutable human review of one Signal maturity transition."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from modules.opportunity.signals.signal_model import SignalStage

class HistoricalComparisonSignalStageReviewDisposition(Enum):
 APPROVED="Approved"
 REJECTED="Rejected"
 DEFERRED="Deferred"

@dataclass(frozen=True)
class HistoricalComparisonSignalStageReview:
 schema_version:int
 support_fingerprint:str
 signal_id:str
 signal_fingerprint:str
 validation_fingerprint:str
 current_stage:SignalStage
 target_stage:SignalStage
 disposition:HistoricalComparisonSignalStageReviewDisposition
 conditions:tuple[str,...]
 monitoring_requirements:tuple[str,...]
 reviewer:str
 rationale:str
 reviewed_at:datetime

__all__=["HistoricalComparisonSignalStageReview","HistoricalComparisonSignalStageReviewDisposition"]
