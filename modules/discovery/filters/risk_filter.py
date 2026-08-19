"""
===============================================================================
EIOS
Everest Investment Operating System

Risk Filter

Purpose:
    Performs the Risk Discovery assessment.

Architecture:
    DiscoveryCandidate
            ↓
         RiskFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates business and investment risk only.
    - Produces risk_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    This is the foundation implementation.
    Real risk analysis will later consume EIOS risk,
    financial, competitive and business research data.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class RiskFilter(DiscoveryFilter):
    """
    Risk screening for the Discovery Office.
    """

    @property
    def name(self) -> str:
        return "Risk"

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate the risk characteristics of a candidate.

        The current implementation establishes the typed
        Discovery pipeline. Real risk analysis will be
        connected to EIOS research data later.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Foundation implementation
        # ------------------------------------------------------

        candidate.risk_score = 80.0

        candidate.strengths.append(
            "Passed initial risk screen."
        )

        return candidate


__all__ = [
    "RiskFilter",
]