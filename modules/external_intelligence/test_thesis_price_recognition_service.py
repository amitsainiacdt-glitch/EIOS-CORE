import unittest

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment, RegimeConfidence
from modules.external_intelligence.change_regime_service import ChangeRegimeService
from modules.external_intelligence.price_recognition import PriceRecognitionPreview, PriceRecognitionState
from modules.external_intelligence.thesis_price_recognition import FundamentalChangeIncorporation, ThesisPriceRecognitionAssessment, ThesisRecognitionDecision
from modules.external_intelligence.thesis_price_recognition_service import ThesisPriceRecognitionService


class ThesisPriceRecognitionServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = ThesisPriceRecognitionService()
        links = tuple(CausalChainLink(stage, f"Statement {stage.value}", f"Mechanism {stage.value}",
                                      ("TE-1",) if index == 0 else ())
                      for index, stage in enumerate(CausalChainStage))
        self.chain = CausalChainAssessment(
            1, "CHAIN-1", "Example", "CHEMICALS", ("CHEMICAL-SPREAD",), ("TE-1",), links,
            (2, 4), ("Selling price remains stable",), "Transmission is uncertain.", True,
            CausalChainService.NON_AUTHORITY,
        )
        self.regime = ChangeRegimeAssessment(
            1, "REGIME-1", "CHAIN-1", ChangeRegime.CYCLICAL, RegimeConfidence.MODERATE,
            ("TE-1",), ("Spread improved repeatedly.",), ("Temporary outage may contribute.",),
            ("Test persistence after restart.",), "Cycle duration remains uncertain.", True,
            ChangeRegimeService.NON_AUTHORITY,
        )

    def market(self, *, state=PriceRecognitionState.UNRECOGNIZED, price_change=7.0):
        return PriceRecognitionPreview(
            "MARKET-1", "PRE-1", "a" * 64, "REVIEW-1", state, price_change, 0.55,
            ("ANCHOR_PRICE",) if price_change >= 20 else (), ("ANCHOR_PRICE", "SECTOR_RELATIVE", "ABNORMAL_VOLUME", "MEDIA_ATTENTION"),
            (), (), "Threshold sensitivity remains.", state != PriceRecognitionState.INSUFFICIENT_DATA,
            "Market-recognition research preview; not an EIP state, recommendation, or trade decision.",
        )

    def assessment(self, **changes):
        values = dict(
            schema_version=1, assessment_id="THESIS-REC-1", causal_chain_id="CHAIN-1",
            regime_assessment_id="REGIME-1", market_snapshot_id="MARKET-1",
            incorporation=FundamentalChangeIncorporation.LIMITED,
            thesis_related_source_ids=("SOURCE-PRICE", "SOURCE-CONSENSUS"),
            thesis_related_dimensions=("CATALYST_PRICE_REACTION", "CONSENSUS_REVISIONS"),
            evidence_rationale="Price moved modestly but consensus has not adopted the margin thesis.",
            uncertainty_statement="Private investor beliefs cannot be directly observed.", public_information_only=True,
            non_authority_statement=ThesisPriceRecognitionService.NON_AUTHORITY,
        )
        values.update(changes)
        return ThesisPriceRecognitionAssessment(**values)

    def test_small_price_rise_does_not_automatically_mean_priced_in(self):
        result = self.service.evaluate(causal_chain=self.chain, regime_assessment=self.regime,
                                       market_recognition=self.market(price_change=7.0), assessment=self.assessment())
        self.assertEqual(result.decision, ThesisRecognitionDecision.ALLOW_EIP_REVIEW)
        self.assertFalse(result.hard_veto)

    def test_same_change_mostly_recognized_is_hard_too_late_veto(self):
        result = self.service.evaluate(
            causal_chain=self.chain, regime_assessment=self.regime, market_recognition=self.market(),
            assessment=self.assessment(incorporation=FundamentalChangeIncorporation.MOST_OR_ALL))
        self.assertEqual(result.decision, ThesisRecognitionDecision.VETO_TOO_LATE)
        self.assertTrue(result.hard_veto)

    def test_broad_market_fully_recognized_remains_hard_veto(self):
        result = self.service.evaluate(
            causal_chain=self.chain, regime_assessment=self.regime,
            market_recognition=self.market(state=PriceRecognitionState.FULLY_RECOGNIZED_POTENTIALLY_LATE),
            assessment=self.assessment(incorporation=FundamentalChangeIncorporation.LIMITED))
        self.assertEqual(result.decision, ThesisRecognitionDecision.VETO_TOO_LATE)

    def test_insufficient_recognition_evidence_holds_instead_of_guessing(self):
        result = self.service.evaluate(
            causal_chain=self.chain, regime_assessment=self.regime, market_recognition=self.market(),
            assessment=self.assessment(incorporation=FundamentalChangeIncorporation.INSUFFICIENT_EVIDENCE,
                                       thesis_related_source_ids=(), thesis_related_dimensions=()))
        self.assertEqual(result.decision, ThesisRecognitionDecision.HOLD_INSUFFICIENT_EVIDENCE)

    def test_requires_exact_thesis_and_market_bindings(self):
        with self.assertRaisesRegex(ValueError, "bind to causal chain"):
            self.service.evaluate(causal_chain=self.chain, regime_assessment=self.regime,
                                  market_recognition=self.market(), assessment=self.assessment(causal_chain_id="OTHER"))
        with self.assertRaisesRegex(ValueError, "bind to market snapshot"):
            self.service.evaluate(causal_chain=self.chain, regime_assessment=self.regime,
                                  market_recognition=self.market(), assessment=self.assessment(market_snapshot_id="OTHER"))

    def test_recognition_conclusion_requires_thesis_related_evidence(self):
        with self.assertRaisesRegex(ValueError, "requires thesis-related"):
            self.service.evaluate(
                causal_chain=self.chain, regime_assessment=self.regime, market_recognition=self.market(),
                assessment=self.assessment(thesis_related_source_ids=(), thesis_related_dimensions=()))


if __name__ == "__main__":
    unittest.main()
