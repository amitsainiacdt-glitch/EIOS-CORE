"""
===============================================================================
EIOS
Everest Investment Operating System

Analysis Pack Processor

Purpose:
    Processes the consolidated AnalysisPack produced by the
    ResearchOrchestrator and persists each typed section into the
    Master Dossier through CompanyResearch.

Architecture:

    ResearchOrchestrator
            ↓
      AnalysisPack
            ↓
    AnalysisPackProcessor
            ↓
      CompanyResearch
            ↓
      Master Dossier

Design Principles:

- No calculations.
- No business logic.
- No scoring.
- No persistence outside CompanyResearch.
- One responsibility: dispatch typed sections.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from modules.research.analysis_pack import AnalysisPack
from modules.research.company_research import CompanyResearch


class AnalysisPackProcessor:
    """
    Dispatches AnalysisPack sections into the typed Master Dossier.
    """

    def __init__(self, research: CompanyResearch):
        self.research = research

    def process(self, pack: AnalysisPack) -> None:

        if pack is None:
            raise ValueError("AnalysisPack cannot be None.")

        # ==========================================================
        # Business
        # ==========================================================

        if pack.business is not None:
            self.research.update_business_quality(pack.business)

        # ==========================================================
        # Financial
        # ==========================================================

        if pack.financial is not None:
            self.research.update_financials(pack.financial)

        # ==========================================================
        # Management
        # ==========================================================

        if pack.management is not None:
            self.research.update_management(pack.management)

        # ==========================================================
        # Ownership
        # ==========================================================

        if pack.ownership is not None:
            self.research.update_ownership(pack.ownership)

        # ==========================================================
        # Competitive
        # ==========================================================

        if pack.competitive is not None:
            self.research.update_competitive(pack.competitive)

        # ==========================================================
        # Risk
        # ==========================================================

        if pack.risk is not None:
            self.research.update_risk(pack.risk)

        # ==========================================================
        # Valuation
        # ==========================================================

        if pack.valuation is not None:
            self.research.update_valuation(pack.valuation)

        # ==========================================================
        # Committee
        # ==========================================================

        if pack.committee is not None:
            self.research.update_committee(pack.committee)

        # ==========================================================
        # Macro
        # ==========================================================

        if pack.macro is not None:
            self.research.update_macro(pack.macro)