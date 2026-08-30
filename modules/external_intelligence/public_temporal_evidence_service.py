"""Builds and orders Temporal Evidence without interpreting economic direction."""

from __future__ import annotations

from datetime import timezone
from hashlib import sha256

from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord, PublicTemporalEvidenceSeries
from modules.observation.observation import Observation


class PublicTemporalEvidenceService:
    def record_from_observation(self, observation):
        if not isinstance(observation, Observation):
            raise ValueError("observation must be an Observation")
        provenance = observation.provenance
        required = {
            "observation_fingerprint": getattr(provenance, "observation_fingerprint", None),
            "source_url": getattr(provenance, "source_url", None),
            "document_hash": getattr(provenance, "document_hash", None),
            "candidate_id": getattr(provenance, "public_fact_candidate_id", None),
            "event_type": getattr(provenance, "public_fact_event_type", None),
            "statement_posture": getattr(provenance, "public_fact_statement_posture", None),
            "proposal_id": getattr(provenance, "public_fact_proposal_id", None),
            "review_id": getattr(provenance, "public_fact_review_id", None),
        }
        missing = tuple(name for name, value in required.items() if not isinstance(value, str) or not value.strip())
        if missing:
            raise ValueError("reviewed factual Observation provenance is incomplete: " + ", ".join(missing))
        known_at = self._utc(provenance.retrieved_at or observation.timestamp)
        if provenance.filing_at is not None:
            event_at, basis = self._utc(provenance.filing_at), "FILING_AT"
        elif provenance.published_at is not None:
            event_at, basis = self._utc(provenance.published_at), "PUBLISHED_AT"
        else:
            event_at, basis = known_at, "KNOWN_AT_FALLBACK"
        identity = f"{required['observation_fingerprint']}\n{event_at.isoformat()}\n{required['event_type']}"
        return PublicTemporalEvidenceRecord(
            1, sha256(identity.encode("utf-8")).hexdigest(), required["observation_fingerprint"],
            observation.entity, required["event_type"], required["statement_posture"], event_at,
            known_at, basis, required["source_url"], required["document_hash"], required["candidate_id"],
            required["proposal_id"], required["review_id"], observation.title, observation.description,
        )

    def build_series(self, records):
        records = tuple(records)
        if not records or not all(isinstance(item, PublicTemporalEvidenceRecord) for item in records):
            raise ValueError("records must contain Temporal Evidence records")
        entities = {item.entity for item in records}; event_types = {item.event_type for item in records}
        if len(entities) != 1 or len(event_types) != 1:
            raise ValueError("one series must contain exactly one entity and event type")
        ordered = tuple(sorted(records, key=lambda item: (item.event_at, item.known_at, item.temporal_evidence_id)))
        if len({item.observation_fingerprint for item in ordered}) != len(ordered):
            raise ValueError("series contains duplicate Observation evidence")
        postures = [item.statement_posture for item in ordered]
        warnings = []
        if any(item.time_basis == "KNOWN_AT_FALLBACK" for item in ordered):
            warnings.append("One or more records lack publication/filing time and use known-at time.")
        if any(item.event_at > item.known_at for item in ordered):
            warnings.append("One or more source event times occur after EIOS known-at time and require review.")
        return PublicTemporalEvidenceSeries(
            ordered[0].entity, ordered[0].event_type, len(ordered), postures.count("ASSERTED"),
            postures.count("NEGATED"), postures.count("UNCERTAIN"), ordered[0].event_at,
            ordered[-1].event_at, ordered, tuple(warnings),
        )

    @staticmethod
    def _utc(value):
        if value.tzinfo is None: return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


__all__ = ["PublicTemporalEvidenceService"]
