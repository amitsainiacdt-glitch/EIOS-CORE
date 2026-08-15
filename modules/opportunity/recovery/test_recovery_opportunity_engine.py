"""
EIOS
Recovery Opportunity Engine Tests
"""

from copy import deepcopy

from modules.opportunity.recovery.recovery_opportunity_engine import (
    RecoveryOpportunityEngine,
)

from modules.opportunity.recovery.recovery_opportunity_signal import (
    RecoveryOpportunityStage,
    RecoveryOpportunityDirection,
    RecoveryOpportunityConfidence,
)

from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
    RecoveryThemeStage,
    RecoveryThemeDirection,
)

from modules.opportunity.recovery.recovery_theme_catalyst_link import (
    RecoveryThemeCatalystLink,
    RecoveryCatalystRelationship,
    RecoveryCatalystRelevance,
    RecoveryCatalystTransmission,
)


def make_theme(
    breadth=80.0,
    confirmed=60.0,
    confidence=85.0,
    coherence=75.0,
    temporal=75.0,
    persistence=70.0,
    contradiction=10.0,
):

    theme = RecoveryThemeAssessment()

    theme.theme_id = "THEME-001"

    theme.theme_name = (
        "Industrial Capital Recovery"
    )

    theme.stage = (
        RecoveryThemeStage.VALIDATED
    )

    theme.direction = (
        RecoveryThemeDirection.POSITIVE
    )

    theme.recovery_breadth = breadth

    theme.confirmed_recovery_breadth = confirmed

    theme.confidence = confidence

    theme.coherence_score = coherence

    theme.temporal_support = temporal

    theme.persistence_score = persistence

    theme.contradiction_score = contradiction

    return theme


def make_link(
    relationship=RecoveryCatalystRelationship.SUPPORTING,
    confidence=80.0,
    strength=80.0,
):

    link = RecoveryThemeCatalystLink()

    link.link_id = "LINK-001"

    link.theme_id = "THEME-001"

    link.theme_name = (
        "Industrial Capital Recovery"
    )

    link.catalyst_id = "CAT-001"

    link.catalyst_family = (
        "CAPACITY_EXPANSION"
    )

    link.catalyst_pattern = (
        "NEW_CAPACITY_ONLINE"
    )

    link.relevance = (
        RecoveryCatalystRelevance.HIGH
    )

    link.relationship = relationship

    link.transmission = (
        RecoveryCatalystTransmission.CAPACITY
    )

    link.catalyst_confidence = confidence

    link.catalyst_strength = strength

    link.supporting_evidence = [
        "Capacity expansion"
    ]

    link.evidence_sources = [
        "Source-A"
    ]

    return link


