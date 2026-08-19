"""
===============================================================================
EIOS
Everest Investment Operating System

Tailwind Filter

Purpose:
    Performs the structural industry and macro tailwind
    Discovery assessment.

Architecture:
    DiscoveryCandidate
            ↓
       TailwindFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates structural tailwinds only.
    - Produces tailwind_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real tailwind analysis will later consume EIOS
    sector, macro, competitive and external intelligence.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class TailwindFilter(DiscoveryFilter):
    """
    Structural industry and macro tailwind screening.
    """

    @property
    def name(self) -> str:
        return "Structural Tailwinds"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate structural tailwinds affecting a candidate.

        The current implementation establishes the typed
        Discovery pipeline. Real tailwind analysis will later
        be connected to EIOS sector and external intelligence.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.tailwind_score = 80.0

        candidate.strengths.append(
            "Passed initial structural tailwind screen."
        )

        return candidate


__all__ = [
    "TailwindFilter",
]