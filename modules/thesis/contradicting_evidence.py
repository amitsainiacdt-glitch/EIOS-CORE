"""
===============================================================================
EIOS
Contradicting Evidence

Purpose:
    Builds the disconfirming evidence section of the investment thesis
    using the typed Master Dossier.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""


class ContradictingEvidence:
    """
    Builds the contradictory evidence section from the typed
    Master Dossier.
    """

    def build(self, dossier):

        risk = dossier.risk

        return {

            "Business Risks":
                risk.business_risks,

            "Financial Risks":
                risk.financial_risks,

            "Management Concerns":
                risk.management_risks,

            "Competitive Threats":
                [],

            "Industry Risks":
                risk.industry_risks,

            "Macro Risks":
                risk.market_risks,

            "Bear Case":
                "Further evidence required to invalidate thesis.",

            "Confidence":
                risk.confidence,
        }