from modules.investment_committee.business_member import BusinessMember
from modules.investment_committee.financial_member import FinancialMember
from modules.investment_committee.management_member import ManagementMember
from modules.investment_committee.risk_member import RiskMember
from modules.investment_committee.competitive_member import CompetitiveMember
from modules.investment_committee.valuation_member import ValuationMember
from modules.investment_committee.thesis_member import ThesisMember
from modules.investment_committee.portfolio_member import PortfolioMember

from modules.investment_committee.committee_vote import CommitteeVote
from modules.investment_committee.recommendation_engine import RecommendationEngine
from modules.investment_committee.confidence_engine import ConfidenceEngine
from modules.investment_committee.decision_summary import DecisionSummary


class CommitteeEngine:
    """
    Orchestrates the complete Investment Committee.
    """

    def __init__(self, research):

        self.research = research

        self.members = [

            BusinessMember(),
            FinancialMember(),
            ManagementMember(),
            RiskMember(),
            CompetitiveMember(),
            ValuationMember(),
            ThesisMember(),

        ]

        self.portfolio_member = PortfolioMember()

        self.vote_engine = CommitteeVote()
        self.recommendation_engine = RecommendationEngine()
        self.confidence_engine = ConfidenceEngine()
        self.summary_engine = DecisionSummary()

    def analyze(self):

        print("\n===================================")
        print("Investment Committee")
        print("===================================")

        responses = []

        for member in self.members:

            response = member.evaluate(self.research)

            responses.append(response)

            print(
                f"{response.member:20}"
                f"{response.vote:8}"
                f"{response.score:5}"
                f"{response.confidence:5}"
            )

        vote_result = self.vote_engine.vote(responses)

        recommendation = self.recommendation_engine.recommend(
            vote_result
        )

        confidence = self.confidence_engine.calculate(
            vote_result,
            recommendation,
        )

        portfolio_vote = self.portfolio_member.evaluate(
            self.research
        )

        summary = self.summary_engine.build(
            vote_result,
            recommendation,
            confidence,
            portfolio_vote,
        )

        self.research.update_committee(summary)

        print("\nCommittee Completed")

        return summary