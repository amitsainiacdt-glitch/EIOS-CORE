"""Write the review-only readiness snapshot for the India Kharif 2026 case."""

import argparse,json
from dataclasses import asdict
from pathlib import Path

from modules.external_intelligence.evidence_confidence_ceiling import EvidenceConfidenceInputs,EvidenceDirectness,calculate_evidence_confidence_ceiling
from modules.external_intelligence.pre_inflection_case_readiness import PreInflectionCaseInputs,assess_pre_inflection_case


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True); args=parser.parse_args()
    inputs=PreInflectionCaseInputs(
        "INDIA-KHARIF-2026",True,True,False,False,True,False,False,True,3,False,False,False,(),
        ("Observed soil moisture or crop condition is not available through the governed public route.","Current reservoir storage is not verified and crop-geography mapped.","Official current output-price payload was not captured.","Mandi arrival quantity and unit are not verified.","No issuer-specific exposure disclosure or dated catalyst is in scope."),
    )
    ceiling=calculate_evidence_confidence_ceiling(EvidenceConfidenceInputs(True,10,14,EvidenceDirectness.INFERRED,False,True,True,True,3,0,3))
    payload={"schema_version":1,"inputs":asdict(inputs),"assessment":asdict(assess_pre_inflection_case(inputs)),"causal_interpretation_confidence_ceiling":asdict(ceiling),"creates_observation":False,"requires_human_review":True,"non_authority_statement":"Research readiness only; not a Signal, Catalyst, Opportunity, recommendation, position, or trade."}
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {path}")


if __name__=="__main__": main()
