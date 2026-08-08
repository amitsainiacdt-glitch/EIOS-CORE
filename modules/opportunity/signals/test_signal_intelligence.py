"""
EIOS
Signal Intelligence Test

Purpose:
Verifies SignalIntelligenceEngine against different
signal conditions.
"""

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDomain,
    SignalType,
    SignalDirection,
)

from modules.opportunity.signals.signal_intelligence import (
    SignalIntelligenceEngine,
)


def main():

    engine = SignalIntelligenceEngine()

    print("=" * 60)
    print("EIOS SIGNAL INTELLIGENCE TEST")
    print("=" * 60)

    # ==========================================================
    # TEST 1 — STRENGTHENING SIGNAL
    # ==========================================================

    strengthening = Signal(
        signal_id="INTEL-001",
        title="Industrial Capex Acceleration",
        description="Industrial investment is accelerating.",
        domain=SignalDomain.MACRO,
        signal_type=SignalType.ACCELERATION,
        direction=SignalDirection.POSITIVE,
        magnitude=90.0,
        probability=85.0,
        relevance=90.0,
        persistence=85.0,
        independent_confirmation=3,
        supporting_sources=[
            "Source A",
            "Source B",
        ],
    )

    result = engine.analyze(
        strengthening
    )

    print("\nTest 1 — Strengthening")
    print(
        f"Strengthening : "
        f"{result.strengthening}"
    )
    print(
        f"Accelerating : "
        f"{result.accelerating}"
    )
    print(
        f"Persistent   : "
        f"{result.persistent}"
    )
    print(
        f"Confidence   : "
        f"{result.confidence:.2f}"
    )

    assert result.strengthening
    assert result.accelerating
    assert result.persistent

    print("PASS")

    # ==========================================================
    # TEST 2 — WEAK SIGNAL
    # ==========================================================

    weak = Signal(
        signal_id="INTEL-002",
        title="Weak Demand Indication",
        description="Initial indication of demand weakness.",
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.CHANGE,
        direction=SignalDirection.NEGATIVE,
        magnitude=25.0,
        probability=30.0,
        relevance=30.0,
        persistence=20.0,
        independent_confirmation=0,
    )

    result = engine.analyze(
        weak
    )

    print("\nTest 2 — Weak Signal")
    print(
        f"Weakening : "
        f"{result.weakening}"
    )
    print(
        f"Fading    : "
        f"{result.fading}"
    )
    print(
        f"Confidence: "
        f"{result.confidence:.2f}"
    )

    assert result.weakening
    assert result.fading

    print("PASS")

    # ==========================================================
    # TEST 3 — CONTRADICTORY SIGNAL
    # ==========================================================

    contradictory = Signal(
        signal_id="INTEL-003",
        title="Mixed Industry Evidence",
        description="Positive and negative evidence conflict.",
        domain=SignalDomain.SECTOR,
        signal_type=SignalType.DIVERGENCE,
        direction=SignalDirection.MIXED,
        magnitude=70.0,
        probability=65.0,
        relevance=75.0,
        persistence=70.0,
        independent_confirmation=2,
        supporting_sources=[
            "Source A",
            "Source B",
        ],
        contradictory_evidence=[
            "Evidence against A",
            "Evidence against B",
        ],
    )

    result = engine.analyze(
        contradictory
    )

    print("\nTest 3 — Contradictory Signal")
    print(
        f"Contradictory : "
        f"{result.contradictory}"
    )
    print(
        f"Contradiction Score : "
        f"{result.contradiction_score:.2f}"
    )

    assert result.contradictory

    print("PASS")

    # ==========================================================
    # TEST 4 — STABLE SIGNAL
    # ==========================================================

    stable = Signal(
        signal_id="INTEL-004",
        title="Stable Industry Trend",
        description="Industry conditions remain stable.",
        domain=SignalDomain.INDUSTRY
        if hasattr(SignalDomain, "INDUSTRY")
        else SignalDomain.SECTOR,
        signal_type=SignalType.TREND,
        direction=SignalDirection.NEUTRAL,
        magnitude=55.0,
        probability=60.0,
        relevance=60.0,
        persistence=60.0,
        independent_confirmation=1,
    )

    result = engine.analyze(
        stable
    )

    print("\nTest 4 — Stable Signal")
    print(
        f"Stable : "
        f"{result.stable}"
    )

    assert result.stable

    print("PASS")

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("SIGNAL INTELLIGENCE : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()