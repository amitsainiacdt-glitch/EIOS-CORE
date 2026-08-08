"""
EIOS
Everest Investment Operating System

Opportunity Ranking Engine Test Suite
"""

from modules.opportunity.ranking.ranking_engine import (
    OpportunityRankingEngine,
)

from modules.opportunity.opportunity_synthesis_engine import (
    OpportunitySynthesis,
)


# ==========================================================
# SYNTHESIS FACTORY
# ==========================================================


def make_opportunity(
    *,
    company: str,
    opportunity_score: float = 80.0,
    confidence: float = 85.0,
    evidence_score: float = 80.0,
    evidence_confidence: float = 85.0,
    asymmetry_score: float = 80.0,
    expected_return: float = 60.0,
    expected_time_months: float = 12.0,
    permanent_loss_probability: float = 5.0,
    downside_probability: float = 15.0,
    evidence_sufficient: bool = True,
    kill_switches: list[str] | None = None,
) -> OpportunitySynthesis:

    return OpportunitySynthesis(
        company=company,
        opportunity_score=opportunity_score,
        confidence=confidence,
        evidence_score=evidence_score,
        evidence_confidence=evidence_confidence,
        asymmetry_score=asymmetry_score,
        expected_return=expected_return,
        expected_time_months=expected_time_months,
        permanent_loss_probability=(
            permanent_loss_probability
        ),
        downside_probability=(
            downside_probability
        ),
        evidence_sufficient=evidence_sufficient,
        kill_switches=(
            kill_switches
            if kill_switches is not None
            else ["THESIS_INVALIDATED"]
        ),
    )


# ==========================================================
# CASE 1
# STRONG OPPORTUNITY
# ==========================================================


def test_strong_opportunity() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="STRONG CO",
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert ranking.eligible

    assert ranking.rank == 1

    assert ranking.research_priority_score > 0

    assert ranking.tier != "EXCLUDED"

    print(
        "Case 1 — Strong Opportunity     : PASS"
    )


# ==========================================================
# CASE 2
# WEAK OPPORTUNITY
# ==========================================================


def test_weak_opportunity() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="WEAK CO",
        opportunity_score=45.0,
        confidence=45.0,
        evidence_score=45.0,
        evidence_confidence=45.0,
        asymmetry_score=40.0,
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert not ranking.eligible

    assert ranking.rank == 0

    assert ranking.tier == "EXCLUDED"

    assert ranking.research_priority_score == 0.0

    print(
        "Case 2 — Weak Opportunity       : PASS"
    )


# ==========================================================
# CASE 3
# NO EVIDENCE GATE
# ==========================================================


def test_no_evidence_gate() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="NO EVIDENCE CO",
        evidence_sufficient=False,
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert not ranking.eligible

    assert not ranking.evidence_gate_passed

    assert any(
        "Evidence gate failed"
        in reason
        for reason
        in ranking.exclusion_reasons
    )

    print(
        "Case 3 — No Evidence Gate       : PASS"
    )


# ==========================================================
# CASE 4
# HIGH PERMANENT LOSS
# ==========================================================


def test_permanent_loss() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="PERMANENT LOSS CO",
        permanent_loss_probability=40.0,
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert not ranking.eligible

    assert not ranking.permanent_loss_gate_passed

    assert any(
        "Permanent-loss gate failed"
        in reason
        for reason
        in ranking.exclusion_reasons
    )

    print(
        "Case 4 — Permanent Loss          : PASS"
    )


# ==========================================================
# CASE 5
# NO KILL SWITCH
# ==========================================================


def test_no_kill_switch() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="NO KILL SWITCH CO",
        kill_switches=[],
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert not ranking.eligible

    assert not ranking.kill_switch_gate_passed

    assert any(
        "Kill-switch gate failed"
        in reason
        for reason
        in ranking.exclusion_reasons
    )

    print(
        "Case 5 — No Kill Switch          : PASS"
    )


# ==========================================================
# CASE 6
# LOW CONFIDENCE
# ==========================================================


def test_low_confidence() -> None:

    engine = OpportunityRankingEngine()

    opportunity = make_opportunity(
        company="LOW CONFIDENCE CO",
        opportunity_score=90.0,
        confidence=50.0,
    )

    result = engine.rank(
        [opportunity]
    )

    ranking = result.rankings[0]

    assert not ranking.eligible

    assert not ranking.confidence_gate_passed

    assert any(
        "Confidence gate failed"
        in reason
        for reason
        in ranking.exclusion_reasons
    )

    print(
        "Case 6 — Low Confidence         : PASS"
    )


