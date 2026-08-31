from dataclasses import replace

from modules.external_intelligence.pre_inflection_calibration import HypothesisCalibrationReport
from modules.external_intelligence.pre_inflection_calibration_drift import assess_calibration_drift


def _report(identity,hit,confidence,gap,brier,ready=True):
    return HypothesisCalibrationReport(identity,25,25,0,0,hit,confidence,gap,brier,ready,())


def main():
    baseline=_report("2026-H1",72,70,-2,0.19)
    stable=assess_calibration_drift(baseline=baseline,recent=_report("2026-H2",70,71,1,0.21)); assert stable.status=="NO_MATERIAL_DRIFT" and not stable.review_required
    drift=assess_calibration_drift(baseline=baseline,recent=_report("2027-H1",50,75,25,0.31)); assert drift.status=="DRIFT_REVIEW_REQUIRED" and {"BRIER_SCORE_DETERIORATION","CALIBRATION_GAP_WIDENED","HIT_RATE_DETERIORATION"}.issubset(drift.reason_codes)
    incomplete=assess_calibration_drift(baseline=baseline,recent=replace(_report("2027-H2",50,60,10,0.25),performance_claim_ready=False,reason_codes=("SAMPLE_TOO_SMALL",)))
    assert incomplete.status=="INSUFFICIENT_FOR_DRIFT_TEST" and incomplete.review_required
    print("PRE-INFLECTION CALIBRATION DRIFT: ALL TESTS PASSED")


if __name__=="__main__": main()
