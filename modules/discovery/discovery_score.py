"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Score

Purpose:
    Aggregates Discovery Office filter scores into a single
    institutional discovery score.

Architecture:
    - Pure scoring engine.
    - Owns no filtering logic.
    - Owns no ranking logic.
    - Calculates overall discovery score.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.discovery.discovery_candidate import DiscoveryCandidate


class DiscoveryScore:
    """
    Calculates the overall Discovery Score.
    """

    def calculate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:

        scores = [
            candidate.quality_score,
            candidate.growth_score,
            candidate.financial_score,
            candidate.management_score,
            candidate.capital_allocation_score,
            candidate.moat_score,
            candidate.risk_score,
            candidate.tailwind_score,
            candidate.valuation_score,
        ]

        valid_scores = [
            score
            for score in scores
            if score > 0
        ]

        if valid_scores:

            candidate.overall_score = (
                sum(valid_scores)
                / len(valid_scores)
            )

        else:

            candidate.overall_score = 0.0

        return candidate