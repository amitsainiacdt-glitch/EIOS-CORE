from dataclasses import dataclass, field


@dataclass
class ValuationSection:
    """
    Stores valuation analysis for the company.
    """

    intrinsic_value: float = 0.0
    current_price: float = 0.0
    margin_of_safety: float = 0.0

    fair_value: float = 0.0
    expected_cagr: float = 0.0

    valuation_method: str = ""

    assumptions: list[str] = field(default_factory=list)

    risks: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)