"""Offline tests for semantic source quality and within-cycle deduplication."""

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.external_observation_adapter import ExternalObservationAdapter
from modules.external_intelligence.observation_deduplication_service import ObservationDeduplicationService
from modules.external_intelligence.source_quality_service import SourceQualityService
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence


def test_semantic_source_classification_and_mime_are_separate():
    classification = SourceQualityService().classify("https://www.sec.gov/filing")
    assert classification.source_type == "REGULATORY"
    assert classification.quality_tier == "TIER_1"

    with TemporaryDirectory() as directory:
        adapter = ExternalObservationAdapter(
            ObservationEngine(persistence=ObservationPersistence(Path(directory) / "observations.json"))
        )
        observation = adapter.ingest(
            title="Filing", description="Issuer filing content", source="https://SEC.gov/filing",
            category="External Web", entity="Issuer", confidence=80,
            cycle_id="cycle-1", job_id="job-1", research_intent="RESULTS",
            retrieved_at=datetime(2026, 8, 22, 10), content_type="application/pdf",
        )
        assert observation.provenance.source_type == "REGULATORY"
        assert observation.provenance.source_quality_tier == "TIER_1"
        assert observation.provenance.content_type == "application/pdf"
        assert observation.timestamp.tzinfo is timezone.utc
        assert observation.provenance.retrieved_at.tzinfo is timezone.utc


def test_canonical_url_fingerprint_and_cross_job_lineage_merge():
    canonicalizer = ObservationDeduplicationService
    first_url = "HTTPS://Example.COM:443/report/?b=2&utm_source=x&a=1#section"
    second_url = "https://example.com/report?a=1&b=2"
    assert canonicalizer.canonicalize_url(first_url) == second_url
    assert canonicalizer.fingerprint(first_url, "same   content") == canonicalizer.fingerprint(second_url, "same content")

    with TemporaryDirectory() as directory:
        path = Path(directory) / "observations.json"
        engine = ObservationEngine(persistence=ObservationPersistence(path))
        adapter = ExternalObservationAdapter(engine)
        common = dict(title="Report", description="same content", category="External Web", entity="Issuer", confidence=70, cycle_id="cycle-1")
        first = adapter.ingest(source=first_url, job_id="job-a", research_intent="DEMAND", **common)
        duplicate = adapter.ingest(source=second_url, job_id="job-b", research_intent="RESULTS", **common)
        assert first is not None
        assert duplicate is None
        assert engine.registry.count() == 1
        lineage = engine.registry.all()[0].provenance
        assert lineage.contributing_job_ids == ("job-a", "job-b")
        assert lineage.contributing_research_intents == ("DEMAND", "RESULTS")
        loaded = ObservationPersistence(path).load()[0].provenance
        assert loaded.contributing_job_ids == lineage.contributing_job_ids

        # Identical material in another cycle is outside this service's scope.
        later = adapter.ingest(source=second_url, job_id="job-c", research_intent="RESULTS", cycle_id="cycle-2", **{k: v for k, v in common.items() if k != "cycle_id"})
        # Cycle scoping does not treat a later cycle as this service's duplicate.
        assert later is not None
        assert engine.registry.count() == 2


def test_legacy_timestamp_and_provenance_loading():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "legacy.json"
        path.write_text(json.dumps([{
            "title": "Legacy", "description": "Legacy", "source": "Archive",
            "category": "External Web", "entity": "Issuer", "confidence": 50,
            "timestamp": "2025-01-01T00:00:00",
            "provenance": {"source_type": "text/html", "retrieved_at": "2025-01-01T01:00:00"},
        }]), encoding="utf-8")
        observation = ObservationPersistence(path).load()[0]
        assert observation.timestamp == datetime(2025, 1, 1, 0, 0, 0)
        assert observation.timestamp.tzinfo is None
        assert observation.provenance.retrieved_at == datetime(2025, 1, 1, 1, 0, 0)
        assert observation.provenance.retrieved_at.tzinfo is None
        assert observation.provenance.source_type == "text/html"
        assert observation.provenance.content_type is None


def main():
    test_semantic_source_classification_and_mime_are_separate()
    test_canonical_url_fingerprint_and_cross_job_lineage_merge()
    test_legacy_timestamp_and_provenance_loading()
    print("SOURCE QUALITY AND CYCLE DEDUPLICATION : ALL TESTS PASSED")


if __name__ == "__main__":
    main()
