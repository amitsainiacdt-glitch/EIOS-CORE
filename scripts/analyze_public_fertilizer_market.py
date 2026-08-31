"""Create a review-only fertilizer balance interpretation from structured records."""

import argparse, json
from pathlib import Path

from modules.external_intelligence.fertilizer_market_interpretation import FertilizerMarketInterpretationService
from modules.external_intelligence.public_fertilizer_market_record import PublicFertilizerMarketPreview, PublicFertilizerMarketRecord


def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("input_path"); parser.add_argument("--output-path",required=True); args=parser.parse_args(argv)
    payload=json.loads(Path(args.input_path).read_text(encoding="utf-8"))
    if payload.get("schema_version")!=1 or payload.get("creates_observation") is not False: raise ValueError("unsafe fertilizer preview")
    preview=PublicFertilizerMarketPreview(payload["acquisition_id"],payload["extraction_id"],payload["period_label"],tuple(PublicFertilizerMarketRecord(**item) for item in payload["records"]))
    result=FertilizerMarketInterpretationService().assess(preview)
    output_payload={**result.__dict__,"balances":[item.__dict__ for item in result.balances]}
    output=Path(args.output_path); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(output_payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"Supply assessment: {result.national_supply_assessment}"); print(f"Sales momentum: {result.sales_momentum_assessment}"); print(f"Company impact: {result.company_impact_assessment}")
    for item in result.balances: print(f"{item.product}: availability/requirement {item.availability_to_requirement_percent}%, sales/requirement {item.sales_to_requirement_percent}%, closing stock {item.closing_stock_lmt} LMT")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created."); return 0


if __name__=="__main__": raise SystemExit(main())
