"""
EIOS
Signal Foundation Test

Purpose:
Verifies the canonical Signal, SignalRegistry and
SignalValidationEngine components.
"""

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)

from modules.opportunity.signals.signal_registry import (
    SignalRegistry,
)

from modules.opportunity.signals.signal_validation import (
    SignalValidationEngine,
)


def main():

    # ==========================================================
    # CREATE SIGNAL
    # ==========================================================

    signal = Signal(
        signal_id="TEST-001",
        title="Industrial Capex Acceleration",
        description=(
            "Evidence indicates accelerating industrial "
            "capital expenditure."
        ),
        domain=SignalDomain.MACRO,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        source="Test Source",
        detected_date="2026-08-08",
        sectors=[
            "Capital Goods",
        ],
        companies=[
            "The Anup Engineering Limited",
        ],
        evidence=[
            "Evidence A",
            "Evidence B",
            "Evidence C",
        ],
        supporting_sources=[
            "Source A",
            "Source B",
        ],
        relevance=90.0,
        persistence=80.0,
        independent_confirmation=2,
    )

    print("=" * 60)
    print("EIOS SIGNAL FOUNDATION TEST")
    print("=" * 60)

    print("\nSignal Created")
    print(f"ID      : {signal.signal_id}")
    print(f"Title   : {signal.title}")
    print(f"Domain  : {signal.domain.value}")

    # ==========================================================
    # REGISTRY
    # ==========================================================

    registry = SignalRegistry()

    registry.add(signal)

    print("\nRegistry")
    print(f"Signals : {registry.count()}")

    retrieved = registry.get(
        "TEST-001"
    )

    assert retrieved is signal

    company_signals = registry.by_company(
        "The Anup Engineering Limited"
    )

    assert len(company_signals) == 1

    sector_signals = registry.by_sector(
        "Capital Goods"
    )

    assert len(sector_signals) == 1

    domain_signals = registry.by_domain(
        SignalDomain.MACRO
    )

    assert len(domain_signals) == 1

    print("Registry Test : PASS")

    # ==========================================================
    # VALIDATION
    # ==========================================================

    validation_engine = (
        SignalValidationEngine()
    )

    result = validation_engine.validate(
        signal
    )

    print("\nValidation")
    print(
        f"Valid      : {result.valid}"
    )

    print(
        f"Score      : "
        f"{result.score:.2f}"
    )

    print(
        f"Confidence : "
        f"{result.confidence:.2f}"
    )

    assert result.score >= 0
    assert result.score <= 100

    assert result.confidence >= 0
    assert result.confidence <= 100

    print("Validation Test : PASS")

    # ==========================================================
    # DUPLICATE PROTECTION
    # ==========================================================

    duplicate_rejected = False

    try:

        registry.add(signal)

    except ValueError:

        duplicate_rejected = True

    assert duplicate_rejected

    print(
        "Duplicate Protection : PASS"
    )

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("SIGNAL FOUNDATION : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()