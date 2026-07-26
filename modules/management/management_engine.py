from modules.management.capital_allocation import CapitalAllocationEngine
from modules.management.governance import GovernanceEngine
from modules.management.behaviour import BehaviourEngine
from modules.management.communication import CommunicationEngine
from modules.management.management_scorecard import ManagementScorecard
from modules.research.company_research import CompanyResearch


class ManagementEngine:

    def __init__(self, research: CompanyResearch):
        self.research = research

        self.capital_allocation = CapitalAllocationEngine()
        self.governance = GovernanceEngine()
        self.behaviour = BehaviourEngine()
        self.communication = CommunicationEngine()
        self.scorecard = ManagementScorecard()

    def analyze(self, management_data: dict):

        print("\nStarting Management Analysis...")

        capital = self.capital_allocation.evaluate(management_data)
        governance = self.governance.evaluate(management_data)
        behaviour = self.behaviour.evaluate(management_data)
        communication = self.communication.evaluate(management_data)

        overall_score = self.scorecard.calculate(
            capital,
            governance,
            behaviour,
            communication
        )

        management_summary = {
            "Capital Allocation": capital,
            "Governance": governance,
            "Behaviour": behaviour,
            "Communication": communication,
            "Overall Score": overall_score
        }

        self.research.update_management(management_summary)

        # =====================================================
        # MANAGEMENT OVERALL SCORE
        # =====================================================

        self.research.dossier.management["Overall Score"] = {
            "Overall Score": overall_score["Overall Score"],
            "Confidence": overall_score["Confidence"],
            "Rating": overall_score["Rating"],
        }

        print("Management Analysis Completed")