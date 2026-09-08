import unittest
from datetime import datetime

from modules.external_intelligence.research_execution_service import ResearchExecutionService
from modules.external_intelligence.research_job import ResearchJob
from modules.external_intelligence.research_scheduler import ResearchScheduler


class CaptureOrchestrator:
    def execute(self, query, **kwargs):
        self.query = query
        return object()


class AuthorityBoundSearchQueryTests(unittest.TestCase):
    def test_primary_indicator_search_is_restricted_to_authority_domain(self):
        orchestrator = CaptureOrchestrator()
        scheduler = ResearchScheduler()
        service = ResearchExecutionService(orchestrator, scheduler)
        job = ResearchJob(
            job_id="AUTHORITY-BOUND", company="COROMANDEL", ticker="COROMANDEL",
            question="Latest official crop protection PBIT margin",
            intent="PRIMARY_INDICATOR_MONITORING", frequency_minutes=1440,
            entity_domain="coromandel.biz",
        )
        scheduler.register(job)
        service.execute(job, run_time=datetime(2026, 9, 8, 6, 0))
        self.assertTrue(orchestrator.query.query.startswith("site:coromandel.biz "))
        self.assertEqual(orchestrator.query.question, job.question)


if __name__ == "__main__":
    unittest.main()
