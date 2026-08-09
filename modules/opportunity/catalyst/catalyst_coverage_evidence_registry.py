"""
EIOS
Everest Investment Operating System

Catalyst Coverage Evidence Registry

Purpose:
    Stores canonical evidence profiles used to determine
    catalyst-pattern development priority.

Architecture:

    CatalystFamily
          ↓
    Evidence Registry
          ↓
    CatalystCoverageEvidence
          ↓
    Coverage Priority Engine

Design Principles:
    - One canonical profile per CatalystFamily.
    - Passive registry only.
    - No company-specific logic.
    - No investment decision.
    - No valuation.
    - No ranking of companies.
    - Unprofiled families remain neutral.
    - Evidence must be explicit and auditable.
"""

from typing import Dict

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CatalystCoverageEvidence,
)


# ==========================================================
# CANONICAL EVIDENCE REGISTRY
# ==========================================================

COVERAGE_EVIDENCE_PROFILES: Dict[
    CatalystFamily,
    CatalystCoverageEvidence,
] = {}


# ==========================================================
# REGISTRATION
# ==========================================================


def _register(
    family: CatalystFamily,
    evidence: CatalystCoverageEvidence,
) -> None:
    """
    Register one canonical evidence profile.

    Duplicate family registration is rejected.
    """

    if family in COVERAGE_EVIDENCE_PROFILES:
        raise ValueError(
            "Duplicate catalyst coverage evidence profile: "
            f"{family.name}"
        )

    COVERAGE_EVIDENCE_PROFILES[
        family
    ] = evidence


# ==========================================================
# INITIAL EVIDENCE PROFILES
# ==========================================================

_register(
    CatalystFamily.REVENUE_GROWTH,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=4,
        cross_sector_applicability=5,
        observability=5,
        persistence=4,
        evidence_availability=5,
        second_order_potential=5,
        market_mispricing_potential=5,
    ),
)


_register(
    CatalystFamily.VOLUME_GROWTH,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=4,
        cross_sector_applicability=4,
        observability=5,
        persistence=4,
        evidence_availability=5,
        second_order_potential=4,
        market_mispricing_potential=4,
    ),
)


_register(
    CatalystFamily.PRICING,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=5,
        cross_sector_applicability=5,
        observability=4,
        persistence=4,
        evidence_availability=4,
        second_order_potential=5,
        market_mispricing_potential=5,
    ),
)


_register(
    CatalystFamily.MARGIN_EXPANSION,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=4,
        cross_sector_applicability=5,
        observability=4,
        persistence=4,
        evidence_availability=5,
        second_order_potential=5,
        market_mispricing_potential=5,
    ),
)


_register(
    CatalystFamily.TECHNOLOGY_ADOPTION,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=5,
        cross_sector_applicability=4,
        observability=3,
        persistence=5,
        evidence_availability=3,
        second_order_potential=5,
        market_mispricing_potential=5,
    ),
)


_register(
    CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
    CatalystCoverageEvidence(
        earnings_impact=5,
        detection_lead_time=5,
        cross_sector_applicability=5,
        observability=4,
        persistence=4,
        evidence_availability=4,
        second_order_potential=5,
        market_mispricing_potential=5,
    ),
)


# ==========================================================
# REGISTRY ACCESS
# ==========================================================


class CatalystCoverageEvidenceRegistry:
    """
    Canonical read-only access to coverage evidence profiles.
    """

    @staticmethod
    def get(
        family: CatalystFamily,
    ) -> CatalystCoverageEvidence:
        """
        Return the evidence profile for a family.

        Unprofiled families deliberately receive a neutral
        evidence profile.
        """

        return COVERAGE_EVIDENCE_PROFILES.get(
            family,
            CatalystCoverageEvidence(),
        )

    @staticmethod
    def has_profile(
        family: CatalystFamily,
    ) -> bool:
        """
        Return True when a family has an explicit profile.
        """

        return (
            family
            in COVERAGE_EVIDENCE_PROFILES
        )

    @staticmethod
    def count() -> int:
        """
        Return the number of explicitly profiled families.
        """

        return len(
            COVERAGE_EVIDENCE_PROFILES
        )

    @staticmethod
    def all() -> Dict[
        CatalystFamily,
        CatalystCoverageEvidence,
    ]:
        """
        Return a copy of the registry.
        """

        return dict(
            COVERAGE_EVIDENCE_PROFILES
        )


__all__ = [
    "COVERAGE_EVIDENCE_PROFILES",
    "CatalystCoverageEvidenceRegistry",
]