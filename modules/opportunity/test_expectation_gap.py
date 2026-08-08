"""
EIOS
Everest Investment Operating System

Expectation Gap Test
"""

from modules.opportunity.catalyst_engine import (
    CatalystEngine,
)

from modules.opportunity.expectation_gap_engine import (
    ExpectationGapEngine,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)


def main():

    print("=" * 60)
    print("EIOS EXPECTATION GAP TEST")
    print("=" * 60)

    # ==========================================================
    # SIGNAL
    # ==========================================================

    signal = Signal(
        signal_id="GAP-001",
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
        catalyst_id="CAT-GAP-001",
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
            "Industrial capex remains elevated."
        ],
        invalidation_conditions=[
            "Industrial orders materially weaken."
        ],
    )

    print("\nCatalyst")
    print(
        f"Score      : "
        f"{catalyst.catalyst_score:.2f}"
    )
    print(
        f"Confidence : "
        f"{catalyst.confidence:.2f}"
    )

    # ==========================================================
    # EXPECTATION GAP
    # ==========================================================

    gap_engine = ExpectationGapEngine()

    gap = gap_engine.analyze(
        gap_id="GAP-001",
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

    print("\nExpectation Gap")

    print(
        f"Market Expectation : "
        f"{gap.market_expectation:.2f}"
    )

    print(
        f"EIOS Expectation   : "
        f"{gap.eios_expectation:.2f}"
    )

    print(
        f"Expectation Gap    : "
        f"{gap.expectation_difference:.2f}"
    )

    print(
        f"Market Earnings    : "
        f"{gap.market_earnings_expectation:.2f}"
    )

    print(
        f"EIOS Earnings      : "
        f"{gap.eios_earnings_expectation:.2f}"
    )

    print(
        f"Earnings Gap       : "
        f"{gap.earnings_gap:.2f}"
    )

    print(
        f"Unrecognized       : "
        f"{gap.unrecognized_potential:.2f}"
    )

    print(
        f"Gap Score          : "
        f"{gap.gap_score:.2f}"
    )

    print(
        f"Confidence         : "
        f"{gap.confidence:.2f}"
    )

    print(
        f"Positive Gap       : "
        f"{gap.positive_gap}"
    )

    # ==========================================================
    # ASSERTIONS
    # ==========================================================

    assert gap.expectation_difference == 35.0

    assert gap.earnings_gap == 35.0

    assert gap.positive_gap

    assert not gap.negative_gap

    assert gap.gap_score > 0

    assert gap.confidence > 0

    assert len(
        gap.invalidation_conditions
    ) == 2

    print("\nExpectation Gap Test : PASS")

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("EXPECTATION GAP : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()