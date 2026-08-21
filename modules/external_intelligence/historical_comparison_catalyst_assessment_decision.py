"""Immutable human decision on one exact Catalyst analysis preview."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class HistoricalComparisonCatalystAssessmentDisposition(Enum):
 APPROVED="Approved"
 REJECTED="Rejected"
 DEFERRED="Deferred"

@dataclass(frozen=True)
class HistoricalComparisonCatalystAssessmentDecision:
 schema_version:int
 analysis_fingerprint:str
 catalyst_id:str
 signal_id:str
 signal_fingerprint:str
 classification_fingerprint:str
 disposition:HistoricalComparisonCatalystAssessmentDisposition
 conditions:tuple[str,...]
 monitoring_requirements:tuple[str,...]
 reviewer:str
 rationale:str
 reviewed_at:datetime

__all__=["HistoricalComparisonCatalystAssessmentDecision","HistoricalComparisonCatalystAssessmentDisposition"]
