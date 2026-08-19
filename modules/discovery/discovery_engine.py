"""
===============================================================================
EIOS
Everest Investment Operating System

Long-Term Discovery Engine

Purpose:
    Coordinates the complete Long-Term Discovery Office.

Architecture:

    UniverseBuilder
          ↓
    DiscoveryCandidate
          ↓
    Discovery Filters
          ↓
    DiscoveryScore
          ↓
    RankingEngine
          ↓
    Ranked Discovery Candidates

Responsibilities:
    - Build the discovery universe.
    - Run the canonical discovery filters.
    - Calculate the overall Discovery Score.
    - Rank Discovery Candidates.

Non-responsibilities:
    - No internet access.
    - No external data retrieval.
    - No valuation calculation.
    - No opportunity scoring.
    - No portfolio allocation.
    - No trade execution.

Design Principle:
    The engine coordinates.
    Filters analyze.
    DiscoveryScore calculates the overall score.
    RankingEngine ranks.
===============================================================================
"""

from modules.discovery.universe_builder import (
    UniverseBuilder,
)

from modules.discovery.filters.quality_filter import (
    QualityFilter,
)

from modules.discovery.filters.growth_filter import (
    GrowthFilter,
)

from modules.discovery.filters.financial_filter import (
    FinancialFilter,
)

from modules.discovery.filters.management_filter import (
    ManagementFilter,
)

from modules.discovery.filters.capital_allocation_filter import (
    CapitalAllocationFilter,
)

from modules.discovery.filters.moat_filter import (
    MoatFilter,
)

from modules.discovery.filters.risk_filter import (
    RiskFilter,
)

from modules.discovery.filters.tailwind_filter import (
    TailwindFilter,
)

from modules.discovery.filters.valuation_filter import (
    ValuationFilter,
)

from modules.discovery.discovery_score import (
    DiscoveryScore,
)

from modules.discovery.ranking_engine import (
    RankingEngine,
)


class DiscoveryEngine:
    """
    Coordinates the complete Long-Term Discovery Office.
    """

    def __init__(self) -> None:

        self.universe_builder = (
            UniverseBuilder()
        )

        self.filters = [
            QualityFilter(),
            GrowthFilter(),
            FinancialFilter(),
            ManagementFilter(),
            CapitalAllocationFilter(),
            MoatFilter(),
            RiskFilter(),
            TailwindFilter(),
            ValuationFilter(),
        ]

        self.discovery_score = (
            DiscoveryScore()
        )

        self.ranking_engine = (
            RankingEngine()
        )

    # ==========================================================
    # DISCOVERY
    # ==========================================================

    def discover(self):
        """
        Execute the complete Long-Term Discovery pipeline.

        Returns:
            Ranked list of DiscoveryCandidate objects.
        """

        candidates = (
            self.universe_builder.build()
        )

        # ------------------------------------------------------
        # Run all Discovery filters
        # ------------------------------------------------------

        for candidate in candidates:

            for discovery_filter in self.filters:

                discovery_filter.evaluate(
                    candidate
                )

            # --------------------------------------------------
            # Calculate overall Discovery Score
            # --------------------------------------------------

            self.discovery_score.calculate(
                candidate
            )

        # ------------------------------------------------------
        # Rank candidates
        # ------------------------------------------------------

        ranked_candidates = (
            self.ranking_engine.rank(
                candidates
            )
        )

        return ranked_candidates


__all__ = [
    "DiscoveryEngine",
]