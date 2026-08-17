"""
EIOS
Everest Investment Operating System

External Source Assessment
===========================

Passive metadata describing an externally retrieved source.

This model performs NO analytical calculation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalSourceAssessment:
    """
    Immutable metadata describing an external source.
    """

    source_url: str = ""

    domain: str = ""

    publisher: str = ""

    source_type: str = ""

    is_primary_source: bool = False

    publication_date: str = ""

    provenance_complete: bool = False

    notes: str = ""


__all__ = [
    "ExternalSourceAssessment",
]