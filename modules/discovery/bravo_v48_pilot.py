"""BRAVO v4.8 pilot: independent discovery, completion and replay audit.

Research-only orchestration over supplied evidence. It does not scrape, trade,
write persistent registries or change the active v4.7 runtime.
"""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, Tuple

from modules.decision.bravo_v47_calibration import (
    BravoAction, BravoEvidence, BravoDecision, evaluate_bravo,
)


class DiscoveryLane(str, Enum):
    DISTRESSED_QUALITY = "distressed_quality"
    OPERATING_REPAIR = "operating_repair"
    BALANCE_SHEET_REPAIR = "balance_sheet_repair"


@dataclass(frozen=True)
class DiscoveryLead:
    ticker: str
    lane: DiscoveryLane
    observed_on: str
    source_urls: Tuple[str, ...]
    what_broke: str
    repair_mechanism: str
    leading_signals: Tuple[str, ...]
    independent_confirmations: Tuple[str, ...] = ()
    next_trigger: str = ""
    adjusted_drawdown_percent: Optional[float] = None
    familiar_registry_name: bool = False
    fatal_risk: bool = False


@dataclass(frozen=True)
class DiscoveryReport:
    screened: int
    investigated: Tuple[DiscoveryLead, ...]
    rejected_early: Tuple[Tuple[str, str], ...]
    distinct_lanes_scanned: Tuple[DiscoveryLane, ...]
    missing_lanes: Tuple[DiscoveryLane, ...]
    novel_leads: int
    false_positives: Optional[int] = None
    missed_opportunities: Optional[int] = None


def _valid_date(s: str, cutoff: date) -> bool:
    try:
        return date.fromisoformat(s) <= cutoff
    except (ValueError, TypeError):
        return False


def discover(leads: Tuple[DiscoveryLead, ...], cutoff: date) -> DiscoveryReport:
    """Discovery is not an ADD gate; missing financials cannot veto investigation."""
    elevated, rejected = [], []
    seen = set()
    for lead in leads:
        ticker = lead.ticker.strip().upper()
        if not ticker or ticker in seen:
            rejected.append((lead.ticker, "Missing ticker or duplicate universe entry"))
            continue
        seen.add(ticker)
        if not _valid_date(lead.observed_on, cutoff):
            rejected.append((ticker, "Invalid or future-dated observation"))
        elif not lead.source_urls or not all(u.startswith("https://") for u in lead.source_urls):
            rejected.append((ticker, "Missing source URL"))
        elif not lead.what_broke.strip() or not lead.repair_mechanism.strip():
            rejected.append((ticker, "No falsifiable repair hypothesis"))
        elif not lead.leading_signals:
            rejected.append((ticker, "No dated leading repair signal"))
        elif lead.fatal_risk:
            rejected.append((ticker, "Known fatal-risk contradiction"))
        else:
            elevated.append(lead)
    lanes = tuple(dict.fromkeys(lead.lane for lead in leads))
    missing = tuple(lane for lane in DiscoveryLane if lane not in lanes)
    elevated.sort(key=lambda l: (l.familiar_registry_name, -len(l.independent_confirmations),
                                 -len(l.leading_signals), l.ticker))
    return DiscoveryReport(
        screened=len(leads), investigated=tuple(elevated),
        rejected_early=tuple(rejected), distinct_lanes_scanned=lanes,
        missing_lanes=missing,
        novel_leads=sum(not lead.familiar_registry_name for lead in elevated),
    )


@dataclass(frozen=True)
class CompletionPacket:
    ticker: str
    decision: BravoDecision
    incomplete_reason: str
    next_evidence: str
    next_review_date: str


def complete(evidence: BravoEvidence, next_evidence: str,
             next_review_date: str) -> CompletionPacket:
    """Always produce a decision and a concrete blocker, never an unexplained WAIT."""
    result = evaluate_bravo(evidence)
    if result.action == BravoAction.WAIT:
        why = "; ".join(result.blockers)
        if not next_evidence.strip() or not next_review_date.strip():
            raise ValueError("WAIT requires a measurable next-evidence task and review date")
        if not _valid_date(next_review_date, date(9999, 12, 31)):
            raise ValueError("Invalid review date")
    else:
        why = ""
    return CompletionPacket(evidence.ticker, result, why, next_evidence, next_review_date)


@dataclass(frozen=True)
class HistoricalReplay:
    ticker: str
    cutoff: str
    evidence_dates: Tuple[str, ...]
    reference_price_date: str
    outcome_price_date: str
    outcome_return_percent: Optional[float]


def audit_replay(replay: HistoricalReplay) -> str:
    """No outcome leakage into cutoff decision packets; never backfill future filings."""
    cutoff = date.fromisoformat(replay.cutoff)
    if not _valid_date(replay.reference_price_date, cutoff):
        return "INVALID_FUTURE_REFERENCE_PRICE"
    if any(not _valid_date(d, cutoff) for d in replay.evidence_dates):
        return "INVALID_LOOKAHEAD_EVIDENCE"
    try:
        if date.fromisoformat(replay.outcome_price_date) <= cutoff:
            return "INVALID_OUTCOME_WINDOW"
    except ValueError:
        return "INVALID_OUTCOME_WINDOW"
    if replay.outcome_return_percent is None:
        return "PENDING_OUTCOME"
    return "REPLAY_ELIGIBLE"


def measure_outcomes(replays: Tuple[HistoricalReplay, ...]) -> dict:
    eligible = [r for r in replays if audit_replay(r) == "REPLAY_ELIGIBLE"]
    return {"replay_eligible": len(eligible),
            "missed_adds": None, "false_positives": None,
            "note": "Cannot label misses/false positives without original dated decisions and benchmarks"}
