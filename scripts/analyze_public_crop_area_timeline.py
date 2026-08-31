"""Compare ordered structured crop-area previews without admitting facts."""

import argparse
import json
from pathlib import Path

from modules.external_intelligence.crop_area_progress_consistency import CropAreaProgressConsistencyService
from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview, PublicCropAreaRecord


def _load(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or payload.get("creates_observation") is not False:
        raise ValueError("unsupported or unsafe crop-area preview")
    records = tuple(PublicCropAreaRecord(**item) for item in payload["records"])
    return PublicCropAreaPreview(payload["acquisition_id"], payload["extraction_id"], payload["period_label"], records)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check an ordered public crop-area timeline.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args(argv)
    if len(args.paths) < 2: raise ValueError("timeline requires at least two crop-area previews")
    previews = [_load(path) for path in args.paths]
    service = CropAreaProgressConsistencyService()
    comparisons = [service.compare(first, second) for first, second in zip(previews, previews[1:])]
    payload = {
        "schema_version": 1, "decision": "BLOCK" if any(item.decision == "BLOCK" for item in comparisons) else "PASS",
        "creates_observation": False, "requires_human_review": True,
        "comparisons": [{**item.__dict__, "changes": [change.__dict__ for change in item.changes]} for item in comparisons],
    }
    output = Path(args.output_path); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Timeline decision: {payload['decision']}")
    for item in comparisons: print(f"{item.earlier_period} -> {item.later_period}: {item.decision}, {item.shared_crop_count} shared crops")
    print("No Observation, Evidence, Meta conclusion, Signal, recommendation, or trade was created.")
    return 0 if payload["decision"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
