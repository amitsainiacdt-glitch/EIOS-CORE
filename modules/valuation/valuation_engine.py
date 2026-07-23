"""
EIOS
Everest Investment Operating System

Valuation Engine

Coordinates all valuation methodologies and updates
the Master Dossier through CompanyResearch.
"""

from modules.research.company_research import CompanyResearch
from modules.valuation.owners_earnings import OwnerEarningsEngine


class ValuationEngine:

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.owner_earnings = OwnerEarningsEngine()

    def analyze(self, financial_data: dict):

        print("\nStarting Valuation Analysis...")

        owner_earnings = self.owner_earnings.evaluate(financial_data)

        valuation_summary = {
            "Owner Earnings": owner_earnings
        }

        self.research.update_valuation(valuation_summary)

        print("Valuation Analysis Completed")