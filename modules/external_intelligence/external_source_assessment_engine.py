"""
EIOS
Everest Investment Operating System

External Source Assessment Engine
=================================

Validates and constructs explicit source-assessment metadata.

This engine performs NO analytical scoring.
"""

from urllib.parse import urlparse

from modules.external_intelligence.external_content_normalizer import (
    NormalizedExternalContent,
)

from modules.external_intelligence.external_source_assessment import (
    ExternalSourceAssessment,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)

from modules.external_intelligence.source_selection import (
    SelectedSource,
)


class ExternalSourceAssessmentEngine:
    """
    Constructs validated ExternalSourceAssessment objects.

    This engine performs deterministic metadata extraction
    and validation only.

    No credibility score.
    No evidence score.
    No confidence calculation.
    No investment analysis.
    """

    def assess(
        self,
        *,
        selected_source: SelectedSource,
        retrieved_content: RetrievedContent,
        normalized_content: NormalizedExternalContent,
        source_type: str = "",
        is_primary_source: bool = False,
        publication_date: str = "",
        notes: str = "",
    ) -> ExternalSourceAssessment:
        """
        Assess explicit metadata associated with one
        successfully retrieved external source.
        """

        if selected_source is None:
            raise ValueError(
                "selected_source must not be None"
            )

        if not isinstance(
            selected_source,
            SelectedSource,
        ):
            raise ValueError(
                "selected_source must be SelectedSource"
            )

        if retrieved_content is None:
            raise ValueError(
                "retrieved_content must not be None"
            )

        if not isinstance(
            retrieved_content,
            RetrievedContent,
        ):
            raise ValueError(
                "retrieved_content must be RetrievedContent"
            )

        if normalized_content is None:
            raise ValueError(
                "normalized_content must not be None"
            )

        if not isinstance(
            normalized_content,
            NormalizedExternalContent,
        ):
            raise ValueError(
                "normalized_content must be "
                "NormalizedExternalContent"
            )

        if not isinstance(
            source_type,
            str,
        ):
            raise ValueError(
                "source_type must be a string"
            )

        if not isinstance(
            is_primary_source,
            bool,
        ):
            raise ValueError(
                "is_primary_source must be a boolean"
            )

        if not isinstance(
            publication_date,
            str,
        ):
            raise ValueError(
                "publication_date must be a string"
            )

        if not isinstance(
            notes,
            str,
        ):
            raise ValueError(
                "notes must be a string"
            )

        source_url = (
            selected_source.result.url
        )

        if not isinstance(
            source_url,
            str,
        ) or not source_url:

            raise ValueError(
                "selected source URL must not be empty"
            )

        if (
            retrieved_content.url
            != source_url
        ):

            raise ValueError(
                "retrieved content URL must match "
                "selected source URL"
            )

        if (
            normalized_content.url
            != source_url
        ):

            raise ValueError(
                "normalized content URL must match "
                "selected source URL"
            )

        domain = (
            urlparse(
                source_url
            ).netloc
        )

        if not domain:
            raise ValueError(
                "source URL must contain a domain"
            )

        publisher = (
            selected_source.result.source
        )

        provenance_complete = bool(
            source_url
            and domain
            and publisher
            and retrieved_content.url
            and normalized_content.url
        )

        return ExternalSourceAssessment(
            source_url=source_url,

            domain=domain,

            publisher=publisher,

            source_type=source_type,

            is_primary_source=is_primary_source,

            publication_date=publication_date,

            provenance_complete=(
                provenance_complete
            ),

            notes=notes,
        )


__all__ = [
    "ExternalSourceAssessmentEngine",
]