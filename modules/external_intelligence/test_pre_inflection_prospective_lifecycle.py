from datetime import datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.evidence_confidence_ceiling import EvidenceConfidenceCeiling
from modules.external_intelligence.mandatory_meta_review import MandatoryMetaReviewDecision,MandatoryMetaReviewReceipt
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview,PreInflectionStrength
from modules.external_intelligence.pre_inflection_calibration import build_hypothesis_calibration_report
from modules.external_intelligence.pre_inflection_case_readiness import PreInflectionCaseReadiness
from modules.external_intelligence.pre_inflection_hypothesis_evaluation import HypothesisDirection,PublicOutcomeMeasurement,HypothesisResolution
from modules.external_intelligence.pre_inflection_hypothesis_freezing_service import HypothesisScope,PreInflectionHypothesisFreezingService
from modules.external_intelligence.pre_inflection_hypothesis_ledger import PreInflectionHypothesisLedger
from modules.external_intelligence.pre_inflection_resolution_ledger import PreInflectionResolutionLedger


def main():
    frozen_at=datetime(2026,8,31,tzinfo=timezone.utc); target=datetime(2026,9,30,tzinfo=timezone.utc); evaluated=datetime(2026,10,2,tzinfo=timezone.utc)
    review=MandatoryMetaReviewReceipt(1,"REV-1","META-1","b"*64,MandatoryMetaReviewDecision.AUTHORIZE_PRE_INFLECTION_REVIEW,"READY_FOR_PRE_INFLECTION",(),"Authorized after contradiction and kill-test review.",frozen_at,"Human Reviewer")
    preview=PreInflectionAssessmentPreview(1,"PRE-1","META-1","b"*64,"REV-1",(),("AGRICULTURE",),("CROP_STAGE_WATER_STRESS",),PreInflectionStrength.CREDIBLE,3,True,(1,2),"LOW",("Irrigation may buffer stress.",),(),(),(),"Transmission remains uncertain.","Crop stress is becoming measurable.","Independent official layers converged.",("Confirm final crop outcome.",),("Crop condition normalizes.",),("No company scope.",),"NOT_ASSESSED",True,"Research only.")
    readiness=PreInflectionCaseReadiness("SECTOR_TRANSMISSION_RESEARCH_READY",True,True,False,False,(),(),"Sector research ready.")
    hypothesis=PreInflectionHypothesisFreezingService().freeze(readiness=readiness,confidence_ceiling=EvidenceConfidenceCeiling(70,True,()),pre_inflection_preview=preview,meta_review=review,scope=HypothesisScope.SECTOR,hypothesis_id="H-LIFE-1",case_id="CASE-1",metric_id="FINAL_AREA_GAP_LHA",geography_id="INDIA",direction=HypothesisDirection.BELOW,threshold_value=-2.0,baseline_value=None,target_date=target,frozen_at=frozen_at,confidence_percent=65,evidence_fingerprints=("a"*64,))
    with TemporaryDirectory() as directory:
        hypothesis_entry=PreInflectionHypothesisLedger(Path(directory)/"hypotheses.jsonl").record(hypothesis)
        outcome=PublicOutcomeMeasurement("O-1","FINAL_AREA_GAP_LHA","INDIA",target,-3.0,"AGRI_MINISTRY","DOC-1","https://agri.example/outcome","c"*64,"Official final report records the national crop area gap.",datetime(2026,10,1,tzinfo=timezone.utc))
        resolution_entry=PreInflectionResolutionLedger(Path(directory)/"resolutions.jsonl").record(hypothesis=hypothesis,hypothesis_entry_hash=hypothesis_entry["entry_hash"],outcome=outcome,evaluated_at=evaluated)
        assert resolution_entry["resolution"]["status"]=="CONFIRMED"
        resolution=HypothesisResolution(hypothesis.hypothesis_id,"CONFIRMED",True,(),evaluated,True)
        calibration=build_hypothesis_calibration_report(cohort_id="LIFECYCLE",expected_hypothesis_ids=(hypothesis.hypothesis_id,),hypotheses=(hypothesis,),resolutions=(resolution,),minimum_sample_size=1)
        assert calibration.performance_claim_ready and calibration.hit_rate_percent==100 and calibration.brier_score==0.1225
    print("PRE-INFLECTION PROSPECTIVE LIFECYCLE: ALL TESTS PASSED")


if __name__=="__main__": main()