def main():

    engine = RecoveryOpportunityEngine()

    # ======================================================
    # ENGINE EXISTS
    # ======================================================

    assert engine is not None

    print(
        "Engine Exists                   : PASS"
    )

    # ======================================================
    # EMPTY THEME
    # ======================================================

    result = engine.assess(
        None,
        [],
    )

    assert (
        result.stage
        == RecoveryOpportunityStage.UNKNOWN
    )

    assert (
        result.opportunity_ready
        is False
    )

    print(
        "Empty Theme                    : PASS"
    )

    # ======================================================
    # THEME WITHOUT CATALYST
    # ======================================================

    theme = make_theme()

    result = engine.assess(
        theme,
        [],
    )

    assert (
        result.catalyst_count
        == 0
    )

    assert (
        result.catalyst_supported
        is False
    )

    assert (
        result.opportunity_ready
        is False
    )

    assert (
        result.stage
        == RecoveryOpportunityStage.DEVELOPING
    )

    print(
        "Recovery Without Catalyst      : PASS"
    )

    # ======================================================
    # CATALYST SUPPORT
    # ======================================================

    link = make_link()

    result = engine.assess(
        theme,
        [link],
    )

    assert (
        result.catalyst_count
        == 1
    )

    assert (
        result.catalyst_supported
        is True
    )

    assert (
        result.supporting_catalyst_count
        == 1
    )

    print(
        "Catalyst Support               : PASS"
    )

    # ======================================================
    # BROAD RECOVERY
    # ======================================================

    assert (
        result.broad_recovery_supported
        is True
    )

    assert (
        result.confirmed_recovery_supported
        is True
    )

    print(
        "Recovery Gates                 : PASS"
    )

    # ======================================================
    # ACTIONABLE
    # ======================================================

    assert (
        result.stage
        == RecoveryOpportunityStage.ACTIONABLE
    )

    assert (
        result.direction
        == RecoveryOpportunityDirection.POSITIVE
    )

    assert (
        result.opportunity_ready
        is True
    )

    assert (
        result.requires_more_evidence
        is False
    )

    print(
        "Actionable Recovery Signal     : PASS"
    )

    # ======================================================
    # CATALYST TRANSFER
    # ======================================================

    assert (
        result.catalyst_families
        == ["CAPACITY_EXPANSION"]
    )

    assert (
        result.catalyst_patterns
        == ["NEW_CAPACITY_ONLINE"]
    )

    assert (
        "Source-A"
        in result.evidence_sources
    )

    print(
        "Catalyst Evidence Transfer    : PASS"
    )

    # ======================================================
    # LOW BREADTH
    # ======================================================

    weak_theme = make_theme(
        breadth=30.0,
        confirmed=10.0,
        confidence=60.0,
        coherence=50.0,
    )

    result = engine.assess(
        weak_theme,
        [link],
    )

    assert (
        result.opportunity_ready
        is False
    )

    assert (
        result.stage
        != RecoveryOpportunityStage.ACTIONABLE
    )

    print(
        "Low Breadth Rejection          : PASS"
    )

    # ======================================================
    # LOW CONFIRMED RECOVERY
    # ======================================================

    weak_confirmation = make_theme(
        breadth=80.0,
        confirmed=20.0,
        confidence=85.0,
        coherence=75.0,
    )

    result = engine.assess(
        weak_confirmation,
        [link],
    )

    assert (
        result.broad_recovery_supported
        is True
    )

    assert (
        result.confirmed_recovery_supported
        is False
    )

    assert (
        result.opportunity_ready
        is False
    )

    print(
        "Low Confirmation Rejection     : PASS"
    )

    # ======================================================
    # WEAK CATALYST
    # ======================================================

    weak_link = make_link(
        confidence=30.0,
        strength=30.0,
    )

    result = engine.assess(
        theme,
        [weak_link],
    )

    assert (
        result.catalyst_supported
        is False
    )

    assert (
        result.opportunity_ready
        is False
    )

    print(
        "Weak Catalyst Rejection        : PASS"
    )

    # ======================================================
    # CONTRADICTION
    # ======================================================

    contradictory_theme = make_theme(
        contradiction=70.0,
    )

    result = engine.assess(
        contradictory_theme,
        [link],
    )

    assert (
        result.direction
        == RecoveryOpportunityDirection.NEGATIVE
    )

    assert (
        result.opportunity_ready
        is False
    )

    assert (
        len(result.warnings)
        > 0
    )

    print(
        "Contradictory Recovery         : PASS"
    )

    # ======================================================
    # CONFIDENCE RANGE
    # ======================================================

    assert (
        result.confidence_level
        in {
            RecoveryOpportunityConfidence.UNKNOWN,
            RecoveryOpportunityConfidence.LOW,
            RecoveryOpportunityConfidence.MODERATE,
            RecoveryOpportunityConfidence.HIGH,
            RecoveryOpportunityConfidence.VERY_HIGH,
        }
    )

    print(
        "Confidence Classification       : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    theme_copy = deepcopy(
        theme
    )

    link_copy = deepcopy(
        link
    )

    engine.assess(
        theme,
        [link],
    )

    assert (
        theme
        == theme_copy
    )

    assert (
        link
        == link_copy
    )

    print(
        "Input Immutability              : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    first = engine.assess(
        theme,
        [link],
    )

    second = engine.assess(
        theme,
        [link],
    )

    assert (
        first.stage
        == second.stage
    )

    assert (
        first.direction
        == second.direction
    )

    assert (
        first.opportunity_ready
        == second.opportunity_ready
    )

    assert (
        first.catalyst_supported
        == second.catalyst_supported
    )

    assert (
        first.reasons
        == second.reasons
    )

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # TRANSPARENT REASONING
    # ======================================================

    assert (
        len(first.reasons)
        > 0
    )

    assert all(
        isinstance(
            reason,
            str,
        )
        for reason in first.reasons
    )

    assert any(
        "Opportunity Engine"
        in text
        for text in (
            first.warnings
            + first.reasons
        )
    )

    print(
        "Transparent Reasoning          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY OPPORTUNITY "
        "ENGINE : PASS"
    )


if __name__ == "__main__":
    main()