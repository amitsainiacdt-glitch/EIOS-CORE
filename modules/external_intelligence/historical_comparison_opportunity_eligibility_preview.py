"""Immutable eligibility result for governed Opportunity synthesis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalComparisonOpportunityEligibilityPreview:
    eligibility_fingerprint: str
    eligible: bool
    company: str
    sector: str
    mispricing_fingerprint: str
    mispricing_creation_receipt_fingerprint: str
    mispricing_assessment_fingerprint: str
    mispricing_analysis_fingerprint: str
    mispricing_eligibility_fingerprint: str
    valuation_fingerprint: str
    valuation_receipt_fingerprint: str
    gap_id: str
    expectation_gap_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    potential_mispricing: bool
    mispricing_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    required_synthesis_inputs: tuple[str, ...]
    missing_governed_inputs: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]


__all__ = ["HistoricalComparisonOpportunityEligibilityPreview"]
