"""Deterministic no-network validation for runtime observation provenance."""

import json
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.external_observation_adapter import (
    ExternalObservationAdapter,
)
from modules.external_intelligence.external_research_orchestrator import (
    ExternalResearchOrchestrator,
)
from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.research_query import ExternalResearchQuery
from modules.external_intelligence.search_provider import SearchProvider
from modules.external_intelligence.search_result import ExternalSearchResult
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence


def test_runtime_observation_provenance_and_legacy_loading():
    retrieved_at = datetime(2026, 8, 20, 9, 30, 0)
    content = "Deterministic normalized research content."

    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "observations.json"
        persistence = ObservationPersistence(path)
        adapter = ExternalObservationAdapter(
            ObservationEngine(persistence=persistence)
        )

        observation = adapter.ingest(
            title="Runtime provenance",
            description=content,
            source="https://Research.Example.com/report/1",
            category="External Web",
            entity="Example Limited",
            confidence=75.0,
            cycle_id="2026-08-20T09:30:00",
            job_id="JOB-001",
            research_intent="DEMAND_VALIDATION",
            retrieved_at=retrieved_at,
            source_type="text/html; charset=utf-8",
        )

        assert observation is not None
        assert observation.provenance is not None
        assert observation.provenance.source_domain == "research.example.com"
        assert observation.provenance.source_type == "WEB"
        assert observation.provenance.source_quality_tier == "TIER_3"
        assert observation.provenance.content_type == "text/html; charset=utf-8"
        assert observation.provenance.content_fingerprint == sha256(
            content.encode("utf-8")
        ).hexdigest()
        assert persistence.load()[0].provenance == observation.provenance

        legacy_path = Path(temp_dir) / "legacy.json"
        legacy_path.write_text(
            json.dumps(
                [{
                    "title": "Legacy",
                    "description": "No provenance field",
                    "source": "Archive",
                    "category": "External Web",
                    "entity": "Example Limited",
                    "confidence": 50.0,
                    "timestamp": "2025-01-01T00:00:00",
                }]
            ),
            encoding="utf-8",
        )
        legacy = ObservationPersistence(legacy_path).load()[0]
        assert legacy.provenance is None
        assert legacy.timestamp == datetime(2025, 1, 1, 0, 0, 0)
        assert legacy.timestamp.tzinfo is None


class NoNetworkSearchProvider(SearchProvider):
    """Deterministic provider used to prove the runtime path stays offline."""

    def search(self, query: ExternalResearchQuery):
        return [
            ExternalSearchResult(
                title="Offline source",
                url="https://offline.example.com/report",
                snippet="Synthetic offline result.",
                source="No-network test",
            )
        ]


class NoNetworkRetriever:
    """Return deterministic content without opening a socket."""

    def retrieve(self, url: str):
        return RetrievedContent(
            url=url,
            status_code=200,
            content=(
                "Deterministic research content long enough to pass the "
                "structural quality gate without any external retrieval."
            ),
            content_type="text/plain",
            headers={"Content-Type": "text/plain"},
        )


def test_no_network_and_production_store_isolation():
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        production_path = root / "data" / "observations.json"
        production_path.parent.mkdir(parents=True)
        production_bytes = b'{"production":"preserve exactly"}'
        production_path.write_bytes(production_bytes)

        test_path = root / "test-store" / "observations.json"
        engine = ObservationEngine(
            persistence=ObservationPersistence(test_path)
        )
        orchestrator = ExternalResearchOrchestrator(
            NoNetworkSearchProvider(),
            retriever=NoNetworkRetriever(),
            observation_engine=engine,
        )
        query = ExternalResearchQuery(
            company="Example Limited",
            ticker="EXAMPLE",
            question="Is deterministic offline evidence available?",
            query="Example Limited deterministic offline evidence",
            intent="DEMAND_VALIDATION",
        )

        def reject_network(*args, **kwargs):
            raise AssertionError("network access is forbidden in this test")

        with patch(
            "requests.sessions.Session.request",
            side_effect=reject_network,
        ):
            result = orchestrator.execute(
                query,
                cycle_id="2026-08-20T10:00:00",
                job_id="JOB-OFFLINE",
                retrieved_at=datetime(2026, 8, 20, 10, 0, 0),
            )

        assert len(result.observations) == 1
        assert test_path.exists()
        assert production_path.read_bytes() == production_bytes


def main():
    test_runtime_observation_provenance_and_legacy_loading()
    test_no_network_and_production_store_isolation()
    print("RUNTIME OBSERVATION PROVENANCE : ALL TESTS PASSED")


if __name__ == "__main__":
    main()
