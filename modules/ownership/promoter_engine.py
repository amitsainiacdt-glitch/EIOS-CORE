"""
===============================================================================
Module: promoter_engine.py

Purpose:
    Analyze promoter ownership quality.

Responsibilities:
    - Validate ownership data
    - Analyze promoter holding
    - Evaluate promoter confidence
    - Generate AnalysisPack

Author:
    EIOS
===============================================================================
"""

from core.base_engine import BaseEngine
from core.analysis_pack import AnalysisPack
from core.pipeline_context import PipelineContext


class PromoterEngine(BaseEngine):
    """
    Promoter Ownership Intelligence Engine.
    """

    ENGINE_NAME = "Promoter"

    def __init__(self):

        self._confidence = 0.0
        self._summary = ""

    # ---------------------------------------------------------------------
    # BaseEngine Contract
    # ---------------------------------------------------------------------

    def validate(self, context: PipelineContext) -> bool:

        if context is None:
            return False

        if context.master_dossier is None:
            return False

        ownership = getattr(
            context.master_dossier,
            "ownership",
            None,
        )

        return ownership is not None

    def analyze(self, context: PipelineContext) -> AnalysisPack:

        if not self.validate(context):
            raise ValueError("Ownership data not available.")

        ownership = context.master_dossier.ownership

        promoter = ownership.get("promoter_percent", 0.0)
        pledge = ownership.get("pledged_percent", 0.0)

        score = self._calculate_score(
            promoter,
            pledge,
        )

        confidence = self._calculate_confidence(
            promoter,
            pledge,
        )

        summary = self._generate_summary(
            promoter,
            pledge,
        )

        self._confidence = confidence
        self._summary = summary

        pack = AnalysisPack(
            engine=self.ENGINE_NAME,
            score=score,
            confidence=confidence,
            summary=summary,
        )

        pack.evidence.append(
            f"Promoter Holding : {promoter:.2f}%"
        )

        pack.evidence.append(
            f"Pledged Shares : {pledge:.2f}%"
        )

        if pledge > 20:
            pack.warnings.append(
                "High promoter pledge detected."
            )

        pack.metadata["promoter_percent"] = promoter
        pack.metadata["pledged_percent"] = pledge

        return pack

    def confidence(self) -> float:

        return self._confidence

    def summary(self) -> str:

        return self._summary

    # ---------------------------------------------------------------------
    # Internal Methods
    # ---------------------------------------------------------------------

    def _calculate_score(
        self,
        promoter: float,
        pledge: float,
    ) -> float:

        score = promoter

        score -= pledge

        score = max(0.0, min(score, 100.0))

        return score

    def _calculate_confidence(
        self,
        promoter: float,
        pledge: float,
    ) -> float:

        if promoter >= 60 and pledge == 0:
            return 1.00

        if promoter >= 50 and pledge < 10:
            return 0.85

        if promoter >= 40:
            return 0.70

        return 0.50

    def _generate_summary(
        self,
        promoter: float,
        pledge: float,
    ) -> str:

        if pledge > 20:
            return (
                f"Promoter holding is {promoter:.2f}% "
                f"with elevated pledge risk."
            )

        if promoter >= 60:
            return (
                f"Strong promoter ownership "
                f"({promoter:.2f}%) with low pledge."
            )

        return (
            f"Moderate promoter ownership "
            f"({promoter:.2f}%)."
        )