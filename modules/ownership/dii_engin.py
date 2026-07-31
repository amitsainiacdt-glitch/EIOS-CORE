"""
===============================================================================
Module: dii_engine.py

Purpose:
    Analyze Domestic Institutional Investor (DII) ownership.

Responsibilities:
    - Validate ownership data
    - Analyze DII holding
    - Detect institutional accumulation/distribution
    - Generate AnalysisPack

Author:
    EIOS
===============================================================================
"""

from core.base_engine import BaseEngine
from core.analysis_pack import AnalysisPack
from core.pipeline_context import PipelineContext


class DIIEngine(BaseEngine):
    """
    Domestic Institutional Investor Intelligence Engine.
    """

    ENGINE_NAME = "DII"

    def __init__(self):

        self._confidence = 0.0
        self._summary = ""

    # ------------------------------------------------------------------
    # BaseEngine Contract
    # ------------------------------------------------------------------

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
            raise ValueError("Ownership data unavailable.")

        ownership = context.master_dossier.ownership

        current = ownership.get("dii_percent", 0.0)
        previous = ownership.get("previous_dii_percent", current)

        change = current - previous

        score = self._calculate_score(current, change)
        confidence = self._calculate_confidence(change)
        summary = self._generate_summary(current, change)

        self._confidence = confidence
        self._summary = summary

        pack = AnalysisPack(
            engine=self.ENGINE_NAME,
            score=score,
            confidence=confidence,
            summary=summary,
        )

        pack.evidence.append(
            f"Current DII Holding: {current:.2f}%"
        )

        pack.evidence.append(
            f"Quarterly Change: {change:.2f}%"
        )

        if change < -2:
            pack.warnings.append(
                "Significant DII selling detected."
            )

        pack.metadata["current_dii"] = current
        pack.metadata["previous_dii"] = previous
        pack.metadata["change"] = change

        return pack

    def confidence(self) -> float:

        return self._confidence

    def summary(self) -> str:

        return self._summary

    # ------------------------------------------------------------------
    # Internal Methods
    # ------------------------------------------------------------------

    def _calculate_score(
        self,
        current: float,
        change: float,
    ) -> float:

        score = 50.0

        score += min(current, 30)

        score += change * 5

        return max(0.0, min(score, 100.0))

    def _calculate_confidence(
        self,
        change: float,
    ) -> float:

        if change >= 2:
            return 1.00

        if change >= 0:
            return 0.85

        if change >= -2:
            return 0.70

        return 0.50

    def _generate_summary(
        self,
        current: float,
        change: float,
    ) -> str:

        if change > 0:
            return (
                f"DII holding increased to "
                f"{current:.2f}%."
            )

        if change < 0:
            return (
                f"DII holding decreased to "
                f"{current:.2f}%."
            )

        return (
            f"DII holding remained stable at "
            f"{current:.2f}%."
        )