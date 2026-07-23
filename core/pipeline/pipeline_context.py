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

        # Company dossier
        self.master_dossier = None

        # Intelligence engine outputs
        self.business_analysis: Optional["AnalysisPack"] = None
        self.financial_analysis: Optional["AnalysisPack"] = None
        self.competitive_analysis: Optional["AnalysisPack"] = None
        self.valuation_analysis: Optional["AnalysisPack"] = None
        self.risk_analysis: Optional["AnalysisPack"] = None
        self.management_analysis: Optional["AnalysisPack"] = None
        self.macro_analysis: Optional["AnalysisPack"] = None

        # Future support
        self.metadata = {}