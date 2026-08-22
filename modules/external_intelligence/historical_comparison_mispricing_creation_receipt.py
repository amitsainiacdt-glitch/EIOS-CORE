"""Immutable receipt for one explicitly materialized governed Mispricing result."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonMispricingCreationReceipt:
    schema_version: int
    analysis_fingerprint: str
    assessment_fingerprint: str
    eligibility_fingerprint: str
    valuation_fingerprint: str
    valuation_receipt_fingerprint: str
    gap_id: str
    expectation_gap_fingerprint: str
    catalyst_id: str
    catalyst_fingerprint: str
    company: str
    cmp: float
    mispricing_fingerprint: str
    potential_mispricing: bool
    mispricing_score: float
    confidence: float
    signal_ids: tuple[str, ...]
    promoted_signal_ids: tuple[str, ...]
    creator: str
    rationale: str
    created_at: datetime


__all__ = ["HistoricalComparisonMispricingCreationReceipt"]
