"""
EIOS
Recovery Opportunity Adapter Tests
"""

from copy import deepcopy

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
    SignalDomain,
    SignalType,
    TimeHorizon,
    EvidenceQuality,
)


def make_signal():

    signal = RecoveryOpportunitySignal()

    signal.signal_id = (
        "REC-OPP::THEME-001"
    )

    signal.theme_id = "THEME-001"

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
        "CAPACITY_EXPANSION"
    ]

    signal.catalyst_patterns = [
        "NEW_CAPACITY_ONLINE"
    ]

    signal.evidence_sources = [
        "Source-A",
        "Source-B",
    ]

    signal.supporting_evidence = [
        "Capacity expansion",
        "Demand recovery",
    ]

    signal.contradictory_evidence = []

    return signal


def main():

    adapter = RecoveryOpportunityAdapter()

    # ======================================================
    # ADAPTER EXISTS
    # ======================================================

    assert adapter is not None

    print(
        "Adapter Exists                  : PASS"
    )

    # ======================================================
    # NONE INPUT PROTECTION
    # ======================================================

    try:
        adapter.create_signal(None)
        assert False
    except ValueError:
        pass

    print(
        "None Input Protection           : PASS"
    )

    # ======================================================
    # CANONICAL SIGNAL CREATION
    # ======================================================

    recovery = make_signal()

    result = (
        adapter.create_signal(
            recovery
        )
    )

    assert isinstance(
        result,
        Signal,
    )

    print(
        "Canonical Signal Creation       : PASS"
    )

    # ======================================================
    # IDENTITY
    # ======================================================

    assert (
        result.signal_id
        == "RECOVERY::REC-OPP::THEME-001"
    )

    assert (
        result.title
        == "Industrial Capital Recovery"
    )

    assert (
        result.themes
        == [
            "Industrial Capital Recovery"
        ]
    )

    print(
        "Identity Transfer               : PASS"
    )

    # ======================================================
    # CLASSIFICATION
    # ======================================================

    assert (
        result.domain
        == SignalDomain.SECTOR
    )

    assert (
        result.signal_type
        == SignalType.INFLECTION
    )

    assert (
        result.direction
        == SignalDirection.POSITIVE
    )

    assert (
        result.stage
        == SignalStage.CATALYST
    )

    assert (
        result.horizon
        == TimeHorizon.MEDIUM_TERM
    )

    print(
        "Classification Transfer         : PASS"
    )

    # ======================================================
    # STRENGTH
    # ======================================================

    assert (
        result.magnitude
        == 80.0
    )

    assert (
        result.probability
        == 85.0
    )

    assert (
        result.persistence
        == 70.0
    )

    assert (
        result.relevance
        == 75.0
    )

    assert (
        result.corroboration
        == 75.0
    )

    assert (
        result.confidence
        == 85.0
    )

    print(
        "Strength Transfer              : PASS"
    )

    # ======================================================
    # EVIDENCE
    # ======================================================

    assert (
        result.evidence
        == [
            "Source-A",
            "Source-B",
        ]
    )

    assert (
        result.supporting_sources
        == [
            "Source-A",
            "Source-B",
        ]
    )

    assert (
        result.contradictory_evidence
        == []
    )

    print(
        "Evidence Transfer              : PASS"
    )

    # ======================================================
    # CATALYST CONTEXT
    # ======================================================

    assert (
        result.causal_chain
        == [
            "NEW_CAPACITY_ONLINE"
        ]
    )

    assert (
        result.independent_confirmation
        == 2
    )

    assert (
        result.metadata[
            "origin"
        ]
        == "RECOVERY_INTELLIGENCE"
    )

    assert (
        result.metadata[
            "opportunity_ready"
        ]
        is True
    )

    assert (
        result.metadata[
            "catalyst_families"
        ]
        == [
            "CAPACITY_EXPANSION"
        ]
    )

    print(
        "Catalyst Context Transfer      : PASS"
    )

    # ======================================================
    # EVIDENCE QUALITY
    # ======================================================

    assert (
        result.evidence_quality
        == EvidenceQuality.A
    )

    print(
        "Evidence Quality Mapping       : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    recovery_copy = deepcopy(
        recovery
    )

    adapter.create_signal(
        recovery
    )

    assert (
        recovery
        == recovery_copy
    )

    print(
        "Input Immutability              : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    first = (
        adapter.create_signal(
            recovery
        )
    )

    second = (
        adapter.create_signal(
            recovery
        )
    )

    assert (
        first
        == second
    )

    print(
        "Deterministic Mapping           : PASS"
    )

    # ======================================================
    # RANGE PROTECTION
    # ======================================================

    extreme = make_signal()

    extreme.recovery_breadth = 999.0

    extreme.recovery_confidence = -50.0

    result = (
        adapter.create_signal(
            extreme
        )
    )

    assert (
        result.magnitude
        == 100.0
    )

    assert (
        result.probability
        == 0.0
    )

    print(
        "Numeric Range Protection        : PASS"
    )

    # ======================================================
    # NO VALUATION FABRICATION
    # ======================================================

    assert (
        result.valuation_impact
        == ""
    )

    assert (
        result.market_expectation
        == ""
    )

    assert (
        result.price_reaction
        == ""
    )

    print(
        "No Valuation Fabrication        : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY → OPPORTUNITY "
        "SIGNAL ADAPTER : PASS"
    )


if __name__ == "__main__":
    main()