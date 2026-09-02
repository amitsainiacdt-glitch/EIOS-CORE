from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.engine_analysis_intake import EngineAnalysisIntakeRepository
from modules.company_intelligence.governed_company_fact import GovernedCompanyFact
from modules.company_intelligence.governed_fact_engine_router import GovernedFactEngineRouter


def governed_fact():
    return GovernedCompanyFact(
        1, "FACT-1", "CANDIDATE-1", "Coromandel International", "CAPACITY_CHANGE",
        "Coromandel commissioned a new plant.", "ASSERTED", (), (), 7,
        "https://www.coromandel.biz/report.pdf", "a" * 64, 82,
        "META-1", "REVIEW-1", datetime.now(timezone.utc),
    )


class EngineAnalysisIntakeTests(unittest.TestCase):
    def test_each_route_becomes_a_traceable_fail_closed_work_item(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); now = datetime.now(timezone.utc); fact = governed_fact()
            route = GovernedFactEngineRouter(root / "routes.jsonl").route(fact, routed_at=now)
            repository = EngineAnalysisIntakeRepository(root / "intake.jsonl")
            work = repository.dispatch(fact, route, created_at=now)
            self.assertEqual(len(work), len(route.target_analysis_queues))
            financial = next(item for item in work if item.analysis_queue == "FINANCIAL_IMPACT_ANALYSIS")
            self.assertEqual(financial.intake_status, "WAITING_FOR_REQUIRED_INPUTS")
            self.assertIn("audited historical financial series", financial.missing_inputs)
            monitoring = next(item for item in work if item.analysis_queue == "CONTINUOUS_MONITORING")
            self.assertEqual(monitoring.intake_status, "MONITORING_ACTIVE")
            self.assertTrue(all(not item.changes_verdict for item in work))
            self.assertEqual(repository.dispatch(fact, route, created_at=now), ())


if __name__ == "__main__":
    unittest.main()
