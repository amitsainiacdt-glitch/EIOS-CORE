"""Governed EIP stage preview; no recommendation or portfolio action."""

from modules.external_intelligence.eip_classification import EIPClassificationPreview, EIPRiskDisposition, EIPStage, EIPValuationRoom
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview, PreInflectionStrength
from modules.external_intelligence.pre_inflection_repository import PreInflectionRepository, StoredPreInflectionAssessment
from modules.external_intelligence.price_recognition import PriceRecognitionPreview, PriceRecognitionState
from modules.external_intelligence.price_recognition_repository import PriceRecognitionRepository, StoredPriceRecognition
from modules.external_intelligence.price_recognition_review import PriceRecognitionReviewDecision, PriceRecognitionReviewReceipt


class EIPClassificationService:
    NON_AUTHORITY = "Research-stage EIP classification; not an investment recommendation, approval, position, or trade instruction."

    def classify(
        self, *, classification_id, stored_pre_inflection, current_pre_inflection,
        stored_recognition, current_recognition, recognition_review,
        risk_disposition, risk_rationale, valuation_room, valuation_rationale,
    ):
        if not isinstance(stored_pre_inflection, StoredPreInflectionAssessment): raise ValueError("stored_pre_inflection is invalid")
        if not isinstance(current_pre_inflection, PreInflectionAssessmentPreview): raise ValueError("current_pre_inflection is invalid")
        if not isinstance(stored_recognition, StoredPriceRecognition): raise ValueError("stored_recognition is invalid")
        if not isinstance(current_recognition, PriceRecognitionPreview): raise ValueError("current_recognition is invalid")
        if not isinstance(recognition_review, PriceRecognitionReviewReceipt): raise ValueError("recognition_review is invalid")
        pre_fingerprint = PreInflectionRepository.fingerprint_payload(PreInflectionRepository.preview_payload(stored_pre_inflection.preview))
        recognition_fingerprint = PriceRecognitionRepository.fingerprint_payload(PriceRecognitionRepository.preview_payload(stored_recognition.preview))
        if stored_pre_inflection.preview_fingerprint != pre_fingerprint or current_pre_inflection != stored_pre_inflection.preview: raise ValueError("Pre-Inflection assessment is stale or altered")
        if stored_recognition.recognition_fingerprint != recognition_fingerprint or current_recognition != stored_recognition.preview: raise ValueError("Price Recognition assessment is stale or altered")
        if current_recognition.pre_inflection_fingerprint != pre_fingerprint: raise ValueError("Price Recognition does not bind to Pre-Inflection")
        if recognition_review.snapshot_id != current_recognition.snapshot_id or recognition_review.recognition_fingerprint != recognition_fingerprint: raise ValueError("Price Recognition review does not bind to assessment")
        risk = risk_disposition if isinstance(risk_disposition, EIPRiskDisposition) else EIPRiskDisposition(risk_disposition)
        valuation = valuation_room if isinstance(valuation_room, EIPValuationRoom) else EIPValuationRoom(valuation_room)
        risk_rationale, valuation_rationale = self._text(risk_rationale), self._text(valuation_rationale)
        reasons = []
        state, strength = current_recognition.state, current_pre_inflection.strength
        if state == PriceRecognitionState.INSUFFICIENT_DATA:
            stage = EIPStage.NOT_CLASSIFIABLE; reasons.append("MARKET_RECOGNITION_DATA_INSUFFICIENT")
        elif state == PriceRecognitionState.FULLY_RECOGNIZED_POTENTIALLY_LATE:
            stage = EIPStage.STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE; reasons.append("MARKET_RECOGNITION_POTENTIALLY_LATE")
        elif strength == PreInflectionStrength.WEAK:
            stage = EIPStage.STAGE_1_POSSIBLE_BOTTOMING; reasons.append("FUNDAMENTAL_EVIDENCE_WEAK")
        elif strength == PreInflectionStrength.EMERGING:
            stage = EIPStage.STAGE_2_PRE_INFLECTION; reasons.append("FUNDAMENTAL_EVIDENCE_EMERGING")
        elif state == PriceRecognitionState.PARTIALLY_RECOGNIZED:
            stage = EIPStage.STAGE_4_EARLY_CONFIRMATION
        elif risk == EIPRiskDisposition.UNRESOLVED:
            stage = EIPStage.STAGE_2_PRE_INFLECTION; reasons.append("BALANCE_SHEET_OR_GOVERNANCE_RISK_UNRESOLVED")
        elif valuation != EIPValuationRoom.SUFFICIENT:
            stage = EIPStage.STAGE_2_PRE_INFLECTION; reasons.append("VALUATION_ROOM_NOT_ESTABLISHED")
        else:
            stage = EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT
        if recognition_review.decision != PriceRecognitionReviewDecision.AUTHORIZE_EIP_REVIEW:
            if stage not in (EIPStage.NOT_CLASSIFIABLE, EIPStage.STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE):
                reasons.append("EIP_REVIEW_NOT_AUTHORIZED")
                stage = EIPStage.NOT_CLASSIFIABLE
        eligible = stage in (EIPStage.STAGE_2_PRE_INFLECTION, EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT, EIPStage.STAGE_4_EARLY_CONFIRMATION) and recognition_review.decision == PriceRecognitionReviewDecision.AUTHORIZE_EIP_REVIEW
        return EIPClassificationPreview(
            self._text(classification_id), current_pre_inflection.preview_id, pre_fingerprint,
            current_recognition.snapshot_id, recognition_fingerprint, recognition_review.review_id,
            stage, strength.value, state.value, risk, valuation, tuple(reasons), risk_rationale,
            valuation_rationale, current_pre_inflection.confirmation_requirements,
            current_pre_inflection.invalidation_conditions, eligible, self.NON_AUTHORITY,
        )

    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()


__all__ = ["EIPClassificationService"]
