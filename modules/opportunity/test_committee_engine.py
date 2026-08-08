"""
EIOS
Everest Investment Operating System

Opportunity Committee Engine Test
"""

from modules.opportunity.committee_engine import (
    OpportunityCommitteeEngine,
)

from modules.opportunity.ranking.ranking_models import (
    OpportunityRanking,
    OpportunityRankingSet,
)


def main() -> None:

    engine = OpportunityCommitteeEngine()

    rankings = OpportunityRankingSet(
        rankings=[
            OpportunityRanking(
                company="Tier1Co",
                rank=1,
                research_priority_score=90.0,
                tier="TIER 1 — PRIORITY RESEARCH",
                priority="VERY HIGH",
                eligible=True,
            ),
            OpportunityRanking(
                company="Tier2Co",
                rank=2,
                research_priority_score=80.0,
                tier="TIER 2 — DEEP RESEARCH",
                priority="HIGH",
                eligible=True,
            ),
            OpportunityRanking(
                company="Tier3Co",
                rank=3,
                research_priority_score=70.0,
                tier="TIER 3 — STANDARD RESEARCH",
                priority="MEDIUM",
                eligible=True,
            ),
            OpportunityRanking(
                company="ExcludedCo",
                rank=0,
                research_priority_score=0.0,
                tier="EXCLUDED",
                priority="DO NOT PROMOTE",
                eligible=False,
                exclusion_reasons=[
                    "Evidence gate failed."
                ],
            ),
        ],
        eligible_count=3,
        excluded_count=1,
        top_company="Tier1Co",
        top_priority_score=90.0,
    )

    result = engine.review(rankings)

    assert result.committee_review_count == 2
    assert result.watchlist_count == 1
    assert result.rejected_count == 1
    assert result.approved_count == 0

    assert result.top_candidate == "Tier1Co"

    decisions = {
        item.company: item
        for item in result.decisions
    }

    assert (
        decisions["Tier1Co"].decision
        == "COMMITTEE_REVIEW"
    )

    assert (
        decisions["Tier2Co"].decision
        == "COMMITTEE_REVIEW"
    )

    assert (
        decisions["Tier3Co"].decision
        == "WATCHLIST"
    )

    assert (
        decisions["ExcludedCo"].decision
        == "REJECT"
    )

    # Approval must never be automatic.
    assert result.approved_count == 0

    # Ranking data must remain unchanged.
    assert rankings.rankings[0].research_priority_score == 90.0

    assert rankings.rankings[0].tier == (
        "TIER 1 — PRIORITY RESEARCH"
    )

    print("Tier 1 → Committee Review : PASS")
    print("Tier 2 → Committee Review : PASS")
    print("Tier 3 → Watchlist         : PASS")
    print("Excluded → Reject         : PASS")
    print("No Automatic Approval     : PASS")
    print("Ranking Immutability      : PASS")

    print()
    print("---")
    print()
    print("EIOS OPPORTUNITY COMMITTEE : PASS")


if __name__ == "__main__":
    main()