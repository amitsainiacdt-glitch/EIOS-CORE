"""
Pipeline Context

Carries information between pipeline stages.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.analysis_pack import AnalysisPack


class PipelineContext:
    """
    Shared context flowing through the EIOS pipeline.
    """

    def __init__(self):

        # ---------------------------------------------------------------------
        # Raw Pipeline Data
        # ---------------------------------------------------------------------

        # Raw observation
        self.observation = None

        # Validated evidence
        self.evidence = None

        # Structured knowledge
        self.knowledge = None

        # Connected entities
        self.relationships = None

        # Investment reasoning
        self.reasoning = None

        # Final recommendation
        self.decision = None

        # Company Master Dossier
        self.master_dossier = None

        # ---------------------------------------------------------------------
        # Intelligence Engine Outputs
        # ---------------------------------------------------------------------

        # Business Intelligence
        self.business_analysis: Optional["AnalysisPack"] = None

        # Financial Intelligence
        self.financial_analysis: Optional["AnalysisPack"] = None

        # Management Intelligence
        self.management_analysis: Optional["AnalysisPack"] = None

        # Ownership Intelligence
        self.ownership_analysis: Optional["AnalysisPack"] = None

        # Competitive Intelligence
        self.competitive_analysis: Optional["AnalysisPack"] = None

        # Risk Intelligence
        self.risk_analysis: Optional["AnalysisPack"] = None

        # Valuation Intelligence
        self.valuation_analysis: Optional["AnalysisPack"] = None

        # Macro Intelligence
        self.macro_analysis: Optional["AnalysisPack"] = None

        # ---------------------------------------------------------------------
        # Pipeline Metadata
        # ---------------------------------------------------------------------

        self.metadata = {}