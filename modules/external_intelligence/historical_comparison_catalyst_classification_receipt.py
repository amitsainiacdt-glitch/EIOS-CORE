"""Immutable receipt for explicit Catalyst taxonomy classification."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class HistoricalComparisonCatalystClassificationReceipt:
 schema_version:int
 eligibility_fingerprint:str
 classification_fingerprint:str
 signal_id:str
 signal_fingerprint:str
 validation_fingerprint:str
 primary_catalyst_id:str
 primary_family:str
 secondary_catalyst_ids:tuple[str,...]
 secondary_families:tuple[str,...]
 confidence:float
 reasoning:tuple[str,...]
 matched_signals:tuple[str,...]
 unclassified_signals:tuple[str,...]
 warnings:tuple[str,...]
 analyst:str
 rationale:str
 classified_at:datetime

__all__=["HistoricalComparisonCatalystClassificationReceipt"]
