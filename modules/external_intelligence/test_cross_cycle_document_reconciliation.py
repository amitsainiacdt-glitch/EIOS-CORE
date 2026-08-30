"""Offline tests for read-only cross-cycle document reconciliation."""

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.cross_cycle_document_reconciliation_service import CrossCycleDocumentReconciliationService
from modules.external_intelligence.external_observation_adapter import ExternalObservationAdapter
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence


def main():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "observations.json"
        engine = ObservationEngine(persistence=ObservationPersistence(path))
        adapter = ExternalObservationAdapter(engine)
        document_hash = sha256(b"one exchange document").hexdigest()
        common = dict(category="External Web", entity="Issuer", confidence=80)

        adapter.ingest(title="Hash cycle one", description="First extraction", source="https://nseindia.com/a.pdf", cycle_id="cycle-1", document_hash=document_hash, retrieved_at=datetime(2026, 8, 1, tzinfo=timezone.utc), **common)
        adapter.ingest(title="Hash cycle two", description="Second extraction", source="https://issuer.example/a.pdf", cycle_id="cycle-2", document_hash=document_hash, retrieved_at=datetime(2026, 8, 2, tzinfo=timezone.utc), **common)
        adapter.ingest(title="ID cycle one", description="Announcement text", source="https://exchange.example.com/a", cycle_id="cycle-1", source_document_id="ANN-7", published_at=datetime(2026, 8, 1), **common)
        adapter.ingest(title="ID cycle three", description="Changed extraction", source="https://exchange.example.com/b", cycle_id="cycle-3", source_document_id="ANN-7", **common)
        adapter.ingest(title="Unmatched strong", description="Only once", source="https://exchange.example.com/c", cycle_id="cycle-1", source_document_id="ANN-8", **common)
        adapter.ingest(title="Legacy identity", description="URL content only", source="https://news.example.com/story", cycle_id="cycle-1", **common)

        observations = engine.registry.all()
        original = deepcopy(observations)
        before = path.read_bytes()
        service = CrossCycleDocumentReconciliationService()
        preview = service.preview(observations)

        assert preview.total_observations == 6
        assert preview.strong_identity_observations == 5
        assert preview.reconciled_group_count == 2
        assert preview.reconciled_observation_count == 4
        assert preview.unmatched_strong_identity_count == 1
        assert preview.missing_strong_identity_count == 1
        assert {group.identity_kind for group in preview.groups} == {"DOCUMENT_HASH", "SOURCE_DOCUMENT_ID"}
        assert all(len(group.cycle_ids) == 2 for group in preview.groups)
        assert observations == original
        assert path.read_bytes() == before

        reversed_preview = service.preview(list(reversed(observations)))
        assert reversed_preview.preview_fingerprint == preview.preview_fingerprint

        try:
            service.preview([object()])
        except ValueError as exc:
            assert "Observation" in str(exc)
        else:
            raise AssertionError("invalid input accepted")

    print("CROSS-CYCLE DOCUMENT RECONCILIATION: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
