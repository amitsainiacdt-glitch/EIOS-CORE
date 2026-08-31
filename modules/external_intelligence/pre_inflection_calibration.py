"""Complete-cohort calibration for resolved pre-inflection hypotheses."""

from dataclasses import dataclass

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisResolution


@dataclass(frozen=True)
class HypothesisCalibrationReport:
    cohort_id: str
    expected_count: int
    resolved_scoreable_count: int
    inconclusive_count: int
    missing_count: int
    hit_rate_percent: float | None
    mean_confidence_percent: float | None
    calibration_gap_points: float | None
    brier_score: float | None
    performance_claim_ready: bool
    reason_codes: tuple[str,...]
    non_authority_statement: str="Research process calibration only; not evidence of future returns or investment skill."


def build_hypothesis_calibration_report(*,cohort_id,expected_hypothesis_ids,hypotheses,resolutions,minimum_sample_size=20):
    expected=tuple(expected_hypothesis_ids)
    if not cohort_id.strip() or not expected: raise ValueError("cohort identity and expected hypotheses are required")
    if len(set(expected))!=len(expected): raise ValueError("expected hypothesis identities must be unique")
    hypotheses=tuple(hypotheses); resolutions=tuple(resolutions)
    hyp={item.hypothesis_id:item for item in hypotheses if isinstance(item,FrozenPreInflectionHypothesis)}
    res={item.hypothesis_id:item for item in resolutions if isinstance(item,HypothesisResolution)}
    if len(hyp)!=len(hypotheses) or len(res)!=len(resolutions): raise ValueError("hypotheses and resolutions must be typed and unique")
    unexpected=(set(hyp)|set(res))-set(expected)
    if unexpected: raise ValueError("cohort contains unexpected hypothesis identities")
    missing=[item for item in expected if item not in hyp or item not in res]
    scoreable=[]; inconclusive=0
    for identity in expected:
        if identity in missing: continue
        hypothesis,resolution=hyp[identity],res[identity]
        if resolution.status in ("CONFIRMED","DISCONFIRMED") and resolution.score_eligible and resolution.successful is not None:
            scoreable.append((hypothesis.confidence_percent/100.0,1.0 if resolution.successful else 0.0))
        else: inconclusive+=1
    count=len(scoreable); reasons=[]
    if missing: reasons.append("INCOMPLETE_COHORT")
    if count<minimum_sample_size: reasons.append("SAMPLE_TOO_SMALL")
    if not scoreable: hit=confidence=gap=brier=None
    else:
        hit=round(100*sum(actual for _,actual in scoreable)/count,2)
        confidence=round(100*sum(probability for probability,_ in scoreable)/count,2)
        gap=round(confidence-hit,2)
        brier=round(sum((probability-actual)**2 for probability,actual in scoreable)/count,4)
    ready=not reasons
    return HypothesisCalibrationReport(cohort_id,len(expected),count,inconclusive,len(missing),hit,confidence,gap,brier,ready,tuple(reasons))


__all__=["HypothesisCalibrationReport","build_hypothesis_calibration_report"]
