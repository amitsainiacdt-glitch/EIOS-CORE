"""Immutable read-only validation preview for one created Signal."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HistoricalComparisonSignalValidationPreview:
    signal_id: str
    signal_fingerprint: str
    governed_input_fingerprint: str
    evidence_id: str
    valid: bool
    score: float
    confidence: float
    source_quality: float
    evidence_quality: float
    relevance: float
    recency: float
    persistence: float
    corroboration: float
    contradiction_penalty: float
    independent_confirmation: int
    reasons: tuple[str,...]
    warnings: tuple[str,...]
    invalidation_reasons: tuple[str,...]

__all__=["HistoricalComparisonSignalValidationPreview"]
