"""Immutable read-only analytical preview for one classified Catalyst."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonCatalystAnalysisPreview:
 catalyst_id:str
 signal_id:str
 signal_fingerprint:str
 classification_fingerprint:str
 primary_catalyst_id:str
 primary_family:str
 secondary_catalyst_ids:tuple[str,...]
 secondary_families:tuple[str,...]
 direction:str
 horizon:str
 magnitude:float
 probability:float
 persistence:float
 market_recognition:float
 catalyst_score:float
 confidence:float
 meets_minimum_score:bool
 evidence:tuple[str,...]
 assumptions:tuple[str,...]
 contradictory_evidence:tuple[str,...]
 invalidation_conditions:tuple[str,...]
 reasons:tuple[str,...]
 warnings:tuple[str,...]

__all__=["HistoricalComparisonCatalystAnalysisPreview"]
