"""
EIOS
Everest Investment Operating System

External Evidence Assessment
=============================

Represents explicit assessment metadata required to convert
an Observation into an Opportunity EvidenceItem.

This model performs NO analytical calculation.

It does NOT:
- calculate evidence score
- calculate confidence
- calculate opportunity score
- determine valuation
- create Signals
- create Catalysts
- make investment decisions

Those responsibilities remain with downstream engines.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceAssessment:
    """
    Explicit assessment supplied for one Observation.

    These values must come from an actual assessment process.
    They are never fabricated by the HTTP retriever.
    """

    category: str = ""

    direction: str = "Supporting"

    strength: float = 0.0

    confidence: float = 0.0

    independent_confirmation: int = 0

    is_primary_source: bool = False

    is_time_sensitive: bool = False

    notes: str = ""


__all__ = [
    "EvidenceAssessment",
]