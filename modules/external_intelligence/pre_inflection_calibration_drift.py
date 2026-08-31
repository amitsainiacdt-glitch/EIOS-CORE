"""Conservative drift detection across complete hypothesis cohorts."""

from dataclasses import dataclass

from modules.external_intelligence.pre_inflection_calibration import HypothesisCalibrationReport


@dataclass(frozen=True)
class CalibrationDriftAssessment:
    status: str
    review_required: bool
    brier_change: float | None
    absolute_calibration_gap_change: float | None
    hit_rate_change_points: float | None
    reason_codes: tuple[str,...]
    permitted_action: str
    non_authority_statement: str="Research-quality control only; it cannot alter positions or make investment decisions."


def assess_calibration_drift(*,baseline,recent,brier_worsening_threshold=0.05,gap_worsening_threshold=10.0,hit_rate_drop_threshold=15.0):
    if not isinstance(baseline,HypothesisCalibrationReport) or not isinstance(recent,HypothesisCalibrationReport): raise ValueError("baseline and recent calibration reports are required")
    reasons=[]
    if baseline.cohort_id==recent.cohort_id: reasons.append("COHORTS_NOT_DISTINCT")
    if not baseline.performance_claim_ready: reasons.append("BASELINE_NOT_RELIABLE")
    if not recent.performance_claim_ready: reasons.append("RECENT_COHORT_NOT_RELIABLE")
    values=(baseline.brier_score,recent.brier_score,baseline.calibration_gap_points,recent.calibration_gap_points,baseline.hit_rate_percent,recent.hit_rate_percent)
    if any(value is None for value in values): reasons.append("CALIBRATION_METRICS_MISSING")
    if reasons:
        return CalibrationDriftAssessment("INSUFFICIENT_FOR_DRIFT_TEST",True,None,None,None,tuple(reasons),"Maintain conservative confidence and obtain a complete scoreable cohort.")
    brier=round(recent.brier_score-baseline.brier_score,4)
    gap=round(abs(recent.calibration_gap_points)-abs(baseline.calibration_gap_points),2)
    hit=round(recent.hit_rate_percent-baseline.hit_rate_percent,2)
    if brier>=brier_worsening_threshold: reasons.append("BRIER_SCORE_DETERIORATION")
    if gap>=gap_worsening_threshold: reasons.append("CALIBRATION_GAP_WIDENED")
    if hit<=-hit_rate_drop_threshold: reasons.append("HIT_RATE_DETERIORATION")
    drift=bool(reasons)
    return CalibrationDriftAssessment("DRIFT_REVIEW_REQUIRED" if drift else "NO_MATERIAL_DRIFT",drift,brier,gap,hit,tuple(reasons),"Suspend confidence escalation; review source mix, regime, thresholds, and analyst process." if drift else "Continue monitoring without automatic confidence escalation.")


__all__=["CalibrationDriftAssessment","assess_calibration_drift"]
