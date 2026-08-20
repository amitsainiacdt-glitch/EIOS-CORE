"""Read-only validation for audit parsing and cycle summarization."""

import io
import json
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_audit_filter import (
    HistoricalComparisonAuditFilter,
)
from modules.external_intelligence.historical_comparison_audit_filter_engine import (
    HistoricalComparisonAuditFilterEngine,
)
from modules.external_intelligence.historical_comparison_cycle_summarizer import (
    HistoricalComparisonCycleSummarizer,
)
from modules.external_intelligence.historical_comparison_audit_timeline_builder import (
    HistoricalComparisonAuditTimelineBuilder,
)
from modules.observation.historical_comparison import ComparisonType
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)
from scripts.summarize_historical_comparison_audit import main as summary_main


CYCLE_ONE = datetime(2026, 8, 20, 12, 0, 0)
CYCLE_TWO = datetime(2026, 8, 20, 13, 0, 0)


def observation(title, *, job_id="JOB-ORDERS") -> dict:
    return {
        "title": title,
        "entity": "Example Limited",
        "category": "External Web",
        "timestamp": CYCLE_ONE.isoformat(),
        "source": "https://research.example.com/report",
        "job_id": job_id,
        "research_intent": "ORDER_AND_CAPACITY",
        "content_fingerprint": sha256(
            title.encode("utf-8")
        ).hexdigest(),
    }


def payload(
    *,
    recorded_at,
    title,
    basis,
    eligible_count,
    historical,
    comparison,
    reason,
    current_job_id="JOB-ORDERS",
) -> dict:
    return {
        "schema_version": 1,
        "recorded_at": recorded_at.isoformat(),
        "current_observation": observation(
            title,
            job_id=current_job_id,
        ),
        "historical_observation": historical,
        "selection": {
            "basis": basis,
            "eligible_count": eligible_count,
            "reason": reason,
        },
        "comparison": comparison,
    }


def comparison(comparison_type, *, changed) -> dict:
    return {
        "type": comparison_type,
        "change_detected": changed,
        "change_direction": "UNKNOWN",
        "materiality": "UNKNOWN",
        "delta": None,
        "provenance": "audit-test",
    }


def write_records(path: Path) -> None:
    records = [
        payload(
            recorded_at=CYCLE_ONE,
            title="Selected current",
            basis="JOB_ID",
            eligible_count=1,
            historical=observation("Selected historical"),
            comparison=comparison("INFORMATION_CHANGE", changed=True),
            reason="Selected history.",
        ),
        payload(
            recorded_at=CYCLE_ONE,
            title="No-match current",
            basis=None,
            eligible_count=0,
            historical=None,
            comparison=None,
            reason="No matching history.",
            current_job_id="JOB-OTHER",
        ),
        payload(
            recorded_at=CYCLE_ONE,
            title="Ambiguous current",
            basis="RESEARCH_INTENT",
            eligible_count=2,
            historical=None,
            comparison=None,
            reason="Historical selection is ambiguous.",
        ),
        payload(
            recorded_at=CYCLE_TWO,
            title="Latest current",
            basis="LEGACY_ENTITY_CATEGORY",
            eligible_count=1,
            historical=observation(
                "Latest historical",
                job_id=None,
            ),
            comparison=comparison("NO_CHANGE", changed=False),
            reason="Selected legacy history.",
        ),
    ]
    path.write_text(
        "".join(json.dumps(item) + "\n" for item in records),
        encoding="utf-8",
    )


def validate_reading_and_summary(path: Path) -> None:
    before = path.read_bytes()
    records = HistoricalComparisonAuditReader(path).read_all()

    assert len(records) == 4
    assert records[0].selection_basis == HistoricalSelectionBasis.JOB_ID
    assert records[0].comparison_type == ComparisonType.INFORMATION_CHANGE
    assert records[0].current_observation.job_id == "JOB-ORDERS"

    cycle_records = HistoricalComparisonAuditReader(path).read_cycle(
        CYCLE_ONE
    )
    assert len(cycle_records) == 3

    summary = HistoricalComparisonCycleSummarizer().summarize(
        records,
        recorded_at=CYCLE_ONE,
    )
    assert summary.record_count == 3
    assert summary.selected_count == 1
    assert summary.no_match_count == 1
    assert summary.ambiguous_count == 1
    assert summary.comparison_count == 1
    assert summary.change_detected_count == 1
    assert summary.job_id_selection_count == 1
    assert summary.research_intent_selection_count == 1
    assert summary.legacy_selection_count == 0
    assert summary.information_change_comparison_count == 1

    assert path.read_bytes() == before


