"""Evidence-first pre-inflection research gate. No feeds, trading, or deployment actions.

Inputs must be point-in-time, source-linked research facts. Numeric scores are
research prioritisation only, never a probability of investment success.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Tuple

KINDS = {"customer_qualification", "commercial_order", "commissioning",
         "utilisation", "dispatch", "pricing", "policy", "cost", "cash_collection"}
TEMPORARY = {"temporary_margin", "working_capital", "productive_capex_debt",
             "underutilised_capacity", "weak_quarter"}
CLASSES = ("Research Now", "Early Watch", "EIP Watch", "Earliest Investable Point",
           "Buy-zone Candidate", "Wait", "Too Late", "Reject")

@dataclass(frozen=True)
class Evidence:
    kind: str
    source_url: str
    published_on: date
    as_of: date
    claim: str
    independent: bool
    points: int = 0

    def __post_init__(self):
        if self.kind not in KINDS or not self.source_url.startswith("https://"):
            raise ValueError("Evidence requires a recognised kind and HTTPS source")
        if self.published_on > self.as_of:
            raise ValueError("Future evidence is prohibited (point-in-time integrity)")
        if not 0 <= self.points <= 25:
            raise ValueError("Evidence points must be 0..25")

@dataclass(frozen=True)
class Candidate:
    ticker: str
    as_of: date
    evidence: Tuple[Evidence, ...]
    future_cash_earnings: int
    expectation_gap: int
    valuation_asymmetry: int
    resilience: int
    timing: int
    forward_quarters: int
    price_recognition: str  # unrecognised / partial / priced_in / unknown
    temporary_flaws: Tuple[str, ...] = ()
    flaws_explained: bool = False
    governance_red_flag: bool = False
    uneconomic_growth: bool = False
    uncontrolled_funding: bool = False
    liquidity_failure: bool = False
    contradictions: Tuple[str, ...] = ()
    kill_tests: Tuple[str, ...] = ()
    cash_bridge: Optional[str] = None

@dataclass(frozen=True)
class Assessment:
    ticker: str
    classification: str
    research_score: int
    reasons: Tuple[str, ...]
    capital_deployment_signal: bool = False
    score_is_probability: bool = False

def assess(candidate: Candidate) -> Assessment:
    if not candidate.ticker.strip():
        raise ValueError("Ticker required")
    for name, val, maxval in (("future_cash_earnings",candidate.future_cash_earnings,20),
                              ("expectation_gap",candidate.expectation_gap,20),
                              ("valuation_asymmetry",candidate.valuation_asymmetry,20),
                              ("resilience",candidate.resilience,10),
                              ("timing",candidate.timing,5)):
        if isinstance(val,bool) or not isinstance(val,int) or not 0 <= val <= maxval:
            raise ValueError(f"{name} outside permitted scoring range")
    if candidate.price_recognition not in ("unrecognised","partial","priced_in","unknown"):
        raise ValueError("Invalid recognition status")
    if any(e.as_of != candidate.as_of for e in candidate.evidence):
        raise ValueError("Evidence must use candidate assessment date")
    if any(x not in TEMPORARY for x in candidate.temporary_flaws):
        raise ValueError("Unknown temporary flaw")
    causal = min(25,sum(e.points for e in candidate.evidence if e.independent))
    score = causal + candidate.future_cash_earnings + candidate.expectation_gap + candidate.valuation_asymmetry + candidate.resilience + candidate.timing
    reasons = []
    hard_fail = candidate.governance_red_flag or candidate.uneconomic_growth or candidate.uncontrolled_funding or candidate.liquidity_failure
    if hard_fail:
        return Assessment(candidate.ticker,"Reject",score,("Thesis-breaking governance, economics, funding or liquidity risk",))
    if candidate.price_recognition == "priced_in":
        return Assessment(candidate.ticker,"Too Late",score,("Business inflection materially priced in",))
    if candidate.price_recognition == "unknown":
        return Assessment(candidate.ticker,"Research Now",score,("Price-recognition gate cannot be verified",))
    if not candidate.evidence or not any(e.independent for e in candidate.evidence):
        return Assessment(candidate.ticker,"Research Now",score,("No independent causal source evidence",))
    if candidate.forward_quarters < 1 or candidate.forward_quarters > 4:
        return Assessment(candidate.ticker,"Early Watch",score,("Inflection outside 1–4 quarter window",))
    if candidate.temporary_flaws and not candidate.flaws_explained:
        return Assessment(candidate.ticker,"EIP Watch",score,("Temporary imperfections remain unexplained",))
    if not candidate.kill_tests or not candidate.contradictions:
        return Assessment(candidate.ticker,"EIP Watch",score,("Missing explicit contradictions or kill tests",))
    if not candidate.cash_bridge:
        return Assessment(candidate.ticker,"EIP Watch",score,("Missing quantified or bounded cash-earnings bridge",))
    if candidate.valuation_asymmetry < 12 or candidate.expectation_gap < 10:
        return Assessment(candidate.ticker,"Wait",score,("Insufficient valuation asymmetry or expectation gap",))
    if score >= 85 and candidate.price_recognition == "unrecognised":
        return Assessment(candidate.ticker,"Buy-zone Candidate",score,("Research gates met; separate deployment decision required",))
    if score >= 70:
        return Assessment(candidate.ticker,"Earliest Investable Point",score,("Early causal inflection justified despite tolerable flaws",))
    return Assessment(candidate.ticker,"EIP Watch" if score >= 50 else "Research Now",score,("Insufficient corroborated research strength",))
