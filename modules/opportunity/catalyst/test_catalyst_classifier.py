"""
EIOS
Everest Investment Operating System

Catalyst Classifier Test Suite

Purpose
-------
Validate deterministic mapping of canonical Signals
to the EIOS Catalyst Taxonomy.

The tests intentionally do NOT invoke the Catalyst Engine.
"""

from modules.opportunity.catalyst.catalyst_classifier import (
    CatalystClassifier,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
    SignalStage,
    TimeHorizon,
)


# ==========================================================
# SIGNAL FACTORY
# ==========================================================


def make_signal(
    *,
    title: str,
    description: str = "",
    economic_mechanism: str = "",
    earnings_impact: str = "",
    themes: list[str] | None = None,
) -> Signal:
    """
    Create a canonical EIOS Signal for testing.
    """

    return Signal(
        signal_id=f"TEST-{title[:12].upper()}",
        title=title,
        description=description,
        domain=SignalDomain.COMPANY,
        signal_type=SignalType.CHANGE,
        direction=SignalDirection.POSITIVE,
        stage=SignalStage.VALIDATED,
        horizon=TimeHorizon.MEDIUM_TERM,
        source="Synthetic test source",
        source_type="Primary",
        companies=["TEST COMPANY"],
        sectors=["Industrial"],
        themes=themes or [],
        economic_mechanism=economic_mechanism,
        supply_demand_impact="Demand impact under test.",
        earnings_impact=earnings_impact,
    )


# ==========================================================
# CASE 1
# CLEAR REVENUE CATALYST
# ==========================================================


def test_revenue_catalyst() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title="Revenue growth acceleration",
        description=(
            "Company revenue growth is accelerating "
            "materially."
        ),
        economic_mechanism=(
            "Higher demand drives revenue growth."
        ),
        earnings_impact=(
            "Revenue and EPS are expected to increase."
        ),
    )

    result = classifier.classify(
        signals=[signal]
    )

    assert result.is_classified

    assert result.primary is not None

    assert (
        result.primary.family
        == CatalystFamily.REVENUE_GROWTH
    )

    assert result.confidence > 0.0

    print(
        "Case 1 — Revenue Catalyst       : PASS"
    )


# ==========================================================
# CASE 2
# CAPITAL CYCLE + CAPACITY
# ==========================================================


def test_capital_cycle_catalyst() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title="Industry capex acceleration",
        description=(
            "Industry capital expenditure is "
            "accelerating and capacity is tightening."
        ),
        economic_mechanism=(
            "Industry capex changes supply-demand "
            "economics."
        ),
        earnings_impact=(
            "Higher utilisation and pricing can "
            "increase margins."
        ),
        themes=[
            "Industry Capex",
            "Capital Cycle",
        ],
    )

    result = classifier.classify(
        signals=[signal]
    )

    assert result.is_classified

    assert result.primary is not None

    assert (
        result.primary.family
        == CatalystFamily.INDUSTRY_CAPITAL_CYCLE
    )

    print(
        "Case 2 — Capital Cycle Catalyst : PASS"
    )


# ==========================================================
# CASE 3
# REGULATORY / POLICY
# ==========================================================


def test_regulatory_catalyst() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title="Regulatory approval",
        description=(
            "New regulatory approval allows the "
            "company to enter an additional market."
        ),
        economic_mechanism=(
            "Regulatory approval removes a market-entry "
            "constraint."
        ),
        earnings_impact=(
            "The approval can create incremental revenue."
        ),
    )

    result = classifier.classify(
        signals=[signal]
    )

    assert result.is_classified

    assert result.primary is not None

    assert (
        result.primary.family
        == CatalystFamily.REGULATORY_CHANGE
    )

    print(
        "Case 3 — Regulatory Catalyst    : PASS"
    )


# ==========================================================
# CASE 4
# MULTI-CATALYST SIGNAL
# ==========================================================


def test_multi_catalyst() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title=(
            "China+1 supply chain relocation "
            "and capacity expansion"
        ),
        description=(
            "Global customers are relocating supply "
            "chains and the company is adding capacity."
        ),
        economic_mechanism=(
            "Supply-chain relocation creates incremental "
            "manufacturing demand."
        ),
        earnings_impact=(
            "Higher orders and capacity utilisation "
            "can accelerate earnings."
        ),
        themes=[
            "China+1",
            "Supply Chain",
            "Capacity Expansion",
        ],
    )

    result = classifier.classify(
        signals=[signal]
    )

    assert result.is_classified

    assert result.primary is not None

    assert len(result.secondary) >= 1

    families = {
        definition.family
        for definition in result.secondary
    }

    assert (
        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
        in families
        or
        CatalystFamily.CAPACITY_EXPANSION
        in families
    )

    print(
        "Case 4 — Multi-Catalyst         : PASS"
    )


# ==========================================================
# CASE 5
# UNKNOWN SIGNAL
# ==========================================================


def test_unknown_signal() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title="Unclassified observation",
        description=(
            "A completely novel observation with "
            "no recognised catalyst terminology."
        ),
        economic_mechanism=(
            "Unknown mechanism."
        ),
        earnings_impact=(
            "Unknown earnings impact."
        ),
        themes=[
            "Novel Theme XYZ",
        ],
    )

    result = classifier.classify(
        signals=[signal]
    )

    assert not result.is_classified

    assert result.primary is None

    assert result.confidence == 0.0

    assert len(
        result.unclassified_signals
    ) == 1

    assert len(
        result.warnings
    ) >= 1

    print(
        "Case 5 — Unknown Signal         : PASS"
    )


# ==========================================================
# CASE 6
# NO SIGNALS
# ==========================================================


def test_no_signals() -> None:

    classifier = CatalystClassifier()

    result = classifier.classify(
        signals=[]
    )

    assert not result.is_classified

    assert result.primary is None

    assert result.confidence == 0.0

    assert len(
        result.warnings
    ) >= 1

    print(
        "Case 6 — No Signals             : PASS"
    )


# ==========================================================
# CASE 7
# SOURCE IMMUTABILITY
# ==========================================================


def test_signal_not_mutated() -> None:

    classifier = CatalystClassifier()

    signal = make_signal(
        title="Revenue growth acceleration",
        description=(
            "Revenue growth is accelerating."
        ),
    )

    original_title = signal.title
    original_direction = signal.direction
    original_stage = signal.stage

    classifier.classify(
        signals=[signal]
    )

    assert signal.title == original_title

    assert (
        signal.direction
        == original_direction
    )

    assert (
        signal.stage
        == original_stage
    )

    print(
        "Case 7 — Signal Immutability     : PASS"
    )


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    print()
    print("=" * 60)
    print(
        "EIOS CATALYST CLASSIFIER TEST"
    )
    print("=" * 60)

    test_revenue_catalyst()

    test_capital_cycle_catalyst()

    test_regulatory_catalyst()

    test_multi_catalyst()

    test_unknown_signal()

    test_no_signals()

    test_signal_not_mutated()

    print()
    print("-" * 60)
    print(
        "EIOS CATALYST CLASSIFIER : PASS"
    )
    print("-" * 60)


if __name__ == "__main__":
    main()