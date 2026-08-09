"""
EIOS
Everest Investment Operating System

Catalyst Development Queue

Purpose:
    Defines the passive data model used to represent
    catalyst-pattern development work.

Important:
    This model does NOT decide priority.
    Priority is produced by the Catalyst Coverage
    Priority Engine.

Architecture:

    Catalyst Family
          ↓
    Coverage Analysis
          ↓
    Evidence Profile
          ↓
    Priority Engine
          ↓
    Development Queue

Design Principles:
    - Passive data model.
    - Immutable records.
    - No company-specific logic.
    - No valuation.
    - No investment decision.
    - No pattern-generation logic.
"""


from dataclasses import dataclass

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage_priority import (
    CoveragePriority,
)


# ==========================================================
# DEVELOPMENT QUEUE RECORD
# ==========================================================


@dataclass(frozen=True)
class CatalystDevelopmentItem:
    """
    Immutable representation of one catalyst-family
    development item.
    """

    family: CatalystFamily

    priority: CoveragePriority

    rationale: str


__all__ = [
    "CatalystDevelopmentItem",
]