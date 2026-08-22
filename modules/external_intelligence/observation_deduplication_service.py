"""Canonical identity and cycle-scoped observation deduplication policy."""

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from modules.observation.observation import Observation, ObservationProvenance


class ObservationDeduplicationService:
    """Build stable identities and merge lineage only inside one cycle."""

    _TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}

    @classmethod
    def canonicalize_url(cls, url: str) -> str:
        parts = urlsplit((url or "").strip())
        scheme = parts.scheme.lower()
        host = (parts.hostname or "").lower().rstrip(".")
        port = parts.port
        if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
            host = f"{host}:{port}"
        path = parts.path or "/"
        if path != "/":
            path = path.rstrip("/") or "/"
        query = sorted(
            (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in cls._TRACKING_KEYS and not key.lower().startswith("utm_")
        )
        return urlunsplit((scheme, host, path, urlencode(query, doseq=True), ""))

    @classmethod
    def fingerprint(cls, url: str, content: str) -> str:
        normalized_content = " ".join((content or "").split())
        identity = f"{cls.canonicalize_url(url)}\n{normalized_content}"
        return sha256(identity.encode("utf-8")).hexdigest()

    @staticmethod
    def merge_contributor(provenance: ObservationProvenance, *, job_id: str | None, research_intent: str | None) -> ObservationProvenance:
        jobs = list(provenance.contributing_job_ids)
        intents = list(provenance.contributing_research_intents)
        for value, collection in ((job_id, jobs), (research_intent, intents)):
            if value and value not in collection:
                collection.append(value)
        return replace(
            provenance,
            contributing_job_ids=tuple(jobs),
            contributing_research_intents=tuple(intents),
        )

    def find_within_cycle(self, observations: list[Observation], provenance: ObservationProvenance) -> Observation | None:
        if not provenance.cycle_id or not provenance.observation_fingerprint:
            return None
        for observation in observations:
            existing = observation.provenance
            if existing and existing.cycle_id == provenance.cycle_id and existing.observation_fingerprint == provenance.observation_fingerprint:
                return observation
        return None


__all__ = ["ObservationDeduplicationService"]
