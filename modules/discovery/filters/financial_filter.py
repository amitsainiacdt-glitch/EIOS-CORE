"""
===============================================================================
EIOS
Everest Investment Operating System

Financial Filter

Purpose:
    Performs the Financial Discovery assessment.

Architecture:
    DiscoveryCandidate
            ↓
      FinancialFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates financial quality only.
    - Produces financial_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real financial analysis will later consume the EIOS
    Financial Engine and canonical financial data.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class FinancialFilter(DiscoveryFilter):
    """
    Financial quality screening for the Discovery Office.
    """

    @property
    def name(self) -> str:
        return "Financial Quality"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate the financial characteristics of a candidate.

        The current implementation establishes the typed
        Discovery pipeline. Real financial metrics will be
        connected through the EIOS Financial Engine later.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.financial_score = 80.0

        candidate.strengths.append(
            "Passed initial financial quality screen."
        )

        return candidate


__all__ = [
    "FinancialFilter",
]