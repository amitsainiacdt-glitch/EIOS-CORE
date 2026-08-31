from dataclasses import replace

from modules.external_intelligence.evidence_confidence_ceiling import EvidenceConfidenceInputs,EvidenceDirectness,calculate_evidence_confidence_ceiling


def main():
    strong=EvidenceConfidenceInputs(True,2,14,EvidenceDirectness.DIRECT,True,True,True,True,3,0,0)
    ceiling=calculate_evidence_confidence_ceiling(strong); assert ceiling.maximum_confidence_percent==95 and ceiling.confidence_eligible
    proxy=calculate_evidence_confidence_ceiling(replace(strong,directness=EvidenceDirectness.PROXY,geography_exact_match=False,independent_source_group_count=1)); assert proxy.maximum_confidence_percent==45 and not proxy.confidence_eligible
    stale=calculate_evidence_confidence_ceiling(replace(strong,age_days=30,unresolved_material_contradictions=1)); assert stale.maximum_confidence_percent==55 and stale.confidence_eligible
    broken=calculate_evidence_confidence_ceiling(replace(strong,schema_compatible=False)); assert not broken.confidence_eligible and "SCHEMA_NOT_COMPATIBLE" in broken.reason_codes
    missing=calculate_evidence_confidence_ceiling(replace(strong,missing_critical_layers=2)); assert missing.maximum_confidence_percent==55
    print("EVIDENCE CONFIDENCE CEILING: ALL TESTS PASSED")


if __name__=="__main__": main()
