"""
EIOS
Everest Investment Operating System

External Source Assessment Engine
=================================

Validates and constructs explicit source-assessment metadata.

This engine performs NO analytical scoring.
"""

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)


class ExternalSourceAssessmentEngine:
    """
    Constructs validated ExternalSourceAssessment objects.

    No credibility score.
    No evidence score.
    No confidence calculation.
    No investment analysis.
    """

    def assess(
        self,
        *,
        source_url: str = "",
        domain: str = "",
        publisher: str = "",
        source_type: str = "",
        is_primary_source: bool = False,
        publication_date: str = "",
        provenance_complete: bool = False,
        notes: str = "",
    ) -> ExternalSourceAssessment:

        if not isinstance(source_url, str):
            raise ValueError(
                "source_url must be a string"
            )

        if not isinstance(domain, str):
            raise ValueError(
                "domain must be a string"
            )

        if not isinstance(publisher, str):
            raise ValueError(
                "publisher must be a string"
            )

        if not isinstance(source_type, str):
            raise ValueError(
                "source_type must be a string"
            )

        if not isinstance(is_primary_source, bool):
            raise ValueError(
                "is_primary_source must be a boolean"
            )

        if not isinstance(publication_date, str):
            raise ValueError(
                "publication_date must be a string"
            )

        if not isinstance(provenance_complete, bool):
            raise ValueError(
                "provenance_complete must be a boolean"
            )

        if not isinstance(notes, str):
            raise ValueError(
                "notes must be a string"
            )

        return ExternalSourceAssessment(
            source_url=source_url,
            domain=domain,
            publisher=publisher,
            source_type=source_type,
            is_primary_source=is_primary_source,
            publication_date=publication_date,
            provenance_complete=provenance_complete,
            notes=notes,
        )


__all__ = [
    "ExternalSourceAssessmentEngine",
]