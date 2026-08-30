"""
EIOS
Everest Investment Operating System

External Observation Adapter
============================

Purpose
-------
Provides the controlled boundary between externally obtained
information and the existing EIOS Observation layer.

Architecture

External Information
        ↓
ExternalObservationAdapter
        ↓
ObservationEngine
        ↓
ObservationRegistry

Design Principles
-----------------
- Does not perform investment analysis.
- Does not create Signals.
- Does not create Evidence.
- Does not calculate valuation.
- Does not calculate opportunity scores.
- Does not modify existing Observation objects.
- Does not fetch from the internet.
- Accepts externally obtained information only.
- Uses the existing ObservationEngine.
- Keeps external ingestion isolated from downstream engines.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from urllib.parse import urlparse

from modules.observation.observation import (
    Observation,
    ObservationProvenance,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)
from modules.external_intelligence.observation_deduplication_service import (
    ObservationDeduplicationService,
)
from modules.external_intelligence.source_quality_service import (
    SourceQualityService,
)


class ExternalObservationAdapter:
    """
    Controlled boundary for converting externally obtained
    information into an EIOS Observation.

    Duplicate information may legitimately return None
    because ObservationEngine owns novelty protection.
    """

    def __init__(
        self,
        observation_engine: ObservationEngine | None = None,
    ) -> None:

        self.observation_engine = (
            observation_engine
            if observation_engine is not None
            else ObservationEngine()
        )

    # ======================================================
    # PUBLIC INGESTION
    # ======================================================

    def ingest(
        self,
        *,
        title: str,
        description: str,
        source: str,
        category: str,
        entity: str,
        confidence: float,
        cycle_id: str | None = None,
        job_id: str | None = None,
        research_intent: str | None = None,
        retrieved_at: datetime | None = None,
        published_at: datetime | None = None,
        filing_at: datetime | None = None,
        source_type: str | None = None,
        content_type: str | None = None,
        source_document_id: str | None = None,
        document_hash: str | None = None,
        extraction_method: str | None = None,
        public_fact_candidate_id: str | None = None,
        public_fact_event_type: str | None = None,
        public_fact_statement_posture: str | None = None,
        public_fact_proposal_id: str | None = None,
        public_fact_review_id: str | None = None,
    ) -> Observation | None:
        """
        Convert externally obtained information into an
        EIOS Observation.

        Returns:
            Observation
                when the information is new.

            None
                when ObservationEngine rejects the
                information as a duplicate.

        No analytical transformation is performed.
        """

        provenance = self._build_provenance(
            cycle_id=cycle_id,
            job_id=job_id,
            research_intent=research_intent,
            retrieved_at=retrieved_at,
            published_at=published_at,
            filing_at=filing_at,
            source=source,
            content_type=content_type or source_type,
            source_document_id=source_document_id,
            document_hash=document_hash,
            extraction_method=extraction_method,
            public_fact_candidate_id=public_fact_candidate_id,
            public_fact_event_type=public_fact_event_type,
            public_fact_statement_posture=public_fact_statement_posture,
            public_fact_proposal_id=public_fact_proposal_id,
            public_fact_review_id=public_fact_review_id,
            content=description,
        )

        duplicate = (
            ObservationDeduplicationService().find_within_cycle(
                self.observation_engine.registry.all(), provenance
            )
            if provenance is not None
            else None
        )
        if duplicate is not None:
            duplicate.provenance = ObservationDeduplicationService.merge_contributor(
                duplicate.provenance,
                job_id=job_id,
                research_intent=research_intent,
            )
            self.observation_engine.save()
            return None

        return self.observation_engine.observe(
            title=title,
            description=description,
            source=source,
            category=category,
            entity=entity,
            confidence=self._clamp_confidence(
                confidence
            ),
            provenance=provenance,
        )

    @staticmethod
    def _build_provenance(
        *,
        cycle_id,
        job_id,
        research_intent,
        retrieved_at,
        published_at,
        filing_at,
        source,
        content_type,
        source_document_id,
        document_hash,
        extraction_method,
        public_fact_candidate_id,
        public_fact_event_type,
        public_fact_statement_posture,
        public_fact_proposal_id,
        public_fact_review_id,
        content,
    ) -> ObservationProvenance | None:
        """Build deterministic lineage only when runtime context is supplied."""

        if all(
            value is None
            for value in (
                cycle_id,
                job_id,
                research_intent,
                retrieved_at,
                published_at,
                filing_at,
                content_type,
                source_document_id,
                document_hash,
                extraction_method,
                public_fact_candidate_id,
                public_fact_event_type,
                public_fact_statement_posture,
                public_fact_proposal_id,
                public_fact_review_id,
            )
        ):
            return None

        parsed = urlparse(source)
        classification = SourceQualityService().classify(source)
        canonical_url = ObservationDeduplicationService.canonicalize_url(source)
        normalized_document_hash = (
            ObservationDeduplicationService.normalize_document_hash(
                document_hash
            )
        )
        normalized_document_id = (
            source_document_id.strip()
            if isinstance(source_document_id, str) and source_document_id.strip()
            else None
        )
        normalized_extraction_method = (
            extraction_method.strip()
            if isinstance(extraction_method, str) and extraction_method.strip()
            else None
        )
        observation_fingerprint = ObservationDeduplicationService.fingerprint(
            source,
            content,
            source_document_id=normalized_document_id,
            document_hash=normalized_document_hash,
            source_domain=parsed.hostname,
        )
        return ObservationProvenance(
            cycle_id=cycle_id,
            job_id=job_id,
            research_intent=research_intent,
            retrieved_at=ExternalObservationAdapter._utc(retrieved_at),
            source_url=source,
            source_domain=parsed.hostname,
            source_type=classification.source_type,
            content_fingerprint=sha256(
                content.encode("utf-8")
            ).hexdigest(),
            content_type=content_type,
            source_quality_tier=classification.quality_tier,
            canonical_url=canonical_url,
            observation_fingerprint=observation_fingerprint,
            published_at=ExternalObservationAdapter._utc(published_at),
            filing_at=ExternalObservationAdapter._utc(filing_at),
            source_document_id=normalized_document_id,
            document_hash=normalized_document_hash,
            extraction_method=normalized_extraction_method,
            public_fact_candidate_id=ExternalObservationAdapter._optional_text(public_fact_candidate_id),
            public_fact_event_type=ExternalObservationAdapter._optional_text(public_fact_event_type),
            public_fact_statement_posture=ExternalObservationAdapter._optional_text(public_fact_statement_posture),
            public_fact_proposal_id=ExternalObservationAdapter._optional_text(public_fact_proposal_id),
            public_fact_review_id=ExternalObservationAdapter._optional_text(public_fact_review_id),
            contributing_job_ids=((job_id,) if job_id else ()),
            contributing_research_intents=((research_intent,) if research_intent else ()),
        )

    @staticmethod
    def _utc(value: datetime | None) -> datetime | None:
        """Normalize new runtime timestamps without changing legacy loads."""

        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _optional_text(value):
        return value.strip() if isinstance(value, str) and value.strip() else None

    # ======================================================
    # CONFIDENCE PROTECTION
    # ======================================================

    @staticmethod
    def _clamp_confidence(
        confidence: float,
    ) -> float:
        """
        Protect the Observation boundary from invalid
        confidence values.

        Confidence is constrained to 0–100.
        """

        try:
            value = float(confidence)

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

        return max(
            0.0,
            min(
                100.0,
                value,
            ),
        )


__all__ = [
    "ExternalObservationAdapter",
]
