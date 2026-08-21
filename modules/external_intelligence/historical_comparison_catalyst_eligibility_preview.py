"""Immutable read-only Catalyst review eligibility for one governed Signal."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonCatalystEligibilityPreview:
    signal_id:str
    signal_fingerprint:str
    validation_fingerprint:str
    governed_input_fingerprint:str
    evidence_id:str
    validation_valid:bool
    human_disposition:str
    eligible_for_catalyst_review:bool
    blockers:tuple[str,...]
    conditions:tuple[str,...]
    monitoring_requirements:tuple[str,...]

__all__=["HistoricalComparisonCatalystEligibilityPreview"]
