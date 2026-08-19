"""
===============================================================================
EIOS
Everest Investment Operating System

Capital Allocation Filter

Purpose:
    Performs the Capital Allocation Discovery assessment.

Architecture:
    DiscoveryCandidate
            ↓
    CapitalAllocationFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates capital allocation quality only.
    - Produces capital_allocation_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real capital allocation analysis will later consume
    EIOS capital allocation research and financial data.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class CapitalAllocationFilter(DiscoveryFilter):
    """
    Capital allocation quality screening.
    """

    @property
    def name(self) -> str:
        return "Capital Allocation"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate capital allocation quality.

        The current implementation establishes the typed
        Discovery pipeline. Real capital allocation analysis
        will be connected to EIOS research data later.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.capital_allocation_score = 80.0

        candidate.strengths.append(
            "Passed initial capital allocation screen."
        )

        return candidate


__all__ = [
    "CapitalAllocationFilter",
]