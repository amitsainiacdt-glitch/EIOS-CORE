import tempfile
import unittest
from pathlib import Path

from modules.external_intelligence.external_research_orchestrator import ExternalResearchOrchestrator
from modules.external_intelligence.research_query import ExternalResearchQuery
from modules.external_intelligence.test_external_research_orchestrator import MockHTTPRetriever, MockSearchProvider
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence
from modules.observation.observation_registry import ObservationRegistry


class PrimaryIndicatorSourceGateTests(unittest.TestCase):
    def test_secondary_domain_cannot_create_primary_indicator_observation(self):
        with tempfile.TemporaryDirectory() as folder:
            persistence=ObservationPersistence(Path(folder)/'observations.json'); persistence.clear()
            engine=ObservationEngine(registry=ObservationRegistry(),persistence=persistence)
            result=ExternalResearchOrchestrator(MockSearchProvider(),retriever=MockHTTPRetriever(),
                observation_engine=engine).execute(
                    ExternalResearchQuery(company='Coromandel',ticker='COROMANDEL',question='Latest rainfall',
                        query='latest rainfall',intent='PRIMARY_INDICATOR_MONITORING'),
                    entity_domain='mausam.imd.gov.in')
        self.assertEqual([],result.observations)


if __name__=='__main__': unittest.main()
