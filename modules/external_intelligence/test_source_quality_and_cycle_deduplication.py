"""Offline tests for semantic source quality and within-cycle deduplication."""

import json
from datetime import datetime, timedelta, timezone
from hashlib import sha256
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
        assert observation.provenance.published_at is None
        assert observation.provenance.filing_at is None
        assert observation.provenance.source_document_id is None
        assert observation.provenance.document_hash is None
        assert observation.provenance.extraction_method is None


def test_primary_source_provenance_round_trip_and_document_identity():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "observations.json"
        engine = ObservationEngine(persistence=ObservationPersistence(path))
        adapter = ExternalObservationAdapter(engine)
        document_hash = sha256(b"canonical filing bytes").hexdigest()
        india = timezone(timedelta(hours=5, minutes=30))

        first = adapter.ingest(
            title="Exchange filing",
            description="Normalized filing text from the first URL.",
            source="https://www.nseindia.com/filing/download?id=123",
            category="External Web",
            entity="Issuer",
            confidence=90,
            cycle_id="cycle-primary-1",
            job_id="nse-job",
            research_intent="REGULATORY_FILING",
            retrieved_at=datetime(2026, 8, 29, 12, tzinfo=india),
            published_at=datetime(2026, 8, 29, 9, 15, tzinfo=india),
            filing_at=datetime(2026, 8, 29, 9, tzinfo=india),
            source_document_id="NSE-ANN-123",
            document_hash=document_hash.upper(),
            extraction_method="pdf_text",
            content_type="application/pdf",
        )
        duplicate = adapter.ingest(
            title="Company IR copy",
            description="Text extracted differently from the same PDF.",
            source="https://issuer.example.com/investors/announcement.pdf",
            category="External Web",
            entity="Issuer",
            confidence=90,
            cycle_id="cycle-primary-1",
            job_id="ir-job",
            research_intent="COMPANY_FILING",
            document_hash=document_hash,
            extraction_method="pdf_text",
        )

        assert first is not None and duplicate is None
        assert engine.registry.count() == 1
        provenance = first.provenance
        assert provenance.published_at == datetime(2026, 8, 29, 3, 45, tzinfo=timezone.utc)
        assert provenance.filing_at == datetime(2026, 8, 29, 3, 30, tzinfo=timezone.utc)
        assert provenance.retrieved_at == datetime(2026, 8, 29, 6, 30, tzinfo=timezone.utc)
        assert provenance.source_document_id == "NSE-ANN-123"
        assert provenance.document_hash == document_hash
        assert provenance.extraction_method == "pdf_text"
        assert provenance.contributing_job_ids == ("nse-job", "ir-job")

        loaded = ObservationPersistence(path).load()[0]
        assert loaded.provenance == provenance

        later = adapter.ingest(
            title="Later retrieval",
            description="Same source document in a later cycle.",
            source="https://archive.example.com/announcement.pdf",
            category="External Web",
            entity="Issuer",
            confidence=90,
            cycle_id="cycle-primary-2",
            job_id="archive-job",
            research_intent="HISTORICAL_RETRIEVAL",
            document_hash=document_hash,
        )
        assert later is not None
        assert engine.registry.count() == 2


def test_source_native_document_id_is_scoped_to_source_domain():
    service = ObservationDeduplicationService
    same_domain_first = service.fingerprint(
        "https://exchange.example.com/a",
        "first extraction",
        source_document_id="ANN-42",
    )
    same_domain_second = service.fingerprint(
        "https://exchange.example.com/b",
        "second extraction",
        source_document_id="ANN-42",
    )
    other_domain = service.fingerprint(
        "https://other.example.com/a",
        "first extraction",
        source_document_id="ANN-42",
    )
    assert same_domain_first == same_domain_second
    assert other_domain != same_domain_first

    try:
        service.normalize_document_hash("not-a-sha256")
    except ValueError as exc:
        assert "SHA-256" in str(exc)
    else:
        raise AssertionError("invalid document hash accepted")


def main():
    test_semantic_source_classification_and_mime_are_separate()
    test_canonical_url_fingerprint_and_cross_job_lineage_merge()
    test_legacy_timestamp_and_provenance_loading()
    test_primary_source_provenance_round_trip_and_document_identity()
    test_source_native_document_id_is_scoped_to_source_domain()
    print("SOURCE QUALITY AND CYCLE DEDUPLICATION : ALL TESTS PASSED")


if __name__ == "__main__":
    main()
