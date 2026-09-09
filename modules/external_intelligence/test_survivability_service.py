import unittest
from datetime import datetime, timezone

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.normalized_valuation import NormalizedValuationResult, NormalizedValuationRoom
from modules.external_intelligence.normalized_valuation_service import NormalizedValuationService
from modules.external_intelligence.survivability import SurvivabilityAssessment, SurvivabilityDecision
from modules.external_intelligence.survivability_service import SurvivabilityService


class SurvivabilityServiceTests(unittest.TestCase):
    def setUp(self):
        links = tuple(CausalChainLink(stage, f"Statement {stage.value}", f"Mechanism {stage.value}",
                                      ("TE-1",) if index == 0 else ())
                      for index, stage in enumerate(CausalChainStage))
        self.chain = CausalChainAssessment(
            1, "CHAIN-1", "Example", "INDUSTRIALS", ("ORDER-CYCLE",), ("TE-1",), links,
            (2, 4), ("Execution continues",), "Timing remains uncertain.", True,
            CausalChainService.NON_AUTHORITY)
        self.valuation = NormalizedValuationResult(
            "VALUE-1", "INR", 100.0, (), NormalizedValuationRoom.SUFFICIENT, True, (),
            NormalizedValuationService.NON_AUTHORITY)
        self.service = SurvivabilityService()

    def assessment(self, **changes):
        values = dict(
            schema_version=1, assessment_id="SURVIVE-1", causal_chain_id="CHAIN-1",
            normalized_valuation_assessment_id="VALUE-1", as_of=datetime(2026, 9, 9, tzinfo=timezone.utc),
            currency="INR", cash_and_liquid_investments=150.0, committed_undrawn_facilities=50.0,
            annual_cash_burn=20.0, debt_due_within_thesis_horizon=100.0, total_debt=200.0,
            normalized_ebitda=100.0, interest_expense=20.0, potential_dilution_percent=5.0,
            unresolved_covenant_breach=False, going_concern_warning=False, critical_governance_threats=(),
            source_ids=("AUDITED-BALANCE-SHEET", "DEBT-MATURITY-NOTE"),
            assumptions=("Committed facilities remain available.",),
            uncertainty_statement="Working-capital requirements can exceed the published base case.",
            public_information_only=True, non_authority_statement=SurvivabilityService.NON_AUTHORITY)
        values.update(changes)
        return SurvivabilityAssessment(**values)

    def evaluate(self, assessment=None, valuation=None):
        return self.service.evaluate(causal_chain=self.chain, normalized_valuation=valuation or self.valuation,
                                     assessment=assessment or self.assessment())

    def test_calculates_survival_through_full_causal_horizon(self):
        result = self.evaluate()
        self.assertEqual(result.thesis_horizon_quarters, 4)
        self.assertEqual(result.horizon_funding_need, 120.0)
        self.assertAlmostEqual(result.liquidity_coverage_ratio, 200.0 / 120.0)
        self.assertEqual(result.debt_to_normalized_ebitda, 2.0)
        self.assertEqual(result.normalized_ebitda_to_interest, 5.0)
        self.assertEqual(result.decision, SurvivabilityDecision.CONTAINED)
        self.assertTrue(result.eligible_for_eip_assembly)

    def test_liquidity_failure_is_a_hard_veto(self):
        result = self.evaluate(self.assessment(cash_and_liquid_investments=40.0,
                                               committed_undrawn_facilities=0.0))
        self.assertEqual(result.decision, SurvivabilityDecision.VETO_SURVIVABILITY_FAILURE)
        self.assertTrue(result.hard_veto)
        self.assertFalse(result.eligible_for_eip_assembly)

    def test_going_concern_covenant_or_governance_threat_is_a_hard_veto(self):
        cases = (
            {"going_concern_warning": True},
            {"unresolved_covenant_breach": True},
            {"critical_governance_threats": ("Auditor resignation remains unresolved.",)},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                self.assertTrue(self.evaluate(self.assessment(**changes)).hard_veto)

    def test_thin_margin_or_high_dilution_holds_without_calling_failure(self):
        thin = self.evaluate(self.assessment(cash_and_liquid_investments=100.0,
                                             committed_undrawn_facilities=30.0))
        self.assertEqual(thin.decision, SurvivabilityDecision.HOLD_INSUFFICIENT_MARGIN)
        self.assertFalse(thin.hard_veto)
        diluted = self.evaluate(self.assessment(potential_dilution_percent=25.0))
        self.assertEqual(diluted.decision, SurvivabilityDecision.HOLD_INSUFFICIENT_MARGIN)

    def test_apparent_survival_cannot_bypass_ineligible_valuation(self):
        blocked = NormalizedValuationResult(
            **{**self.valuation.__dict__, "valuation_room": NormalizedValuationRoom.INSUFFICIENT,
               "eligible_for_eip_assembly": False})
        result = self.evaluate(valuation=blocked)
        self.assertFalse(result.eligible_for_eip_assembly)
        self.assertIn("NORMALIZED_VALUATION_NOT_ELIGIBLE", result.reason_codes)

    def test_requires_dated_public_sources_and_matching_currency(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self.evaluate(self.assessment(as_of=datetime(2026, 9, 9)))
        with self.assertRaisesRegex(ValueError, "source_ids"):
            self.evaluate(self.assessment(source_ids=()))
        with self.assertRaisesRegex(ValueError, "currency mismatch"):
            self.evaluate(self.assessment(currency="USD"))
        with self.assertRaisesRegex(ValueError, "public information only"):
            self.evaluate(self.assessment(public_information_only=False))


if __name__ == "__main__":
    unittest.main()
