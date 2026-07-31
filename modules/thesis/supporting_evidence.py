"""
EIOS
Everest Investment Operating System

Supporting Evidence Builder

Builds thesis-supporting evidence from completed Master Dossier domains.

Business and Financial intelligence are consumed from their
typed Master Dossier sections.
"""


class SupportingEvidence:

    def build(self, dossier):

        evidence = []

        # ---------------------------------------------------------
        # Business
        # ---------------------------------------------------------

        business = dossier.business

        business_analysis_completed = bool(
            business.summary
            or business.evidence
            or business.score
            or business.rating
        )

        if business_analysis_completed:
            evidence.append(
                "Business Quality analysis completed successfully."
            )

        # ---------------------------------------------------------
        # Financial
        # ---------------------------------------------------------

        financial = dossier.financial

        financial_analysis_completed = bool(
            financial.summary
            or financial.evidence
            or financial.score
            or financial.rating
        )

        if financial_analysis_completed:
            evidence.append(
                "Financial analysis supports the investment case."
            )

        # ---------------------------------------------------------
        # Management
        # ---------------------------------------------------------

        if dossier.management:
            evidence.append(
                "Management assessment completed."
            )

        # ---------------------------------------------------------
        # Competitive
        # ---------------------------------------------------------

        if dossier.competitive:
            evidence.append(
                "Competitive intelligence completed."
            )

        # ---------------------------------------------------------
        # Valuation
        # ---------------------------------------------------------

        if dossier.valuation:
            evidence.append(
                "Valuation analysis available."
            )

        # ---------------------------------------------------------
        # Supporting Evidence Output
        # ---------------------------------------------------------

        return {
            "Financial Evidence": (
                ["Financial Engine completed."]
                if financial_analysis_completed
                else []
            ),
            "Business Evidence": (
                ["Business Quality Engine completed."]
                if business_analysis_completed
                else []
            ),
            "Management Evidence": (
                ["Management Engine completed."]
                if dossier.management
                else []
            ),
            "Competitive Evidence": (
                ["Competitive Intelligence completed."]
                if dossier.competitive
                else []
            ),
            "Industry Evidence": evidence,
            "Macro Evidence": [],
            "Evidence Strength": (
                "Strong"
                if len(evidence) >= 4
                else "Moderate"
            ),
            "Confidence": 60,
        }