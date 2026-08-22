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
        source_type: str | None = None,
        content_type: str | None = None,
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
            source=source,
            content_type=content_type or source_type,
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
        source,
        content_type,
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
                content_type,
            )
        ):
            return None

        parsed = urlparse(source)
        classification = SourceQualityService().classify(source)
        canonical_url = ObservationDeduplicationService.canonicalize_url(source)
        observation_fingerprint = ObservationDeduplicationService.fingerprint(source, content)
        aware_retrieved_at = retrieved_at
        if aware_retrieved_at is not None:
            if aware_retrieved_at.tzinfo is None:
                aware_retrieved_at = aware_retrieved_at.replace(tzinfo=timezone.utc)
            else:
                aware_retrieved_at = aware_retrieved_at.astimezone(timezone.utc)
        return ObservationProvenance(
            cycle_id=cycle_id,
            job_id=job_id,
            research_intent=research_intent,
            retrieved_at=aware_retrieved_at,
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
            contributing_job_ids=((job_id,) if job_id else ()),
            contributing_research_intents=((research_intent,) if research_intent else ()),
        )

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
