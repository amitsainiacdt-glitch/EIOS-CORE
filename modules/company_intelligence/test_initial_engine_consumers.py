from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.engine_analysis_intake import EngineAnalysisIntakeRepository
from modules.company_intelligence.governed_company_fact import GovernedCompanyFact
from modules.company_intelligence.governed_fact_engine_router import GovernedFactEngineRouter
from modules.company_intelligence.initial_engine_consumers import InitialEngineAnalysisRepository


def fact():
    return GovernedCompanyFact(
        1, "FACT-1", "CANDIDATE-1", "Coromandel International", "CAPACITY_CHANGE",
        "Coromandel commissioned capacity worth INR 125 crore on 28 August 2026.",
        "ASSERTED", ("INR 125 crore",), ("28 August 2026",), 7,
        "https://www.coromandel.biz/report.pdf", "a" * 64, 82,
        "META-1", "REVIEW-1", datetime.now(timezone.utc),
    )


class InitialEngineConsumerTests(unittest.TestCase):
    def test_supported_consumers_return_safe_traceable_results(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); now = datetime.now(timezone.utc); item = fact()
            route = GovernedFactEngineRouter(root / "routes.jsonl").route(item, routed_at=now)
            work = EngineAnalysisIntakeRepository(root / "intake.jsonl").dispatch(item, route, created_at=now)
            repository = InitialEngineAnalysisRepository(root / "results.jsonl")
            results = repository.consume_available(item, work, completed_at=now)
            self.assertEqual({result.analysis_queue for result in results}, {"COMPANY_EVENT_ANALYSIS", "CONTRADICTION_SEARCH", "CONTINUOUS_MONITORING"})
            event = next(result for result in results if result.analysis_queue == "COMPANY_EVENT_ANALYSIS")
            self.assertEqual(event.result_status, "FACTUAL_EVENT_CONFIRMED_IMPACT_UNPROVEN")
            monitoring = next(result for result in results if result.analysis_queue == "CONTINUOUS_MONITORING")
            self.assertIn("28 August 2026", monitoring.monitoring_terms)
            self.assertTrue(all(not result.changes_verdict for result in results))
            self.assertEqual(repository.consume_available(item, work, completed_at=now), ())


if __name__ == "__main__":
    unittest.main()
