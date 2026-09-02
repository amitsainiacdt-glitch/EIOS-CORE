import unittest

from modules.company_intelligence.discovery_change_classifier import classify_discovery_change


class DiscoveryChangeClassifierTests(unittest.TestCase):
    def observation(self, title, *, intent="CURRENT_NEWS", tier="TIER_2"):
        return {"title": title, "description": "", "source": "https://example.com", "timestamp": "2026-09-01", "provenance": {"research_intent": intent, "source_quality_tier": tier}}

    def test_unrelated_discovery_is_held(self):
        result = classify_discovery_change(self.observation("Weather in Chennai"), "Coromandel International")
        self.assertEqual(result.review_status, "LOW_RELEVANCE_HOLD")
        self.assertEqual(result.verdict_impact, "NONE")

    def test_non_official_document_discovery_is_authority_held(self):
        result = classify_discovery_change(self.observation("Coromandel International annual results", intent="OFFICIAL_DOCUMENT_DISCOVERY"), "Coromandel International")
        self.assertEqual(result.review_status, "SOURCE_AUTHORITY_HOLD")

    def test_relevant_news_stays_review_pending(self):
        result = classify_discovery_change(self.observation("Coromandel International schedules earnings call"), "Coromandel International")
        self.assertEqual(result.review_status, "PENDING_HUMAN_REVIEW")


if __name__ == "__main__":
    unittest.main()
