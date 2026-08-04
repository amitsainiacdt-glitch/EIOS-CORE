"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Engine

Purpose:
    Coordinates the Discovery Office.

Architecture:
    - Owns no scoring logic.
    - Owns no filtering logic.
    - Coordinates discovery.
    - Filters perform analysis.
    - Ranking Engine performs ranking.

Author:
    EIOS

Release:
    3.1
===============================================================================
"""

from modules.discovery.universe_builder import UniverseBuilder
from modules.discovery.filters.quality_filter import QualityFilter


class DiscoveryEngine:
    """
    Coordinates the Discovery Office.
    """

    def __init__(self):

        self.universe_builder = UniverseBuilder()

        self.quality_filter = QualityFilter()

    # ==========================================================
    # Discovery
    # ==========================================================

    def discover(self):

        print()
        print("=" * 60)
        print("DISCOVERY OFFICE")
        print("=" * 60)

        candidates = self.universe_builder.build()

        print(
            f"Universe Size : {len(candidates)} companies"
        )

        print()

        # ------------------------------------------------------
        # Quality Filter
        # ------------------------------------------------------

        for candidate in candidates:

            self.quality_filter.evaluate(candidate)

        # ------------------------------------------------------
        # Display
        # ------------------------------------------------------

        print(
            f"{'Ticker':15}"
            f"{'Quality':>12}"
        )

        print("-" * 30)

        for candidate in candidates:

            print(
                f"{candidate.ticker:15}"
                f"{candidate.quality_score:>12.1f}"
            )

        print()
        print("Discovery completed.")

        return candidates