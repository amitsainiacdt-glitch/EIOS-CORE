"""Immutable before/after Catalyst preview using approved in-memory stage promotion."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonPromotedStageCatalystPreview:
 promotion_fingerprint:str
 support_fingerprint:str
 cluster_id:str
 catalyst_id:str
 signal_ids:tuple[str,...]
 promoted_signal_ids:tuple[str,...]
 original_stages:tuple[str,...]
 effective_stages:tuple[str,...]
 baseline_catalyst_score:float
 promoted_catalyst_score:float
 score_change:float
 baseline_catalyst_confidence:float
 promoted_catalyst_confidence:float
 baseline_meets_minimum:bool
 promoted_meets_minimum:bool
 primary_catalyst_id:str
 primary_family:str
 classification_confidence:float
 reasons:tuple[str,...]
 warnings:tuple[str,...]

__all__=["HistoricalComparisonPromotedStageCatalystPreview"]
