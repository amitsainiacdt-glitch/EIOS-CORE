"""
EIOS
Everest Investment Operating System

Catalyst Development Queue Engine

Purpose:
    Converts Catalyst Coverage Priority records into a
    structured development queue.

Important:
    This engine does NOT create catalyst patterns.
    It only identifies which uncovered catalyst families
    are currently in the development queue.

Architecture:

    Catalyst Coverage
            ↓
    Coverage Priority Engine
            ↓
    Development Queue Engine
            ↓
    Catalyst Development Items

Design Principles:
    - Uses canonical CatalystFamily taxonomy.
    - Uses existing Coverage Priority Engine.
    - Does not invent catalyst families.
    - Does not modify the catalyst registry.
    - Does not generate patterns.
    - Does not perform valuation.
    - Does not make investment decisions.
"""


from typing import List

from modules.opportunity.catalyst.catalyst_coverage_priority_engine import (
    CatalystCoveragePriorityEngine,
)

from modules.opportunity.catalyst.catalyst_development_queue import (
    CatalystDevelopmentItem,
)


class CatalystDevelopmentQueueEngine:
    """
    Builds the catalyst-pattern development queue.
    """

    @staticmethod
    def build_queue() -> List[CatalystDevelopmentItem]:
        """
        Convert the existing coverage-priority queue into
        development items.
        """

        priority_queue = (
            CatalystCoveragePriorityEngine.build_queue()
        )

        return [
            CatalystDevelopmentItem(
                family=item.family,
                priority=item.priority,
                rationale=item.rationale,
            )
            for item in priority_queue
        ]

    @staticmethod
    def count() -> int:
        """
        Return the number of catalyst families currently
        requiring pattern development.
        """

        return len(
            CatalystDevelopmentQueueEngine.build_queue()
        )


__all__ = [
    "CatalystDevelopmentQueueEngine",
]