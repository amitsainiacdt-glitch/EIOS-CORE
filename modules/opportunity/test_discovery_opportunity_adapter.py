"""
EIOS
Everest Investment Operating System

Discovery → Opportunity Intake Test
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.opportunity.discovery_opportunity_adapter import (
    DiscoveryOpportunityAdapter,
)


def main() -> None:

    candidate = DiscoveryCandidate(
        company_name="Test Company",
        ticker="TEST",
        sector="Industrial",
        industry="Engineering",

        quality_score=90.0,
        growth_score=85.0,
        financial_score=88.0,
        management_score=82.0,
        capital_allocation_score=80.0,
        moat_score=86.0,
        risk_score=75.0,
        tailwind_score=90.0,
        valuation_score=70.0,

        overall_score=84.0,

        status="Passed",

        strengths=[
            "Strong competitive position",
            "Large growth runway",
        ],

        concerns=[
            "Valuation requires further research",
        ],

        catalysts=[
            "Capacity expansion",
            "Industry upcycle",
        ],

        risks=[
            "Execution risk",
        ],

        discovery_notes=[
            "Candidate identified during Discovery screening."
        ],

        confidence=82.0,

        source="EIOS Discovery Office",
    )

    adapter = DiscoveryOpportunityAdapter()

    intake = adapter.create_intake(
        candidate
    )

    # ======================================================
    # Identity
    # ======================================================

    assert intake.company == "Test Company"
    assert intake.ticker == "TEST"
    assert intake.sector == "Industrial"
    assert intake.industry == "Engineering"

    # ======================================================
    # Discovery scores preserved
    # ======================================================

    assert intake.discovery_score == 84.0
    assert intake.discovery_confidence == 82.0

    # ======================================================
    # Intelligence preserved
    # ======================================================

    assert (
        "Capacity expansion"
        in intake.catalysts
    )

    assert (
        "Execution risk"
        in intake.risks
    )

    assert (
        "Strong competitive position"
        in intake.strengths
    )

    # ======================================================
    # No Opportunity analysis invented
    # ======================================================

    assert intake.research_status == (
        "NOT_STARTED"
    )

    # ======================================================
    # Source object remains unchanged
    # ======================================================

    assert candidate.overall_score == 84.0
    assert candidate.confidence == 82.0

    print(
        "Discovery → Intake Identity : PASS"
    )

    print(
        "Discovery Score Preservation : PASS"
    )

    print(
        "Discovery Intelligence       : PASS"
    )

    print(
        "No Invented Analysis         : PASS"
    )

    print(
        "Source Immutability          : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS DISCOVERY → OPPORTUNITY INTAKE : PASS"
    )


if __name__ == "__main__":
    main()