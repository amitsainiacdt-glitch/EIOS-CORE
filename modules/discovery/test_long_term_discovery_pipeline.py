"""
===============================================================================
EIOS
Everest Investment Operating System

Long-Term Discovery Pipeline Test

Purpose:
    Verifies the complete Long-Term Discovery pipeline.

Architecture:

    Universe
        ↓
    DiscoveryCandidate
        ↓
    9 Discovery Filters
        ↓
    Discovery Score
        ↓
    Ranking
        ↓
    Opportunity Research Intake

Design Principles:
    - Verifies orchestration only.
    - Does not perform real-world analysis.
    - Does not access the internet.
    - Does not perform valuation independently.
    - Does not make investment decisions.
    - Verifies preservation of Discovery intelligence.
===============================================================================
"""

from modules.discovery.discovery_engine import (
    DiscoveryEngine,
)

from modules.opportunity.discovery_opportunity_adapter import (
    DiscoveryOpportunityAdapter,
)

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)


def main() -> None:

    print("=" * 60)
    print(
        "EIOS LONG-TERM DISCOVERY PIPELINE TEST"
    )
    print("=" * 60)

    # ==========================================================
    # TEST 1 — ENGINE CREATION
    # ==========================================================

    engine = DiscoveryEngine()

    assert engine is not None

    print(
        "Test 1 — Discovery Engine Creation     : PASS"
    )

    # ==========================================================
    # TEST 2 — FILTER COUNT
    # ==========================================================

    assert len(engine.filters) == 9

    print(
        "Test 2 — Nine Discovery Filters        : PASS"
    )

    # ==========================================================
    # TEST 3 — DISCOVERY EXECUTION
    # ==========================================================

    candidates = engine.discover()

    assert candidates is not None
    assert len(candidates) == 3

    print(
        "Test 3 — Discovery Execution            : PASS"
    )

    # ==========================================================
    # TEST 4 — FILTER SCORES
    # ==========================================================

    for candidate in candidates:

        assert candidate.quality_score > 0
        assert candidate.growth_score > 0
        assert candidate.financial_score > 0
        assert candidate.management_score > 0
        assert candidate.capital_allocation_score > 0
        assert candidate.moat_score > 0
        assert candidate.risk_score > 0
        assert candidate.tailwind_score > 0
        assert candidate.valuation_score > 0

    print(
        "Test 4 — All Filter Scores             : PASS"
    )

    # ==========================================================
    # TEST 5 — OVERALL DISCOVERY SCORE
    # ==========================================================

    for candidate in candidates:

        assert candidate.overall_score > 0
        assert candidate.overall_score <= 100

    print(
        "Test 5 — Discovery Score               : PASS"
    )

    # ==========================================================
    # TEST 6 — RANKING
    # ==========================================================

    scores = [
        candidate.overall_score
        for candidate in candidates
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )

    print(
        "Test 6 — Ranking                        : PASS"
    )

    # ==========================================================
    # TEST 7 — DISCOVERY INTELLIGENCE
    # ==========================================================

    for candidate in candidates:

        assert candidate.strengths

    print(
        "Test 7 — Discovery Intelligence         : PASS"
    )

    # ==========================================================
    # TEST 8 — DISCOVERY → OPPORTUNITY
    # ==========================================================

    adapter = DiscoveryOpportunityAdapter()

    intake = adapter.create_intake(
        candidates[0]
    )

    assert isinstance(
        intake,
        OpportunityResearchIntake,
    )

    print(
        "Test 8 — Discovery → Opportunity        : PASS"
    )

    # ==========================================================
    # TEST 9 — IDENTITY PRESERVATION
    # ==========================================================

    assert (
        intake.company
        == candidates[0].company_name
    )

    assert (
        intake.ticker
        == candidates[0].ticker
    )

    assert (
        intake.sector
        == candidates[0].sector
    )

    assert (
        intake.industry
        == candidates[0].industry
    )

    print(
        "Test 9 — Identity Preservation           : PASS"
    )

    # ==========================================================
    # TEST 10 — SCORE PRESERVATION
    # ==========================================================

    assert (
        intake.discovery_score
        == candidates[0].overall_score
    )

    assert (
        intake.discovery_confidence
        == candidates[0].confidence
    )

    print(
        "Test 10 — Score Preservation             : PASS"
    )

    # ==========================================================
    # TEST 11 — INTELLIGENCE PRESERVATION
    # ==========================================================

    assert (
        intake.strengths
        == candidates[0].strengths
    )

    assert (
        intake.concerns
        == candidates[0].concerns
    )

    assert (
        intake.catalysts
        == candidates[0].catalysts
    )

    assert (
        intake.risks
        == candidates[0].risks
    )

    print(
        "Test 11 — Intelligence Preservation      : PASS"
    )

    # ==========================================================
    # TEST 12 — NO INVENTED ANALYSIS
    # ==========================================================

    assert (
        intake.research_status
        == "NOT_STARTED"
    )

    assert (
        intake.research_questions == []
    )

    print(
        "Test 12 — No Invented Opportunity       : PASS"
    )

    # ==========================================================
    # TEST 13 — ANALYTICAL BOUNDARY
    # ==========================================================

    forbidden_methods = [
        "calculate_intrinsic_value",
        "calculate_opportunity_score",
        "rank_opportunity",
        "allocate_portfolio",
        "execute_trade",
    ]

    for method in forbidden_methods:

        assert not hasattr(
            engine,
            method,
        )

    print(
        "Test 13 — Analytical Boundary            : PASS"
    )

    # ==========================================================
    # OUTPUT
    # ==========================================================

    print()
    print("Ranked Discovery Candidates")
    print("-" * 60)

    for index, candidate in enumerate(
        candidates,
        start=1,
    ):

        print(
            f"{index}. "
            f"{candidate.ticker:15}"
            f"Score: "
            f"{candidate.overall_score:.2f}"
        )

    print()
    print(
        "Opportunity Intake"
    )

    print(
        f"Company : {intake.company}"
    )

    print(
        f"Ticker  : {intake.ticker}"
    )

    print(
        f"Sector  : {intake.sector}"
    )

    print(
        f"Score   : {intake.discovery_score:.2f}"
    )

    print(
        f"Status  : {intake.research_status}"
    )

    # ==========================================================
    # FINAL
    # ==========================================================

    print()
    print("=" * 60)
    print(
        "EIOS LONG-TERM DISCOVERY PIPELINE : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()