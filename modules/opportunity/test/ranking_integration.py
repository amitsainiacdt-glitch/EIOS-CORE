"""
EIOS
Everest Investment Operating System

Opportunity Ranking → Synthesis Integration Test

Purpose:
Verify that the Ranking Engine correctly consumes
real OpportunitySynthesis objects without recalculating
the underlying analytical engines.
"""

from modules.opportunity.opportunity_synthesis_engine import (
    OpportunitySynthesis,
)

from modules.opportunity.ranking.ranking_engine import (
    OpportunityRankingEngine,
)


def build_opportunity(
    *,
    company: str,
    opportunity_score: float,
    confidence: float,
    evidence_score: float,
    evidence_confidence: float,
    evidence_sufficient: bool,
    permanent_loss_probability: float,
    downside_probability: float,
    expected_return: float,
    expected_time_months: float,
    kill_switches: list[str],
) -> OpportunitySynthesis:

    return OpportunitySynthesis(
        company=company,
        sector="Industrial",
        opportunity_score=opportunity_score,
        confidence=confidence,
        evidence_score=evidence_score,
        evidence_confidence=evidence_confidence,
        evidence_sufficient=evidence_sufficient,
        permanent_loss_probability=permanent_loss_probability,
        downside_probability=downside_probability,
        expected_return=expected_return,
        expected_time_months=expected_time_months,
        kill_switches=kill_switches,
    )


def main() -> None:

    engine = OpportunityRankingEngine()

    # ======================================================
    # CASE 1 — Strong opportunity
    # ======================================================

    strong = build_opportunity(
        company="StrongCo",
        opportunity_score=90.0,
        confidence=90.0,
        evidence_score=90.0,
        evidence_confidence=90.0,
        evidence_sufficient=True,
        permanent_loss_probability=5.0,
        downside_probability=10.0,
        expected_return=80.0,
        expected_time_months=24.0,
        kill_switches=["ROCE falls below threshold"],
    )

    # ======================================================
    # CASE 2 — Weaker but eligible opportunity
    # ======================================================

    weak = build_opportunity(
        company="WeakCo",
        opportunity_score=68.0,
        confidence=70.0,
        evidence_score=70.0,
        evidence_confidence=70.0,
        evidence_sufficient=True,
        permanent_loss_probability=10.0,
        downside_probability=20.0,
        expected_return=35.0,
        expected_time_months=48.0,
        kill_switches=["Demand deteriorates"],
    )

    # ======================================================
    # CASE 3 — Evidence failure
    # ======================================================

    no_evidence = build_opportunity(
        company="NoEvidenceCo",
        opportunity_score=95.0,
        confidence=90.0,
        evidence_score=30.0,
        evidence_confidence=30.0,
        evidence_sufficient=False,
        permanent_loss_probability=5.0,
        downside_probability=10.0,
        expected_return=100.0,
        expected_time_months=24.0,
        kill_switches=["Thesis invalidated"],
    )

    # ======================================================
    # CASE 4 — Permanent-loss failure
    # ======================================================

    permanent_loss = build_opportunity(
        company="PermanentLossCo",
        opportunity_score=95.0,
        confidence=90.0,
        evidence_score=90.0,
        evidence_confidence=90.0,
        evidence_sufficient=True,
        permanent_loss_probability=40.0,
        downside_probability=30.0,
        expected_return=120.0,
        expected_time_months=24.0,
        kill_switches=["Balance sheet deterioration"],
    )

    # ======================================================
    # CASE 5 — No kill switch
    # ======================================================

    no_kill_switch = build_opportunity(
        company="NoKillSwitchCo",
        opportunity_score=88.0,
        confidence=85.0,
        evidence_score=85.0,
        evidence_confidence=85.0,
        evidence_sufficient=True,
        permanent_loss_probability=5.0,
        downside_probability=10.0,
        expected_return=70.0,
        expected_time_months=24.0,
        kill_switches=[],
    )

    opportunities = [
        strong,
        weak,
        no_evidence,
        permanent_loss,
        no_kill_switch,
    ]

    # ======================================================
    # RANK
    # ======================================================

    result = engine.rank(opportunities)

    assert result.eligible_count == 2
    assert result.excluded_count == 3

    assert result.top_company == "StrongCo"

    assert result.rankings[0].company == "StrongCo"
    assert result.rankings[0].eligible is True
    assert result.rankings[0].rank == 1

    assert result.rankings[1].company == "WeakCo"
    assert result.rankings[1].eligible is True
    assert result.rankings[1].rank == 2

    # ======================================================
    # EXCLUSION CHECKS
    # ======================================================

    excluded = {
        item.company: item
        for item in result.rankings
        if not item.eligible
    }

    assert "NoEvidenceCo" in excluded
    assert "PermanentLossCo" in excluded
    assert "NoKillSwitchCo" in excluded

    # ======================================================
    # SYNTHESIS IMMUTABILITY
    # ======================================================

    assert strong.opportunity_score == 90.0
    assert strong.confidence == 90.0
    assert strong.evidence_score == 90.0

    assert weak.opportunity_score == 68.0
    assert weak.confidence == 70.0

    # ======================================================
    # SCORE PRESERVATION
    # ======================================================

    strong_ranking = next(
        item
        for item in result.rankings
        if item.company == "StrongCo"
    )

    assert strong_ranking.opportunity_score == 90.0
    assert strong_ranking.confidence_score == 90.0
    assert strong_ranking.evidence_score == 90.0
    assert strong_ranking.evidence_confidence == 90.0

    print("Strong Synthesis → Ranking : PASS")
    print("Competitive Ranking        : PASS")
    print("Evidence Gate              : PASS")
    print("Permanent Loss Gate        : PASS")
    print("Kill Switch Gate           : PASS")
    print("Score Preservation         : PASS")
    print("Synthesis Immutability     : PASS")

    print()
    print("---")
    print()
    print("EIOS RANKING → SYNTHESIS INTEGRATION : PASS")


if __name__ == "__main__":
    main()