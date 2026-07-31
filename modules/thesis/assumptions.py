"""
EIOS
Everest Investment Operating System

Thesis Assumptions Builder

Builds thesis assumptions from completed Master Dossier research domains.

Business and Financial intelligence are consumed from their
typed Master Dossier sections.
"""


class Assumptions:

    def build(self, dossier):

        assumptions = []

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
            assumptions.append(
                "Business quality remains stable."
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
            assumptions.append(
                "Financial performance remains within expected range."
            )

        # ---------------------------------------------------------
        # Management
        # ---------------------------------------------------------

        if dossier.management:
            assumptions.append(
                "Management continues current capital allocation discipline."
            )

        # ---------------------------------------------------------
        # Competitive
        # ---------------------------------------------------------

        if dossier.competitive:
            assumptions.append(
                "Competitive position remains stable."
            )

        return assumptions