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
    def fingerprint(
        cls,
        url: str,
        content: str,
        *,
        source_document_id: str | None = None,
        document_hash: str | None = None,
        source_domain: str | None = None,
    ) -> str:
        """Build identity using supplied document evidence when available."""

        normalized_hash = cls.normalize_document_hash(document_hash)
        if normalized_hash is not None:
            identity = f"document-hash\n{normalized_hash}"
            return sha256(identity.encode("utf-8")).hexdigest()

        normalized_document_id = (source_document_id or "").strip()
        if normalized_document_id:
            domain = (source_domain or urlsplit(url).hostname or "").lower().rstrip(".")
            identity = f"source-document-id\n{domain}\n{normalized_document_id}"
            return sha256(identity.encode("utf-8")).hexdigest()

        normalized_content = " ".join((content or "").split())
        identity = f"{cls.canonicalize_url(url)}\n{normalized_content}"
        return sha256(identity.encode("utf-8")).hexdigest()

    @staticmethod
    def normalize_document_hash(value: str | None) -> str | None:
        """Validate an optional caller-supplied SHA-256 document identity."""

        if value is None:
            return None
        normalized = value.strip().casefold()
        if not normalized:
            return None
        if len(normalized) != 64:
            raise ValueError("document_hash must be a SHA-256 hexadecimal digest")
        try:
            int(normalized, 16)
        except ValueError as exc:
            raise ValueError(
                "document_hash must be a SHA-256 hexadecimal digest"
            ) from exc
        return normalized

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
