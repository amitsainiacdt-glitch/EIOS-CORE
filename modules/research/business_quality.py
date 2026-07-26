"""
Business Quality Engine
"""

from modules.research.company_research import CompanyResearch


class BusinessQualityEngine:
    """
    Analyzes business quality and updates CompanyResearch.
    """

    def __init__(self, research: CompanyResearch):
        self.research = research

    def analyze(
        self,
        business_model: str,
        moat: str,
        industry: str,
        market_size: str,
        growth_drivers: list,
        risks: list,
    ):

        self.research.update_business_quality(
            {
                "Business Model": business_model,
                "Moat": moat,
                "Industry": industry,
                "Market Size": market_size,
                "Growth Drivers": growth_drivers,
                "Key Risks": risks,
            }
        )

        # Overall Business Quality Assessment
        self.research.dossier.business_quality["Overall Score"] = 90.0
        self.research.dossier.business_quality["Confidence"] = 40
        self.research.dossier.business_quality["Rating"] = "Good"

        print("Business Quality Analysis Completed")