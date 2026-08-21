"""Immutable receipt for a governed entity Evidence pack score."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonGovernedScoringReceipt:
    schema_version: int
    governed_input_fingerprint: str
    pack_fingerprint: str
    entity: str
    evidence_score: float
    confidence: float
    sufficiently_supported: bool
    evidence_gaps: tuple[str, ...]
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    warnings: tuple[str, ...]
    analyst: str
    rescored_at: datetime


__all__ = ["HistoricalComparisonGovernedScoringReceipt"]
