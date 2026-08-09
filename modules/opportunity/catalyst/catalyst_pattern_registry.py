"""
EIOS
Everest Investment Operating System

Catalyst Pattern Registry

Purpose:
    Canonical registry assembling catalyst patterns from
    family-specific pattern modules.

Architecture:

    Catalyst Taxonomy
            ↓
    Family Pattern Modules
            ↓
    Catalyst Pattern Registry
            ↓
    Opportunity Engine

Design Principles:
    - Pattern definitions live in family modules.
    - Registry is the canonical access layer.
    - Duplicate IDs are rejected.
    - Registry performs no analysis.
    - Registry performs no scoring.
    - Registry performs no ranking.
    - Registry performs no valuation.
"""


from typing import Dict, List


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


from modules.opportunity.catalyst.patterns.capacity_patterns import (
    CAPACITY_PATTERNS,
)


from modules.opportunity.catalyst.patterns.order_patterns import (
    ORDER_PATTERNS,
)


from modules.opportunity.catalyst.patterns.regulatory_patterns import (
    REGULATORY_PATTERNS,
)


from modules.opportunity.catalyst.patterns.revenue_patterns import (
    REVENUE_PATTERNS,
)


# ==========================================================
# CANONICAL REGISTRY
# ==========================================================


CATALYST_PATTERNS: Dict[
    str,
    CatalystPattern,
] = {}


# ==========================================================
# REGISTRATION
# ==========================================================


def _register(
    patterns: List[CatalystPattern],
) -> None:
    """
    Register canonical catalyst patterns.

    Duplicate pattern IDs are rejected immediately.
    """

    for pattern in patterns:

        if pattern.pattern_id in CATALYST_PATTERNS:

            raise ValueError(
                "Duplicate catalyst pattern ID: "
                f"{pattern.pattern_id}"
            )

        CATALYST_PATTERNS[
            pattern.pattern_id
        ] = pattern


# ==========================================================
# FAMILY REGISTRATION
# ==========================================================


_register(
    CAPACITY_PATTERNS
)


_register(
    ORDER_PATTERNS
)


_register(
    REGULATORY_PATTERNS
)


_register(
    REVENUE_PATTERNS
)


# ==========================================================
# REGISTRY ACCESS
# ==========================================================


class CatalystPatternRegistry:
    """
    Canonical read-only access to catalyst patterns.
    """

    @staticmethod
    def all() -> List[CatalystPattern]:
        """
        Return all registered catalyst patterns.
        """

        return list(
            CATALYST_PATTERNS.values()
        )

    @staticmethod
    def get(
        pattern_id: str,
    ) -> CatalystPattern:
        """
        Return a catalyst pattern by canonical ID.
        """

        return CATALYST_PATTERNS[
            pattern_id
        ]

    @staticmethod
    def get_by_family(
        family: CatalystFamily,
    ) -> List[CatalystPattern]:
        """
        Return all patterns belonging to a family.
        """

        return [
            pattern
            for pattern in CATALYST_PATTERNS.values()
            if pattern.family == family
        ]

    @staticmethod
    def count() -> int:
        """
        Return total registered pattern count.
        """

        return len(
            CATALYST_PATTERNS
        )


__all__ = [
    "CATALYST_PATTERNS",
    "CatalystPatternRegistry",
]