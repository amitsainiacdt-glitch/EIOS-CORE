"""Immutable eligibility result for governed Mispricing analysis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalComparisonMispricingEligibilityPreview:
    eligibility_fingerprint: str
    eligible: bool
    gap_id: str
    expectation_gap_fingerprint: str
    gap_creation_receipt_fingerprint: str
    gap_assessment_fingerprint: str
    analysis_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    material_gap: bool
    positive_gap: bool
    negative_gap: bool
    gap_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    required_analysis_inputs: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]


__all__ = ["HistoricalComparisonMispricingEligibilityPreview"]
