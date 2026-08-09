"""
EIOS
Everest Investment Operating System

Catalyst Coverage Evidence Registry Test
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CatalystCoverageEvidence,
)

from modules.opportunity.catalyst.catalyst_coverage_evidence_registry import (
    CatalystCoverageEvidenceRegistry,
)


def main() -> None:

    # ======================================================
    # REGISTRY COUNT
    # ======================================================

    assert (
        CatalystCoverageEvidenceRegistry.count()
        == 6
    )

    # ======================================================
    # EXPLICIT PROFILES
    # ======================================================

    profiled_families = [
        CatalystFamily.REVENUE_GROWTH,
        CatalystFamily.VOLUME_GROWTH,
        CatalystFamily.PRICING,
        CatalystFamily.MARGIN_EXPANSION,
        CatalystFamily.TECHNOLOGY_ADOPTION,
        CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
    ]

    for family in profiled_families:

        assert (
            CatalystCoverageEvidenceRegistry.has_profile(
                family
            )
        )

        evidence = (
            CatalystCoverageEvidenceRegistry.get(
                family
            )
        )

        assert isinstance(
            evidence,
            CatalystCoverageEvidence,
        )

    # ======================================================
    # EVIDENCE RANGE
    # ======================================================

    for family in profiled_families:

        evidence = (
            CatalystCoverageEvidenceRegistry.get(
                family
            )
        )

        values = [
            evidence.earnings_impact,
            evidence.detection_lead_time,
            evidence.cross_sector_applicability,
            evidence.observability,
            evidence.persistence,
            evidence.evidence_availability,
            evidence.second_order_potential,
            evidence.market_mispricing_potential,
        ]

        for value in values:

            assert 0 <= value <= 5

    # ======================================================
    # UNPROFILED FAMILY REMAINS NEUTRAL
    # ======================================================

    evidence = (
        CatalystCoverageEvidenceRegistry.get(
            CatalystFamily.PRODUCT_MIX
        )
    )

    assert isinstance(
        evidence,
        CatalystCoverageEvidence,
    )

    assert (
        evidence
        == CatalystCoverageEvidence()
    )

    assert not (
        CatalystCoverageEvidenceRegistry.has_profile(
            CatalystFamily.PRODUCT_MIX
        )
    )

    # ======================================================
    # REGISTRY COPY
    # ======================================================

    profiles = (
        CatalystCoverageEvidenceRegistry.all()
    )

    assert isinstance(
        profiles,
        dict,
    )

    assert len(profiles) == 6

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Registry Count               : PASS"
    )

    print(
        "Explicit Profile Retrieval   : PASS"
    )

    print(
        "Evidence Type Integrity      : PASS"
    )

    print(
        "Evidence Range Validation    : PASS"
    )

    print(
        "Neutral Unprofiled Family    : PASS"
    )

    print(
        "Registry Copy Integrity      : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST COVERAGE EVIDENCE REGISTRY : PASS"
    )


if __name__ == "__main__":
    main()