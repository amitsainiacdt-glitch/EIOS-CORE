import unittest
from datetime import datetime, timezone

from modules.external_intelligence.eip_expectation_gap import EIPExpectationGapResult, ExpectationGapDirection, ExpectationGapMateriality
from modules.external_intelligence.eip_expectation_gap_service import EIPExpectationGapService
from modules.external_intelligence.normalized_valuation import NormalizedOperatingScenario, NormalizedScenarioKind, NormalizedValuationAssessment, NormalizedValuationRoom
from modules.external_intelligence.normalized_valuation_service import NormalizedValuationService


class NormalizedValuationServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = NormalizedValuationService()
        self.gap = EIPExpectationGapResult(
            "GAP-1", "EBITDA_MARGIN", "PERCENT", datetime(2027, 3, 31, tzinfo=timezone.utc),
            12.0, 16.0, 4.0, 33.33, ExpectationGapDirection.POSITIVE,
            ExpectationGapMateriality.MODERATE, True, (), EIPExpectationGapService.NON_AUTHORITY)

    @staticmethod
    def scenario(kind, revenue, margin, multiple):
        return NormalizedOperatingScenario(
            kind, revenue, margin, multiple, (f"SOURCE-{kind.value}",),
            f"Public evidence and explicit assumptions support the {kind.value} case.")

    def assessment(self, **changes):
        values = dict(
            schema_version=1, assessment_id="VALUE-1", expectation_gap_assessment_id="GAP-1",
            currency="INR", current_price=100.0, current_price_source_ids=("EXCHANGE-PRICE",),
            net_debt=100.0, shares_outstanding=10.0,
            scenarios=(
                self.scenario(NormalizedScenarioKind.CURRENT_TROUGH, 1000.0, 8.0, 8.0),
                self.scenario(NormalizedScenarioKind.REASONABLE_RECOVERY, 1100.0, 12.0, 10.0),
                self.scenario(NormalizedScenarioKind.STRONG_NORMALIZATION, 1200.0, 15.0, 12.0),
            ),
            assumptions=("Net debt and share count remain stable through the horizon.",),
            uncertainty_statement="Margins and valuation multiples can differ materially from scenarios.",
            public_information_only=True, non_authority_statement=NormalizedValuationService.NON_AUTHORITY,
        )
        values.update(changes)
        return NormalizedValuationAssessment(**values)

    def test_calculates_three_transparent_scenarios(self):
        result = self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment())
        self.assertEqual([item.kind for item in result.scenarios], list(NormalizedScenarioKind))
        self.assertEqual(result.scenarios[0].normalized_ebitda, 80.0)
        self.assertEqual(result.scenarios[1].value_per_share, 122.0)
        self.assertEqual(result.valuation_room, NormalizedValuationRoom.SUFFICIENT)
        self.assertTrue(result.eligible_for_eip_assembly)

    def test_strong_case_alone_cannot_establish_valuation_room(self):
        scenarios = list(self.assessment().scenarios)
        scenarios[1] = self.scenario(NormalizedScenarioKind.REASONABLE_RECOVERY, 1000.0, 10.0, 10.0)
        result = self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment(scenarios=tuple(scenarios)))
        self.assertEqual(result.valuation_room, NormalizedValuationRoom.INSUFFICIENT)
        self.assertGreater(result.scenarios[2].upside_downside_percent, 20.0)
        self.assertFalse(result.eligible_for_eip_assembly)

    def test_requires_fixed_scenario_order_and_non_declining_ebitda(self):
        scenarios = self.assessment().scenarios
        with self.assertRaisesRegex(ValueError, "in order"):
            self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment(scenarios=(scenarios[1], scenarios[0], scenarios[2])))
        falling = (
            scenarios[0], self.scenario(NormalizedScenarioKind.REASONABLE_RECOVERY, 900.0, 8.0, 10.0), scenarios[2])
        with self.assertRaisesRegex(ValueError, "must not decline"):
            self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment(scenarios=falling))

    def test_rejects_invalid_financial_inputs_and_missing_sources(self):
        with self.assertRaisesRegex(ValueError, "current_price must be positive"):
            self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment(current_price=0.0))
        bad = list(self.assessment().scenarios)
        bad[1] = NormalizedOperatingScenario(NormalizedScenarioKind.REASONABLE_RECOVERY, 1100, 12, 10, (), "Reasonable case")
        with self.assertRaisesRegex(ValueError, "assumption_source_ids"):
            self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment(scenarios=tuple(bad)))

    def test_ineligible_expectation_gap_blocks_valuation_assembly(self):
        blocked_gap = EIPExpectationGapResult(
            **{**self.gap.__dict__, "eligible_for_eip_assembly": False,
               "reason_codes": ("MATERIAL_EXPECTATION_GAP_NOT_ESTABLISHED",)})
        result = self.service.evaluate(expectation_gap=blocked_gap, assessment=self.assessment())
        self.assertEqual(result.valuation_room, NormalizedValuationRoom.NOT_ASSESSABLE)
        self.assertFalse(result.eligible_for_eip_assembly)

    def test_price_history_and_trailing_pe_are_not_valuation_inputs(self):
        result = self.service.evaluate(expectation_gap=self.gap, assessment=self.assessment())
        self.assertFalse(hasattr(result, "distance_from_52_week_high"))
        self.assertFalse(hasattr(result, "trailing_pe"))


if __name__ == "__main__":
    unittest.main()
