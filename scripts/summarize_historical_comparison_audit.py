"""Read and summarize one historical comparison audit cycle."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_cycle_summarizer import (
    HistoricalComparisonCycleSummarizer,
)
from modules.external_intelligence.historical_comparison_audit_timeline_builder import (
    HistoricalComparisonAuditTimelineBuilder,
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
    parser.add_argument(
        "--all-cycles",
        action="store_true",
        help="Summarize every audit cycle in chronological order.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit stable machine-readable JSON.",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.all_cycles and args.recorded_at:
        print(
            "Configuration error: --all-cycles and --recorded-at "
            "cannot be used together."
        )
        return 1
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
        if args.json:
            print(
                json.dumps(
                    {
                        "schema_version": 1,
                        "cycle_count": 0,
                        "record_count": 0,
                        "cycles": [],
                        "financial_interpretation_performed": False,
                    },
                    sort_keys=True,
                )
            )
        else:
            print("No historical comparison audit records were found.")
        return 0

    if args.all_cycles:
        try:
            timeline = HistoricalComparisonAuditTimelineBuilder().build(
                records
            )
        except ValueError as exc:
            print(f"Audit timeline error: {exc}")
            return 1

        if args.json:
            print(json.dumps(_timeline_payload(timeline), sort_keys=True))
        else:
            _print_timeline(timeline)
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

    if args.json:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "cycle": _summary_payload(summary),
                    "financial_interpretation_performed": False,
                },
                sort_keys=True,
            )
        )
        return 0

    _print_summary(summary)
    return 0


def _summary_payload(summary) -> dict:
    return {
        "recorded_at": summary.recorded_at.isoformat(),
        "record_count": summary.record_count,
        "selected_count": summary.selected_count,
        "no_match_count": summary.no_match_count,
        "ambiguous_count": summary.ambiguous_count,
        "comparison_count": summary.comparison_count,
        "change_detected_count": summary.change_detected_count,
        "job_id_selection_count": summary.job_id_selection_count,
        "research_intent_selection_count": (
            summary.research_intent_selection_count
        ),
        "legacy_selection_count": summary.legacy_selection_count,
        "no_change_comparison_count": (
            summary.no_change_comparison_count
        ),
        "information_change_comparison_count": (
            summary.information_change_comparison_count
        ),
        "source_change_comparison_count": (
            summary.source_change_comparison_count
        ),
    }


def _timeline_payload(timeline) -> dict:
    return {
        "schema_version": 1,
        "cycle_count": timeline.cycle_count,
        "record_count": timeline.record_count,
        "cycles": [
            _summary_payload(summary)
            for summary in timeline.cycles
        ],
        "financial_interpretation_performed": False,
    }


def _print_timeline(timeline) -> None:
    print("EIOS HISTORICAL COMPARISON AUDIT TIMELINE")
    print(f"Cycles: {timeline.cycle_count}")
    print(f"Records: {timeline.record_count}")

    for summary in timeline.cycles:
        print("---")
        _print_summary(summary, include_heading=False)

    print("No financial interpretation was performed.")


def _print_summary(summary, *, include_heading=True) -> None:
    if include_heading:
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
    if include_heading:
        print("No financial interpretation was performed.")


if __name__ == "__main__":
    raise SystemExit(main())
