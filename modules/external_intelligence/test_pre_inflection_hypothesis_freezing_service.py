from dataclasses import replace
from datetime import datetime,timezone

from modules.external_intelligence.evidence_confidence_ceiling import EvidenceConfidenceCeiling
from modules.external_intelligence.mandatory_meta_review import MandatoryMetaReviewDecision,MandatoryMetaReviewReceipt
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview,PreInflectionStrength
from modules.external_intelligence.pre_inflection_case_readiness import PreInflectionCaseReadiness
from modules.external_intelligence.pre_inflection_hypothesis_evaluation import HypothesisDirection
from modules.external_intelligence.pre_inflection_hypothesis_freezing_service import HypothesisScope,PreInflectionHypothesisFreezingService


def main():
    service=PreInflectionHypothesisFreezingService(); now=datetime(2026,8,31,tzinfo=timezone.utc); target=datetime(2026,9,30,tzinfo=timezone.utc)
    sector=PreInflectionCaseReadiness("SECTOR_TRANSMISSION_RESEARCH_READY",True,True,False,False,(),(),"Sector ready")
    ceiling=EvidenceConfidenceCeiling(70,True,())
    review=MandatoryMetaReviewReceipt(1,"REV-1","META-1","b"*64,MandatoryMetaReviewDecision.AUTHORIZE_PRE_INFLECTION_REVIEW,"READY_FOR_PRE_INFLECTION",(),"Reviewed and authorized.",now,"Human Reviewer")
    preview=PreInflectionAssessmentPreview(1,"PRE-1","META-1","b"*64,"REV-1",(),("AGRICULTURE",),("CROP_STAGE_WATER_STRESS",),PreInflectionStrength.CREDIBLE,2,True,(1,2),"LOW",(),(),(),(),"Uncertain.","Crop transmission is changing.","Current public evidence converged.",("Confirm output prices.",),("Crop conditions normalize.",),("No company balance sheet in scope.",),"NOT_ASSESSED",True,"Research only.")
    fields=dict(readiness=sector,confidence_ceiling=ceiling,pre_inflection_preview=preview,meta_review=review,scope=HypothesisScope.SECTOR,hypothesis_id="H-1",case_id="C-1",metric_id="M",geography_id="INDIA",direction=HypothesisDirection.ABOVE,threshold_value=1,baseline_value=None,target_date=target,frozen_at=now,confidence_percent=65,evidence_fingerprints=("a"*64,))
    hypothesis=service.freeze(**fields); assert hypothesis.confidence_percent==65 and len(hypothesis.hypothesis_fingerprint)==64
    hint=replace(sector,stage="WEATHER_CROP_HINT_ONLY",sector_transmission_ready=False)
    try: service.freeze(**{**fields,"readiness":hint})
    except ValueError as exc: assert "sector-transmission" in str(exc)
    else: raise AssertionError("hint-only case froze hypothesis")
    try: service.freeze(**{**fields,"confidence_percent":75})
    except ValueError as exc: assert "exceeds" in str(exc)
    else: raise AssertionError("over-ceiling confidence accepted")
    try: service.freeze(**{**fields,"scope":HypothesisScope.COMPANY})
    except ValueError as exc: assert "company-case" in str(exc)
    else: raise AssertionError("sector-only case froze company hypothesis")
    held_review=replace(review,decision=MandatoryMetaReviewDecision.HOLD_FOR_RESEARCH)
    try: service.freeze(**{**fields,"meta_review":held_review})
    except ValueError as exc: assert "did not authorize" in str(exc)
    else: raise AssertionError("held Meta review froze hypothesis")
    try: service.freeze(**{**fields,"pre_inflection_preview":replace(preview,meta_review_id="REV-X")})
    except ValueError as exc: assert "does not bind" in str(exc)
    else: raise AssertionError("unbound preview froze hypothesis")
    print("PRE-INFLECTION HYPOTHESIS FREEZING SERVICE: ALL TESTS PASSED")


if __name__=="__main__": main()
