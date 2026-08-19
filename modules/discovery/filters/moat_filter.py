"""
===============================================================================
EIOS
Everest Investment Operating System

Moat Filter

Purpose:
    Performs the competitive-moat Discovery assessment.

Architecture:
    DiscoveryCandidate
            ↓
         MoatFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates competitive advantage only.
    - Produces moat_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real moat analysis will later consume EIOS competitive
    intelligence and business-quality research.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class MoatFilter(DiscoveryFilter):
    """
    Competitive-moat screening.
    """

    @property
    def name(self) -> str:
        return "Competitive Moat"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate the competitive moat of a candidate.

        The current implementation establishes the typed
        Discovery pipeline. Real competitive-moat analysis
        will be connected to EIOS research data later.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.moat_score = 80.0

        candidate.strengths.append(
            "Passed initial competitive moat screen."
        )

        return candidate


__all__ = [
    "MoatFilter",
]