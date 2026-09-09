import unittest

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment, RegimeConfidence
from modules.external_intelligence.change_regime_service import ChangeRegimeService
from modules.external_intelligence.sector_causal_indicator import CausalEffectDirection, SectorCausalIndicatorDefinition
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


class ChangeRegimeServiceTests(unittest.TestCase):
    def setUp(self):
        definition = SectorCausalIndicatorDefinition(
            1, "AUTO-INVENTORY", 1, "Dealer inventory", ("AUTOS",), ("INVENTORY",), "channel stock",
            CausalEffectDirection.SUPPORTIVE, 2, 4, "Dealer inventory normalizes before production",
            ("revenue", "margin"), ("AUTO_MANUFACTURER",), ("registration authority",),
            ("dealer survey",), "source family", 2, 2, 60, ("festival stocking",),
            ("discounting worsens",), ("inventory rebuilds",), True, (),
        )
        registry = SectorCausalIndicatorRegistry()
        registry.register(definition)
        self.chain_service = CausalChainService(registry)
        self.service = ChangeRegimeService(self.chain_service)
        links = tuple(CausalChainLink(stage, f"Statement {stage.value}", f"Mechanism {stage.value}",
                                      ("TE-1",) if index == 0 else ())
                      for index, stage in enumerate(CausalChainStage))
        self.chain = CausalChainAssessment(
            1, "CHAIN-AUTO", "Example Auto", "AUTOS", ("AUTO-INVENTORY",), ("TE-1",), links,
            (2, 4), ("Demand remains stable",), "The duration of normalization remains uncertain.", True,
            CausalChainService.NON_AUTHORITY,
        )

    def assessment(self, **changes):
        values = dict(
            schema_version=1, assessment_id="REGIME-1", causal_chain_id="CHAIN-AUTO",
            regime=ChangeRegime.CYCLICAL, confidence=RegimeConfidence.MODERATE,
            input_temporal_evidence_ids=("TE-1",),
            classification_basis=("Inventory has declined across repeated reporting periods.",),
            alternative_explanations=("Seasonal destocking could explain part of the decline.",),
            distinguishing_tests=("Compare with the same pre-festival period in prior years.",),
            uncertainty_statement="The evidence does not yet establish a structural demand change.",
            public_information_only=True, non_authority_statement=ChangeRegimeService.NON_AUTHORITY,
        )
        values.update(changes)
        return ChangeRegimeAssessment(**values)

    def test_accepts_explainable_ordinal_regime(self):
        result = self.service.validate(causal_chain=self.chain, assessment=self.assessment())
        self.assertEqual(result.regime, ChangeRegime.CYCLICAL)
        self.assertTrue(self.service.may_enter_meta_review(causal_chain=self.chain, assessment=result))

    def test_rejects_stale_chain_or_evidence_binding(self):
        with self.assertRaisesRegex(ValueError, "bind to causal chain"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(causal_chain_id="OTHER"))
        with self.assertRaisesRegex(ValueError, "exactly bind"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(input_temporal_evidence_ids=("TE-2",)))

    def test_requires_alternatives_tests_and_uncertainty(self):
        with self.assertRaisesRegex(ValueError, "alternative_explanations"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(alternative_explanations=()))
        with self.assertRaisesRegex(ValueError, "distinguishing_tests"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(distinguishing_tests=()))
        with self.assertRaisesRegex(ValueError, "uncertainty_statement"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(uncertainty_statement=" "))

    def test_noise_and_speculative_narrative_cannot_advance(self):
        for regime in (ChangeRegime.STATISTICAL_NOISE, ChangeRegime.SPECULATIVE_NARRATIVE):
            with self.subTest(regime=regime):
                item = self.assessment(regime=regime, confidence=RegimeConfidence.LOW)
                self.service.validate(causal_chain=self.chain, assessment=item)
                self.assertFalse(self.service.may_enter_meta_review(causal_chain=self.chain, assessment=item))

    def test_noise_or_narrative_cannot_claim_high_causal_confidence(self):
        with self.assertRaisesRegex(ValueError, "cannot carry high"):
            self.service.validate(causal_chain=self.chain, assessment=self.assessment(
                regime=ChangeRegime.SPECULATIVE_NARRATIVE, confidence=RegimeConfidence.HIGH))

    def test_reported_financial_recovery_is_not_a_required_field(self):
        result = self.service.validate(causal_chain=self.chain, assessment=self.assessment())
        self.assertFalse(hasattr(result, "reported_revenue_recovery"))
        self.assertFalse(hasattr(result, "reported_pat_recovery"))


if __name__ == "__main__":
    unittest.main()
