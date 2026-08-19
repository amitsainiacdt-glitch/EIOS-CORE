"""
===============================================================================
EIOS
Everest Investment Operating System

Growth Filter

Purpose:
    Performs the Long-Term Discovery growth assessment.

Architecture:
    DiscoveryCandidate
            ↓
        GrowthFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates growth only.
    - Produces growth_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real growth analysis will later consume EIOS financial data.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class GrowthFilter(DiscoveryFilter):
    """
    Long-Term Discovery growth screening.
    """

    @property
    def name(self) -> str:
        return "Growth"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate the growth characteristics of a candidate.

        Current implementation is deliberately a foundation
        implementation until the financial data layer is connected.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.growth_score = 80.0

        candidate.strengths.append(
            "Passed initial growth screen."
        )

        return candidate


__all__ = [
    "GrowthFilter",
]