import tempfile
import unittest
from pathlib import Path

from modules.external_intelligence.external_research_orchestrator import ExternalResearchOrchestrator
from modules.external_intelligence.research_query import ExternalResearchQuery
from modules.external_intelligence.search_result import ExternalSearchResult
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence
from modules.observation.observation_registry import ObservationRegistry


class Provider:
    def search(self, query):
        return [ExternalSearchResult(
            title="Official update", url="https://example.com/update.pdf",
            snippet="short search snippet", source="Test Search",
            raw_content=("Official industrial demand update for the reporting period. " * 8),
            delivery_provider="TEST_PROVIDER_RAW_CONTENT",
        )]


class BlockedRetriever:
    def retrieve(self, url):
        raise RuntimeError("issuer blocks direct automated retrieval")


class ProviderRawContentFallbackTests(unittest.TestCase):
    def test_preserved_raw_content_can_continue_with_explicit_delivery_lineage(self):
        with tempfile.TemporaryDirectory() as folder:
            engine = ObservationEngine(
                registry=ObservationRegistry(),
                persistence=ObservationPersistence(Path(folder) / "observations.json"),
            )
            result = ExternalResearchOrchestrator(
                Provider(), retriever=BlockedRetriever(), observation_engine=engine,
            ).execute(ExternalResearchQuery(
                company="Example", ticker="EXAMPLE", question="Industrial demand update",
                query="industrial demand update", intent="GENERAL_RESEARCH",
            ), job_id="RAW-FALLBACK", cycle_id="cycle-1")

        self.assertEqual(len(result.retrieved_content), 1)
        self.assertEqual(result.retrieval_failures, [])
        self.assertEqual(len(result.observations), 1)
        self.assertEqual(result.observations[0].provenance.extraction_method, "TEST_PROVIDER_RAW_CONTENT")
        self.assertNotIn("short search snippet", result.observations[0].description)


if __name__ == "__main__":
    unittest.main()
