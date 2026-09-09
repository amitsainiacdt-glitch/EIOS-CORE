import unittest
from datetime import datetime, timezone

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment, RegimeConfidence
from modules.external_intelligence.change_regime_service import ChangeRegimeService
from modules.external_intelligence.eip_expectation_gap import (
    EIPExpectationGapAssessment, ExpectationGapDirection, ExpectationGapMateriality,
    FavorableMetricDirection, GovernedExpectationMeasure,
)
from modules.external_intelligence.eip_expectation_gap_service import EIPExpectationGapService
from modules.external_intelligence.thesis_price_recognition import (
    FundamentalChangeIncorporation, ThesisPriceRecognitionGateResult, ThesisRecognitionDecision,
)
from modules.external_intelligence.thesis_price_recognition_service import ThesisPriceRecognitionService


class EIPExpectationGapServiceTests(unittest.TestCase):
    def setUp(self):
        links = tuple(CausalChainLink(stage, f"Statement {stage.value}", f"Mechanism {stage.value}",
                                      ("TE-1",) if index == 0 else ())
                      for index, stage in enumerate(CausalChainStage))
        self.chain = CausalChainAssessment(
            1, "CHAIN-1", "Example", "CHEMICALS", ("CHEMICAL-SPREAD",), ("TE-1",), links,
            (2, 4), ("Selling price remains stable",), "Transmission is uncertain.", True,
            CausalChainService.NON_AUTHORITY)
        self.regime = ChangeRegimeAssessment(
            1, "REGIME-1", "CHAIN-1", ChangeRegime.CYCLICAL, RegimeConfidence.MODERATE,
            ("TE-1",), ("Spread improved.",), ("Outage may contribute.",), ("Test persistence.",),
            "Duration remains uncertain.", True, ChangeRegimeService.NON_AUTHORITY)
        self.recognition = ThesisPriceRecognitionGateResult(
            ThesisRecognitionDecision.ALLOW_EIP_REVIEW, FundamentalChangeIncorporation.LIMITED,
            (), "RECOGNITION-1", False, ThesisPriceRecognitionService.NON_AUTHORITY)
        self.service = EIPExpectationGapService()
        self.horizon = datetime(2027, 3, 31, tzinfo=timezone.utc)

    def measure(self, value, *, metric="EBITDA_MARGIN", unit="PERCENT", horizon=None, source="SOURCE"):
        return GovernedExpectationMeasure(metric, unit, horizon or self.horizon, value, (source,),
                                          "Public evidence supports this stated expectation.")

    def assessment(self, **changes):
        values = dict(
            schema_version=1, assessment_id="GAP-1", causal_chain_id="CHAIN-1",
            regime_assessment_id="REGIME-1", thesis_recognition_assessment_id="RECOGNITION-1",
            market_expectation=self.measure(12.0, source="CONSENSUS"),
            causal_eios_expectation=self.measure(16.0, source="CAUSAL-EVIDENCE"),
            favorable_direction=FavorableMetricDirection.HIGHER, direction=ExpectationGapDirection.POSITIVE,
            materiality=ExpectationGapMateriality.MODERATE,
            materiality_rationale="Four percentage points is material to normalized earnings.",
            assumptions=("Volumes remain broadly stable.",), contradictions=(),
            invalidation_conditions=("Product spread reverses.",),
            uncertainty_statement="The timing of margin transmission remains uncertain.",
            public_information_only=True, non_authority_statement=EIPExpectationGapService.NON_AUTHORITY,
        )
        values.update(changes)
        return EIPExpectationGapAssessment(**values)

    def evaluate(self, assessment=None, recognition=None):
        return self.service.evaluate(causal_chain=self.chain, regime_assessment=self.regime,
                                     recognition_gate=recognition or self.recognition,
                                     assessment=assessment or self.assessment())

    def test_calculates_comparable_positive_gap_without_abstract_score(self):
        result = self.evaluate()
        self.assertEqual(result.absolute_gap, 4.0)
        self.assertAlmostEqual(result.relative_gap_percent, 33.3333333333)
        self.assertTrue(result.eligible_for_eip_assembly)
        self.assertFalse(hasattr(result, "gap_score"))

    def test_requires_same_metric_unit_and_horizon(self):
        with self.assertRaisesRegex(ValueError, "same metric, unit, and horizon"):
            self.evaluate(self.assessment(causal_eios_expectation=self.measure(16.0, metric="PAT")))
        with self.assertRaisesRegex(ValueError, "same metric, unit, and horizon"):
            self.evaluate(self.assessment(causal_eios_expectation=self.measure(
                16.0, horizon=datetime(2027, 6, 30, tzinfo=timezone.utc))))

    def test_declared_direction_must_match_figures_and_business_direction(self):
        with self.assertRaisesRegex(ValueError, "disagrees"):
            self.evaluate(self.assessment(direction=ExpectationGapDirection.NEGATIVE))
        lower_is_better = self.assessment(
            market_expectation=self.measure(8.0, metric="CREDIT_COST"),
            causal_eios_expectation=self.measure(5.0, metric="CREDIT_COST"),
            favorable_direction=FavorableMetricDirection.LOWER)
        self.assertEqual(self.evaluate(lower_is_better).direction, ExpectationGapDirection.POSITIVE)

    def test_no_or_uncertain_material_gap_cannot_enter_eip_assembly(self):
        equal = self.assessment(causal_eios_expectation=self.measure(12.0, source="CAUSAL-EVIDENCE"),
                                direction=ExpectationGapDirection.NO_CLEAR_GAP,
                                materiality=ExpectationGapMateriality.IMMATERIAL)
        self.assertFalse(self.evaluate(equal).eligible_for_eip_assembly)
        uncertain = self.assessment(materiality=ExpectationGapMateriality.UNCERTAIN)
        self.assertFalse(self.evaluate(uncertain).eligible_for_eip_assembly)

    def test_price_recognition_veto_cannot_be_bypassed(self):
        veto = ThesisPriceRecognitionGateResult(
            ThesisRecognitionDecision.VETO_TOO_LATE, FundamentalChangeIncorporation.MOST_OR_ALL,
            ("SAME_FUNDAMENTAL_CHANGE_MOSTLY_OR_FULLY_RECOGNIZED",), "RECOGNITION-1", True,
            ThesisPriceRecognitionService.NON_AUTHORITY)
        result = self.evaluate(recognition=veto)
        self.assertFalse(result.eligible_for_eip_assembly)
        self.assertIn("PRICE_RECOGNITION_DID_NOT_ALLOW_EIP_REVIEW", result.reason_codes)

    def test_requires_public_dated_sources_assumptions_and_kill_condition(self):
        with self.assertRaisesRegex(ValueError, "public information only"):
            self.evaluate(self.assessment(public_information_only=False))
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self.evaluate(self.assessment(market_expectation=self.measure(
                12.0, horizon=datetime(2027, 3, 31))))
        with self.assertRaisesRegex(ValueError, "invalidation_conditions"):
            self.evaluate(self.assessment(invalidation_conditions=()))


if __name__ == "__main__":
    unittest.main()
