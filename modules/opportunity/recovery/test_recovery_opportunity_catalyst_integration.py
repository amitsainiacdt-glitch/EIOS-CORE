"""
EIOS
Everest Investment Operating System

Recovery Opportunity → Catalyst Engine Integration Test

Purpose
-------
Proves that a Recovery Opportunity Signal can cross the
canonical Signal boundary and be consumed by the existing
Catalyst Engine.

This test does NOT modify the Catalyst Engine.

Architecture under test:

Recovery Opportunity Signal
        ↓
Recovery Opportunity Adapter
        ↓
Canonical Opportunity Signal
        ↓
Catalyst Engine
        ↓
Catalyst Assessment
"""

from copy import deepcopy

from modules.opportunity.catalyst_engine import (
    CatalystEngine,
    Catalyst,
)

from modules.opportunity.recovery.recovery_opportunity_adapter import (
    RecoveryOpportunityAdapter,
)

from modules.opportunity.recovery.recovery_opportunity_signal import (
    RecoveryOpportunitySignal,
    RecoveryOpportunityStage,
    RecoveryOpportunityDirection,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDirection,
    SignalStage,
)


# ==========================================================
# RECOVERY SIGNAL FACTORY
# ==========================================================


def make_recovery_signal() -> RecoveryOpportunitySignal:
    """
    Create a deterministic Recovery Opportunity Signal
    suitable for Catalyst Engine integration testing.
    """

    signal = RecoveryOpportunitySignal()

    signal.signal_id = (
        "REC-OPP::CATALYST-INTEGRATION"
    )

    signal.theme_id = (
        "THEME::INDUSTRIAL-RECOVERY"
    )

    signal.theme_name = (
        "Industrial Capital Recovery"
    )

    signal.recovery_breadth = 80.0

    signal.confirmed_recovery_breadth = 60.0

    signal.recovery_confidence = 85.0

    signal.recovery_coherence = 75.0

    signal.temporal_support = 75.0

    signal.persistence_score = 70.0

    signal.contradiction_score = 10.0

    signal.catalyst_count = 2

    signal.catalyst_confidence = 85.0

    signal.catalyst_strength = 80.0

    signal.catalyst_coherence = 75.0

    signal.catalyst_supported = True

    signal.broad_recovery_supported = True

    signal.confirmed_recovery_supported = True

    signal.direction = (
        RecoveryOpportunityDirection.POSITIVE
    )

    signal.stage = (
        RecoveryOpportunityStage.ACTIONABLE
    )

    signal.opportunity_ready = True

    signal.requires_more_evidence = False

    signal.catalyst_families = [
        "CAPACITY_EXPANSION",
    ]

    signal.catalyst_patterns = [
        "NEW_CAPACITY_ONLINE",
    ]

    signal.evidence_sources = [
        "Recovery Source A",
        "Recovery Source B",
    ]

    signal.supporting_evidence = [
        "Industrial demand recovery",
        "Capacity expansion",
        "Improving utilisation",
    ]

    signal.contradictory_evidence = []

    return signal


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    # ======================================================
    # 1. ENGINE EXISTS
    # ======================================================

    engine = CatalystEngine()

    assert engine is not None

    print(
        "Catalyst Engine Exists          : PASS"
    )

    # ======================================================
    # 2. ADAPTER EXISTS
    # ======================================================

    adapter = RecoveryOpportunityAdapter()

    assert adapter is not None

    print(
        "Recovery Adapter Exists         : PASS"
    )

    # ======================================================
    # 3. RECOVERY → CANONICAL SIGNAL
    # ======================================================

    recovery_signal = (
        make_recovery_signal()
    )

    canonical_signal = (
        adapter.create_signal(
            recovery_signal
        )
    )

    assert isinstance(
        canonical_signal,
        Signal,
    )

    print(
        "Canonical Signal Creation       : PASS"
    )

    # ======================================================
    # 4. RECOVERY IDENTITY SURVIVES
    # ======================================================

    assert (
        canonical_signal.signal_id
        == (
            "RECOVERY::"
            "REC-OPP::CATALYST-INTEGRATION"
        )
    )

    assert (
        canonical_signal.themes
        == [
            "Industrial Capital Recovery"
        ]
    )

    print(
        "Recovery Identity Transfer      : PASS"
    )

    # ======================================================
    # 5. RECOVERY DIRECTION SURVIVES
    # ======================================================

    assert (
        canonical_signal.direction
        == SignalDirection.POSITIVE
    )

    assert (
        canonical_signal.stage
        == SignalStage.CATALYST
    )

    print(
        "Recovery Classification         : PASS"
    )

    # ======================================================
    # 6. RECOVERY EVIDENCE SURVIVES
    # ======================================================

    assert (
        canonical_signal.evidence
        == [
            "Recovery Source A",
            "Recovery Source B",
        ]
    )

    assert (
        canonical_signal.contradictory_evidence
        == []
    )

    assert (
        canonical_signal.confidence
        == 85.0
    )

    print(
        "Recovery Evidence Transfer      : PASS"
    )

    # ======================================================
    # 7. INPUT IMMUTABILITY
    # ======================================================

    recovery_copy = deepcopy(
        recovery_signal
    )

    adapter.create_signal(
        recovery_signal
    )

    assert (
        recovery_signal
        == recovery_copy
    )

    print(
        "Recovery Input Immutability     : PASS"
    )

    # ======================================================
    # 8. CATALYST ENGINE CONSUMES
    # ======================================================

    catalyst = engine.analyze(
        catalyst_id=(
            "CAT::RECOVERY::"
            "INDUSTRIAL-CAPITAL"
        ),
        title=(
            "Industrial Capital Recovery"
        ),
        trigger=(
            "Broadening industrial recovery "
            "with supporting capacity expansion."
        ),
        signals=[
            canonical_signal
        ],
        description=(
            "Recovery-derived catalyst "
            "integration test."
        ),
        economic_impact=(
            "Improving industrial demand and "
            "capacity utilisation."
        ),
        earnings_impact=(
            "Potential improvement in earnings "
            "through demand and utilisation recovery."
        ),
        affected_sectors=[
            "Industrial",
        ],
        affected_companies=[],
        assumptions=[],
        invalidation_conditions=[
            "Recovery breadth contracts materially.",
            "Catalyst evidence deteriorates.",
        ],
    )

    assert isinstance(
        catalyst,
        Catalyst,
    )

    print(
        "Catalyst Engine Consumption     : PASS"
    )

    # ======================================================
    # 9. SIGNAL PRESERVED IN CATALYST
    # ======================================================

    assert (
        len(catalyst.signals)
        == 1
    )

    assert (
        catalyst.signals[0]
        == canonical_signal
    )

    print(
        "Signal Preservation             : PASS"
    )

    # ======================================================
    # 10. DIRECTION TRANSFERRED
    # ======================================================

    assert (
        catalyst.direction
        == SignalDirection.POSITIVE
    )

    print(
        "Catalyst Direction              : PASS"
    )

    # ======================================================
    # 11. EVIDENCE COLLECTED
    # ======================================================

    assert (
        len(catalyst.evidence)
        >= 1
    )

    print(
        "Catalyst Evidence Collection    : PASS"
    )

    # ======================================================
    # 12. CONTRADICTIONS PRESERVED
    # ======================================================

    assert (
        catalyst.contradictory_evidence
        == canonical_signal.contradictory_evidence
    )

    print(
        "Contradiction Transfer          : PASS"
    )

    # ======================================================
    # 13. CATALYST ANALYSIS COMPLETED
    # ======================================================

    assert (
        catalyst.catalyst_score
        >= 0.0
    )

    assert (
        catalyst.catalyst_score
        <= 100.0
    )

    assert (
        catalyst.confidence
        >= 0.0
    )

    assert (
        catalyst.confidence
        <= 100.0
    )

    print(
        "Catalyst Analysis               : PASS"
    )

    # ======================================================
    # 14. NO SOURCE MUTATION
    # ======================================================

    assert (
        canonical_signal.direction
        == SignalDirection.POSITIVE
    )

    assert (
        canonical_signal.confidence
        == 85.0
    )

    assert (
        canonical_signal.evidence
        == [
            "Recovery Source A",
            "Recovery Source B",
        ]
    )

    print(
        "Canonical Signal Immutability   : PASS"
    )

    # ======================================================
    # 15. DETERMINISM
    # ======================================================

    second_signal = (
        adapter.create_signal(
            make_recovery_signal()
        )
    )

    second_catalyst = engine.analyze(
        catalyst_id=(
            "CAT::RECOVERY::"
            "INDUSTRIAL-CAPITAL"
        ),
        title=(
            "Industrial Capital Recovery"
        ),
        trigger=(
            "Broadening industrial recovery "
            "with supporting capacity expansion."
        ),
        signals=[
            second_signal
        ],
        description=(
            "Recovery-derived catalyst "
            "integration test."
        ),
        economic_impact=(
            "Improving industrial demand and "
            "capacity utilisation."
        ),
        earnings_impact=(
            "Potential improvement in earnings "
            "through demand and utilisation recovery."
        ),
        affected_sectors=[
            "Industrial",
        ],
        affected_companies=[],
        assumptions=[],
        invalidation_conditions=[
            "Recovery breadth contracts materially.",
            "Catalyst evidence deteriorates.",
        ],
    )

    assert (
        catalyst.direction
        == second_catalyst.direction
    )

    assert (
        catalyst.horizon
        == second_catalyst.horizon
    )

    assert (
        catalyst.magnitude
        == second_catalyst.magnitude
    )

    assert (
        catalyst.probability
        == second_catalyst.probability
    )

    assert (
        catalyst.persistence
        == second_catalyst.persistence
    )

    assert (
        catalyst.catalyst_score
        == second_catalyst.catalyst_score
    )

    assert (
        catalyst.confidence
        == second_catalyst.confidence
    )

    print(
        "Deterministic Integration        : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY → CANONICAL SIGNAL "
        "→ CATALYST ENGINE : PASS"
    )


if __name__ == "__main__":
    main()