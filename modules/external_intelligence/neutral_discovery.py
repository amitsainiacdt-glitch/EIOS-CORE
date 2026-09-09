"""Anti-anchoring market-universe and research-priority contracts."""

from dataclasses import dataclass
from enum import Enum


class NeutralDiscoveryFactorKind(str, Enum):
    CAUSAL_EVIDENCE_FRESHNESS = "CAUSAL_EVIDENCE_FRESHNESS"
    CAUSAL_COVERAGE_GAP = "CAUSAL_COVERAGE_GAP"
    EXPECTED_INFORMATION_GAIN = "EXPECTED_INFORMATION_GAIN"
    CONTRADICTION_VALUE = "CONTRADICTION_VALUE"
    PRIMARY_SOURCE_AVAILABILITY = "PRIMARY_SOURCE_AVAILABILITY"


@dataclass(frozen=True)
class NeutralDiscoveryFactor:
    kind: NeutralDiscoveryFactorKind
    priority_points: int
    rationale: str


@dataclass(frozen=True)
class NeutralDiscoveryCandidate:
    ticker: str
    company: str
    sector_id: str
    evidence_fingerprint: str
    factors: tuple[NeutralDiscoveryFactor, ...]
    is_current_holding: bool = False
    is_watchlisted: bool = False
    was_previously_discussed: bool = False


@dataclass(frozen=True)
class NeutralDiscoveryUniverse:
    schema_version: int
    universe_id: str
    target_sector_ids: tuple[str, ...]
    candidates: tuple[NeutralDiscoveryCandidate, ...]
    selection_limit: int
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class NeutralDiscoveryResult:
    universe_id: str
    selected_tickers: tuple[str, ...]
    priority_by_ticker: tuple[tuple[str, int], ...]
    covered_sector_ids: tuple[str, ...]
    missing_sector_ids: tuple[str, ...]
    selection_fingerprint: str
    status: str
    reason_codes: tuple[str, ...]
    anchor_context_tickers: tuple[str, ...]
    creates_opportunity: bool
    non_authority_statement: str


__all__ = [
    "NeutralDiscoveryCandidate", "NeutralDiscoveryFactor", "NeutralDiscoveryFactorKind",
    "NeutralDiscoveryResult", "NeutralDiscoveryUniverse",
]