def validate_command(path: Path) -> None:
    before = path.read_bytes()
    output = io.StringIO()

    with redirect_stdout(output):
        result = summary_main(["--path", str(path)])

    assert result == 0
    rendered = output.getvalue()
    assert CYCLE_TWO.isoformat() in rendered
    assert "Records: 1" in rendered
    assert "Legacy selections: 1" in rendered
    assert "No financial interpretation was performed." in rendered

    output = io.StringIO()
    with redirect_stdout(output):
        result = summary_main(
            ["--path", str(path), "--all-cycles", "--json"]
        )

    assert result == 0
    timeline = json.loads(output.getvalue())
    assert timeline["schema_version"] == 1
    assert timeline["cycle_count"] == 2
    assert timeline["record_count"] == 4
    assert timeline["financial_interpretation_performed"] is False
    assert [
        cycle["recorded_at"]
        for cycle in timeline["cycles"]
    ] == [CYCLE_ONE.isoformat(), CYCLE_TWO.isoformat()]
    assert timeline["cycles"][0]["record_count"] == 3
    assert timeline["cycles"][1]["legacy_selection_count"] == 1

    output = io.StringIO()
    with redirect_stdout(output):
        result = summary_main(
            [
                "--path",
                str(path),
                "--all-cycles",
                "--json",
                "--job-id",
                " job-other ",
                "--from",
                CYCLE_ONE.isoformat(),
                "--to",
                CYCLE_ONE.isoformat(),
            ]
        )

    assert result == 0
    filtered = json.loads(output.getvalue())
    assert filtered["cycle_count"] == 1
    assert filtered["record_count"] == 1
    assert filtered["filters"]["job_id"] == " job-other "
    assert filtered["cycles"][0]["no_match_count"] == 1
    assert path.read_bytes() == before


def validate_timeline(records) -> None:
    timeline = HistoricalComparisonAuditTimelineBuilder().build(
        reversed(records)
    )
    assert timeline.cycle_count == 2
    assert timeline.record_count == 4
    assert [cycle.recorded_at for cycle in timeline.cycles] == [
        CYCLE_ONE,
        CYCLE_TWO,
    ]

    assert HistoricalComparisonAuditTimelineBuilder().build([]).cycles == ()

    mixed = [
        records[0],
        replace(
            records[-1],
            recorded_at=CYCLE_TWO.replace(tzinfo=timezone.utc),
        ),
    ]
    try:
        HistoricalComparisonAuditTimelineBuilder().build(mixed)
        raise AssertionError("Mixed timezone-awareness was accepted")
    except ValueError as exc:
        assert "timezone" in str(exc).casefold()


def validate_filters(records) -> None:
    engine = HistoricalComparisonAuditFilterEngine()

    job_records = engine.filter(
        records,
        HistoricalComparisonAuditFilter(job_id=" job-orders "),
    )
    assert len(job_records) == 3

    intent_records = engine.filter(
        records,
        HistoricalComparisonAuditFilter(
            selection_basis=(
                HistoricalSelectionBasis.RESEARCH_INTENT
            )
        ),
    )
    assert len(intent_records) == 1
    assert intent_records[0].eligible_count == 2

    changed_records = engine.filter(
        records,
        HistoricalComparisonAuditFilter(
            comparison_type=ComparisonType.INFORMATION_CHANGE
        ),
    )
    assert len(changed_records) == 1
    assert changed_records[0].change_detected is True

    latest_records = engine.filter(
        records,
        HistoricalComparisonAuditFilter(
            entity=" example   limited ",
            category="external web",
            recorded_from=CYCLE_TWO,
            recorded_to=CYCLE_TWO,
        ),
    )
    assert len(latest_records) == 1
    assert latest_records[0].recorded_at == CYCLE_TWO

    try:
        engine.filter(
            records,
            HistoricalComparisonAuditFilter(
                recorded_from=CYCLE_TWO,
                recorded_to=CYCLE_ONE,
            ),
        )
        raise AssertionError("Reversed runtime bounds were accepted")
    except ValueError as exc:
        assert "later" in str(exc).casefold()

    try:
        engine.filter(
            records,
            HistoricalComparisonAuditFilter(job_id=123),
        )
        raise AssertionError("Non-string job filter was accepted")
    except ValueError as exc:
        assert "string" in str(exc).casefold()


def validate_failures(root: Path) -> None:
    missing = root / "missing.jsonl"
    assert HistoricalComparisonAuditReader(missing).read_all() == ()

    malformed = root / "malformed.jsonl"
    malformed.write_text(
        json.dumps({"schema_version": 99}) + "\n",
        encoding="utf-8",
    )
    before = malformed.read_bytes()

    try:
        HistoricalComparisonAuditReader(malformed).read_all()
        raise AssertionError("Unsupported schema was accepted")
    except ValueError as exc:
        assert "line 1" in str(exc)
        assert "schema" in str(exc).casefold()

    assert malformed.read_bytes() == before

    inconsistent = root / "inconsistent.jsonl"
    invalid_record = payload(
        recorded_at=CYCLE_ONE,
        title="Invalid current",
        basis="JOB_ID",
        eligible_count=1,
        historical=None,
        comparison=comparison("NO_CHANGE", changed=False),
        reason="Invalid comparison without history.",
    )
    inconsistent.write_text(
        json.dumps(invalid_record) + "\n",
        encoding="utf-8",
    )

    try:
        HistoricalComparisonAuditReader(inconsistent).read_all()
        raise AssertionError("Comparison without history was accepted")
    except ValueError as exc:
        assert "historical observation" in str(exc).casefold()


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        path = root / "historical.jsonl"
        write_records(path)
        validate_reading_and_summary(path)
        records = HistoricalComparisonAuditReader(path).read_all()
        validate_timeline(records)
        validate_filters(records)
        validate_command(path)
        validate_failures(root)

    print(
        "HISTORICAL COMPARISON AUDIT READER AND SUMMARY: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
