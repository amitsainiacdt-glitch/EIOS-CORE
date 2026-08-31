"""Look-ahead-safe resolution of frozen pre-inflection research hypotheses."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib,re


class HypothesisDirection(str,Enum):
    ABOVE="ABOVE"
    BELOW="BELOW"
    INCREASE="INCREASE"
    DECREASE="DECREASE"


@dataclass(frozen=True)
class FrozenPreInflectionHypothesis:
    hypothesis_id: str
    case_id: str
    metric_id: str
    geography_id: str
    direction: HypothesisDirection
    threshold_value: float
    baseline_value: float | None
    target_date: datetime
    frozen_at: datetime
    confidence_percent: float
    evidence_fingerprints: tuple[str,...]
    hypothesis_fingerprint: str
    non_authority_statement: str

    @classmethod
    def fingerprint(cls, *, hypothesis_id,case_id,metric_id,geography_id,direction,threshold_value,baseline_value,target_date,frozen_at,confidence_percent,evidence_fingerprints):
        direction=direction.value if isinstance(direction,HypothesisDirection) else str(direction)
        canonical="\n".join((hypothesis_id,case_id,metric_id,geography_id,direction,str(float(threshold_value)),str(None if baseline_value is None else float(baseline_value)),target_date.isoformat(),frozen_at.isoformat(),str(float(confidence_percent)),*evidence_fingerprints))
        return hashlib.sha256(canonical.encode()).hexdigest()


@dataclass(frozen=True)
class PublicOutcomeMeasurement:
    outcome_id: str
    metric_id: str
    geography_id: str
    reporting_date: datetime
    observed_value: float
    authority_id: str
    source_document_id: str
    source_url: str
    document_hash: str
    exact_passage: str
    acquired_at: datetime


@dataclass(frozen=True)
class HypothesisResolution:
    hypothesis_id: str
    status: str
    successful: bool | None
    reason_codes: tuple[str,...]
    evaluated_at: datetime
    score_eligible: bool
    non_authority_statement: str="Research calibration result only; not a recommendation, position, or trade."


def resolve_hypothesis(hypothesis,outcome,*,evaluated_at):
    if not isinstance(hypothesis,FrozenPreInflectionHypothesis) or not isinstance(outcome,PublicOutcomeMeasurement): raise ValueError("frozen hypothesis and public outcome are required")
    for value,name in ((hypothesis.target_date,"target_date"),(hypothesis.frozen_at,"frozen_at"),(outcome.reporting_date,"reporting_date"),(outcome.acquired_at,"acquired_at"),(evaluated_at,"evaluated_at")):
        if value.tzinfo is None: raise ValueError(f"{name} must be timezone-aware")
    expected=FrozenPreInflectionHypothesis.fingerprint(hypothesis_id=hypothesis.hypothesis_id,case_id=hypothesis.case_id,metric_id=hypothesis.metric_id,geography_id=hypothesis.geography_id,direction=hypothesis.direction,threshold_value=hypothesis.threshold_value,baseline_value=hypothesis.baseline_value,target_date=hypothesis.target_date,frozen_at=hypothesis.frozen_at,confidence_percent=hypothesis.confidence_percent,evidence_fingerprints=hypothesis.evidence_fingerprints)
    reasons=[]
    if expected!=hypothesis.hypothesis_fingerprint: reasons.append("HYPOTHESIS_FINGERPRINT_MISMATCH")
    if hypothesis.frozen_at>=hypothesis.target_date: reasons.append("HYPOTHESIS_NOT_FROZEN_BEFORE_TARGET")
    if not 0<hypothesis.confidence_percent<100: reasons.append("INVALID_CONFIDENCE")
    if not hypothesis.evidence_fingerprints or any(not re.fullmatch(r"[0-9a-f]{64}",x) for x in hypothesis.evidence_fingerprints): reasons.append("INVALID_EVIDENCE_BINDING")
    if outcome.metric_id!=hypothesis.metric_id or outcome.geography_id!=hypothesis.geography_id: reasons.append("OUTCOME_SCOPE_MISMATCH")
    if outcome.reporting_date<hypothesis.target_date: reasons.append("OUTCOME_PRECEDES_TARGET")
    if outcome.acquired_at<outcome.reporting_date: reasons.append("OUTCOME_ACQUISITION_PRECEDES_REPORT")
    if evaluated_at<outcome.acquired_at: reasons.append("EVALUATION_PRECEDES_ACQUISITION")
    if not re.fullmatch(r"[0-9a-f]{64}",outcome.document_hash): reasons.append("INVALID_OUTCOME_HASH")
    if not outcome.source_url.startswith("https://") or len(outcome.exact_passage.split())<6: reasons.append("OUTCOME_LINEAGE_INCOMPLETE")
    direction=hypothesis.direction if isinstance(hypothesis.direction,HypothesisDirection) else HypothesisDirection(hypothesis.direction)
    if direction in (HypothesisDirection.INCREASE,HypothesisDirection.DECREASE) and hypothesis.baseline_value is None: reasons.append("BASELINE_REQUIRED")
    if reasons: return HypothesisResolution(hypothesis.hypothesis_id,"INVALID_OR_INCONCLUSIVE",None,tuple(reasons),evaluated_at,False)
    if direction==HypothesisDirection.ABOVE: success=outcome.observed_value>hypothesis.threshold_value
    elif direction==HypothesisDirection.BELOW: success=outcome.observed_value<hypothesis.threshold_value
    elif direction==HypothesisDirection.INCREASE: success=outcome.observed_value-hypothesis.baseline_value>=hypothesis.threshold_value
    else: success=hypothesis.baseline_value-outcome.observed_value>=hypothesis.threshold_value
    return HypothesisResolution(hypothesis.hypothesis_id,"CONFIRMED" if success else "DISCONFIRMED",success,(),evaluated_at,True)


__all__=["HypothesisDirection","FrozenPreInflectionHypothesis","PublicOutcomeMeasurement","HypothesisResolution","resolve_hypothesis"]
