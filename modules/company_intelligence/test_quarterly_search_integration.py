from dataclasses import replace
from datetime import datetime, timezone
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from modules.external_intelligence.external_research_orchestrator import ExternalResearchOrchestrator
from modules.external_intelligence.research_query import ExternalResearchQuery
from modules.external_intelligence.source_selection import SelectedSource
from modules.company_intelligence import test_automatic_official_document_pipeline as fixtures
from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline


class QuarterSearchIntegrationTests(unittest.TestCase):
    def run_search(self, target):
        engine = ExternalResearchOrchestrator.__new__(ExternalResearchOrchestrator)
        results = [SimpleNamespace(title=t, url='https://www.coromandel.biz/'+str(i)+'.pdf')
                   for i,t in enumerate(['Q3 FY26 results','Q1 FY27 results','Financial results'])]
        engine.search_engine = Mock()
        engine.search_engine.search.return_value = results
        engine.source_selection_engine = Mock()
        engine.source_selection_engine.select.side_effect = lambda items, **kw: [SelectedSource(r) for r in items]
        engine.retriever = Mock()
        engine.retriever.retrieve.side_effect = OSError('Test: no network')
        query = ExternalResearchQuery('Coromandel','COROMANDEL','Find results','original query',
            'OFFICIAL_DOCUMENT_DISCOVERY',target,'www.coromandel.biz')
        return engine, engine.execute(query)

    def test_only_target_title_reaches_retrieval(self):
        engine,result = self.run_search('2026-06-30')
        self.assertEqual(engine.retriever.retrieve.call_count,1)
        self.assertEqual(result.quarter_screening['candidate_count'],1)
        self.assertIn('"FY27"',engine.search_engine.search.call_args.args[0].query)
        self.assertEqual(len(result.quarter_screening['results']),3)
        self.assertEqual(result.observations,[])

    def test_general_research_unchanged(self):
        engine,result = self.run_search(None)
        self.assertEqual(engine.retriever.retrieve.call_count,3)
        self.assertIsNone(result.quarter_screening)
        self.assertEqual(result.query.query,'original query')

    def test_targeted_collection_cannot_fallback_to_annual(self):
        adapter = Mock()
        archive = fixtures.FakeArchive()
        job = replace(fixtures.job(),quarter_period_end='2026-06-30')
        older = SelectedSource(SimpleNamespace(title='Q3 FY26 results',url='https://www.coromandel.biz/old.pdf'))
        pipeline = AutomaticOfficialDocumentPipeline(archive,object(),adapter_factory=adapter,
            source_manifest={'companies':{'COROMANDEL':{'sources':[{'source_type':'ANNUAL_REPORT',
            'authority':'ISSUER_OFFICIAL','document_urls':['https://www.coromandel.biz/annual.pdf']}]}}})
        result = pipeline.run([job],[SimpleNamespace(selected_sources=[older])],cycle_id='TEST',acquired_at=datetime.now(timezone.utc))
        self.assertEqual(result.archived,0)
        adapter.return_value.acquire.assert_not_called()

    def test_invalid_target_job_fails_validation(self):
        with self.assertRaises(ValueError):
            replace(fixtures.job('CURRENT_NEWS'),quarter_period_end='2026-06-30').validate()
