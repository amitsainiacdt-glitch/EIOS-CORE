"""
EIOS
Everest Investment Operating System

Opportunity Synthesis → Ranking → Committee Integration Test
"""

from modules.opportunity.opportunity_synthesis_engine import (
    OpportunitySynthesis,
)

from modules.opportunity.ranking.ranking_engine import (
    OpportunityRankingEngine,
)

from modules.opportunity.committee_engine import (
    OpportunityCommitteeEngine,
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
        permanent_loss_probability=(
            permanent_loss_probability
        ),
        expected_return=expected_return,
        expected_time_months=expected_time_months,
        kill_switches=list(kill_switches),
    )


def main() -> None:

    # ======================================================
    # BUILD REAL SYNTHESIS OBJECTS
    # ======================================================

    priority = build_opportunity(
        company="PriorityCo",
        opportunity_score=92.0,
        confidence=90.0,
        evidence_score=90.0,
        evidence_confidence=90.0,
        evidence_sufficient=True,
        permanent_loss_probability=5.0,
        expected_return=80.0,
        expected_time_months=24.0,
        kill_switches=[
            "ROCE falls below threshold"
        ],
    )

    watch = build_opportunity(
        company="WatchCo",
        opportunity_score=70.0,
        confidence=70.0,
        evidence_score=70.0,
        evidence_confidence=70.0,
        evidence_sufficient=True,
        permanent_loss_probability=10.0,
        expected_return=35.0,
        expected_time_months=48.0,
        kill_switches=[
            "Demand deteriorates"
        ],
    )

    no_evidence = build_opportunity(
        company="NoEvidenceCo",
        opportunity_score=95.0,
        confidence=90.0,
        evidence_score=30.0,
        evidence_confidence=30.0,
        evidence_sufficient=False,
        permanent_loss_probability=5.0,
        expected_return=100.0,
        expected_time_months=24.0,
        kill_switches=[
            "Evidence invalidates thesis"
        ],
    )

    permanent_loss = build_opportunity(
        company="PermanentLossCo",
        opportunity_score=95.0,
        confidence=90.0,
        evidence_score=90.0,
        evidence_confidence=90.0,
        evidence_sufficient=True,
        permanent_loss_probability=40.0,
        expected_return=120.0,
        expected_time_months=24.0,
        kill_switches=[
            "Balance sheet deteriorates"
        ],
    )

    no_kill_switch = build_opportunity(
        company="NoKillSwitchCo",
        opportunity_score=90.0,
        confidence=90.0,
        evidence_score=90.0,
        evidence_confidence=90.0,
        evidence_sufficient=True,
        permanent_loss_probability=5.0,
        expected_return=90.0,
        expected_time_months=24.0,
        kill_switches=[],
    )

    opportunities = [
        priority,
        watch,
        no_evidence,
        permanent_loss,
        no_kill_switch,
    ]

    # ======================================================
    # SYNTHESIS → RANKING
    # ======================================================

    ranking_engine = OpportunityRankingEngine()

    ranking_set = ranking_engine.rank(
        opportunities
    )

    assert ranking_set.eligible_count == 2
    assert ranking_set.excluded_count == 3

    assert ranking_set.top_company == "PriorityCo"

    # ======================================================
    # RANKING → COMMITTEE
    # ======================================================

    committee_engine = OpportunityCommitteeEngine()

    committee_result = committee_engine.review(
        ranking_set
    )

    # ======================================================
    # COMMITTEE COUNTS
    # ======================================================

    assert (
        committee_result.committee_review_count
        == 1
    )

    assert (
        committee_result.watchlist_count
        == 1
    )

    assert (
        committee_result.rejected_count
        == 3
    )

    # Approval must never be automatic.

    assert (
        committee_result.approved_count
        == 0
    )

    assert (
        committee_result.top_candidate
        == "PriorityCo"
    )

    # ======================================================
    # DECISION MAP
    # ======================================================

    decisions = {
        item.company: item
        for item in committee_result.decisions
    }

    assert (
        decisions["PriorityCo"].decision
        == "COMMITTEE_REVIEW"
    )

    assert (
        decisions["WatchCo"].decision
        == "WATCHLIST"
    )

    assert (
        decisions["NoEvidenceCo"].decision
        == "REJECT"
    )

    assert (
        decisions["PermanentLossCo"].decision
        == "REJECT"
    )

    assert (
        decisions["NoKillSwitchCo"].decision
        == "REJECT"
    )

    # ======================================================
    # SCORE PRESERVATION
    # ======================================================

    assert priority.opportunity_score == 92.0
    assert priority.confidence == 90.0
    assert priority.evidence_score == 90.0

    # ======================================================
    # NO AUTOMATIC APPROVAL
    # ======================================================

    assert all(
        item.decision != "APPROVED"
        for item in committee_result.decisions
    )

    print(
        "Synthesis → Ranking       : PASS"
    )

    print(
        "Ranking → Committee       : PASS"
    )

    print(
        "Priority → Committee Review : PASS"
    )

    print(
        "Watch → Watchlist         : PASS"
    )

    print(
        "Evidence Failure → Reject : PASS"
    )

    print(
        "Permanent Loss → Reject   : PASS"
    )

    print(
        "No Kill Switch → Reject   : PASS"
    )

    print(
        "No Automatic Approval     : PASS"
    )

    print(
        "Score Preservation        : PASS"
    )

    print()
    print("---")
    print()
    print(
        "EIOS SYNTHESIS → RANKING → COMMITTEE : PASS"
    )


if __name__ == "__main__":
    main()