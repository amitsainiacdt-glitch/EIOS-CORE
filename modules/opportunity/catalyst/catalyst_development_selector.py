"""
EIOS
Everest Investment Operating System

Catalyst Development Selector

Purpose:
    Selects the next catalyst family for pattern development
    from the existing Catalyst Development Queue.

Important:
    This selector determines DEVELOPMENT ORDER only.

    It does NOT:
        - rank companies
        - rank investments
        - perform valuation
        - make investment decisions
        - generate catalyst patterns

Selection principle:

    Higher development priority first.

    Within the same priority:
        deterministic CatalystFamily enum order.
"""

from typing import Optional

from modules.opportunity.catalyst.catalyst_development_queue import (
    CatalystDevelopmentItem,
)

from modules.opportunity.catalyst.catalyst_development_queue_engine import (
    CatalystDevelopmentQueueEngine,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CoveragePriority,
)


# ==========================================================
# PRIORITY ORDER
# ==========================================================


_PRIORITY_RANK = {
    CoveragePriority.CRITICAL: 0,
    CoveragePriority.HIGH: 1,
    CoveragePriority.MEDIUM: 2,
    CoveragePriority.LOW: 3,
}


# ==========================================================
# SELECTOR
# ==========================================================


class CatalystDevelopmentSelector:
    """
    Selects the next catalyst development item.
    """

    @staticmethod
    def select_next() -> Optional[
        CatalystDevelopmentItem
    ]:
        """
        Return the highest-priority development item.

        Ties are resolved deterministically using the
        canonical CatalystFamily enum order.
        """

        queue = (
            CatalystDevelopmentQueueEngine.build_queue()
        )

        if not queue:
            return None

        return min(
            queue,
            key=lambda item: (
                _PRIORITY_RANK[item.priority],
                list(type(item.family)).index(
                    item.family
                ),
            ),
        )


__all__ = [
    "CatalystDevelopmentSelector",
]