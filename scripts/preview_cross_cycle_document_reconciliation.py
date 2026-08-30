"""Print a read-only cross-cycle document reconciliation preview."""

import argparse
import json
from pathlib import Path

from modules.external_intelligence.cross_cycle_document_reconciliation_service import CrossCycleDocumentReconciliationService
from modules.observation.observation_persistence import ObservationPersistence


def parser():
    result = argparse.ArgumentParser(description="Preview repeated strong document identities across Observation cycles.")
    result.add_argument("--observation-path", required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    path = Path(args.observation_path)
    try:
        before = path.read_bytes()
        preview = CrossCycleDocumentReconciliationService().preview(
            ObservationPersistence(path).load()
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Cross-cycle reconciliation error: {exc}")
        return 1
    if path.read_bytes() != before:
        print("Cross-cycle reconciliation error: Observation storage changed.")
        return 1
    service = CrossCycleDocumentReconciliationService()
    payload = {**preview.__dict__}
    payload["groups"] = [service.group_payload(group) for group in preview.groups]
    payload["warnings"] = list(preview.warnings)
    print(json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False))
    print("Read-only preview: no Observation was merged, deleted, or modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
