from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.governed_company_fact import GovernedCompanyFact
from modules.company_intelligence.governed_fact_engine_router import GovernedFactEngineRouter


def fact(event_type="CAPACITY_CHANGE"):
    return GovernedCompanyFact(
        1, "FACT-1", "CANDIDATE-1", "Coromandel International", event_type,
        "Coromandel commissioned a new plant.", "ASSERTED", (), (), 7,
        "https://www.coromandel.biz/report.pdf", "a" * 64, 82,
        "META-1", "REVIEW-1", datetime.now(timezone.utc),
    )


class GovernedFactEngineRouterTests(unittest.TestCase):
    def test_capacity_fact_is_routed_but_cannot_change_verdict(self):
        with TemporaryDirectory() as directory:
            router = GovernedFactEngineRouter(Path(directory) / "routes.jsonl")
            route = router.route(fact(), routed_at=datetime.now(timezone.utc))
            self.assertIn("financials", route.target_layers)
            self.assertIn("management", route.target_layers)
            self.assertIn("CATALYST_READINESS", route.target_analysis_queues)
            self.assertFalse(route.creates_evidence)
            self.assertFalse(route.creates_catalyst)
            self.assertFalse(route.changes_verdict)
            with self.assertRaisesRegex(ValueError, "already routed"):
                router.route(fact(), routed_at=datetime.now(timezone.utc))

    def test_weather_fact_routes_to_macro_sector_and_company_exposure(self):
        with TemporaryDirectory() as directory:
            route = GovernedFactEngineRouter(Path(directory) / "routes.jsonl").route(
                fact("WEATHER_ANOMALY"), routed_at=datetime.now(timezone.utc)
            )
            self.assertTrue({"macro", "sector", "micro"}.issubset(route.target_layers))
            self.assertIn("COMPANY_EXPOSURE_ANALYSIS", route.target_analysis_queues)


if __name__ == "__main__":
    unittest.main()
