"""
===============================================================================
Module: ownership_report.py

Purpose:
    Generate the final Ownership AnalysisPack.

Responsibilities:
    - Build Ownership AnalysisPack
    - Combine Scorecard
    - Combine Reasoning
    - Populate Evidence
    - Populate Metadata

Author:
    EIOS
===============================================================================
"""

from core.analysis_pack import AnalysisPack

from .ownership_scorecard import OwnershipScoreCard


class OwnershipReportGenerator:
    """
    Generates the final ownership report.
    """

    ENGINE_NAME = "Ownership"

    def generate(
        self,
        scorecard: OwnershipScoreCard,
        reasoning: str,
        evidence: list[str] | None = None,
        warnings: list[str] | None = None,
        assumptions: list[str] | None = None,
    ) -> AnalysisPack:

        evidence = evidence or []
        warnings = warnings or []
        assumptions = assumptions or []

        report = AnalysisPack(
            engine=self.ENGINE_NAME,
            score=scorecard.total_score,
            confidence=self._confidence(scorecard),
            summary=reasoning,
        )

        report.evidence.extend(evidence)
        report.warnings.extend(warnings)
        report.assumptions.extend(assumptions)

        report.metadata["rating"] = scorecard.rating
        report.metadata["promoter_score"] = scorecard.promoter_score
        report.metadata["fii_score"] = scorecard.fii_score
        report.metadata["dii_score"] = scorecard.dii_score
        report.metadata["insider_score"] = scorecard.insider_score
        report.metadata["concentration_score"] = (
            scorecard.concentration_score
        )
        report.metadata["governance_score"] = (
            scorecard.governance_score
        )

        return report

    def _confidence(
        self,
        scorecard: OwnershipScoreCard,
    ) -> float:
        """
        Calculate confidence from ownership quality.
        """

        score = scorecard.total_score

        if score >= 90:
            return 1.00

        if score >= 80:
            return 0.90

        if score >= 70:
            return 0.80

        if score >= 60:
            return 0.70

        return 0.50