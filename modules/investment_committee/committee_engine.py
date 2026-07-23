from modules.investment_committee.business_member import BusinessMember
from modules.investment_committee.committee_vote import CommitteeVote
from modules.investment_committee.recommendation_engine import RecommendationEngine
from modules.investment_committee.confidence_engine import ConfidenceEngine
from modules.investment_committee.portfolio_fit import PortfolioFit
from modules.investment_committee.decision_summary import DecisionSummary


class CommitteeEngine:

    def __init__(self, research):

        self.research = research

        # Committee Members
        self.business_member = BusinessMember()

        # Committee Engines
        self.committee_vote = CommitteeVote()
        self.recommendation_engine = RecommendationEngine()
        self.confidence_engine = ConfidenceEngine()
        self.portfolio_fit = PortfolioFit()
        self.decision_summary = DecisionSummary()

    def analyze(self):

        print("\n=====================================")
        print("Starting Investment Committee Analysis")
        print("=====================================")

        # -------------------------------------
        # Business Committee Vote
        # -------------------------------------

        business_vote = self.business_member.evaluate(self.research)

        print("\nBusiness Committee")
        print("---------------------------")
        print(f"Vote       : {business_vote['Vote']}")
        print(f"Score      : {business_vote['Score']}")
        print(f"Confidence : {business_vote['Confidence']}")
        print(f"Reason     : {business_vote['Reason']}")

        # -------------------------------------
        # Build Committee Data
        # -------------------------------------

        committee_data = {
            "Business": business_vote
        }

        # -------------------------------------
        # Committee Vote
        # -------------------------------------

        vote = self.committee_vote.vote(committee_data)

        # -------------------------------------
        # Recommendation
        # -------------------------------------

        recommendation = self.recommendation_engine.recommend(
            vote
        )

        # -------------------------------------
        # Confidence
        # -------------------------------------

        confidence = self.confidence_engine.calculate(
            vote,
            recommendation
        )

        # -------------------------------------
        # Portfolio Fit
        # -------------------------------------

        portfolio_fit = self.portfolio_fit.evaluate(
            committee_data
        )

        # -------------------------------------
        # Decision Summary
        # -------------------------------------

        summary = self.decision_summary.build(
            vote,
            recommendation,
            confidence,
            portfolio_fit
        )

        # -------------------------------------
        # Save to Research
        # -------------------------------------

        self.research.update_committee(summary)

        print("\n=====================================")
        print("Investment Committee Completed")
        print("=====================================")

        return summary