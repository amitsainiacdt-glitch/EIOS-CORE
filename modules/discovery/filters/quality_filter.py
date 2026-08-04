"""
===============================================================================
EIOS
Everest Investment Operating System

Quality Filter

Purpose:
    Performs the first stage of Discovery Office screening.

Architecture:
    - Evaluates only business quality.
    - Produces quality_score.
    - Does not rank companies.
    - Does not calculate overall score.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.discovery.discovery_candidate import DiscoveryCandidate


class QualityFilter:
    """
    First-stage quality screening.
    """

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:

        # ---------------------------------------------------------
        # Temporary Sprint 9 logic
        # ---------------------------------------------------------

        candidate.quality_score = 80.0

        candidate.strengths.append(
            "Passed initial quality screen."
        )

        return candidate