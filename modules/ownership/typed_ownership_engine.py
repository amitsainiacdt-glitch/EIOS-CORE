"""
===============================================================================
EIOS
Everest Investment Operating System

Typed Ownership Engine

Purpose:
    Produces Ownership Intelligence and persists it into the typed
    Master Dossier.

Architecture:
    TypedOwnershipEngine
        -> OwnershipSection
        -> CompanyResearch
        -> MasterDossier

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from modules.research.company_research import CompanyResearch
from modules.master_dossier.ownership_section import OwnershipSection


class TypedOwnershipEngine:
    """
    Produces typed Ownership Intelligence.
    """

    def __init__(self, research: CompanyResearch):
        self.research = research

    def analyze(
        self,
        promoter_holding: float,
        promoter_pledge: float,
        fii_holding: float,
        dii_holding: float,
        public_holding: float,
        promoter_trend: str,
        fii_trend: str,
        dii_trend: str,
    ) -> OwnershipSection:

        ownership = OwnershipSection()

        # ==========================================================
        # Ownership Details
        # ==========================================================

        ownership.promoter_holding = promoter_holding
        ownership.promoter_pledge = promoter_pledge

        ownership.fii_holding = fii_holding
        ownership.dii_holding = dii_holding
        ownership.public_holding = public_holding

        # ==========================================================
        # Trend Analysis
        # ==========================================================

        ownership.promoter_trend = promoter_trend
        ownership.fii_trend = fii_trend
        ownership.dii_trend = dii_trend

        # ==========================================================
        # Initial Institutional Scores
        # ==========================================================

        ownership.promoter_score = 80.0
        ownership.fii_score = 75.0
        ownership.dii_score = 70.0
        ownership.insider_score = 75.0
        ownership.concentration_score = 80.0
        ownership.governance_score = 85.0

        ownership.score = (
            ownership.promoter_score
            + ownership.fii_score
            + ownership.dii_score
            + ownership.insider_score
            + ownership.concentration_score
            + ownership.governance_score
        ) / 6

        ownership.confidence = 75.0
        ownership.rating = "A"

        ownership.summary = (
            "Ownership analysis completed successfully."
        )

        ownership.strengths = [
            "Stable promoter ownership"
        ]

        ownership.weaknesses = []

        ownership.opportunities = [
            "Increasing institutional participation"
        ]

        ownership.risks = [
            "Promoter pledge should remain under observation"
        ]

        ownership.evidence = [
            "Promoter Holding",
            "FII Holding",
            "DII Holding",
        ]

        ownership.assumptions = [
            "Ownership data supplied is accurate."
        ]

        ownership.source = "TypedOwnershipEngine"

        # ==========================================================
        # Persist to Master Dossier
        # ==========================================================

        self.research.update_ownership(ownership)

        print("Ownership Analysis Completed")

        return ownership