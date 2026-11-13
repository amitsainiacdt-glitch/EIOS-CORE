"""FOX corporate-action adjustment and historical-series audit.

FAIL CLOSED: only fully verified split/bonus histories may produce comparable
split-adjusted price observations. This is NOT total-return adjustment:
dividends, rights, mergers, demergers and unreviewed events still block an
admissible investment backtest. All data and proofs are supplied by a reviewer;
a source URL string alone is NOT proof that a claim is true.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import isfinite, prod
from typing import Sequence, Optional

ALLOWED_ACTIONS = {"SPLIT", "BONUS"}
ALLOWED_SERIES = {"EQ", "BE"}

@dataclass(frozen=True)
class ObservedBar:
    ticker: str
    isin: str
    series: str
    session: str
    raw_open: float
    raw_close: float
    source_sha256: str

@dataclass(frozen=True)
class CapitalEvent:
    ticker: str
    effective_trade_date: str
    old_isin: str
    new_isin: str
    kind: str
    new_shares_per_old: float
    source_url: str
    publication_timestamp: str
    reviewer_confirmed: bool = False

@dataclass(frozen=True)
class ReviewAttestation:
    ticker: str
    start_session: str
    end_session: str
    reference_session: str
    corporate_actions_complete: bool = False
    distributions_reviewed: bool = False
    rights_and_demergers_reviewed: bool = False
    symbol_isin_history_reviewed: bool = False
    series_liquidity_reviewed: bool = False
    primary_filing_timestamps_reviewed: bool = False
    reviewer_reference: str = ""

@dataclass(frozen=True)
class AdjustedBar:
    ticker: str
    isin: str
    series: str
    session: str
    adjusted_open: float
    adjusted_close: float
    cumulative_price_factor: float
    source_sha256: str
    verified_adjusted: bool = False
    backtest_admissible: bool = False

@dataclass(frozen=True)
class AuditResult:
    ticker: str
    adjusted_bars: tuple[AdjustedBar, ...]
    blockers: tuple[str, ...]
    backtest_admissible: bool

def _day(v: str) -> date:
    return date.fromisoformat(v)

def _positive(v: float) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(v) and v > 0

def adjust_history(bars: Sequence[ObservedBar],
                   events: Sequence[CapitalEvent],
                   review: ReviewAttestation) -> AuditResult:
    blockers: list[str] = []
    if not bars:
        return AuditResult(review.ticker, (), ("No raw exchange bars",), False)
    try:
        start, end, anchor = map(_day, (review.start_session, review.end_session, review.reference_session))
        if start > end or not (start <= anchor <= end):
            blockers.append("Invalid review interval/reference session")
    except ValueError:
        return AuditResult(review.ticker, (), ("Invalid review ISO date",), False)

    raw = sorted(bars, key=lambda x: x.session)
    if len({x.session for x in raw}) != len(raw):
        blockers.append("Duplicate raw trading sessions or mixed series")
    if any(x.ticker != review.ticker for x in raw):
        blockers.append("Raw ticker does not match review")
    if any(not(x.isin and len(x.isin) == 12 and x.series in ALLOWED_SERIES
                 and len(x.source_sha256) == 64
                 and all(ch in '0123456789abcdefABCDEF' for ch in x.source_sha256)
                 and _positive(x.raw_open) and _positive(x.raw_close)) for x in raw):
        blockers.append("Invalid ISIN/series/price/archive checksum")
    try:
        days = [_day(x.session) for x in raw]
        if days[0] != start or days[-1] != end:
            blockers.append("Raw series does not cover reviewed start/end")
        if anchor not in days:
            blockers.append("Reference session missing from exchange bars")
    except ValueError:
        blockers.append("Invalid bar session date")
        return AuditResult(review.ticker, (), tuple(blockers), False)

    actions = sorted(events, key=lambda e: e.effective_trade_date)
    if len({x.effective_trade_date for x in actions}) != len(actions):
        blockers.append("Multiple corporate actions on same ex-date need explicit combined treatment")
    for e in actions:
        try:
            when = _day(e.effective_trade_date)
        except ValueError:
            blockers.append("Invalid corporate-action date")
            continue
        if (e.ticker != review.ticker or e.kind not in ALLOWED_ACTIONS
                or not _positive(e.new_shares_per_old)
                or not e.source_url.startswith("https://")
                or not e.publication_timestamp or not e.reviewer_confirmed):
            blockers.append("Unverified or unsupported corporate action")
        if not (start <= when <= end):
            blockers.append("Corporate action outside reviewed range")
    for field, label in (
        (review.corporate_actions_complete,"Full corporate-action coverage not certified"),
        (review.distributions_reviewed,"Dividend/total-return treatment not certified"),
        (review.rights_and_demergers_reviewed,"Rights/demerger review not certified"),
        (review.symbol_isin_history_reviewed,"ISIN/symbol lineage not certified"),
        (review.series_liquidity_reviewed,"BE/EQ execution and liquidity not reviewed"),
        (review.primary_filing_timestamps_reviewed,"Original signal publication time not verified"),
        (bool(review.reviewer_reference),"No independent reviewer evidence reference"),
    ):
        if not field: blockers.append(label)
    # A certificate asserts review; it must still be independently audited.
    # For continuity, each change across adjacent observed days must be explainable
    # by one of the supplied ex-date transitions (never price jump inference).
    byday = {_day(x.session):x for x in raw}
    isins = {x.isin for x in raw}
    transitions = {(e.old_isin, e.new_isin) for e in actions if e.old_isin != e.new_isin}
    if len(isins) > 1:
        for old, new in zip(raw, raw[1:]):
            if old.isin != new.isin and (old.isin,new.isin) not in transitions:
                blockers.append("Unexplained ISIN transition")
                break
    if any(e.old_isin and e.new_isin and
           (e.old_isin not in isins or e.new_isin not in isins)
           for e in actions if start < _day(e.effective_trade_date) <= end):
        blockers.append("Corporate-action lineage does not reconcile with observed ISINs")
    if len({x.series for x in raw}) > 1:
        blockers.append("Series transitions require session-specific execution model")
    # Display adjusted values even when review incomplete, but NEVER mark them verified.
    adjusted = []
    valid_actions = [e for e in actions
                     if e.kind in ALLOWED_ACTIONS and _positive(e.new_shares_per_old)]
    for b in raw:
        d = _day(b.session)
        # Convert pre-event prices to the reference-session share basis.
        # Events strictly after this observation and on/before reference date.
        ratio = prod(1 / e.new_shares_per_old for e in valid_actions
                     if d < _day(e.effective_trade_date) <= anchor)
        # In cases where an observation follows anchor and future price basis changes,
        # adjust back to the anchor share basis (inverse factor).
        ratio *= prod(e.new_shares_per_old for e in valid_actions
                      if anchor < _day(e.effective_trade_date) <= d)
        adjusted.append(AdjustedBar(
            b.ticker,b.isin,b.series,b.session,
            round(b.raw_open*ratio,8),round(b.raw_close*ratio,8),
            round(ratio,12),b.source_sha256))
    ok = not blockers
    if ok:
        adjusted = [AdjustedBar(x.ticker,x.isin,x.series,x.session,
                    x.adjusted_open,x.adjusted_close,x.cumulative_price_factor,
                    x.source_sha256,True,True) for x in adjusted]
    return AuditResult(review.ticker,tuple(adjusted),tuple(dict.fromkeys(blockers)),ok)
