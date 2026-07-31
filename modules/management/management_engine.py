from modules.management.capital_allocation import CapitalAllocationEngine
from modules.management.governance import GovernanceEngine
from modules.management.behaviour import BehaviourEngine
from modules.management.communication import CommunicationEngine
from modules.management.management_scorecard import ManagementScorecard

from modules.research.company_research import CompanyResearch

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine

from modules.intelligence.management_intelligence import ManagementIntelligence


class ManagementEngine:

    def __init__(self, research: CompanyResearch):
        self.research = research

        self.capital_allocation = CapitalAllocationEngine()
        self.governance = GovernanceEngine()
        self.behaviour = BehaviourEngine()
        self.communication = CommunicationEngine()
        self.scorecard = ManagementScorecard()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, management_data: dict):

        print("\nStarting Management Analysis...")

        capital = self.capital_allocation.evaluate(management_data)
        governance = self.governance.evaluate(management_data)
        behaviour = self.behaviour.evaluate(management_data)
        communication = self.communication.evaluate(management_data)

        overall = self.scorecard.calculate(
            capital,
            governance,
            behaviour,
            communication,
        )

        score_result = self.scoring_engine.calculate(
            score=overall["Raw Score"],
            max_score=overall["Max Score"],
        )

        confidence_result = self.confidence_engine.calculate(
            evidence_items=4,
            expected_items=10,
        )

        management_summary = {
            "Capital Allocation": capital,
            "Governance": governance,
            "Behaviour": behaviour,
            "Communication": communication,
            "Overall Score": {
                "Overall Score": score_result.percentage,
                "Raw Score": score_result.score,
                "Maximum Score": score_result.max_score,
                "Confidence": confidence_result.confidence,
                "Rating": score_result.grade,
            },
        }

        self.research.update_management(management_summary)

        # =====================================================
        # MANAGEMENT OVERALL SCORE
        # =====================================================

        self.research.dossier.management["Overall Score"] = {
            "Overall Score": score_result.percentage,
            "Raw Score": score_result.score,
            "Maximum Score": score_result.max_score,
            "Confidence": confidence_result.confidence,
            "Rating": score_result.grade,
        }

        # =====================================================
        # PUBLISH MANAGEMENT INTELLIGENCE
        # =====================================================

        management_intelligence = ManagementIntelligence.build(
            self.research,
            confidence_result,
        )

        self.research.context.publish_intelligence(
            management_intelligence
        )

        print("Management Analysis Completed")