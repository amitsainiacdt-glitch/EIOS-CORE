"""
EIOS
Recovery Theme → Catalyst Intelligence Engine Tests
"""

from copy import deepcopy

from modules.opportunity.recovery.recovery_theme_catalyst_engine import (
    RecoveryThemeCatalystEngine,
)

from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
    RecoveryThemeStage,
    RecoveryThemeDirection,
)

from modules.opportunity.recovery.recovery_theme_catalyst_link import (
    RecoveryCatalystRelevance,
    RecoveryCatalystRelationship,
    RecoveryCatalystTransmission,
)


def make_theme():

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

    theme.recovery_breadth = 80.0

    theme.confirmed_recovery_breadth = 60.0

    theme.confidence = 85.0

    theme.economic_mechanism = (
        "Industrial capex recovery"
    )

    return theme


def make_catalyst():

    return {
        "catalyst_id": "CAT-001",
        "catalyst_family": "CAPACITY_EXPANSION",
        "catalyst_pattern": "NEW_CAPACITY_ONLINE",
        "relevance": "High",
        "relationship": "Accelerating",
        "transmission": "Capacity",
        "rationale": (
            "Capacity expansion can reinforce "
            "the recovery."
        ),
        "expected_effect": (
            "Higher industrial output."
        ),
        "catalyst_strength": 80.0,
        "catalyst_confidence": 75.0,
        "timing": "6-18 Months",
        "persistence": "Medium",
        "dependencies": [
            "Demand persistence"
        ],
        "supporting_evidence": [
            "Order growth"
        ],
        "contradictory_evidence": [],
        "evidence_sources": [
            "Source-A"
        ],
        "beneficiaries": [
            "Industrial suppliers"
        ],
        "adversely_affected": [],
        "second_order_effects": [
            "Higher utilization"
        ],
        "transmission_channels": [
            "Capacity",
            "Volume",
        ],
        "risks": [
            "Execution risk"
        ],
        "invalidation_conditions": [
            "Demand reversal"
        ],
        "contradiction_score": 10.0,
    }


def main():

    engine = RecoveryThemeCatalystEngine()

    # ======================================================
    # ENGINE EXISTS
    # ======================================================

    assert engine is not None

    print(
        "Engine Exists                   : PASS"
    )

    # ======================================================
    # EMPTY INPUT
    # ======================================================

    theme = make_theme()

    result = engine.assess(
        theme,
        [],
    )

    assert result == []

    print(
        "Empty Catalyst Input           : PASS"
    )

    # ======================================================
    # SINGLE LINK
    # ======================================================

    catalyst = make_catalyst()

    result = engine.assess(
        theme,
        [catalyst],
    )

    assert len(result) == 1

    link = result[0]

    print(
        "Single Catalyst Link           : PASS"
    )

    # ======================================================
    # IDENTITY
    # ======================================================

    assert link.theme_id == "THEME-001"

    assert link.catalyst_id == "CAT-001"

    assert (
        link.catalyst_family
        == "CAPACITY_EXPANSION"
    )

    assert (
        link.catalyst_pattern
        == "NEW_CAPACITY_ONLINE"
    )

    print(
        "Identity Transfer              : PASS"
    )

    # ======================================================
    # ENUM TRANSFER
    # ======================================================

    assert (
        link.relevance
        == RecoveryCatalystRelevance.HIGH
    )

    assert (
        link.relationship
        == RecoveryCatalystRelationship.ACCELERATING
    )

    assert (
        link.transmission
        == RecoveryCatalystTransmission.CAPACITY
    )

    print(
        "Classification Transfer       : PASS"
    )

    # ======================================================
    # RECOVERY TRANSFER
    # ======================================================

    assert link.recovery_breadth == 80.0

    assert (
        link.confirmed_recovery_breadth
        == 60.0
    )

    assert link.recovery_confidence == 85.0

    assert (
        link.recovery_stage
        == "Validated Theme"
    )

    assert (
        link.recovery_direction
        == "Positive"
    )

    print(
        "Recovery Context Transfer     : PASS"
    )

    # ======================================================
    # CATALYST DATA
    # ======================================================

    assert link.catalyst_strength == 80.0

    assert link.catalyst_confidence == 75.0

    assert (
        link.catalyst_timing
        == "6-18 Months"
    )

    assert (
        "Demand persistence"
        in link.catalyst_dependencies
    )

    print(
        "Catalyst Context Transfer     : PASS"
    )

    # ======================================================
    # EVIDENCE
    # ======================================================

    assert (
        "Order growth"
        in link.supporting_evidence
    )

    assert (
        "Source-A"
        in link.evidence_sources
    )

    assert (
        "Execution risk"
        in link.key_risks
    )

    print(
        "Evidence Transfer             : PASS"
    )

    # ======================================================
    # REASONING
    # ======================================================

    assert len(link.reasons) > 0

    assert all(
        isinstance(reason, str)
        for reason in link.reasons
    )

    print(
        "Transparent Reasoning         : PASS"
    )

    # ======================================================
    # CONTRADICTION
    # ======================================================

    contradictory = make_catalyst()

    contradictory[
        "contradiction_score"
    ] = 75.0

    result = engine.assess(
        theme,
        [contradictory],
    )

    assert (
        result[0].contradiction_score
        == 75.0
    )

    assert len(
        result[0].warnings
    ) > 0

    print(
        "Contradictory Evidence        : PASS"
    )

    # ======================================================
    # MULTIPLE CATALYSTS
    # ======================================================

    second = make_catalyst()

    second[
        "catalyst_id"
    ] = "CAT-002"

    second[
        "catalyst_family"
    ] = "ORDER_CONTRACT"

    result = engine.assess(
        theme,
        [
            catalyst,
            second,
        ],
    )

    assert len(result) == 2

    assert (
        result[0].catalyst_id
        == "CAT-001"
    )

    assert (
        result[1].catalyst_id
        == "CAT-002"
    )

    print(
        "Multiple Catalyst Links       : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    theme_copy = deepcopy(theme)

    catalyst_copy = deepcopy(catalyst)

    engine.assess(
        theme,
        [catalyst],
    )

    assert theme == theme_copy

    assert catalyst == catalyst_copy

    print(
        "Input Immutability             : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    first = engine.assess(
        theme,
        [catalyst],
    )

    second_result = engine.assess(
        theme,
        [catalyst],
    )

    assert (
        first[0].link_id
        == second_result[0].link_id
    )

    assert (
        first[0].relevance
        == second_result[0].relevance
    )

    assert (
        first[0].relationship
        == second_result[0].relationship
    )

    assert (
        first[0].transmission
        == second_result[0].transmission
    )

    assert (
        first[0].reasons
        == second_result[0].reasons
    )

    print(
        "Deterministic Assessment       : PASS"
    )

    # ======================================================
    # RANGE PROTECTION
    # ======================================================

    extreme = make_catalyst()

    extreme[
        "catalyst_strength"
    ] = 999.0

    extreme[
        "catalyst_confidence"
    ] = -50.0

    result = engine.assess(
        theme,
        [extreme],
    )

    assert (
        result[0].catalyst_strength
        == 100.0
    )

    assert (
        result[0].catalyst_confidence
        == 0.0
    )

    print(
        "Numeric Range Protection       : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY THEME → "
        "CATALYST ENGINE : PASS"
    )


if __name__ == "__main__":
    main()