# ==========================================================
# CASE 7
# RESEARCH EFFICIENCY
# ==========================================================


def test_research_efficiency() -> None:

    engine = OpportunityRankingEngine()

    fast = make_opportunity(
        company="FAST THESIS",
        expected_return=60.0,
        expected_time_months=6.0,
    )

    slow = make_opportunity(
        company="SLOW THESIS",
        expected_return=60.0,
        expected_time_months=36.0,
    )

    fast_result = engine.rank(
        [fast]
    )

    slow_result = engine.rank(
        [slow]
    )

    fast_score = (
        fast_result
        .rankings[0]
        .research_efficiency_score
    )

    slow_score = (
        slow_result
        .rankings[0]
        .research_efficiency_score
    )

    assert fast_score > slow_score

    print(
        "Case 7 — Research Efficiency    : PASS"
    )


# ==========================================================
# CASE 8
# COMPETITIVE RANKING
# ==========================================================


def test_competitive_ranking() -> None:

    engine = OpportunityRankingEngine()

    opportunity_a = make_opportunity(
        company="COMPANY A",
        opportunity_score=90.0,
        confidence=90.0,
        expected_return=70.0,
        expected_time_months=12.0,
    )

    opportunity_b = make_opportunity(
        company="COMPANY B",
        opportunity_score=75.0,
        confidence=80.0,
        expected_return=50.0,
        expected_time_months=24.0,
    )

    opportunity_c = make_opportunity(
        company="COMPANY C",
        opportunity_score=60.0,
        confidence=65.0,
        expected_return=35.0,
        expected_time_months=24.0,
    )

    result = engine.rank(
        [
            opportunity_b,
            opportunity_c,
            opportunity_a,
        ]
    )

    eligible = [
        item
        for item in result.rankings
        if item.eligible
    ]

    assert len(eligible) == 3

    assert (
        eligible[0].company
        == "COMPANY A"
    )

    assert eligible[0].rank == 1

    assert eligible[1].rank == 2

    assert eligible[2].rank == 3

    assert (
        result.top_company
        == "COMPANY A"
    )

    print(
        "Case 8 — Competitive Ranking     : PASS"
    )


# ==========================================================
# CASE 9
# HIGH SCORE BUT BAD RISK
# ==========================================================


def test_high_score_bad_risk() -> None:

    engine = OpportunityRankingEngine()

    attractive_but_risky = make_opportunity(
        company="RISKY CO",
        opportunity_score=95.0,
        confidence=95.0,
        permanent_loss_probability=30.0,
    )

    safer = make_opportunity(
        company="SAFER CO",
        opportunity_score=82.0,
        confidence=85.0,
        permanent_loss_probability=5.0,
    )

    result = engine.rank(
        [
            attractive_but_risky,
            safer,
        ]
    )

    rankings = result.rankings

    risky = next(
        item
        for item in rankings
        if item.company == "RISKY CO"
    )

    safe = next(
        item
        for item in rankings
        if item.company == "SAFER CO"
    )

    assert not risky.eligible

    assert safe.eligible

    assert safe.rank == 1

    print(
        "Case 9 — High Score / Bad Risk   : PASS"
    )


# ==========================================================
# CASE 10
# EMPTY INPUT
# ==========================================================


def test_empty_input() -> None:

    engine = OpportunityRankingEngine()

    result = engine.rank(
        []
    )

    assert result.rankings == []

    assert result.eligible_count == 0

    assert result.excluded_count == 0

    assert len(
        result.warnings
    ) > 0

    print(
        "Case 10 — Empty Input             : PASS"
    )


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    print()
    print(
        "EIOS OPPORTUNITY RANKING ENGINE TEST"
    )
    print()

    test_strong_opportunity()

    test_weak_opportunity()

    test_no_evidence_gate()

    test_permanent_loss()

    test_no_kill_switch()

    test_low_confidence()

    test_research_efficiency()

    test_competitive_ranking()

    test_high_score_bad_risk()

    test_empty_input()

    print()
    print(
        "----------------------------------------------"
    )
    print(
        "EIOS OPPORTUNITY RANKING ENGINE : PASS"
    )
    print(
        "----------------------------------------------"
    )


if __name__ == "__main__":
    main()