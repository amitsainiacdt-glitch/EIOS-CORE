"""
Management Analysis Engine
"""

from modules.research.company_research import CompanyResearch


class ManagementEngine:
    """
    Evaluates the quality of management and updates CompanyResearch.
    """

    def __init__(self, research: CompanyResearch):
        self.research = research

    def analyze(
        self,
        promoter_holding: float,
        capital_allocation: str,
        governance: str,
        execution: str,
        communication: str,
        red_flags: list,
    ):

        self.research.update_management(
            {
                "Promoter Holding": promoter_holding,
                "Capital Allocation": capital_allocation,
                "Corporate Governance": governance,
                "Execution": execution,
                "Communication": communication,
                "Red Flags": red_flags,
            }
        )

        print("Management Analysis Completed")