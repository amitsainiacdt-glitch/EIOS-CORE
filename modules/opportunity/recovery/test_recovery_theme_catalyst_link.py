"""
EIOS
Recovery Theme → Catalyst Link Model Tests
"""


from modules.opportunity.recovery.recovery_theme_catalyst_link import (
    RecoveryThemeCatalystLink,
    RecoveryCatalystRelevance,
    RecoveryCatalystRelationship,
    RecoveryCatalystTransmission,
)


def main():

    # ======================================================
    # MODEL
    # ======================================================

    link = RecoveryThemeCatalystLink()

    assert isinstance(
        link,
        RecoveryThemeCatalystLink,
    )

    print(
        "Link Type                     : PASS"
    )

    # ======================================================
    # DEFAULT ENUMS
    # ======================================================

    assert (
        link.relevance
        == RecoveryCatalystRelevance.UNKNOWN
    )

    assert (
        link.relationship
        == RecoveryCatalystRelationship.UNKNOWN
    )

    assert (
        link.transmission
        == RecoveryCatalystTransmission.UNKNOWN
    )

    print(
        "Default Enum Integrity         : PASS"
    )

    # ======================================================
    # DEFAULT NUMERICS
    # ======================================================

    assert (
        link.recovery_breadth
        == 0.0
    )

    assert (
        link.confirmed_recovery_breadth
        == 0.0
    )

    assert (
        link.recovery_confidence
        == 0.0
    )

    assert (
        link.catalyst_strength
        == 0.0
    )

    assert (
        link.catalyst_confidence
        == 0.0
    )

    assert (
        link.contradiction_score
        == 0.0
    )

    print(
        "Numeric Defaults              : PASS"
    )

    # ======================================================
    # LIST INTEGRITY
    # ======================================================

    assert (
        link.catalyst_dependencies
        == []
    )

    assert (
        link.supporting_evidence
        == []
    )

    assert (
        link.contradictory_evidence
        == []
    )

    assert (
        link.evidence_sources
        == []
    )

    assert (
        link.potential_beneficiaries
        == []
    )

    assert (
        link.potential_adversely_affected
        == []
    )

    assert (
        link.second_order_effects
        == []
    )

    assert (
        link.transmission_channels
        == []
    )

    assert (
        link.key_risks
        == []
    )

    assert (
        link.invalidation_conditions
        == []
    )

    assert (
        link.reasons
        == []
    )

    assert (
        link.warnings
        == []
    )

    print(
        "List Field Integrity           : PASS"
    )

    # ======================================================
    # PASSIVE BEHAVIOR
    # ======================================================

    link.link_id = (
        "LINK-001"
    )

    link.theme_id = (
        "THEME-INDUSTRIAL-CAPEX"
    )

    link.theme_name = (
        "Industrial Capital Cycle"
    )

    link.catalyst_family = (
        "CAPACITY_EXPANSION"
    )

    link.catalyst_pattern = (
        "NEW_CAPACITY_ONLINE"
    )

    link.relevance = (
        RecoveryCatalystRelevance.HIGH
    )

    link.relationship = (
        RecoveryCatalystRelationship.ACCELERATING
    )

    link.transmission = (
        RecoveryCatalystTransmission.CAPACITY
    )

    link.recovery_breadth = 75.0

    link.confirmed_recovery_breadth = 50.0

    link.catalyst_strength = 80.0

    assert (
        link.link_id
        == "LINK-001"
    )

    assert (
        link.theme_id
        == "THEME-INDUSTRIAL-CAPEX"
    )

    assert (
        link.catalyst_family
        == "CAPACITY_EXPANSION"
    )

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

    assert (
        link.recovery_breadth
        == 75.0
    )

    print(
        "Passive Model Behavior         : PASS"
    )

    # ======================================================
    # NO CALCULATION
    # ======================================================

    link.recovery_breadth = 91.0

    link.catalyst_strength = 87.0

    assert (
        link.recovery_breadth
        == 91.0
    )

    assert (
        link.catalyst_strength
        == 87.0
    )

    print(
        "Passive Numeric Behavior       : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS RECOVERY THEME → "
        "CATALYST LINK MODEL : PASS"
    )


if __name__ == "__main__":
    main()