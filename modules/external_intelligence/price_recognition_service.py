"""Multi-dimensional Price Recognition Gate; no EIP or trade decision."""

from dataclasses import dataclass

from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview
from modules.external_intelligence.pre_inflection_repository import PreInflectionRepository, StoredPreInflectionAssessment
from modules.external_intelligence.pre_inflection_review import PreInflectionReviewDecision, PreInflectionReviewReceipt
from modules.external_intelligence.price_recognition import PriceRecognitionPreview, PriceRecognitionState, PublicMarketRecognitionSnapshot


@dataclass(frozen=True)
class PriceRecognitionPolicy:
    anchor_price_change_pct: float = 20.0
    sector_relative_return_pct: float = 10.0
    week_52_position: float = 0.75
    abnormal_volume_ratio: float = 1.5
    valuation_rerating_pct: float = 15.0
    analyst_revision_breadth: float = 0.40
    media_attention_change_pct: float = 50.0
    momentum_return_pct: float = 10.0
    minimum_available_dimensions: int = 4


class PriceRecognitionService:
    NON_AUTHORITY = "Market-recognition research preview; not an EIP state, recommendation, or trade decision."

    def __init__(self, policy=None): self.policy = policy or PriceRecognitionPolicy()

    def preview(self, *, stored_pre_inflection, current_pre_inflection, pre_inflection_review, market_snapshot):
        if not isinstance(stored_pre_inflection, StoredPreInflectionAssessment): raise ValueError("stored_pre_inflection is invalid")
        if not isinstance(current_pre_inflection, PreInflectionAssessmentPreview): raise ValueError("current_pre_inflection is invalid")
        if not isinstance(pre_inflection_review, PreInflectionReviewReceipt): raise ValueError("pre_inflection_review is invalid")
        if not isinstance(market_snapshot, PublicMarketRecognitionSnapshot): raise ValueError("market_snapshot is invalid")
        expected = PreInflectionRepository.fingerprint_payload(PreInflectionRepository.preview_payload(stored_pre_inflection.preview))
        if stored_pre_inflection.preview_fingerprint != expected: raise ValueError("stored Pre-Inflection fingerprint mismatch")
        if current_pre_inflection != stored_pre_inflection.preview: raise ValueError("Pre-Inflection assessment is stale")
        if pre_inflection_review.preview_id != stored_pre_inflection.preview.preview_id or pre_inflection_review.preview_fingerprint != expected: raise ValueError("Pre-Inflection review does not bind to assessment")
        if pre_inflection_review.decision != PreInflectionReviewDecision.AUTHORIZE_PRICE_RECOGNITION_REVIEW: raise ValueError("Price Recognition requires human authorization")
        if not market_snapshot.public_information_only: raise ValueError("Price Recognition accepts public information only")
        if market_snapshot.entity.casefold() not in {item.casefold() for item in current_pre_inflection.entity_scope}: raise ValueError("market snapshot entity is outside Pre-Inflection scope")
        if not market_snapshot.source_ids: raise ValueError("market snapshot requires source identity")
        if market_snapshot.anchor_price <= 0 or market_snapshot.current_price <= 0: raise ValueError("market prices must be positive")
        if market_snapshot.abnormal_volume_ratio is not None and market_snapshot.abnormal_volume_ratio < 0: raise ValueError("abnormal_volume_ratio must be non-negative")
        if market_snapshot.analyst_revision_breadth is not None and not -1.0 <= market_snapshot.analyst_revision_breadth <= 1.0: raise ValueError("analyst_revision_breadth must be between -1 and 1")

        price_change = (market_snapshot.current_price / market_snapshot.anchor_price - 1.0) * 100.0
        position = None
        if market_snapshot.week_52_low is not None and market_snapshot.week_52_high is not None:
            if market_snapshot.week_52_low <= 0 or market_snapshot.week_52_high <= market_snapshot.week_52_low: raise ValueError("52-week range is invalid")
            position = max(0.0, min(1.0, (market_snapshot.current_price - market_snapshot.week_52_low) / (market_snapshot.week_52_high - market_snapshot.week_52_low)))
        horizon_returns = tuple(value for value in (market_snapshot.return_1m_pct, market_snapshot.return_3m_pct, market_snapshot.return_6m_pct, market_snapshot.return_12m_pct) if value is not None)
        momentum_count = sum(value >= self.policy.momentum_return_pct for value in horizon_returns) if len(horizon_returns) >= 3 else None
        values = {
            "ANCHOR_PRICE": (price_change, self.policy.anchor_price_change_pct),
            "MULTI_HORIZON_MOMENTUM": (momentum_count, 2),
            "SECTOR_RELATIVE": (market_snapshot.sector_relative_return_pct, self.policy.sector_relative_return_pct),
            "WEEK_52_POSITION": (position, self.policy.week_52_position),
            "ABNORMAL_VOLUME": (market_snapshot.abnormal_volume_ratio, self.policy.abnormal_volume_ratio),
            "VALUATION_RERATING": (market_snapshot.valuation_rerating_pct, self.policy.valuation_rerating_pct),
            "ANALYST_REVISIONS": (market_snapshot.analyst_revision_breadth, self.policy.analyst_revision_breadth),
            "MEDIA_ATTENTION": (market_snapshot.media_attention_change_pct, self.policy.media_attention_change_pct),
        }
        available = tuple(name for name, (value, _) in values.items() if value is not None)
        missing = tuple(name for name in values if name not in available)
        recognized = tuple(name for name, (value, threshold) in values.items() if value is not None and value >= threshold)
        reasons = []
        if len(available) < self.policy.minimum_available_dimensions:
            state = PriceRecognitionState.INSUFFICIENT_DATA; reasons.append("MARKET_DATA_COVERAGE_INSUFFICIENT")
        elif len(recognized) <= 1:
            state = PriceRecognitionState.UNRECOGNIZED
        elif len(recognized) == 2:
            state = PriceRecognitionState.EARLY_RECOGNITION
        elif len(recognized) <= 4:
            state = PriceRecognitionState.PARTIALLY_RECOGNIZED
        else:
            state = PriceRecognitionState.FULLY_RECOGNIZED_POTENTIALLY_LATE
        if missing: reasons.append("MARKET_DIMENSIONS_MISSING")
        eligible = state in (PriceRecognitionState.UNRECOGNIZED, PriceRecognitionState.EARLY_RECOGNITION, PriceRecognitionState.PARTIALLY_RECOGNIZED)
        uncertainty = "Recognition is a multi-dimensional public-market estimate; missing dimensions and threshold sensitivity remain explicit."
        return PriceRecognitionPreview(
            market_snapshot.snapshot_id, current_pre_inflection.preview_id, expected, pre_inflection_review.review_id,
            state, price_change, position, recognized, available, missing, tuple(reasons), uncertainty, eligible, self.NON_AUTHORITY,
        )


__all__ = ["PriceRecognitionPolicy", "PriceRecognitionService"]
