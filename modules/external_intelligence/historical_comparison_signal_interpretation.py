"""Immutable human Signal interpretation for governed historical Evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from modules.opportunity.signals.signal_interpretation import SignalInterpretation


@dataclass(frozen=True)
class HistoricalComparisonSignalInterpretation:
    schema_version: int
    governed_input_fingerprint: str
    pack_fingerprint: str
    entity: str
    evidence_id: str
    interpretation: SignalInterpretation
    analyst: str
    rationale: str
    interpreted_at: datetime


__all__ = ["HistoricalComparisonSignalInterpretation"]
