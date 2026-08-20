"""Read-only validation for audit parsing and cycle summarization."""

import io
import json
from contextlib import redirect_stdout
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.historical_comparison_audit_reader import (
    HistoricalComparisonAuditReader,
)
from modules.external_intelligence.historical_comparison_cycle_summarizer import (
    HistoricalComparisonCycleSummarizer,
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
) -> dict:
    return {
        "schema_version": 1,
        "recorded_at": recorded_at.isoformat(),
        "current_observation": observation(title),
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
    assert path.read_bytes() == before


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
        validate_command(path)
        validate_failures(root)

    print(
        "HISTORICAL COMPARISON AUDIT READER AND SUMMARY: "
        "ALL TESTS PASSED"
    )


if __name__ == "__main__":
    main()
