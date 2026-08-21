"""Preview exact source observations for accepted historical reviews."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_resolver import (
    HistoricalComparisonAcceptedObservationResolver,
)
from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_candidate_builder import (
    HistoricalComparisonReviewCandidateBuilder,
)
from modules.external_intelligence.historical_comparison_review_decision_ledger import (
    HistoricalComparisonReviewDecisionLedger,
)
from modules.external_intelligence.historical_comparison_review_reconciler import (
    HistoricalComparisonReviewReconciler,
)
from modules.observation.observation_persistence import ObservationPersistence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve accepted historical review candidates to exact persisted "
            "Observations without creating Evidence."
        )
    )
    parser.add_argument("--audit-path")
    parser.add_argument("--ledger-path")
    parser.add_argument("--observation-path")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    values = {
        "audit": args.audit_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH", ""
        ).strip(),
        "ledger": args.ledger_path or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH", ""
        ).strip(),
        "observation": args.observation_path or os.environ.get(
            "EIOS_OBSERVATION_PATH", ""
        ).strip(),
    }
    if any(not value for value in values.values()):
        print("Configuration error: audit, ledger, and observation paths are required.")
        return 1

    paths = {name: Path(value) for name, value in values.items()}
    if len({path.resolve() for path in paths.values()}) != 3:
        print("Accepted observation preview error: all source paths must differ.")
        return 1
    before = {
        name: path.read_bytes() if path.is_file() else None
        for name, path in paths.items()
    }

    try:
        candidates = HistoricalComparisonReviewCandidateBuilder().build(
            HistoricalComparisonAuditReader(paths["audit"]).read_all()
        )
        reconciled = HistoricalComparisonReviewReconciler().reconcile(
            candidates,
            HistoricalComparisonReviewDecisionLedger(paths["ledger"]).read_all(),
        )
        accepted = tuple(
            candidate
            for candidate in reconciled
            if candidate.status == HistoricalComparisonReviewStatus.ACCEPTED
        )
        observations = ObservationPersistence(paths["observation"]).load()
        resolver = HistoricalComparisonAcceptedObservationResolver()
        previews = tuple(
            resolver.resolve(candidate, observations) for candidate in accepted
        )
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Accepted observation preview error: {exc}")
        return 1

    for name, path in paths.items():
        if before[name] is not None and path.read_bytes() != before[name]:
            print(f"Accepted observation preview error: {name} file changed.")
            return 1

    payload = {
        "schema_version": 1,
        "candidate_count": len(reconciled),
        "accepted_count": len(accepted),
        "resolved_count": len(previews),
        "previews": [_payload(preview) for preview in previews],
        "assessment_required": bool(previews),
        "source_files_modified": False,
        "evidence_created": False,
        "financial_interpretation_performed": False,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        _print_text(payload)
    return 0


def _payload(preview) -> dict:
    return {
        "candidate_id": preview.candidate_id,
        "audit_recorded_at": preview.audit_recorded_at.isoformat(),
        "reviewer": preview.reviewer,
        "review_reason": preview.review_reason,
        "reviewed_at": preview.reviewed_at.isoformat(),
        "observation": {
            "title": preview.title,
            "description": preview.description,
            "source": preview.source,
            "category": preview.category,
            "entity": preview.entity,
            "confidence": preview.confidence,
            "timestamp": preview.timestamp.isoformat(),
            "cycle_id": preview.cycle_id,
            "job_id": preview.job_id,
            "research_intent": preview.research_intent,
            "retrieved_at": (
                preview.retrieved_at.isoformat()
                if preview.retrieved_at is not None
                else None
            ),
            "source_url": preview.source_url,
            "source_domain": preview.source_domain,
            "source_type": preview.source_type,
            "content_fingerprint": preview.content_fingerprint,
        },
        "evidence_assessment_supplied": False,
    }


def _print_text(payload) -> None:
    print("EIOS ACCEPTED-REVIEW OBSERVATION RESOLUTION PREVIEW")
    print(f"Review candidates: {payload['candidate_count']}")
    print(f"Accepted: {payload['accepted_count']}")
    print(f"Resolved: {payload['resolved_count']}")
    for preview in payload["previews"]:
        observation = preview["observation"]
        print("---")
        print(f"Candidate ID: {preview['candidate_id']}")
        print(f"Entity: {observation['entity']}")
        print(f"Title: {observation['title']}")
        print(f"Fingerprint: {observation['content_fingerprint']}")
        print("Evidence assessment supplied: no")
    print("No source files were modified.")
    print("No Evidence was created.")
    print("No financial interpretation was performed.")


if __name__ == "__main__":
    raise SystemExit(main())
