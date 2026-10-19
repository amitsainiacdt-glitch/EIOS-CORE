"""EIOS Earnings Multiplication and Supplier-Graph Research Engine.

Pure, point-in-time calculations. All financial inputs are sourced externally;
this module has NO market-data ingestion and NEVER issues capital instructions.
"""
from dataclasses import dataclass
from datetime import date
from typing import Tuple, Optional


@dataclass(frozen=True)
class LinkEvidence:
    supplier: str
    customer: str
    relationship: str
    source_url: str
    published_on: date
    asof: date
    independent: bool
    customer_programme: str = ""

    def __post_init__(self):
        if not (self.supplier.strip() and self.customer.strip() and self.relationship.strip()):
            raise ValueError("Supplier, customer and relationship required")
        if not self.source_url.startswith("https://"):
            raise ValueError("HTTPS evidence reference required")
        if self.published_on > self.asof:
            raise ValueError("Future information forbidden")


@dataclass(frozen=True)
class EconomicScenario:
    """INR crore unless otherwise labelled. Inputs are scenario assumptions."""
    name: str
    sales: float
    operating_margin_pct: float
    depreciation: float
    interest: float
    tax_rate_pct: float
    capex: float
    incremental_working_capital: float
    diluted_shares_crore: float
    exit_pe: float

    def __post_init__(self):
        if min(self.sales, self.depreciation, self.interest, self.capex,
               self.incremental_working_capital) < 0:
            raise ValueError("Negative economic inputs not supported")
        if not 0 <= self.operating_margin_pct <= 100 or not 0 <= self.tax_rate_pct <= 100:
            raise ValueError("Invalid percentage")
        if self.diluted_shares_crore <= 0 or self.exit_pe <= 0:
            raise ValueError("Shares and multiples must be positive")


@dataclass(frozen=True)
class ScenarioOutcome:
    name: str
    ebit: float
    pat: float
    eps: float
    owner_cash_after_growth: float
    cash_per_share: float
    implied_price: float


def calculate(scenario: EconomicScenario) -> ScenarioOutcome:
    ebit = scenario.sales * scenario.operating_margin_pct / 100
    pretax = ebit - scenario.depreciation - scenario.interest
    pat = pretax - max(pretax, 0) * scenario.tax_rate_pct / 100
    owner_cash = pat + scenario.depreciation - scenario.capex - scenario.incremental_working_capital
    return ScenarioOutcome(scenario.name, round(ebit, 4), round(pat, 4),
                           round(pat / scenario.diluted_shares_crore, 4),
                           round(owner_cash, 4),
                           round(owner_cash / scenario.diluted_shares_crore, 4),
                           round((pat / scenario.diluted_shares_crore) * scenario.exit_pe, 4))


@dataclass(frozen=True)
class MultiplicationCase:
    ticker: str
    asof: date
    market_price: Optional[float]
    current: EconomicScenario
    bear: EconomicScenario
    base: EconomicScenario
    bull: EconomicScenario
    links: Tuple[LinkEvidence, ...] = ()
    existing_shareholder_dilution_checked: bool = False
    price_recognition_checked: bool = False
    causal_evidence_verified: bool = False
    thesis_kill_tests: Tuple[str, ...] = ()


@dataclass(frozen=True)
class MultiplicationAssessment:
    ticker: str
    status: str
    base_owner_cash_multiple: Optional[float]
    bull_owner_cash_multiple: Optional[float]
    scenario_prices: Tuple[Tuple[str, float], ...]
    research_reasons: Tuple[str, ...]
    capital_action: str = "NOT_ASSESSED"


def assess_multiplication(case: MultiplicationCase) -> MultiplicationAssessment:
    """Conservative triage: never converts upside scenarios into return probabilities."""
    if not case.ticker.strip():
        raise ValueError("Ticker required")
    if any(link.asof > case.asof for link in case.links):
        raise ValueError("Later supplier evidence is prohibited")
    outcomes = tuple(calculate(s) for s in (case.bear, case.base, case.bull))
    now = calculate(case.current)
    prices = tuple((x.name, x.implied_price) for x in outcomes)
    if not (outcomes[0].implied_price <= outcomes[1].implied_price <= outcomes[2].implied_price):
        raise ValueError("Scenarios must be ordered bear <= base <= bull")
    reasons = []
    if case.market_price is None or case.market_price <= 0:
        reasons.append("PRICE_UNAVAILABLE")
    if not case.price_recognition_checked:
        reasons.append("RECOGNITION_NOT_CHECKED")
    if not case.causal_evidence_verified:
        reasons.append("CAUSAL_EVIDENCE_UNVERIFIED")
    if not case.existing_shareholder_dilution_checked:
        reasons.append("DILUTION_UNVERIFIED")
    if not case.thesis_kill_tests:
        reasons.append("KILL_TESTS_MISSING")
    if now.owner_cash_after_growth <= 0:
        reasons.append("NON_POSITIVE_BASELINE_OWNER_CASH")
        multiples = (None, None)
    else:
        multiples = (round(outcomes[1].owner_cash_after_growth/now.owner_cash_after_growth,2),
                     round(outcomes[2].owner_cash_after_growth/now.owner_cash_after_growth,2))
    if case.links and not any(link.independent for link in case.links):
        reasons.append("RELATIONSHIPS_NOT_INDEPENDENTLY_CORROBORATED")
    if reasons:
        status = "RESEARCH_INCOMPLETE"
    elif outcomes[1].owner_cash_after_growth <= 0:
        status = "ECONOMIC_CAUTION"
    elif case.market_price is not None and outcomes[1].implied_price <= case.market_price:
        status = "INSUFFICIENT_BASE_VALUATION_ASYMMETRY"
    else:
        status = "READY_FOR_SEPARATE_EIP_REVIEW"
    return MultiplicationAssessment(case.ticker,status,*multiples,prices,tuple(reasons))


def independently_verified_suppliers(links: Tuple[LinkEvidence, ...], asof: date) -> Tuple[str, ...]:
    """Neutral supplier candidates: do not infer relationships from sector proximity."""
    return tuple(sorted({x.supplier for x in links if x.independent and x.asof <= asof and x.published_on <= asof}))
