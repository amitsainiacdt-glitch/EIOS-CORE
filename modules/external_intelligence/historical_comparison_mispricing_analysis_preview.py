"""Immutable read-only result of governed Mispricing analysis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalComparisonMispricingAnalysisPreview:
    analysis_fingerprint: str
    eligibility_fingerprint: str
    valuation_fingerprint: str
    valuation_receipt_fingerprint: str
    gap_id: str
    expectation_gap_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    company: str
    cmp: float
    intrinsic_value: float
    fair_value: float
    valuation_upside: float
    valuation_discount: float
    catalyst_score: float
    expectation_gap_score: float
    expectation_difference: float
    earnings_gap: float
    market_recognition: float
    unrecognized_potential: float
    mispricing_score: float
    confidence: float
    valuation_support: bool
    catalyst_support: bool
    expectation_support: bool
    potential_mispricing: bool
    evidence: tuple[str, ...]
    assumptions: tuple[str, ...]
    disconfirming_evidence: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]


__all__ = ["HistoricalComparisonMispricingAnalysisPreview"]
