"""Analyze state fertilizer balances without admitting facts."""

import argparse,json
from pathlib import Path
from modules.external_intelligence.public_state_fertilizer_record import PublicStateFertilizerPreview,PublicStateFertilizerRecord
from modules.external_intelligence.state_fertilizer_balance_analysis import StateFertilizerBalanceAnalysisService


def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("input_path"); parser.add_argument("--output-path",required=True); args=parser.parse_args(argv)
    payload=json.loads(Path(args.input_path).read_text(encoding="utf-8")); preview=PublicStateFertilizerPreview(payload["acquisition_id"],payload["extraction_id"],payload["period_label"],tuple(PublicStateFertilizerRecord(**item) for item in payload["records"]))
    result=StateFertilizerBalanceAnalysisService().assess(preview); output_payload={**result.__dict__,"state_requirement_gaps":[item.__dict__ for item in result.state_requirement_gaps]}
    output=Path(args.output_path); output.write_text(json.dumps(output_payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"States: {result.state_count}"); print(f"State-product requirement gaps: {len(result.state_requirement_gaps)}");
    for item in result.state_requirement_gaps: print(f"{item.state} {item.product}: availability gap {item.availability_gap_lmt} LMT, closing stock {item.closing_stock_lmt} LMT")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created."); return 0


if __name__=="__main__": raise SystemExit(main())
