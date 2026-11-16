"""FOX attributable-owner valuation worksheet (research only; never executes trades).

Estimates are *conditional scenarios*, not independently verified facts.
Inputs require dated source provenance and documented economic assumptions.
No arbitrary share-price targets or fabricated missing inputs are generated.
"""
from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Optional, Tuple
from urllib.parse import urlparse

@dataclass(frozen=True)
class Scenario:
    name: str
    attributable_profit_cr: float
    terminal_pe: float
    probability: float
    reason: str

@dataclass(frozen=True)
class Worksheet:
    ticker: str
    as_of: str
    price_as_of: str
    market_price: Optional[float]
    fully_diluted_shares_cr: Optional[float]
    horizon_years: float
    evidence: Tuple[Tuple[str, str], ...]  # (filing URL, published ISO date)
    scenarios: Tuple[Scenario, ...]
    share_count_source: str
    profit_bridge: str
    cash_conversion_bridge: str
    financing_and_governance_review: str
    source_inputs_verified: bool = False

@dataclass(frozen=True)
class WorksheetResult:
    state: str
    blockers: Tuple[str, ...]
    prices: Tuple[Tuple[str, float], ...] = ()
    base_cagr_pct: Optional[float] = None
    bear_downside_pct: Optional[float] = None
    base_upside_pct: Optional[float] = None
    upside_downside_ratio: Optional[float] = None
    weighted_value: Optional[float] = None
    conditional_ceiling: Optional[float] = None
    capital_deployment_rupees: int = 0

def _positive(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and isfinite(v) and v>0

def evaluate_worksheet(w: Worksheet) -> WorksheetResult:
    missing=[]
    try:
        asof=date.fromisoformat(w.as_of)
        priced=date.fromisoformat(w.price_as_of)
        if priced>asof: missing.append("Price date after decision date")
    except (TypeError,ValueError):
        missing.append("Invalid decision/price date")
        asof=None
    if not _positive(w.market_price): missing.append("Dated positive market price missing")
    if not _positive(w.fully_diluted_shares_cr): missing.append("Fully diluted share count missing")
    if not _positive(w.horizon_years): missing.append("Valid horizon missing")
    if not w.evidence: missing.append("Primary filing provenance missing")
    for url,publication in w.evidence:
        parsed=urlparse(url)
        if parsed.scheme!="https" or not parsed.netloc:
            missing.append("Invalid filing URL")
        try:
            published=date.fromisoformat(publication)
            if asof is not None and published>asof:
                missing.append("Look-ahead filing publication date")
        except (ValueError,TypeError):
            missing.append("Missing filing publication date")
    for value,label in ((w.share_count_source,"Share count source"),
                        (w.profit_bridge,"Attributable profit bridge"),
                        (w.cash_conversion_bridge,"Cash conversion bridge"),
                        (w.financing_and_governance_review,"Financing/governance review")):
        if not value.strip(): missing.append(label+" missing")
    if not w.source_inputs_verified: missing.append("Financial inputs not independently checked")
    if len(w.scenarios)!=3 or tuple(s.name for s in w.scenarios)!=("bear","base","bull"):
        missing.append("Expected bear/base/bull cases")
    else:
        for s in w.scenarios:
            if not _positive(s.attributable_profit_cr) or not _positive(s.terminal_pe):
                missing.append("Invalid scenario earnings or PE")
            if not isinstance(s.probability,(int,float)) or not isfinite(s.probability) or s.probability<0:
                missing.append("Invalid probability")
            if not s.reason.strip(): missing.append("Unexplained scenario assumptions")
        if not missing and abs(sum(s.probability for s in w.scenarios)-1)>1e-7:
            missing.append("Scenario probabilities do not sum to 100%")
    if missing:
        return WorksheetResult("UNDERWRITING_INCOMPLETE",tuple(dict.fromkeys(missing)))
    values=tuple(s.attributable_profit_cr*s.terminal_pe/w.fully_diluted_shares_cr for s in w.scenarios)
    if not values[0]<=values[1]<=values[2]:
        return WorksheetResult("UNDERWRITING_INCOMPLETE",("Bear/base/bull ordering invalid",))
    bear,base,bull=values
    price=w.market_price
    cagr=100*((base/price)**(1/w.horizon_years)-1)
    downside=max(0,100*(price-bear)/price)
    upside=100*(base-price)/price
    ratio=upside/downside if downside>0 else (float("inf") if upside>0 else 0)
    weighted=sum(v*s.probability for v,s in zip(values,w.scenarios))
    ceiling=min(base/(1.18**w.horizon_years),(base+2*bear)/3,weighted)
    failures=[]
    if cagr<18: failures.append("Base CAGR below 18%")
    if ratio<2: failures.append("Base upside/bear downside below 2:1")
    if weighted<=price: failures.append("Weighted value does not exceed price")
    state="ECONOMIC_FAILURE" if failures else "SCENARIO_SCREEN_PASSED_NOT_ADD"
    return WorksheetResult(state,tuple(failures),tuple((s.name,round(v,2)) for s,v in zip(w.scenarios,values)),
                           round(cagr,2),round(downside,2),round(upside,2),
                           round(ratio,2),round(weighted,2),round(ceiling,2))
