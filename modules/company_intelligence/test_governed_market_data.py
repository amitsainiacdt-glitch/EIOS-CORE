import unittest
from datetime import datetime, timezone

from modules.company_intelligence.governed_market_data import GovernedMarketData


class GovernedMarketDataTests(unittest.TestCase):
    def test_missing_inputs_are_blocked(self):
        item = GovernedMarketData("COROMANDEL", datetime.now(timezone.utc))
        self.assertFalse(item.ready_for_valuation)
        self.assertEqual(item.gate()["status"], "BLOCKED_MISSING_MARKET_DATA")

    def test_governed_price_and_expectation_are_ready(self):
        item = GovernedMarketData(
            "COROMANDEL", datetime.now(timezone.utc), current_price=1000, consensus_eps=50,
            source_id="approved-provider", status="GOVERNED",
        )
        self.assertTrue(item.ready_for_valuation)
        self.assertEqual(item.gate()["status"], "READY")

    def test_governed_data_requires_source(self):
        with self.assertRaises(ValueError):
            GovernedMarketData("COROMANDEL", datetime.now(timezone.utc), status="GOVERNED")


if __name__ == "__main__":
    unittest.main()
