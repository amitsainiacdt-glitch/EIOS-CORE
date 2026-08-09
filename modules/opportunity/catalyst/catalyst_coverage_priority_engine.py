"""
EIOS
Everest Investment Operating System

Catalyst Coverage Priority Engine

Purpose:
    Converts canonical Catalyst Coverage Evidence into a
    structured development-priority queue.

Important:
    This engine prioritizes PATTERN DEVELOPMENT.
    It does NOT rank companies or investment opportunities.

Design Principles:
    - Uses the canonical CatalystFamily taxonomy.
    - Uses CatalystCoverageAnalyzer.
    - Uses CatalystCoverageEvidenceRegistry.
    - Does not invent catalyst families.
    - Does not modify the pattern registry.
    - Does not perform valuation.
    - Does not make investment decisions.
"""

from typing import List

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage import (
    CatalystCoverageAnalyzer,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CatalystCoveragePriority,
    CatalystCoverageEvidence,
    CoveragePriority,
)

from modules.opportunity.catalyst.catalyst_coverage_evidence_registry import (
    CatalystCoverageEvidenceRegistry,
)


class CatalystCoveragePriorityEngine:
    """
    Determines development priority for uncovered
    Catalyst Families.
    """

    @staticmethod
    def _default_evidence() -> CatalystCoverageEvidence:
        """
        Return a neutral evidence profile.

        Used automatically for families that do not yet
        have an explicit evidence profile.
        """

        return CatalystCoverageEvidence()

    @staticmethod
    def _priority_from_evidence(
        evidence: CatalystCoverageEvidence,
    ) -> CoveragePriority:
        """
        Convert an evidence profile into development priority.

        Total possible score:
            0 to 40

        Thresholds:

            0–11   → LOW
            12–23  → MEDIUM
            24–31  → HIGH
            32–40  → CRITICAL
        """

        values = [
            evidence.earnings_impact,
            evidence.detection_lead_time,
            evidence.cross_sector_applicability,
            evidence.observability,
            evidence.persistence,
            evidence.evidence_availability,
            evidence.second_order_potential,
            evidence.market_mispricing_potential,
        ]

        total = sum(values)

        if total >= 32:
            return CoveragePriority.CRITICAL

        if total >= 24:
            return CoveragePriority.HIGH

        if total >= 12:
            return CoveragePriority.MEDIUM

        return CoveragePriority.LOW

    @staticmethod
    def build_queue() -> List[CatalystCoveragePriority]:
        """
        Build a development queue containing only
        currently uncovered Catalyst Families.

        Explicit evidence profiles are retrieved from the
        canonical Evidence Registry.

        Unprofiled families remain neutral.
        """

        queue: List[
            CatalystCoveragePriority
        ] = []

        coverage = (
            CatalystCoverageAnalyzer.analyze()
        )

        for item in coverage:

            if item.covered:
                continue

            evidence = (
                CatalystCoverageEvidenceRegistry.get(
                    item.family
                )
            )

            priority = (
                CatalystCoveragePriorityEngine
                ._priority_from_evidence(
                    evidence
                )
            )

            if (
                CatalystCoverageEvidenceRegistry
                .has_profile(item.family)
            ):
                rationale = (
                    "Family is currently uncovered. "
                    "Priority is derived from its "
                    "canonical evidence profile."
                )

            else:
                evidence = (
                    CatalystCoveragePriorityEngine
                    ._default_evidence()
                )

                priority = (
                    CatalystCoveragePriorityEngine
                    ._priority_from_evidence(
                        evidence
                    )
                )

                rationale = (
                    "Family is currently uncovered. "
                    "No explicit evidence profile exists; "
                    "priority remains neutral."
                )

            queue.append(
                CatalystCoveragePriority(
                    family=item.family,
                    priority=priority,
                    rationale=rationale,
                    evidence=evidence,
                )
            )

        return queue

    @staticmethod
    def uncovered_count() -> int:
        """
        Return the number of families in the
        development queue.
        """

        return len(
            CatalystCoveragePriorityEngine.build_queue()
        )

    @staticmethod
    def contains(
        family: CatalystFamily,
    ) -> bool:
        """
        Determine whether a family requires
        pattern development.
        """

        return any(
            item.family == family
            for item
            in CatalystCoveragePriorityEngine.build_queue()
        )


__all__ = [
    "CatalystCoveragePriorityEngine",
]