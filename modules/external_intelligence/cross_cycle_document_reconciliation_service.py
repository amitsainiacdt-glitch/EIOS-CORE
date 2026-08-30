"""Read-only reconciliation of strong document identity across cycles."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from modules.external_intelligence.cross_cycle_document_reconciliation_preview import (
    CrossCycleDocumentGroup,
    CrossCycleDocumentReconciliationPreview,
)
from modules.external_intelligence.observation_deduplication_service import ObservationDeduplicationService
from modules.observation.observation import Observation


class CrossCycleDocumentReconciliationService:
    """Find repeated strong document identities without mutating observations."""

    def preview(self, observations) -> CrossCycleDocumentReconciliationPreview:
        if not isinstance(observations, (list, tuple)):
            raise ValueError("observations must be a list or tuple")
        if any(not isinstance(item, Observation) for item in observations):
            raise ValueError("every item must be an Observation")

        buckets = {}
        strong_count = 0
        missing_count = 0
        for observation in observations:
            identity = self._identity(observation)
            if identity is None:
                missing_count += 1
                continue
            strong_count += 1
            buckets.setdefault(identity, []).append(observation)

        groups = []
        unmatched_count = 0
        for identity, members in sorted(buckets.items()):
            cycle_ids = tuple(sorted({
                item.provenance.cycle_id
                for item in members
                if item.provenance and item.provenance.cycle_id
            }))
            if len(cycle_ids) < 2:
                unmatched_count += len(members)
                continue
            groups.append(self._group(identity, members, cycle_ids))

        groups_tuple = tuple(groups)
        reconciled_count = sum(
            len(group.observation_fingerprints) for group in groups_tuple
        )
        warnings = []
        if missing_count:
            warnings.append(
                f"{missing_count} Observations have no strong document identity."
            )
        if unmatched_count:
            warnings.append(
                f"{unmatched_count} strong-identity Observations occur in only one cycle."
            )
        payload = {
            "total_observations": len(observations),
            "strong_identity_observations": strong_count,
            "reconciled_group_count": len(groups_tuple),
            "reconciled_observation_count": reconciled_count,
            "unmatched_strong_identity_count": unmatched_count,
            "missing_strong_identity_count": missing_count,
            "groups": [self.group_payload(group) for group in groups_tuple],
            "warnings": warnings,
        }
        fingerprint = hashlib.sha256(
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
        return CrossCycleDocumentReconciliationPreview(
            fingerprint,
            len(observations),
            strong_count,
            len(groups_tuple),
            reconciled_count,
            unmatched_count,
            missing_count,
            groups_tuple,
            tuple(warnings),
        )

    @staticmethod
    def _identity(observation):
        provenance = observation.provenance
        if provenance is None:
            return None
        document_hash = ObservationDeduplicationService.normalize_document_hash(
            provenance.document_hash
        )
        if document_hash:
            return "DOCUMENT_HASH", document_hash
        document_id = (provenance.source_document_id or "").strip()
        domain = (provenance.source_domain or "").strip().casefold().rstrip(".")
        if document_id and domain:
            return "SOURCE_DOCUMENT_ID", f"{domain}\n{document_id}"
        return None

    def _group(self, identity, members, cycle_ids):
        kind, value = identity
        ordered = sorted(
            members,
            key=lambda item: (
                item.provenance.cycle_id or "",
                item.provenance.source_url or "",
                item.provenance.observation_fingerprint or "",
            ),
        )
        first = ordered[0].provenance
        published = [self._utc(item.provenance.published_at) for item in ordered if item.provenance.published_at]
        filed = [self._utc(item.provenance.filing_at) for item in ordered if item.provenance.filing_at]
        retrieved = [self._utc(item.provenance.retrieved_at) for item in ordered if item.provenance.retrieved_at]
        observation_fingerprints = tuple(
            item.provenance.observation_fingerprint
            or hashlib.sha256(
                f"{item.entity}\n{item.timestamp.isoformat()}\n{item.source}".encode("utf-8")
            ).hexdigest()
            for item in ordered
        )
        return CrossCycleDocumentGroup(
            kind,
            hashlib.sha256(f"{kind}\n{value}".encode("utf-8")).hexdigest(),
            value if kind == "DOCUMENT_HASH" else None,
            first.source_domain if kind == "SOURCE_DOCUMENT_ID" else None,
            first.source_document_id if kind == "SOURCE_DOCUMENT_ID" else None,
            cycle_ids,
            observation_fingerprints,
            tuple(item.provenance.source_url or item.source for item in ordered),
            min(published) if published else None,
            min(filed) if filed else None,
            min(retrieved) if retrieved else None,
            max(retrieved) if retrieved else None,
        )

    @staticmethod
    def _utc(value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def group_payload(group):
        """Return one group as a stable JSON-compatible audit payload."""

        payload = {**group.__dict__}
        for key in ("cycle_ids", "observation_fingerprints", "source_urls"):
            payload[key] = list(payload[key])
        for key in (
            "earliest_published_at",
            "earliest_filing_at",
            "earliest_retrieved_at",
            "latest_retrieved_at",
        ):
            if payload[key] is not None:
                payload[key] = payload[key].isoformat()
        return payload


__all__ = ["CrossCycleDocumentReconciliationService"]
