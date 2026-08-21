"""Immutable read-only support preview for a multi-Signal Catalyst."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonMultiSignalCatalystSupportPreview:
 support_fingerprint:str
 cluster_id:str
 theme:str
 catalyst_id:str
 signal_ids:tuple[str,...]
 signal_fingerprints:tuple[str,...]
 validation_fingerprints:tuple[str,...]
 signal_count:int
 independent_sources:int
 average_strength:float
 average_confidence:float
 contradiction_count:int
 cluster_score:float
 cluster_confidence:float
 cluster_emerging:bool
 primary_catalyst_id:str
 primary_family:str
 classification_confidence:float
 catalyst_score:float
 catalyst_confidence:float
 meets_minimum_catalyst_score:bool
 independently_supported:bool
 stage_promotion_required:bool
 reasons:tuple[str,...]
 warnings:tuple[str,...]

__all__=["HistoricalComparisonMultiSignalCatalystSupportPreview"]
