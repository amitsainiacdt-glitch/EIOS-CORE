from datetime import datetime,timezone

from modules.external_intelligence.pre_inflection_calibration import build_hypothesis_calibration_report
from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection,HypothesisResolution


def _hypothesis(identity,confidence):
    frozen=datetime(2026,1,1,tzinfo=timezone.utc); target=datetime(2026,3,31,tzinfo=timezone.utc); evidence=("a"*64,)
    values=dict(hypothesis_id=identity,case_id="C",metric_id="M",geography_id="INDIA",direction=HypothesisDirection.ABOVE,threshold_value=1.0,baseline_value=None,target_date=target,frozen_at=frozen,confidence_percent=confidence,evidence_fingerprints=evidence)
    return FrozenPreInflectionHypothesis(**values,hypothesis_fingerprint=FrozenPreInflectionHypothesis.fingerprint(**values),non_authority_statement="Research only")


def main():
    hypotheses=tuple(_hypothesis(f"H-{i}",70) for i in range(1,5)); now=datetime(2026,4,2,tzinfo=timezone.utc)
    resolutions=(HypothesisResolution("H-1","CONFIRMED",True,(),now,True),HypothesisResolution("H-2","DISCONFIRMED",False,(),now,True),HypothesisResolution("H-3","CONFIRMED",True,(),now,True),HypothesisResolution("H-4","INVALID_OR_INCONCLUSIVE",None,("OUTCOME_SCOPE_MISMATCH",),now,False))
    report=build_hypothesis_calibration_report(cohort_id="Q1",expected_hypothesis_ids=tuple(x.hypothesis_id for x in hypotheses),hypotheses=hypotheses,resolutions=resolutions,minimum_sample_size=3)
    assert report.resolved_scoreable_count==3 and report.inconclusive_count==1 and report.hit_rate_percent==66.67 and report.brier_score==0.2233 and report.performance_claim_ready
    incomplete=build_hypothesis_calibration_report(cohort_id="Q1",expected_hypothesis_ids=("H-1","H-2","H-3","H-4","H-5"),hypotheses=hypotheses,resolutions=resolutions,minimum_sample_size=3)
    assert not incomplete.performance_claim_ready and "INCOMPLETE_COHORT" in incomplete.reason_codes and incomplete.missing_count==1
    small=build_hypothesis_calibration_report(cohort_id="Q1",expected_hypothesis_ids=tuple(x.hypothesis_id for x in hypotheses),hypotheses=hypotheses,resolutions=resolutions,minimum_sample_size=20)
    assert "SAMPLE_TOO_SMALL" in small.reason_codes
    print("PRE-INFLECTION CALIBRATION: ALL TESTS PASSED")


if __name__=="__main__": main()
