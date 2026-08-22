"""Immutable read-only result of governed Expectation Gap analysis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalComparisonExpectationGapAnalysisPreview:
    analysis_fingerprint: str
    eligibility_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    creation_receipt_fingerprint: str
    gap_id: str
    company: str
    sector: str
    market_expectation: float
    eios_expectation: float
    expectation_difference: float
    market_earnings_expectation: float
    eios_earnings_expectation: float
    earnings_gap: float
    market_recognition: float
    unrecognized_potential: float
    positive_gap: bool
    negative_gap: bool
    material_gap: bool
    gap_score: float
    confidence: float
    evidence: tuple[str, ...]
    assumptions: tuple[str, ...]
    disconfirming_evidence: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]


__all__ = ["HistoricalComparisonExpectationGapAnalysisPreview"]
