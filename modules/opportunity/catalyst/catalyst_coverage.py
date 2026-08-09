"""
EIOS
Everest Investment Operating System

Catalyst Coverage Analyzer

Purpose:
    Measures coverage of the canonical Catalyst Taxonomy
    by the currently registered Catalyst Pattern Registry.

Design Principles:
    - Uses the canonical CatalystFamily taxonomy.
    - Uses the canonical CatalystPatternRegistry.
    - Performs no catalyst scoring.
    - Performs no catalyst ranking.
    - Performs no investment decision.
    - Does not invent catalyst patterns.
    - Reports coverage only.
"""

from dataclasses import dataclass
from typing import List

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_pattern_registry import (
    CatalystPatternRegistry,
)


# ==========================================================
# COVERAGE RECORD
# ==========================================================


@dataclass(frozen=True)
class CatalystCoverage:
    """
    Immutable coverage record for one catalyst family.
    """

    family: CatalystFamily

    pattern_count: int

    covered: bool


# ==========================================================
# COVERAGE ANALYZER
# ==========================================================


class CatalystCoverageAnalyzer:
    """
    Measures pattern coverage across the canonical
    CatalystFamily taxonomy.
    """

    @staticmethod
    def analyze() -> List[CatalystCoverage]:
        """
        Return coverage information for every canonical
        catalyst family.
        """

        coverage: List[CatalystCoverage] = []

        for family in CatalystFamily:

            patterns = (
                CatalystPatternRegistry.get_by_family(
                    family
                )
            )

            coverage.append(
                CatalystCoverage(
                    family=family,
                    pattern_count=len(patterns),
                    covered=len(patterns) > 0,
                )
            )

        return coverage

    @staticmethod
    def covered_families() -> List[CatalystCoverage]:
        """
        Return families having at least one registered pattern.
        """

        return [
            item
            for item in CatalystCoverageAnalyzer.analyze()
            if item.covered
        ]

    @staticmethod
    def uncovered_families() -> List[CatalystCoverage]:
        """
        Return canonical families having no registered patterns.
        """

        return [
            item
            for item in CatalystCoverageAnalyzer.analyze()
            if not item.covered
        ]

    @staticmethod
    def family_count() -> int:
        """
        Return the number of canonical catalyst families.
        """

        return len(
            list(CatalystFamily)
        )

    @staticmethod
    def covered_count() -> int:
        """
        Return the number of covered catalyst families.
        """

        return len(
            CatalystCoverageAnalyzer.covered_families()
        )

    @staticmethod
    def uncovered_count() -> int:
        """
        Return the number of uncovered catalyst families.
        """

        return len(
            CatalystCoverageAnalyzer.uncovered_families()
        )


__all__ = [
    "CatalystCoverage",
    "CatalystCoverageAnalyzer",
]