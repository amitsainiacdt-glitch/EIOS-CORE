"""Maps governed EIP results to understandable labels without weakening gates."""

from modules.external_intelligence.causal_first_eip_packet import CausalFirstEIPDecisionPacket, CausalFirstEIPPacketDecision
from modules.external_intelligence.causal_first_eip_packet_service import CausalFirstEIPPacketService
from modules.external_intelligence.eip_classification import EIPStage
from modules.external_intelligence.eip_repository import EIPRepository, StoredEIPClassification
from modules.external_intelligence.eip_review import EIPReviewDecision, EIPReviewReceipt
from modules.external_intelligence.reader_eip_classification import ReaderEIPClassification, ReaderEIPClassificationResult


class ReaderEIPClassificationService:
    NON_AUTHORITY = "Plain-language research status; not a recommendation, position, order, or trade instruction."

    def classify(self, *, packet, stored_eip=None, eip_review=None):
        if not isinstance(packet, CausalFirstEIPDecisionPacket):
            raise ValueError("packet must be CausalFirstEIPDecisionPacket")
        packet_fingerprint = CausalFirstEIPPacketService.fingerprint(packet)
        stage = None
        reasons = list(packet.reason_codes)

        if packet.decision == CausalFirstEIPPacketDecision.VETO_SURVIVABILITY_FAILURE:
            label = ReaderEIPClassification.REJECT
        elif packet.decision == CausalFirstEIPPacketDecision.VETO_TOO_LATE:
            label = ReaderEIPClassification.TOO_LATE
        elif packet.decision == CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH:
            if "CHANGE_REGIME_NOT_EIP_ELIGIBLE" in reasons:
                label = ReaderEIPClassification.REJECT
            elif any(code in reasons for code in ("NORMALIZED_VALUATION_NOT_READY", "SURVIVABILITY_NOT_READY")):
                label = ReaderEIPClassification.WAIT
            else:
                label = ReaderEIPClassification.RESEARCH_NOW
        else:
            label, stage, more = self._from_governed_eip(packet, stored_eip, eip_review)
            reasons.extend(more)

        headline, explanation = self._words(label)
        return ReaderEIPClassificationResult(
            packet.packet_id, packet_fingerprint, label, None if stage is None else stage.value,
            headline, explanation, tuple(reasons), False, self.NON_AUTHORITY,
        )

    @staticmethod
    def _from_governed_eip(packet, stored_eip, eip_review):
        if stored_eip is None:
            return ReaderEIPClassification.EARLY_WATCH, None, ("GOVERNED_EIP_CLASSIFICATION_PENDING",)
        if not isinstance(stored_eip, StoredEIPClassification):
            raise ValueError("stored_eip must be StoredEIPClassification")
        expected = EIPRepository.fingerprint_payload(EIPRepository.classification_payload(stored_eip.classification))
        if stored_eip.classification_fingerprint != expected:
            raise ValueError("stored EIP classification fingerprint mismatch")
        item = stored_eip.classification
        if item.pre_inflection_preview_id != packet.pre_inflection_preview_id:
            raise ValueError("EIP classification does not bind to causal-first packet")
        stage = item.stage
        if stage == EIPStage.STAGE_0_DETERIORATION:
            return ReaderEIPClassification.REJECT, stage, ("INTERNAL_STAGE_DETERIORATION",)
        if stage == EIPStage.STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE:
            return ReaderEIPClassification.TOO_LATE, stage, ("INTERNAL_STAGE_POTENTIALLY_LATE",)
        if stage == EIPStage.NOT_CLASSIFIABLE:
            return ReaderEIPClassification.RESEARCH_NOW, stage, ("INTERNAL_STAGE_NOT_CLASSIFIABLE",)
        if stage in (EIPStage.STAGE_1_POSSIBLE_BOTTOMING, EIPStage.STAGE_2_PRE_INFLECTION):
            return ReaderEIPClassification.EARLY_WATCH, stage, ("INTERNAL_STAGE_EARLY",)
        if eip_review is None:
            return ReaderEIPClassification.EARLY_WATCH, stage, ("HUMAN_EIP_REVIEW_PENDING",)
        if not isinstance(eip_review, EIPReviewReceipt):
            raise ValueError("eip_review must be EIPReviewReceipt")
        if (eip_review.classification_id, eip_review.classification_fingerprint, eip_review.stage) != (
                item.classification_id, expected, stage.value):
            raise ValueError("EIP review does not bind to stored classification")
        if eip_review.decision == EIPReviewDecision.REJECT_EIP_CLASSIFICATION:
            return ReaderEIPClassification.REJECT, stage, ("HUMAN_EIP_REVIEW_REJECTED",)
        if eip_review.decision == EIPReviewDecision.HOLD_EIP_RESEARCH:
            return ReaderEIPClassification.WAIT, stage, ("HUMAN_EIP_REVIEW_HELD",)
        if stage == EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT:
            return ReaderEIPClassification.EARLIEST_INVESTABLE_POINT, stage, ("GOVERNED_STAGE_3_REVIEWED",)
        if stage == EIPStage.STAGE_4_EARLY_CONFIRMATION:
            return ReaderEIPClassification.BUY_ZONE_CANDIDATE, stage, ("GOVERNED_STAGE_4_REVIEWED_FOR_DOWNSTREAM_EVIDENCE",)
        raise ValueError("unsupported EIP stage")

    @staticmethod
    def _words(label):
        return {
            ReaderEIPClassification.RESEARCH_NOW: ("Research now", "The idea is important enough to investigate, but essential evidence is still missing."),
            ReaderEIPClassification.EARLY_WATCH: ("Early watch", "The causal change may be forming, but the governed EIP review is not complete."),
            ReaderEIPClassification.EARLIEST_INVESTABLE_POINT: ("Earliest Investable Point", "Independent causal evidence, recognition, expectations, valuation and survivability have passed governed review; downstream investment review is still required."),
            ReaderEIPClassification.BUY_ZONE_CANDIDATE: ("Buy-zone candidate", "The reviewed EIP has received early confirmation and may enter downstream Evidence and Opportunity review; this is not a buy instruction."),
            ReaderEIPClassification.WAIT: ("Wait", "The thesis may be interesting, but valuation, survivability or human review does not yet provide enough room to proceed."),
            ReaderEIPClassification.TOO_LATE: ("Too late", "The same fundamental improvement appears substantially recognized, so EIOS will not present it as an early opportunity."),
            ReaderEIPClassification.REJECT: ("Reject", "A hard risk, deterioration, noise, speculative narrative or reviewed failure prevents this candidate from advancing."),
        }[label]


__all__ = ["ReaderEIPClassificationService"]
