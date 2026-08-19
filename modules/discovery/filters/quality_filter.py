"""
===============================================================================
EIOS
Everest Investment Operating System

Quality Filter

Purpose:
    Performs the first-stage Long-Term Discovery screening.

Architecture:
    DiscoveryCandidate
            ↓
      QualityFilter
            ↓
    DiscoveryCandidate

Design Principles:
    - Implements the canonical DiscoveryFilter contract.
    - Evaluates business quality only.
    - Produces quality_score.
    - Does not calculate overall Discovery Score.
    - Does not rank companies.
    - Does not perform valuation.
    - Does not make investment decisions.

NOTE:
    The current scoring logic is intentionally a temporary
    foundation implementation. Real business-quality analysis
    will be connected to EIOS research data later.
===============================================================================
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.discovery.filters.discovery_filter import (
    DiscoveryFilter,
)


class QualityFilter(DiscoveryFilter):
    """
    First-stage Long-Term Discovery quality screening.
    """

    # ==========================================================
    # NAME
    # ==========================================================

    @property
    def name(self) -> str:
        return "Business Quality"

    # ==========================================================
    # EVALUATE
    # ==========================================================

    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate business quality.

        This implementation provides only the existing
        Sprint-9 foundation behaviour.

        It does not invent additional analytical inputs.
        """

        if candidate is None:
            raise ValueError(
                "candidate must not be None"
            )

        # ------------------------------------------------------
        # Existing Sprint-9 foundation logic
        # ------------------------------------------------------

        candidate.quality_score = 80.0

        candidate.strengths.append(
            "Passed initial quality screen."
        )

        return candidate


__all__ = [
    "QualityFilter",
]