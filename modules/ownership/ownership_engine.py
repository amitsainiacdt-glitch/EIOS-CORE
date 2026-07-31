"""
===============================================================================
Module: ownership_engine.py

Purpose:
    Main orchestrator for Ownership Intelligence.

Responsibilities:
    - Validate pipeline context
    - Execute ownership analysis
    - Combine results from ownership sub-engines
    - Produce a standard AnalysisPack

Author:
    EIOS
===============================================================================
"""

from core.base_engine import BaseEngine
from core.analysis_pack import AnalysisPack
from core.pipeline_context import PipelineContext

from .promoter_engine import PromoterEngine


class OwnershipEngine(BaseEngine):
    """
    Ownership Intelligence Engine.
    """

    ENGINE_NAME = "Ownership"

    def __init__(self):

        self._confidence = 0.0
        self._summary = ""

        self.promoter_engine = PromoterEngine()

    # ------------------------------------------------------------------
    # BaseEngine Contract
    # ------------------------------------------------------------------

    def validate(self, context: PipelineContext) -> bool:
        """
        Validate required pipeline data.
        """

        if context is None:
            return False

        if context.master_dossier is None:
            return False

        return True

    def analyze(self, context: PipelineContext) -> AnalysisPack:
        """
        Execute ownership analysis.
        """

        if not self.validate(context):
            raise ValueError("Invalid PipelineContext.")

        promoter_pack = self.promoter_engine.analyze(context)

        score = promoter_pack.score
        confidence = promoter_pack.confidence

        self._confidence = confidence
        self._summary = promoter_pack.summary

        pack = AnalysisPack(
            engine=self.ENGINE_NAME,
            score=score,
            confidence=confidence,
            summary=self._summary,
        )

        pack.evidence.extend(promoter_pack.evidence)
        pack.assumptions.extend(promoter_pack.assumptions)
        pack.warnings.extend(promoter_pack.warnings)

        pack.metadata["promoter"] = promoter_pack.metadata

        context.ownership_analysis = pack

        return pack

    def confidence(self) -> float:
        """
        Return analysis confidence.
        """

        return self._confidence

    def summary(self) -> str:
        """
        Return latest ownership summary.
        """

        return self._summary