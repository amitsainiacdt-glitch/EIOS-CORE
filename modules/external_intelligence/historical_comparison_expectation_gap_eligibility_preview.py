"""Immutable eligibility result for governed Expectation Gap analysis."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonExpectationGapEligibilityPreview:
 eligibility_fingerprint:str
 eligible:bool
 catalyst_id:str
 catalyst_fingerprint:str
 creation_receipt_fingerprint:str
 assessment_fingerprint:str
 preview_fingerprint:str
 promotion_fingerprint:str
 support_fingerprint:str
 signal_ids:tuple[str,...]
 promoted_signal_ids:tuple[str,...]
 primary_catalyst_id:str
 primary_family:str
 catalyst_score:float
 catalyst_confidence:float
 required_analysis_inputs:tuple[str,...]
 blockers:tuple[str,...]
 warnings:tuple[str,...]

__all__=["HistoricalComparisonExpectationGapEligibilityPreview"]
