"""
EIOS
Everest Investment Operating System

Investment Thesis Builder

Builds the investment thesis from the Master Dossier.

Architecture:
    Business intelligence is consumed from the typed
    MasterDossier.business section.

    Financial intelligence is consumed from the typed
    MasterDossier.financial section.
"""


class InvestmentThesis:

    def build(self, dossier):

        business = dossier.business
        financial = dossier.financial
        management = dossier.management
        valuation = dossier.valuation
        competitive = dossier.competitive

        # ---------------------------------------------------------
        # Business Summary
        # ---------------------------------------------------------

        business_summary = (
            f"{dossier.company_name} operates in the "
            f"{dossier.industry} industry."
        )

        # ---------------------------------------------------------
        # Investment Thesis
        # ---------------------------------------------------------

        investment_thesis = (
            "The company demonstrates attractive business "
            "fundamentals based on completed EIOS research."
        )

        long_term_drivers = [
            "Business Quality",
            "Financial Strength",
            "Competitive Position",
            "Management Execution",
            "Capital Allocation",
        ]

        # ---------------------------------------------------------
        # Competitive Advantage
        # ---------------------------------------------------------

        competitive_advantage = (
            business.moat
            if business.moat
            else "Under Evaluation"
        )

        expected_outcome = "Potential Long-term Compounder"

        time_horizon = "5-10 Years"

        # ---------------------------------------------------------
        # Domain Completion State
        # ---------------------------------------------------------

        business_analysis_completed = bool(
            business.summary
            or business.evidence
            or business.score
            or business.rating
        )

        financial_analysis_completed = bool(
            financial.summary
            or financial.evidence
            or financial.score
            or financial.rating
        )

        # ---------------------------------------------------------
        # Thesis Output
        # ---------------------------------------------------------

        return {
            "Business Summary": business_summary,
            "Investment Thesis": investment_thesis,
            "Long-term Drivers": long_term_drivers,
            "Competitive Advantage": competitive_advantage,
            "Expected Outcome": expected_outcome,
            "Time Horizon": time_horizon,
            "Supporting Modules": {
                "Business Quality": business_analysis_completed,
                "Financial Analysis": financial_analysis_completed,
                "Management Analysis": bool(management),
                "Competitive Analysis": bool(competitive),
                "Valuation": bool(valuation),
            },
            "Confidence": 60,
        }