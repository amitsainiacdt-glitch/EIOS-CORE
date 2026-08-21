"""Immutable human governance for one exact entity Evidence pack score."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalComparisonGovernanceKillSwitch:
    name: str
    condition: str
    severity: str
    measurable: bool
    threshold: str
    monitoring_frequency: str
    rationale: str
    triggered: bool


@dataclass(frozen=True)
class HistoricalComparisonEvidenceGovernance:
    schema_version: int
    pack_fingerprint: str
    entity: str
    assumptions: tuple[str, ...]
    kill_switches: tuple[HistoricalComparisonGovernanceKillSwitch, ...]
    monitoring_signals: tuple[str, ...]
    analyst: str
    rationale: str
    governed_at: datetime


__all__ = [
    "HistoricalComparisonEvidenceGovernance",
    "HistoricalComparisonGovernanceKillSwitch",
]
