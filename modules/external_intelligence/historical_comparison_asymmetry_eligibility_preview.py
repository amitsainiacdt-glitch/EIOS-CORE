"""Immutable eligibility result for governed Asymmetry analysis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalComparisonAsymmetryEligibilityPreview:
    eligibility_fingerprint: str
    eligible: bool
    company: str
    mispricing_fingerprint: str
    mispricing_creation_receipt_fingerprint: str
    mispricing_assessment_fingerprint: str
    mispricing_analysis_fingerprint: str
    potential_mispricing: bool
    mispricing_score: float
    confidence: float
    gap_id: str
    expectation_gap_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    valuation_fingerprint: str
    valuation_receipt_fingerprint: str
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    required_analysis_inputs: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]


__all__ = ["HistoricalComparisonAsymmetryEligibilityPreview"]
