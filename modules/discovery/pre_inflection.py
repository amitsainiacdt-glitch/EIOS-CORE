"""Point-in-time, evidence-first pre-inflection research assessment.

This module does not fetch market data, place trades, or change the established
long-term discovery, EIP or 10x registries. Inputs must be sourced independently.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Tuple

CLASSIFICATIONS = ("Research Now", "Early Watch", "EIP Watch",
                   "Earliest Investable Point", "Buy-zone Candidate",
                   "Wait", "Too Late", "Reject")
WEIGHTS = {"causal":25, "cash_earnings":20, "expectation_gap":20,
           "valuation":20, "resilience":10, "timing":5}

@dataclass(frozen=True)
class Evidence:
    fact: str
    source_url: str
    published_on: date
    available_on: date
    independent: bool = False
    contradicts_thesis: bool = False
    def valid_asof(self, asof:date) -> bool:
        return (bool(self.fact.strip()) and self.source_url.startswith(("https://", "http://"))
                and self.published_on <= self.available_on <= asof)

@dataclass(frozen=True)
class InflectionCase:
    ticker: str
    sector: str
    asof: date
    evidence: Tuple[Evidence, ...]
    causal_chain: str
    next_2_to_4_quarter_trigger: str
    cash_earnings_bridge: str
    expectation_gap: str
    contradictions: Tuple[str, ...]
    kill_tests: Tuple[str, ...]
    price_recognition_checked: bool
    materially_rerated: bool
    thesis_broken: bool
    temporary_imperfections_explained: bool
    scoring: dict = field(default_factory=dict)
    capital_action: Optional[str] = None

@dataclass(frozen=True)
class ResearchAssessment:
    ticker: str
    classification: str
    score: float
    reasons: Tuple[str, ...]
    capital_action: str = "NOT_ASSESSED"
    folder: str = "EIP_RESEARCH_ONLY"

def assess(case:InflectionCase) -> ResearchAssessment:
    """Research triage; scores never convert into probabilities or trades."""
    if case.capital_action is not None:
        raise ValueError("Capital deployment must be assessed in a separate process")
    if not case.ticker.strip() or not case.sector.strip():
        raise ValueError("Ticker and sector are mandatory")
    if any(key not in WEIGHTS for key in case.scoring):
        raise ValueError("Unknown scoring dimension")
    if any(not isinstance(value,(int,float)) or isinstance(value,bool) or not 0<=value<=1
           for value in case.scoring.values()):
        raise ValueError("Scores must be fractions in [0,1]")
    score=round(sum(WEIGHTS[k]*case.scoring.get(k,0) for k in WEIGHTS),1)
    valid=tuple(e for e in case.evidence if e.valid_asof(case.asof))
    independent=any(e.independent and not e.contradicts_thesis for e in valid)
    contradictions=tuple(case.contradictions)+tuple(e.fact for e in valid if e.contradicts_thesis)
    required=(case.causal_chain, case.next_2_to_4_quarter_trigger,
              case.cash_earnings_bridge, case.expectation_gap)
    if case.thesis_broken:
        return ResearchAssessment(case.ticker,"Reject",score,("THESIS_BROKEN",))
    if case.materially_rerated:
        return ResearchAssessment(case.ticker,"Too Late",score,("MATERIAL_PRICE_RECOGNITION",))
    if not valid:
        return ResearchAssessment(case.ticker,"Research Now",score,("NO_VALID_POINT_IN_TIME_EVIDENCE",))
    if not independent:
        return ResearchAssessment(case.ticker,"Research Now",score,("NO_INDEPENDENT_CORROBORATION",))
    if not all(s.strip() for s in required) or not case.kill_tests:
        return ResearchAssessment(case.ticker,"Research Now",score,("INCOMPLETE_CAUSAL_ECONOMICS_OR_KILL_TESTS",))
    if not case.price_recognition_checked:
        return ResearchAssessment(case.ticker,"EIP Watch",score,("PRICE_RECOGNITION_UNVERIFIED",))
    if score>=85 and case.scoring.get("valuation",0)>=0.75 and case.scoring.get("cash_earnings",0)>=0.7 and case.temporary_imperfections_explained:
        return ResearchAssessment(case.ticker,"Buy-zone Candidate",score,("RESEARCH_GATES_PASSED","SEPARATE_DEPLOYMENT_REVIEW_REQUIRED"))
    if score>=70 and case.scoring.get("valuation",0)>=0.6 and case.scoring.get("cash_earnings",0)>=0.6:
        return ResearchAssessment(case.ticker,"Earliest Investable Point",score,("LEADING_EVIDENCE_PRECEDES_FINANCIAL_CONFIRMATION",))
    if score>=50:
        return ResearchAssessment(case.ticker,"EIP Watch",score,("MATERIAL_UNCERTAINTY_REMAINS",))
    return ResearchAssessment(case.ticker,"Early Watch",score,("INSUFFICIENT_ASYMMETRY",))

def empty_scan_report(asof:date, assessments:Tuple[ResearchAssessment,...]) -> dict:
    qualifying=[a.ticker for a in assessments if a.classification in ("Earliest Investable Point","Buy-zone Candidate")]
    return {"asof":asof.isoformat(),"fresh_qualifiers":qualifying,
            "summary":("Fresh EIP candidates: "+", ".join(qualifying)) if qualifying else "No fresh high-conviction opportunity qualified.",
            "capital_deployment":"NOT_ASSESSED"}
