from modules.investment_committee.committee_vote import CommitteeVote
from modules.investment_committee.committee_response import CommitteeResponse
from modules.master_dossier.committee_section import CommitteeSection


class CommitteeEngine:
    """
    Investment Committee Engine

    Supports both:

        CommitteeEngine(research)

    and

        CommitteeEngine(members, research)
    """

    def __init__(self, members_or_research, research=None):

        # -------------------------------------------------
        # Backward Compatibility
        # CommitteeEngine(research)
        # -------------------------------------------------

        if research is None and not isinstance(
            members_or_research, (list, tuple)
        ):

            self.research = members_or_research

            from modules.investment_committee.business_member import (
                BusinessMember,
            )
            from modules.investment_committee.financial_member import (
                FinancialMember,
            )
            from modules.investment_committee.management_member import (
                ManagementMember,
            )
            from modules.investment_committee.ownership_member import (
                OwnershipMember,
            )
            from modules.investment_committee.risk_member import (
                RiskMember,
            )
            from modules.investment_committee.competitive_member import (
                CompetitiveMember,
            )
            from modules.investment_committee.valuation_member import (
                ValuationMember,
            )
            from modules.investment_committee.thesis_member import (
                ThesisMember,
            )
            from modules.investment_committee.portfolio_member import (
                PortfolioMember,
            )

            self.members = [
                BusinessMember(),
                FinancialMember(),
                ManagementMember(),
                OwnershipMember(),
                RiskMember(),
                CompetitiveMember(),
                ValuationMember(),
                ThesisMember(),
                PortfolioMember(),
            ]

        # -------------------------------------------------
        # New Constructor
        # -------------------------------------------------

        else:
            self.members = members_or_research
            self.research = research

    # =====================================================
    # Backward Compatible API
    # =====================================================

    def analyze(self, research=None):

        if research is None:
            research = self.research

        if research is None:
            raise ValueError("Research object is required.")

        return self.evaluate(research)

    # =====================================================
    # Main Evaluation
    # =====================================================

    def evaluate(self, research):

        responses = []

        print()
        print("=" * 60)
        print("INVESTMENT COMMITTEE")
        print("=" * 60)

        print(
            f"{'Member':15}"
            f"{'Vote':10}"
            f"{'Score':>10}"
            f"{'Confidence':>14}"
        )

        print("-" * 60)

        for member in self.members:

            response = member.evaluate(research)

            # ---------------------------------------------
            # Backward compatibility for legacy members
            # ---------------------------------------------

            if isinstance(response, dict):

                response = CommitteeResponse(
                    member=response.get(
                        "member",
                        response.get("Member", "Unknown"),
                    ),
                    vote=response.get(
                        "vote",
                        response.get("Vote", "Watch"),
                    ),
                    score=response.get(
                        "score",
                        response.get("Score", 0),
                    ),
                    confidence=response.get(
                        "confidence",
                        response.get("Confidence", 0),
                    ),
                    reason=response.get("reason", ""),
                    evidence=response.get("evidence", []),
                    warnings=response.get("warnings", []),
                    metrics=response.get("metrics", {}),
                    risks=response.get("risks", []),
                    recommendation=response.get(
                        "recommendation",
                        "",
                    ),
                    weight=response.get("weight", 10),
                )

            responses.append(response)

            print(
                f"{response.member:15}"
                f"{response.vote:10}"
                f"{response.score:>10.1f}"
                f"{response.confidence:>14.1f}"
            )

        print("-" * 60)

        committee_vote = CommitteeVote(responses)

        # =====================================================
        # Typed Committee Section
        # =====================================================

        committee = CommitteeSection()

        committee.recommendation = committee_vote.final_vote
        committee.overall_score = committee_vote.average_score
        committee.confidence = committee_vote.average_confidence

        committee.summary = (
            f"Final Vote: {committee_vote.final_vote} | "
            f"Average Score: {committee_vote.average_score:.1f}"
        )

        committee.total_members = len(responses)

        committee.pass_votes = sum(
            1 for r in responses if r.vote == "Pass"
        )

        committee.watch_votes = sum(
            1 for r in responses if r.vote == "Watch"
        )

        committee.reject_votes = sum(
            1 for r in responses if r.vote == "Reject"
        )

        for response in responses:

            member = response.member.lower()

            if member == "business":
                committee.business_score = response.score
                committee.business_vote = response.vote

            elif member == "financial":
                committee.financial_score = response.score
                committee.financial_vote = response.vote

            elif member == "management":
                committee.management_score = response.score
                committee.management_vote = response.vote

            elif member == "ownership":
                committee.ownership_score = response.score
                committee.ownership_vote = response.vote

            elif member == "competitive":
                committee.competitive_score = response.score
                committee.competitive_vote = response.vote

            elif member == "risk":
                committee.risk_score = response.score
                committee.risk_vote = response.vote

            elif member == "valuation":
                committee.valuation_score = response.score
                committee.valuation_vote = response.vote

        research.update_committee(committee)

        print()
        print(committee_vote)

        return committee_vote