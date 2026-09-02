from datetime import datetime, timezone
import unittest

from modules.company_intelligence.company_intelligence_snapshot import (
    CompanyIntelligenceSnapshot,
    IntelligenceLayer,
    IntelligenceLayerStatus,
    MANDATORY_VERDICT_LAYERS,
    assess_verdict_readiness,
)


def layer(status=IntelligenceLayerStatus.READY, coverage=100):
    return IntelligenceLayer(status, "Governed layer.", ("SOURCE-1",), coverage_percent=coverage)


class CompanyIntelligenceSnapshotTests(unittest.TestCase):
    def test_all_mandatory_layers_allow_verdict_readiness(self):
        layers = {name: layer() for name in MANDATORY_VERDICT_LAYERS}
        status, gaps = assess_verdict_readiness(layers)
        self.assertEqual(status, "READY")
        self.assertEqual(gaps, ())

    def test_partial_financials_force_research_hold(self):
        layers = {name: layer() for name in MANDATORY_VERDICT_LAYERS}
        layers["financials"] = layer(IntelligenceLayerStatus.PARTIAL, 40)
        status, gaps = assess_verdict_readiness(layers)
        self.assertEqual(status, "RESEARCH_HOLD")
        self.assertIn("financials: PARTIAL", gaps)

    def test_snapshot_rejects_ready_verdict_when_a_layer_is_incomplete(self):
        layers = {name: layer() for name in MANDATORY_VERDICT_LAYERS}
        layers["news_and_filings"] = layer(IntelligenceLayerStatus.NOT_STARTED, 0)
        with self.assertRaisesRegex(ValueError, "verdict cannot be READY"):
            CompanyIntelligenceSnapshot(
                1,
                "SNAPSHOT-1",
                "Example Limited",
                "EXAMPLE",
                datetime.now(timezone.utc),
                layers,
                "READY",
                verdict="INVEST",
                confidence_percent=80,
            )

    def test_snapshot_never_creates_recommendation_during_assembly(self):
        layers = {name: layer() for name in MANDATORY_VERDICT_LAYERS}
        with self.assertRaisesRegex(ValueError, "cannot itself create a recommendation"):
            CompanyIntelligenceSnapshot(
                1,
                "SNAPSHOT-2",
                "Example Limited",
                "EXAMPLE",
                datetime.now(timezone.utc),
                layers,
                "READY",
                verdict="INVEST",
                confidence_percent=80,
                creates_recommendation=True,
            )


if __name__ == "__main__":
    unittest.main()
