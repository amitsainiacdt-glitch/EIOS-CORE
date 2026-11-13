"""FOX v4.8 bounded-risk research ADD underwriting (no execution authority).

The detector identifies INVESTIGATE candidates. This distinct evaluator decides
whether sufficient *point-in-time* evidence supports a research ADD. It does not
write trade orders, create portfolio positions or bypass explicit user approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from math import isfinite
from typing import Optional, Tuple
from urllib.parse import urlparse


class FoxAction(str, Enum):
    EIP_ADD = "EIP ADD"
    VALUE_ADD = "VALUE ADD"
    SPECIAL_SITUATION_ADD = "SPECIAL SITUATION ADD"
    WAIT = "WAIT"
    REJECT = "REJECT"


class RiskClass(str, Enum):
    TOLERABLE = "TOLERABLE"
    BOUNDED_UNRESOLVED = "BOUNDED UNRESOLVED"
    THESIS_BREAKING = "THESIS BREAKING"


@dataclass(frozen=True)
class RiskItem:
    description: str
    category: RiskClass
    estimated_downside_rupees_per_share: Optional[float] = None
    kill_test: str = ""


@dataclass(frozen=True)
class ValuationZone:
    version: int
    locked_on: str
    low: float
    high: float
    reference_price: float
    thesis_fingerprint: str
    primary_source_url: str
    revision_reason: str = ""
    evidence_changed: bool = False


@dataclass(frozen=True)
class FoxUnderwriting:
    ticker: str
    lane: str                    # EIP, VALUE, SPECIAL SITUATION
    as_of: str                   # Point-in-time decision date
    price_as_of: str
    price: Optional[float]
    primary_urls: Tuple[str, ...]
    causal_signals: Tuple[str, ...]
    horizon_years: float
    bear_value: Optional[float]
    base_value: Optional[float]
    bull_value: Optional[float]
    probabilities: Tuple[float, float, float] = (0.25, 0.50, 0.25)
    diluted_share_count_verified: bool = False
    financing_survival_verified: bool = False
    governance_evaluated: bool = False
    cash_conversion_evaluated: bool = False
    valuation_evidence_verified: bool = False
    risk_items: Tuple[RiskItem, ...] = ()
    recovery_mechanism: str = ""
    research_zone: Optional[ValuationZone] = None
    previous_zone: Optional[ValuationZone] = None
    catalyst_date: str = ""
    next_kill_test: str = ""


@dataclass(frozen=True)
class FoxDecision:
    action: FoxAction
    blockers: Tuple[str, ...]
    confidence: str
    base_upside_pct: Optional[float] = None
    bear_downside_pct: Optional[float] = None
    upside_downside_ratio: Optional[float] = None
    base_cagr_pct: Optional[float] = None
    weighted_value: Optional[float] = None
    research_risk_budget_pct: float = 0.0
    capital_deployment_rupees: int = 0
    evidence_gaps: Tuple[str, ...] = ()
    economic_failures: Tuple[str, ...] = ()


def _valid_num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)


def _url_ok(url):
    p = urlparse(url)
    return p.scheme == "https" and bool(p.netloc)


# Explicitly separate unavailable decision-critical facts from known poor economics.
# No missing-evidence flag by itself implies a worsening underlying business.
ECONOMIC_BLOCKERS = frozenset({
    "Base annualised return below 18%",
    "Base upside/bear downside below 2:1",
    "Base equity value does not exceed price",
    "Probability-weighted value does not exceed price",
    "Price above locked research zone ceiling",
})

def _wait(blockers, confidence, *metrics):
    evidence = tuple(b for b in blockers if b not in ECONOMIC_BLOCKERS)
    economics = tuple(b for b in blockers if b in ECONOMIC_BLOCKERS)
    return FoxDecision(FoxAction.WAIT, tuple(blockers), confidence, *metrics,
                       evidence_gaps=evidence, economic_failures=economics)


def evaluate_fox(e: FoxUnderwriting) -> FoxDecision:
    blockers = []
    fatal = [r.description for r in e.risk_items if r.category == RiskClass.THESIS_BREAKING]
    if fatal:
        return FoxDecision(FoxAction.REJECT, tuple(fatal), "high")
    try:
        as_of, price_day = date.fromisoformat(e.as_of), date.fromisoformat(e.price_as_of)
        if price_day > as_of:
            blockers.append("Look-ahead: price newer than decision date")
        if as_of > date.today():
            blockers.append("Decision date lies in the future")
    except (ValueError, TypeError):
        blockers.append("Invalid point-in-time date")
    if not e.primary_urls or not all(_url_ok(u) for u in e.primary_urls):
        blockers.append("Verified primary filings missing")
    if len({s.strip().casefold() for s in e.causal_signals if s.strip()}) < 2:
        blockers.append("Fewer than two corroborated leading causal signals")
    if not e.recovery_mechanism.strip():
        blockers.append("No testable recovery mechanism")
    if not e.diluted_share_count_verified:
        blockers.append("Fully diluted equity denominator unverified")
    if not e.financing_survival_verified:
        blockers.append("Financing / survival bridge unverified")
    if not e.governance_evaluated:
        blockers.append("Governance/RPT risk unassessed")
    if not e.cash_conversion_evaluated:
        blockers.append("Cash conversion unassessed")
    if not e.valuation_evidence_verified:
        blockers.append("Scenario valuation inputs unverified")
    if not e.next_kill_test.strip():
        blockers.append("Missing falsifiable kill test")
    if not e.catalyst_date:
        blockers.append("Catalyst date missing")
    else:
        try:
            date.fromisoformat(e.catalyst_date)
        except ValueError:
            blockers.append("Invalid catalyst date")
    if e.lane not in ("EIP", "VALUE", "SPECIAL SITUATION"):
        blockers.append("Unsupported ADD lane")
    if not e.research_zone:
        blockers.append("No dated, locked valuation band")
    else:
        z = e.research_zone
        try:
            date.fromisoformat(z.locked_on)
        except ValueError:
            blockers.append("Invalid zone date")
        if not (z.version >= 1 and _valid_num(z.low) and _valid_num(z.high)
                and z.low > 0 and z.high >= z.low
                and _valid_num(z.reference_price) and z.reference_price > 0
                and z.thesis_fingerprint and _url_ok(z.primary_source_url)):
            blockers.append("Research zone lacks auditable valuation provenance")
        if e.previous_zone:
            p = e.previous_zone
            if z.version <= p.version:
                blockers.append("Buy-zone revision must increment version")
            if (z.low, z.high) != (p.low, p.high) and (
                    not z.evidence_changed or not z.revision_reason.strip()):
                blockers.append("Price-only/missing-evidence buy-zone revision prohibited")
    vals = (e.price, e.bear_value, e.base_value, e.bull_value, e.horizon_years)
    if not all(_valid_num(v) and v > 0 for v in vals):
        blockers.append("Incomplete positive dated bear/base/bull valuation")
        return _wait(blockers, "low")
    price, bear, base, bull, years = vals
    if not bear <= base <= bull:
        blockers.append("Scenario ordering invalid")
    probs = e.probabilities
    if len(probs) != 3 or any(not _valid_num(p) or p < 0 for p in probs) or abs(sum(probs)-1)>0.000001:
        blockers.append("Scenario probabilities must sum to 1")
        weighted = None
    else:
        weighted = sum(p*v for p,v in zip(probs,(bear,base,bull)))
    upside = 100*(base/price-1)
    downside = max(0,100*(1-bear/price))
    ratio = upside/downside if downside else (float("inf") if upside>0 else 0)
    cagr = 100*((base/price)**(1/years)-1)
    if cagr < 18:
        blockers.append("Base annualised return below 18%")
    if ratio < 2:
        blockers.append("Base upside/bear downside below 2:1")
    if base <= price:
        blockers.append("Base equity value does not exceed price")
    if weighted is not None and weighted <= price:
        blockers.append("Probability-weighted value does not exceed price")
    # Original zone is a MAXIMUM admissible price, not a two-sided trap.
    # Falling beneath its lower edge improves price asymmetry if the
    # independently verified business thesis and funding risks remain intact.
    # All economic/evidence gates still apply; no price-only ADD upgrade.
    if e.research_zone is not None and price > e.research_zone.high:
        blockers.append("Price above locked research zone ceiling")
    if any(r.category == RiskClass.BOUNDED_UNRESOLVED and (
            not _valid_num(r.estimated_downside_rupees_per_share)
            or r.estimated_downside_rupees_per_share < 0
            or not r.kill_test.strip()) for r in e.risk_items):
        blockers.append("Bounded unresolved risks lack quantified downside or kill tests")
    metrics = (round(upside,2),round(downside,2),round(ratio,2),round(cagr,2))
    if blockers:
        return _wait(blockers,"low" if len(blockers)>2 else "moderate",
                 *metrics,round(weighted,2) if weighted is not None else None)
    conditional = any(r.category == RiskClass.BOUNDED_UNRESOLVED for r in e.risk_items)
    risk_budget = 1.0 if conditional else 2.0
    action = {"EIP":FoxAction.EIP_ADD,"VALUE":FoxAction.VALUE_ADD,
              "SPECIAL SITUATION":FoxAction.SPECIAL_SITUATION_ADD}[e.lane]
    return FoxDecision(action,(),"conditional" if conditional else "moderate",
                       *metrics,round(weighted,2),risk_budget)
