"""
===============================================================================
EIOS
Everest Investment Operating System

Ranking Engine

Purpose:
    Ranks Discovery Candidates based on Discovery Score.

Architecture:
    - Owns no scoring logic.
    - Owns no filtering logic.
    - Sorts candidates by overall_score.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.discovery.discovery_candidate import DiscoveryCandidate


class RankingEngine:
    """
    Ranks Discovery Candidates.
    """

    def rank(
        self,
        candidates: list[DiscoveryCandidate],
    ) -> list[DiscoveryCandidate]:

        return sorted(
            candidates,
            key=lambda candidate: candidate.overall_score,
            reverse=True,
        )