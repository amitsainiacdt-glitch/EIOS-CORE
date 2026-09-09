import unittest
from datetime import datetime, timezone

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.causal_first_eip_packet import CausalFirstEIPPacketDecision
from modules.external_intelligence.causal_first_eip_packet_service import CausalFirstEIPPacketService
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment, RegimeConfidence
from modules.external_intelligence.change_regime_service import ChangeRegimeService
from modules.external_intelligence.eip_expectation_gap import *
from modules.external_intelligence.eip_expectation_gap_service import EIPExpectationGapService
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaGateDecision, MandatoryMetaGateResult
from modules.external_intelligence.normalized_valuation import *
from modules.external_intelligence.normalized_valuation_service import NormalizedValuationService
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview, PreInflectionStrength
from modules.external_intelligence.survivability import *
from modules.external_intelligence.survivability_service import SurvivabilityService
from modules.external_intelligence.thesis_price_recognition import *
from modules.external_intelligence.thesis_price_recognition_service import ThesisPriceRecognitionService


class CausalFirstEIPPacketServiceTests(unittest.TestCase):
    def setUp(self):
        now = datetime(2026, 9, 9, tzinfo=timezone.utc)
        horizon = datetime(2027, 3, 31, tzinfo=timezone.utc)
        links = tuple(CausalChainLink(stage, f"Statement {stage.value}", f"Mechanism {stage.value}",
                                      ("TE-1",) if index == 0 else ()) for index, stage in enumerate(CausalChainStage))
        self.chain = CausalChainAssessment(1, "CHAIN-1", "Example", "CHEMICALS", ("IND-1",), ("TE-1",), links,
                                            (2, 4), ("Assumption",), "Uncertain timing", True, CausalChainService.NON_AUTHORITY)
        self.pre_inflection = PreInflectionAssessmentPreview(
            1, "PRE-1", "META-1", "b" * 64, "META-REVIEW-1", ("Example",), ("CHEMICALS",),
            ("IND-1",), PreInflectionStrength.CREDIBLE, 2, True, (2, 4), "LOW", (), (), (), (),
            "Some timing uncertainty remains.", "Input economics are improving.", "Independent evidence now agrees.",
            ("Margins respond later.",), ("Spread reverses.",), ("Liquidity remains adequate.",),
            "NOT_ASSESSED", True,
            "Research-stage Pre-Inflection preview; not a Signal, EIP state, Opportunity, recommendation, or trade decision.")
        self.regime = ChangeRegimeAssessment(1, "REGIME-1", "CHAIN-1", ChangeRegime.CYCLICAL, RegimeConfidence.MODERATE,
                                              ("TE-1",), ("Basis",), ("Alternative",), ("Test",), "Uncertain", True,
                                              ChangeRegimeService.NON_AUTHORITY)
        self.recognition_assessment = ThesisPriceRecognitionAssessment(
            1, "REC-1", "CHAIN-1", "REGIME-1", "MARKET-1", FundamentalChangeIncorporation.LIMITED,
            ("PRICE",), ("CATALYST_PRICE_REACTION",), "Same-thesis evidence", "Beliefs uncertain", True,
            ThesisPriceRecognitionService.NON_AUTHORITY)
        self.recognition = ThesisPriceRecognitionGateResult(ThesisRecognitionDecision.ALLOW_EIP_REVIEW,
            FundamentalChangeIncorporation.LIMITED, (), "REC-1", False, ThesisPriceRecognitionService.NON_AUTHORITY)
        measure_market = GovernedExpectationMeasure("MARGIN", "PERCENT", horizon, 12, ("CONSENSUS",), "Market expects 12")
        measure_eios = GovernedExpectationMeasure("MARGIN", "PERCENT", horizon, 16, ("EVIDENCE",), "Evidence implies 16")
        self.gap_assessment = EIPExpectationGapAssessment(
            1, "GAP-1", "CHAIN-1", "REGIME-1", "REC-1", measure_market, measure_eios,
            FavorableMetricDirection.HIGHER, ExpectationGapDirection.POSITIVE, ExpectationGapMateriality.MODERATE,
            "Material earnings effect", ("Volumes stable",), (), ("Spread reverses",), "Timing uncertain", True,
            EIPExpectationGapService.NON_AUTHORITY)
        self.gap = EIPExpectationGapResult("GAP-1", "MARGIN", "PERCENT", horizon, 12, 16, 4, 33.33,
            ExpectationGapDirection.POSITIVE, ExpectationGapMateriality.MODERATE, True, (), EIPExpectationGapService.NON_AUTHORITY)
        scenarios = tuple(NormalizedOperatingScenario(kind, 1000 + index * 100, 8 + index * 4, 8 + index * 2,
                          (f"SOURCE-{index}",), "Scenario rationale") for index, kind in enumerate(NormalizedScenarioKind))
        self.valuation_assessment = NormalizedValuationAssessment(1, "VALUE-1", "GAP-1", "INR", 100, ("PRICE",),
            100, 10, scenarios, ("Debt stable",), "Scenario uncertainty", True, NormalizedValuationService.NON_AUTHORITY)
        self.valuation = NormalizedValuationResult("VALUE-1", "INR", 100, (), NormalizedValuationRoom.SUFFICIENT,
                                                   True, (), NormalizedValuationService.NON_AUTHORITY)
        self.survival_assessment = SurvivabilityAssessment(1, "SURVIVE-1", "CHAIN-1", "VALUE-1", now, "INR",
            150, 50, 20, 100, 200, 100, 20, 5, False, False, (), ("BALANCE-SHEET",), ("Facility available",),
            "Working capital uncertain", True, SurvivabilityService.NON_AUTHORITY)
        self.survival = SurvivabilityGateResult("SURVIVE-1", 4, 200, 120, 1.67, 2, 5, 5,
            SurvivabilityDecision.CONTAINED, False, True, (), SurvivabilityService.NON_AUTHORITY)
        self.meta = MandatoryMetaGateResult(MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION, (), "META-1", ("TE-1",))
        self.service = CausalFirstEIPPacketService()

    def inputs(self, **changes):
        values = dict(packet_id="PACKET-1", meta_gate=self.meta, pre_inflection=self.pre_inflection, causal_chain=self.chain,
            regime_assessment=self.regime, recognition_assessment=self.recognition_assessment,
            recognition_gate=self.recognition, expectation_gap_assessment=self.gap_assessment,
            expectation_gap=self.gap, normalized_valuation_assessment=self.valuation_assessment,
            normalized_valuation=self.valuation, survivability_assessment=self.survival_assessment,
            survivability=self.survival)
        values.update(changes)
        return values

    def test_ready_packet_keeps_separate_fingerprints_and_creates_no_eip(self):
        packet = self.service.assemble(**self.inputs())
        self.assertEqual(packet.decision, CausalFirstEIPPacketDecision.READY_FOR_GOVERNED_EIP_CLASSIFICATION)
        self.assertEqual(len(packet.component_fingerprints), 12)
        self.assertTrue(all(len(value) == 64 for _, value in packet.component_fingerprints))
        self.assertTrue(packet.all_components_ready)
        self.assertFalse(packet.creates_eip)
        self.assertFalse(hasattr(packet, "combined_score"))

    def test_meta_or_component_hold_prevents_readiness(self):
        held_meta = MandatoryMetaGateResult(MandatoryMetaGateDecision.HOLD_FOR_RESEARCH, ("MORE_EVIDENCE",), "META-1", ("TE-1",))
        packet = self.service.assemble(**self.inputs(meta_gate=held_meta))
        self.assertEqual(packet.decision, CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH)
        self.assertIn("MANDATORY_META_NOT_READY", packet.reason_codes)
        held_gap = EIPExpectationGapResult(**{**self.gap.__dict__, "eligible_for_eip_assembly": False})
        self.assertEqual(self.service.assemble(**self.inputs(expectation_gap=held_gap)).decision,
                         CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH)

    def test_too_late_and_survivability_are_hard_vetoes(self):
        late = ThesisPriceRecognitionGateResult(ThesisRecognitionDecision.VETO_TOO_LATE,
            FundamentalChangeIncorporation.MOST_OR_ALL, ("PRICED",), "REC-1", True,
            ThesisPriceRecognitionService.NON_AUTHORITY)
        self.assertEqual(self.service.assemble(**self.inputs(recognition_gate=late)).decision,
                         CausalFirstEIPPacketDecision.VETO_TOO_LATE)
        failed = SurvivabilityGateResult(**{**self.survival.__dict__, "decision": SurvivabilityDecision.VETO_SURVIVABILITY_FAILURE,
                                            "hard_veto": True, "eligible_for_eip_assembly": False})
        self.assertEqual(self.service.assemble(**self.inputs(recognition_gate=late, survivability=failed)).decision,
                         CausalFirstEIPPacketDecision.VETO_SURVIVABILITY_FAILURE)

    def test_noise_or_speculative_narrative_holds(self):
        noise = ChangeRegimeAssessment(**{**self.regime.__dict__, "regime": ChangeRegime.STATISTICAL_NOISE,
                                           "confidence": RegimeConfidence.LOW})
        packet = self.service.assemble(**self.inputs(regime_assessment=noise))
        self.assertIn("CHANGE_REGIME_NOT_EIP_ELIGIBLE", packet.reason_codes)

    def test_stale_cross_component_binding_is_rejected(self):
        stale = EIPExpectationGapAssessment(**{**self.gap_assessment.__dict__, "causal_chain_id": "OTHER"})
        with self.assertRaisesRegex(ValueError, "gap/causal chain"):
            self.service.assemble(**self.inputs(expectation_gap_assessment=stale))
        wrong_meta = MandatoryMetaGateResult(MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION, (), "META-1", ("TE-2",))
        with self.assertRaisesRegex(ValueError, "Mandatory Meta evidence"):
            self.service.assemble(**self.inputs(meta_gate=wrong_meta))

    def test_any_component_change_changes_its_fingerprint(self):
        first = dict(self.service.assemble(**self.inputs()).component_fingerprints)
        changed = SurvivabilityAssessment(**{**self.survival_assessment.__dict__, "cash_and_liquid_investments": 151})
        second = dict(self.service.assemble(**self.inputs(survivability_assessment=changed)).component_fingerprints)
        self.assertNotEqual(first["survivability_assessment"], second["survivability_assessment"])
        self.assertEqual(first["causal_chain"], second["causal_chain"])


if __name__ == "__main__":
    unittest.main()
