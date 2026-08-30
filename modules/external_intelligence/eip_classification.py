"""Passive Earliest Investable Point classification preview."""

from dataclasses import dataclass
from enum import Enum


class EIPStage(str, Enum):
    NOT_CLASSIFIABLE = "NOT_CLASSIFIABLE"
    STAGE_0_DETERIORATION = "STAGE_0_DETERIORATION"
    STAGE_1_POSSIBLE_BOTTOMING = "STAGE_1_POSSIBLE_BOTTOMING"
    STAGE_2_PRE_INFLECTION = "STAGE_2_PRE_INFLECTION"
    STAGE_3_EARLIEST_INVESTABLE_POINT = "STAGE_3_EARLIEST_INVESTABLE_POINT"
    STAGE_4_EARLY_CONFIRMATION = "STAGE_4_EARLY_CONFIRMATION"
    STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE = "STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE"


class EIPRiskDisposition(str, Enum):
    CLEAR = "CLEAR"
    CONTAINED = "CONTAINED"
    UNRESOLVED = "UNRESOLVED"


class EIPValuationRoom(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    UNCERTAIN = "UNCERTAIN"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class EIPClassificationPreview:
    classification_id: str
    pre_inflection_preview_id: str
    pre_inflection_fingerprint: str
    recognition_snapshot_id: str
    recognition_fingerprint: str
    price_recognition_review_id: str
    stage: EIPStage
    pre_inflection_strength: str
    price_recognition_state: str
    risk_disposition: EIPRiskDisposition
    valuation_room: EIPValuationRoom
    reason_codes: tuple[str, ...]
    risk_rationale: str
    valuation_rationale: str
    confirmation_requirements: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    eligible_for_human_eip_review: bool
    non_authority_statement: str


__all__ = ["EIPClassificationPreview", "EIPRiskDisposition", "EIPStage", "EIPValuationRoom"]
