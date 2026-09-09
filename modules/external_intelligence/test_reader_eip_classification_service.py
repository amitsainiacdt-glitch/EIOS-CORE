import unittest
from datetime import datetime, timezone

from modules.external_intelligence.causal_first_eip_packet import CausalFirstEIPDecisionPacket, CausalFirstEIPPacketDecision
from modules.external_intelligence.eip_classification import EIPClassificationPreview, EIPRiskDisposition, EIPStage, EIPValuationRoom
from modules.external_intelligence.eip_repository import EIPRepository, StoredEIPClassification
from modules.external_intelligence.eip_review import EIPReviewDecision, EIPReviewReceipt
from modules.external_intelligence.reader_eip_classification import ReaderEIPClassification
from modules.external_intelligence.reader_eip_classification_service import ReaderEIPClassificationService
from modules.external_intelligence import test_causal_first_eip_packet_service as packet_fixture_module


class ReaderEIPClassificationServiceTests(unittest.TestCase):
    def setUp(self):
        fixture = packet_fixture_module.CausalFirstEIPPacketServiceTests()
        fixture.setUp()
        self.packet = fixture.service.assemble(**fixture.inputs())
        self.service = ReaderEIPClassificationService()

    def packet_with(self, decision, reasons=()):
        return CausalFirstEIPDecisionPacket(**{**self.packet.__dict__, "decision": decision,
                                               "reason_codes": reasons,
                                               "all_components_ready": decision == CausalFirstEIPPacketDecision.READY_FOR_GOVERNED_EIP_CLASSIFICATION})

    def stored(self, stage):
        item = EIPClassificationPreview(
            "EIP-1", self.packet.pre_inflection_preview_id, "a" * 64, "MARKET-1", "b" * 64,
            "PRICE-REVIEW-1", stage, "CREDIBLE", "UNRECOGNIZED", EIPRiskDisposition.CONTAINED,
            EIPValuationRoom.SUFFICIENT, (), "Risks contained", "Valuation room exists",
            ("Results later confirm",), ("Causal indicator reverses",), True,
            "Research-stage EIP classification; not an investment recommendation, approval, position, or trade instruction.")
        fingerprint = EIPRepository.fingerprint_payload(EIPRepository.classification_payload(item))
        return StoredEIPClassification(fingerprint, item)

    @staticmethod
    def review(stored, decision):
        return EIPReviewReceipt(1, "EIP-REVIEW-1", stored.classification.classification_id,
            stored.classification_fingerprint, stored.classification.stage.value, decision,
            "Human reviewed the governed classification.", datetime(2026, 9, 9, tzinfo=timezone.utc), "Reviewer")

    def test_packet_holds_map_to_research_wait_or_reject(self):
        research = self.packet_with(CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH, ("MANDATORY_META_NOT_READY",))
        self.assertEqual(self.service.classify(packet=research).classification, ReaderEIPClassification.RESEARCH_NOW)
        wait = self.packet_with(CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH, ("NORMALIZED_VALUATION_NOT_READY",))
        self.assertEqual(self.service.classify(packet=wait).classification, ReaderEIPClassification.WAIT)
        noise = self.packet_with(CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH, ("CHANGE_REGIME_NOT_EIP_ELIGIBLE",))
        self.assertEqual(self.service.classify(packet=noise).classification, ReaderEIPClassification.REJECT)

    def test_hard_vetoes_map_to_too_late_or_reject(self):
        late = self.packet_with(CausalFirstEIPPacketDecision.VETO_TOO_LATE)
        self.assertEqual(self.service.classify(packet=late).classification, ReaderEIPClassification.TOO_LATE)
        failed = self.packet_with(CausalFirstEIPPacketDecision.VETO_SURVIVABILITY_FAILURE)
        self.assertEqual(self.service.classify(packet=failed).classification, ReaderEIPClassification.REJECT)

    def test_ready_packet_without_governed_classification_is_early_watch(self):
        result = self.service.classify(packet=self.packet)
        self.assertEqual(result.classification, ReaderEIPClassification.EARLY_WATCH)
        self.assertFalse(result.creates_investment_decision)

    def test_reviewed_stage_three_maps_to_eip(self):
        stored = self.stored(EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT)
        result = self.service.classify(packet=self.packet, stored_eip=stored,
                                       eip_review=self.review(stored, EIPReviewDecision.AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW))
        self.assertEqual(result.classification, ReaderEIPClassification.EARLIEST_INVESTABLE_POINT)

    def test_buy_zone_requires_reviewed_stage_four(self):
        stored = self.stored(EIPStage.STAGE_4_EARLY_CONFIRMATION)
        self.assertEqual(self.service.classify(packet=self.packet, stored_eip=stored).classification,
                         ReaderEIPClassification.EARLY_WATCH)
        result = self.service.classify(packet=self.packet, stored_eip=stored,
                                       eip_review=self.review(stored, EIPReviewDecision.AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW))
        self.assertEqual(result.classification, ReaderEIPClassification.BUY_ZONE_CANDIDATE)
        self.assertFalse(result.creates_investment_decision)

    def test_human_hold_and_reject_remain_visible(self):
        stored = self.stored(EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT)
        held = self.service.classify(packet=self.packet, stored_eip=stored,
                                     eip_review=self.review(stored, EIPReviewDecision.HOLD_EIP_RESEARCH))
        self.assertEqual(held.classification, ReaderEIPClassification.WAIT)
        rejected = self.service.classify(packet=self.packet, stored_eip=stored,
            eip_review=self.review(stored, EIPReviewDecision.REJECT_EIP_CLASSIFICATION))
        self.assertEqual(rejected.classification, ReaderEIPClassification.REJECT)

    def test_stale_internal_classification_or_review_is_rejected(self):
        stored = self.stored(EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT)
        wrong_item = EIPClassificationPreview(**{**stored.classification.__dict__, "pre_inflection_preview_id": "OTHER"})
        wrong = StoredEIPClassification(EIPRepository.fingerprint_payload(EIPRepository.classification_payload(wrong_item)), wrong_item)
        with self.assertRaisesRegex(ValueError, "does not bind"):
            self.service.classify(packet=self.packet, stored_eip=wrong)
        review = EIPReviewReceipt(**{**self.review(stored, EIPReviewDecision.AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW).__dict__,
                                    "classification_fingerprint": "c" * 64})
        with self.assertRaisesRegex(ValueError, "review does not bind"):
            self.service.classify(packet=self.packet, stored_eip=stored, eip_review=review)


if __name__ == "__main__":
    unittest.main()
