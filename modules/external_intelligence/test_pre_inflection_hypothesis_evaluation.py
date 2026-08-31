from dataclasses import replace
from datetime import datetime,timezone

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection,PublicOutcomeMeasurement,resolve_hypothesis


def main():
    frozen=datetime(2026,8,1,tzinfo=timezone.utc); target=datetime(2026,9,30,tzinfo=timezone.utc); evidence=("a"*64,"b"*64)
    values=dict(hypothesis_id="H-1",case_id="C-1",metric_id="MAIZE_AREA_GAP_LHA",geography_id="INDIA",direction=HypothesisDirection.BELOW,threshold_value=-2.0,baseline_value=None,target_date=target,frozen_at=frozen,confidence_percent=70.0,evidence_fingerprints=evidence)
    fingerprint=FrozenPreInflectionHypothesis.fingerprint(**values)
    hypothesis=FrozenPreInflectionHypothesis(**values,hypothesis_fingerprint=fingerprint,non_authority_statement="Research hypothesis only.")
    outcome=PublicOutcomeMeasurement("O-1","MAIZE_AREA_GAP_LHA","INDIA",target,-3.1,"AGRI_MINISTRY","DOC-1","https://agri.example/doc","c"*64,"Official report records the final maize area gap below prior year.",datetime(2026,10,1,tzinfo=timezone.utc))
    confirmed=resolve_hypothesis(hypothesis,outcome,evaluated_at=datetime(2026,10,2,tzinfo=timezone.utc)); assert confirmed.status=="CONFIRMED" and confirmed.score_eligible
    wrong=resolve_hypothesis(hypothesis,replace(outcome,observed_value=-1.0),evaluated_at=datetime(2026,10,2,tzinfo=timezone.utc)); assert wrong.status=="DISCONFIRMED" and wrong.successful is False
    tampered=resolve_hypothesis(replace(hypothesis,threshold_value=-4.0),outcome,evaluated_at=datetime(2026,10,2,tzinfo=timezone.utc)); assert "HYPOTHESIS_FINGERPRINT_MISMATCH" in tampered.reason_codes and not tampered.score_eligible
    early=resolve_hypothesis(hypothesis,replace(outcome,reporting_date=datetime(2026,9,1,tzinfo=timezone.utc)),evaluated_at=datetime(2026,10,2,tzinfo=timezone.utc)); assert "OUTCOME_PRECEDES_TARGET" in early.reason_codes
    print("PRE-INFLECTION HYPOTHESIS EVALUATION: ALL TESTS PASSED")


if __name__=="__main__": main()
