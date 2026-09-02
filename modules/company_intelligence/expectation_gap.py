"""Fail-closed expectation-gap calculation for the valuation boundary."""

from dataclasses import dataclass

from .governed_market_data import GovernedMarketData


@dataclass(frozen=True)
class ExpectationGapResult:
    status: str
    verdict: str | None
    gap_percent: float | None
    explanation: str


def calculate_expectation_gap(market: GovernedMarketData, intrinsic_value: float | None) -> ExpectationGapResult:
    if not market.ready_for_valuation or intrinsic_value is None or intrinsic_value <= 0:
        return ExpectationGapResult(
            "BLOCKED_MISSING_VALUATION_INPUTS", None, None,
            "EIOS cannot measure an expectation gap until governed price, consensus expectations and intrinsic value are available.",
        )
    gap = (intrinsic_value / market.current_price - 1) * 100
    verdict = "POTENTIAL_UPSIDE" if gap >= 20 else "POTENTIAL_DOWNSIDE" if gap <= -20 else "NO_CLEAR_GAP"
    return ExpectationGapResult(
        "READY", verdict, round(gap, 1),
        f"Intrinsic value is {abs(gap):.1f}% {'above' if gap >= 0 else 'below'} the current price; this is a valuation observation, not a recommendation.",
    )


__all__ = ["ExpectationGapResult", "calculate_expectation_gap"]
