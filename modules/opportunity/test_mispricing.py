"""
EIOS
Everest Investment Operating System

Mispricing Engine Test
"""

from dataclasses import dataclass

from modules.opportunity.catalyst_engine import (
    CatalystEngine,
)

from modules.opportunity.expectation_gap_engine import (
    ExpectationGapEngine,
)

from modules.opportunity.mispricing_engine import (
    MispricingEngine,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)


# ==========================================================
# TEST VALUATION OBJECT
# ==========================================================

@dataclass
class TestValuation:

    intrinsic_value: float = 4518.65

    fair_value: float = 4518.65

    confidence: float = 80.0


def main():

    print("=" * 60)
    print("EIOS MISPRICING ENGINE TEST")
    print("=" * 60)

    # ==========================================================
    # CURRENT MARKET PRICE
    # ==========================================================

    cmp = 3500.0

    valuation = TestValuation()

    # ==========================================================
    # SIGNAL
    # ==========================================================

    signal = Signal(
        signal_id="MIS-001",
        title="Industrial Capex Acceleration",
        description=(
            "Industrial investment is accelerating."
        ),
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=85.0,
        probability=85.0,
        relevance=90.0,
        persistence=85.0,
        confidence=85.0,
        market_recognition=25.0,
        source="Industry Data",
        supporting_sources=[
            "Industry Data",
            "Company Disclosures",
        ],
        evidence=[
            "Order inflows accelerating.",
            "Capacity expansion increasing.",
        ],
        sectors=[
            "Capital Goods",
        ],
        companies=[
            "The Anup Engineering Limited",
        ],
        independent_confirmation=2,
    )

    # ==========================================================
    # CATALYST
    # ==========================================================

    catalyst_engine = CatalystEngine()

    catalyst = catalyst_engine.analyze(
        catalyst_id="MIS-CAT-001",
        title="Capital Goods Cycle Acceleration",
        trigger="Industrial capex acceleration",
        signals=[signal],
        description=(
            "Industrial investment is creating stronger "
            "demand for capital goods."
        ),
        economic_impact=(
            "Higher equipment demand and utilization."
        ),
        earnings_impact=(
            "Potential revenue and margin acceleration."
        ),
        affected_sectors=[
            "Capital Goods",
        ],
        affected_companies=[
            "The Anup Engineering Limited",
        ],
        assumptions=[
            "Industrial capex remains elevated.",
        ],
        invalidation_conditions=[
            "Industrial orders materially weaken.",
        ],
    )

    # ==========================================================
    # EXPECTATION GAP
    # ==========================================================

    gap_engine = ExpectationGapEngine()

    expectation_gap = gap_engine.analyze(
        gap_id="MIS-GAP-001",
        company="The Anup Engineering Limited",
        sector="Capital Goods",
        catalyst=catalyst,
        market_expectation=45.0,
        eios_expectation=80.0,
        market_earnings_expectation=40.0,
        eios_earnings_expectation=75.0,
        assumptions=[
            "Order growth persists.",
            "Capacity additions translate into revenue.",
        ],
        invalidation_conditions=[
            "Order inflows reverse.",
            "Industrial capex cycle weakens.",
        ],
    )

    # ==========================================================
    # MISPRICING
    # ==========================================================

    engine = MispricingEngine()

    result = engine.analyze(
        company="The Anup Engineering Limited",
        cmp=cmp,
        valuation=valuation,
        catalyst=catalyst,
        expectation_gap=expectation_gap,
        assumptions=[
            "Existing intrinsic value estimate remains valid.",
            "Catalyst converts into earnings.",
        ],
        invalidation_conditions=[
            "Intrinsic value assumptions deteriorate.",
            "Catalyst fails to translate into earnings.",
        ],
    )

    # ==========================================================
    # OUTPUT
    # ==========================================================

    print("\nValuation")

    print(
        f"Current Price     : "
        f"{result.cmp:.2f}"
    )

    print(
        f"Intrinsic Value   : "
        f"{result.intrinsic_value:.2f}"
    )

    print(
        f"Fair Value        : "
        f"{result.fair_value:.2f}"
    )

    print(
        f"Valuation Upside  : "
        f"{result.valuation_upside:.2f}%"
    )

    print(
        f"Valuation Support : "
        f"{result.valuation_support}"
    )

    print("\nOpportunity Intelligence")

    print(
        f"Catalyst Score    : "
        f"{result.catalyst_score:.2f}"
    )

    print(
        f"Expectation Gap   : "
        f"{result.expectation_difference:.2f}"
    )

    print(
        f"Earnings Gap      : "
        f"{result.earnings_gap:.2f}"
    )

    print(
        f"Market Recognition: "
        f"{result.market_recognition:.2f}"
    )

    print(
        f"Mispricing Score  : "
        f"{result.mispricing_score:.2f}"
    )

    print(
        f"Confidence        : "
        f"{result.confidence:.2f}"
    )

    print(
        f"Potential Mispricing : "
        f"{result.potential_mispricing}"
    )

    # ==========================================================
    # ASSERTIONS
    # ==========================================================

    assert result.intrinsic_value == 4518.65

    assert result.fair_value == 4518.65

    assert result.valuation_upside > 0

    assert result.valuation_support

    assert result.catalyst_support

    assert result.expectation_support

    assert result.mispricing_score > 0

    assert result.confidence > 0

    assert result.potential_mispricing

    assert len(
        result.invalidation_conditions
    ) == 2

    print("\nMispricing Test : PASS")

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("MISPRICING ENGINE : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()