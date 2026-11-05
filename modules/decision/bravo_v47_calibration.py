"""BRAVO v4.7 research-decision calibration. Not an execution/trading engine.

Keeps exploratory candidates separate from ADD. Weak trailing cash flow is not a
hard block by itself when a documented, funded recovery mechanism is present.
No orders, target positions, or capital deployment originate from this module.
"""
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from datetime import date
from urllib.parse import urlparse
from typing import Optional, Tuple


class BravoAction(str, Enum):
    EIP_ADD = "EIP ADD"
    VALUE_ADD = "VALUE ADD"
    SPECIAL_SITUATION_ADD = "SPECIAL SITUATION ADD"
    WAIT = "WAIT"
    REJECT = "REJECT"


class AddLane(str, Enum):
    EIP = "EIP"
    VALUE = "VALUE"
    SPECIAL_SITUATION = "SPECIAL SITUATION"


@dataclass(frozen=True)
class BravoEvidence:
    ticker: str
    lane: AddLane
    as_of_date: str
    filing_urls: Tuple[str, ...]
    causal_indicators: Tuple[str, ...]
    price: Optional[float]
    base_value: Optional[float]
    bear_value: Optional[float]
    bull_value: Optional[float]
    horizon_years: float = 2.5
    diluted_basis_verified: bool = False
    cash_financing_reviewed: bool = False
    governance_reviewed: bool = False
    fatal_risk: bool = False
    fatal_risk_reason: str = ""
    permanent_loss_bounded: bool = False
    temporary_weaknesses: Tuple[str, ...] = ()
    weakness_repair_mechanism: str = ""
    approval_to_trade: bool = False  # Deliberately ignored: research never trades.


@dataclass(frozen=True)
class BravoDecision:
    action: BravoAction
    confidence: str
    blockers: Tuple[str, ...]
    base_cagr_percent: Optional[float]
    base_upside_percent: Optional[float]
    bear_downside_percent: Optional[float]
    upside_to_downside: Optional[float]
    capital_deployment_rupees: int = field(default=0)


def evaluate_bravo(e: BravoEvidence) -> BravoDecision:
    """Explicit decision gates: no generic score can override a fatal risk."""
    blockers = []
    if e.fatal_risk:
        return BravoDecision(BravoAction.REJECT, "high", (e.fatal_risk_reason or "Fatal risk",),
                             None, None, None, None)
    try:
        filing_date = date.fromisoformat(e.as_of_date)
        if filing_date > date.today():
            blockers.append("As-of date is in the future")
    except (ValueError, TypeError):
        blockers.append("Missing or invalid ISO as-of date")
    if not e.filing_urls or any(urlparse(u).scheme not in ("https", "http") or not urlparse(u).netloc for u in e.filing_urls):
        blockers.append("Missing or malformed primary-source filing URL")
    if len({v.strip().lower() for v in e.causal_indicators if v.strip()}) < 2:
        blockers.append("Fewer than two corroborated leading indicators")
    if not e.diluted_basis_verified:
        blockers.append("Fully diluted shareholder basis unverified")
    if not e.cash_financing_reviewed:
        blockers.append("Cash conversion / funding bridge unreviewed")
    if not e.governance_reviewed:
        blockers.append("Governance and related-party review incomplete")
    if not e.permanent_loss_bounded:
        blockers.append("Permanent-loss and financing risks not bounded")
    if e.temporary_weaknesses and not e.weakness_repair_mechanism:
        blockers.append("Temporary weakness has no testable repair mechanism")
    values = (e.price, e.base_value, e.bear_value, e.bull_value)
    if any(v is None or not isfinite(v) or v <= 0 for v in values) or not isfinite(e.horizon_years) or e.horizon_years <= 0:
        blockers.append("Complete positive dated scenario valuation required")
        return BravoDecision(BravoAction.WAIT, "low", tuple(blockers), None, None, None, None)
    price, base, bear, bull = values
    if not (bear <= base <= bull):
        blockers.append("Scenario values must satisfy bear <= base <= bull")
    base_upside = (base / price - 1) * 100
    downside = max(0.0, (1 - bear / price) * 100)
    base_cagr = ((base / price) ** (1 / e.horizon_years) - 1) * 100
    ratio = base_upside / downside if downside > 0 else (float("inf") if base_upside > 0 else 0.0)
    if base_cagr < 18.0:
        blockers.append("Base-case CAGR below 18% preference")
    if ratio < 2.0:
        blockers.append("Base upside / bear downside below 2:1")
    if base <= price:
        blockers.append("No positive base-case upside")
    if blockers:
        return BravoDecision(BravoAction.WAIT, "low" if len(blockers) > 2 else "medium",
                             tuple(blockers), round(base_cagr, 2), round(base_upside, 2),
                             round(downside, 2), round(ratio, 2))
    kind = {AddLane.EIP: BravoAction.EIP_ADD,
            AddLane.VALUE: BravoAction.VALUE_ADD,
            AddLane.SPECIAL_SITUATION: BravoAction.SPECIAL_SITUATION_ADD}[e.lane]
    return BravoDecision(kind, "moderate", (),
                         round(base_cagr, 2), round(base_upside, 2),
                         round(downside, 2), round(ratio, 2))
