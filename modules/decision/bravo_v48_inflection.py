"""BRAVO v4.8: deterministic research triage, NOT an order/ADD engine.

Uses point-in-time numeric evidence. This helper produces an INVESTIGATE alert,
not an investment recommendation. No market crawling or persistence here.
"""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from math import isfinite
from typing import Optional, Tuple


class InflectionAction(str, Enum):
    INVESTIGATE = "INVESTIGATE"
    NO_NEW_INFLECTION = "NO NEW INFLECTION"
    REJECT = "REJECT"


@dataclass(frozen=True)
class InflectionEvidence:
    ticker: str
    as_of_date: str
    price_as_of_date: str
    price: Optional[float]
    source_urls: Tuple[str, ...] = ()
    order_intake_growth_yoy_pct: Optional[float] = None
    operating_volume_growth_yoy_pct: Optional[float] = None
    distribution_network_growth_yoy_pct: Optional[float] = None
    orderbook_to_ttm_revenue: Optional[float] = None
    sequential_revenue_growth_pct: Optional[float] = None
    sequential_unit_margin_change_pct: Optional[float] = None
    verified_capacity_or_customer_milestone: bool = False
    share_drawdown_adjusted_pct: Optional[float] = None
    funding_survival_reviewed: bool = False
    downside_bounded: bool = False
    fatal_contradiction: bool = False
    fatal_reason: str = ""
    verified_diluted_valuation: bool = False
    fixed_zone_exists: bool = False


@dataclass(frozen=True)
class InflectionResult:
    action: InflectionAction
    signals: Tuple[str, ...]
    blockers: Tuple[str, ...]
    capital_deployment_rupees: int = 0


def _number(x):
    return x is not None and isinstance(x, (int, float)) and not isinstance(x, bool) and isfinite(x)


def detect_inflection(e: InflectionEvidence) -> InflectionResult:
    blockers = []
    signals = []
    try:
        observation = date.fromisoformat(e.as_of_date)
        price_date = date.fromisoformat(e.price_as_of_date)
        if price_date > observation:
            blockers.append("Price observation postdates evidence snapshot: no point-in-time classification")
    except (TypeError, ValueError):
        blockers.append("Missing or invalid ISO evidence/price date")
    if not _number(e.price) or e.price <= 0:
        blockers.append("Verified positive dated price unavailable")
    if not e.source_urls or not all(u.startswith("https://") for u in e.source_urls):
        blockers.append("Dated primary source URLs missing")
    if e.fatal_contradiction:
        return InflectionResult(InflectionAction.REJECT, (), (e.fatal_reason or "Thesis-breaking risk",))
    if _number(e.order_intake_growth_yoy_pct) and e.order_intake_growth_yoy_pct >= 25:
        signals.append("Accelerating order intake")
    if _number(e.operating_volume_growth_yoy_pct) and e.operating_volume_growth_yoy_pct >= 15:
        signals.append("Accelerating operating volumes")
    if _number(e.distribution_network_growth_yoy_pct) and e.distribution_network_growth_yoy_pct >= 15:
        signals.append("Network expansion")
    if _number(e.orderbook_to_ttm_revenue) and e.orderbook_to_ttm_revenue >= 1:
        signals.append("Order book exceeds trailing revenue")
    if _number(e.sequential_revenue_growth_pct) and e.sequential_revenue_growth_pct >= 15:
        signals.append("Sequential revenue recovery")
    if _number(e.sequential_unit_margin_change_pct) and e.sequential_unit_margin_change_pct >= 2:
        signals.append("Sequential unit-margin improvement")
    if e.verified_capacity_or_customer_milestone:
        signals.append("Verified capacity/customer milestone")
    if _number(e.share_drawdown_adjusted_pct) and e.share_drawdown_adjusted_pct <= -30:
        signals.append("Distressed adjusted share price (discovery only)")
    causal = [s for s in signals if not s.startswith("Distressed")]
    # Related volume and footprint metrics can trigger investigation, not ADD;
    # actual economic independence, profitability and capex returns remain unverified.
    if len(causal) < 2:
        blockers.append("Fewer than two independent causal signals; drawdown is not a catalyst")
    if not e.funding_survival_reviewed:
        blockers.append("Funding survival unreviewed")
    if not e.downside_bounded:
        blockers.append("Downside not bounded")
    if not e.verified_diluted_valuation:
        blockers.append("Diluted valuation not verified: cannot issue ADD")
    if not e.fixed_zone_exists:
        blockers.append("Fixed dated research valuation zone not established")
    # Only evidence-integrity failures veto investigation. Incomplete valuation\n    # or an unvalidated dated zone must block ADD, not investigative triage.\n    critical = any(b.startswith(("Price observation postdates", "Missing or invalid ISO",\n                                 "Verified positive dated price unavailable",\n                                 "Dated primary source URLs missing")) for b in blockers)
    action = InflectionAction.INVESTIGATE if len(causal) >= 2 and not critical else InflectionAction.NO_NEW_INFLECTION
    return InflectionResult(action, tuple(signals), tuple(blockers))
