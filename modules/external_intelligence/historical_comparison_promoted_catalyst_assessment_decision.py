"""Immutable human decision on one exact promoted-stage Catalyst preview."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class HistoricalComparisonPromotedCatalystAssessmentDisposition(Enum):
 APPROVED="Approved"
 REJECTED="Rejected"
 DEFERRED="Deferred"

@dataclass(frozen=True)
class HistoricalComparisonPromotedCatalystAssessmentDecision:
 schema_version:int
 preview_fingerprint:str
 promotion_fingerprint:str
 support_fingerprint:str
 catalyst_id:str
 signal_ids:tuple[str,...]
 promoted_signal_ids:tuple[str,...]
 disposition:HistoricalComparisonPromotedCatalystAssessmentDisposition
 conditions:tuple[str,...]
 monitoring_requirements:tuple[str,...]
 reviewer:str
 rationale:str
 reviewed_at:datetime

__all__=["HistoricalComparisonPromotedCatalystAssessmentDecision","HistoricalComparisonPromotedCatalystAssessmentDisposition"]
