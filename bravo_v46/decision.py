"""BRAVO v4.6: evidence-gated research decisions, not trade instructions."""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from math import isfinite

class Verdict(str, Enum):
    ADD = "ADD"
    WAIT = "WAIT"
    REJECT = "REJECT"

@dataclass(frozen=True)
class Scenario:
    bear: float
    base: float
    bull: float
    bear_probability: float
    base_probability: float
    bull_probability: float
    years: float = 2.0

@dataclass(frozen=True)
class Evidence:
    causal_indicators: int
    independently_verified: bool
    valuation_reconciled: bool
    funding_credible: bool
    governance_hard_stop: bool = False
    thesis_broken: bool = False
    material_pending: bool = False
    trigger: str = ""
    review_date: date | None = None

@dataclass(frozen=True)
class Decision:
    verdict: Verdict
    rationale: str
    weighted_value: float | None
    annualized_value_return: float | None
    base_upside_to_bear_downside: float | None
    trigger: str
    review_date: date | None
    capital_authorized: bool = False

def evaluate(price: float, scenario: Scenario, evidence: Evidence,
             minimum_annual_return: float = 0.18,
             minimum_asymmetry: float = 2.0) -> Decision:
    values = (price, scenario.bear, scenario.base, scenario.bull,
              scenario.bear_probability, scenario.base_probability,
              scenario.bull_probability, scenario.years)
    if not all(isfinite(v) for v in values):
        raise ValueError("All numeric inputs must be finite")
    if price <= 0 or scenario.years <= 0 or min(scenario.bear, scenario.base, scenario.bull) < 0:
        raise ValueError("Invalid price, valuation, or horizon")
    if not scenario.bear <= scenario.base <= scenario.bull:
        raise ValueError("Scenario values must be ordered bear <= base <= bull")
    probs = (scenario.bear_probability, scenario.base_probability, scenario.bull_probability)
    if any(p < 0 or p > 1 for p in probs) or abs(sum(probs) - 1) > 1e-8:
        raise ValueError("Probabilities must be in [0,1] and sum to one")
    if not 0 <= minimum_annual_return < 1 or minimum_asymmetry <= 0:
        raise ValueError("Invalid decision thresholds")
    if evidence.causal_indicators < 0:
        raise ValueError("Invalid indicator count")
    expected = sum(v*p for v,p in zip((scenario.bear, scenario.base, scenario.bull), probs))
    annual = (expected / price)**(1/scenario.years)-1
    downside = price - scenario.bear
    asymmetry = (scenario.base-price)/downside if downside > 0 else None
    def result(v, reason):
        return Decision(v, reason, expected, annual, asymmetry,
                        evidence.trigger, evidence.review_date, False)
    if evidence.governance_hard_stop or evidence.thesis_broken:
        return result(Verdict.REJECT, "Confirmed governance or thesis-breaking failure")
    if not evidence.independently_verified or not evidence.valuation_reconciled:
        return result(Verdict.WAIT, "Decision-critical evidence or diluted valuation unverified")
    if evidence.material_pending or not evidence.funding_credible:
        return result(Verdict.WAIT, "Material funding or evidence gate unresolved")
    if evidence.causal_indicators < 2:
        return result(Verdict.REJECT, "Insufficient independent causal indicators")
    if annual >= minimum_annual_return and (asymmetry is None or asymmetry >= minimum_asymmetry) and scenario.base > price:
        return result(Verdict.ADD, "Evidence and scenario-based return hurdles passed")
    return result(Verdict.REJECT, "Risk-adjusted return or downside asymmetry inadequate")
