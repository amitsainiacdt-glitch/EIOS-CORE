"""Read and summarize one historical comparison audit cycle."""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_cycle_summarizer import (
    HistoricalComparisonCycleSummarizer,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read an EIOS historical comparison audit and print "
            "count-only facts for one runtime cycle."
        )
    )
    parser.add_argument(
        "--path",
        help=(
            "Audit JSON Lines path. Defaults to "
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH."
        ),
    )
    parser.add_argument(
        "--recorded-at",
        help=(
            "Exact ISO runtime timestamp. Defaults to the latest "
            "appended audit cycle."
        ),
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    path_value = (
        args.path
        or os.environ.get(
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH",
            "",
        ).strip()
    )

    if not path_value:
        print(
            "Configuration error: provide --path or set "
            "EIOS_HISTORICAL_COMPARISON_AUDIT_PATH."
        )
        return 1

    reader = HistoricalComparisonAuditReader(Path(path_value))

    try:
        records = reader.read_all()
    except ValueError as exc:
        print(f"Audit read error: {exc}")
        return 1

    if not records:
        print("No historical comparison audit records were found.")
        return 0

    if args.recorded_at:
        try:
            recorded_at = datetime.fromisoformat(args.recorded_at)
        except ValueError:
            print("Configuration error: --recorded-at must be ISO format.")
            return 1
    else:
        recorded_at = records[-1].recorded_at

    summary = HistoricalComparisonCycleSummarizer().summarize(
        records,
        recorded_at=recorded_at,
    )

    print("EIOS HISTORICAL COMPARISON AUDIT SUMMARY")
    print(f"Recorded at: {summary.recorded_at.isoformat()}")
    print(f"Records: {summary.record_count}")
    print(f"Selected history: {summary.selected_count}")
    print(f"No match: {summary.no_match_count}")
    print(f"Ambiguous: {summary.ambiguous_count}")
    print(f"Comparisons: {summary.comparison_count}")
    print(f"Changes detected: {summary.change_detected_count}")
    print(f"Job-ID selections: {summary.job_id_selection_count}")
    print(
        "Research-intent selections: "
        f"{summary.research_intent_selection_count}"
    )
    print(f"Legacy selections: {summary.legacy_selection_count}")
    print(
        "No-change comparisons: "
        f"{summary.no_change_comparison_count}"
    )
    print(
        "Information-change comparisons: "
        f"{summary.information_change_comparison_count}"
    )
    print(
        "Source-change comparisons: "
        f"{summary.source_change_comparison_count}"
    )
    print("No financial interpretation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
