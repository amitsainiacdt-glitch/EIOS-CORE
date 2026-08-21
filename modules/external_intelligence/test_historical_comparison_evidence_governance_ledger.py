"""No-network validation for exact-pack human Evidence governance."""

import io
import json
from contextlib import redirect_stdout
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence import test_historical_comparison_audit_reader_summary as audit_test
from modules.external_intelligence.evidence_intelligence_adapter import EvidenceIntelligenceAdapter
from modules.external_intelligence.historical_comparison_entity_evidence_pack_analyzer import HistoricalComparisonEntityEvidencePackAnalyzer
from modules.external_intelligence.historical_comparison_evidence_governance_ledger import HistoricalComparisonEvidenceGovernanceLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.test_historical_comparison_evidence_pack_scoring import build_chain
from modules.opportunity.catalyst.catalyst_classifier import CatalystClassifier
from modules.opportunity.evidence_engine import OpportunityEvidenceEngine
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine
from scripts.record_historical_comparison_evidence_governance import main as record_main


def kill_switch():
    return {
        "name": "Order momentum reversal",
        "condition": "Reported order momentum turns negative.",
        "severity": "High",
        "measurable": True,
        "threshold": "Two consecutive reporting periods below zero growth",
        "monitoring_frequency": "Quarterly",
        "rationale": "The assessed change depends on sustained order momentum.",
        "triggered": False,
    }


def governance_values(scoring):
    return {
        "assumptions": ["Reported order data remains comparable across periods."],
        "kill_switches": [kill_switch()],
        "monitoring_signals": ["Quarterly order intake growth"],
        "analyst": "Human Analyst",
        "rationale": "Explicit governance for the exact scored pack.",
        "governed_at": scoring.analyzed_at + timedelta(minutes=5),
    }


def make_scoring(root, audit_path):
    chain = build_chain(root, audit_path)
    pack = chain[4]
    conversion = chain[3]
    scoring_path = root / "scoring.jsonl"
    result, scoring = HistoricalComparisonEvidencePackScoringLedger(
        scoring_path
    ).analyze(
        pack,
        analyst="Scoring Analyst",
        analyzed_at=conversion.converted_at + timedelta(minutes=5),
    )
    return scoring_path, scoring


def validate_ledger(root, scoring):
    path = root / "direct-governance.jsonl"
    ledger = HistoricalComparisonEvidenceGovernanceLedger(path)
    governance = ledger.record(scoring, **governance_values(scoring))
    assert governance.pack_fingerprint == scoring.pack_fingerprint
    assert governance.entity == scoring.entity
    assert len(governance.assumptions) == 1
    assert governance.kill_switches[0].severity == "High"
    assert governance.kill_switches[0].triggered is False
    assert ledger.read_all() == (governance,)
    before = path.read_bytes()
    try:
        ledger.record(scoring, **governance_values(scoring))
        raise AssertionError("duplicate governance was accepted")
    except ValueError as exc:
        assert "already exists" in str(exc).casefold()
    assert path.read_bytes() == before

    invalid_cases = (
        ({"assumptions": []}, "assumptions"),
        ({"monitoring_signals": []}, "monitoring"),
        ({"kill_switches": []}, "kill_switches"),
        ({"kill_switches": [{**kill_switch(), "severity": "Unknown"}]}, "severity"),
        ({"kill_switches": [{**kill_switch(), "triggered": 0}]}, "boolean"),
        ({"governed_at": scoring.analyzed_at - timedelta(seconds=1)}, "precedes"),
    )
    for index, (override, expected) in enumerate(invalid_cases):
        values = governance_values(scoring)
        values.update(override)
        invalid = HistoricalComparisonEvidenceGovernanceLedger(
            root / f"invalid-{index}.jsonl"
        )
        try:
            invalid.record(scoring, **values)
            raise AssertionError(f"invalid governance accepted: {expected}")
        except ValueError as exc:
            assert expected in str(exc).casefold()
        assert not invalid.path.exists()


def validate_command(root, scoring_path, scoring):
    governance_path = root / "command-governance.jsonl"
    scoring_before = scoring_path.read_bytes()
    output = io.StringIO()
    kill_json = json.dumps(kill_switch(), separators=(",", ":"))
    with (
        patch.object(OpportunityEvidenceEngine, "analyze", side_effect=AssertionError("rescore")) as rescore,
        patch.object(HistoricalComparisonEntityEvidencePackAnalyzer, "analyze", side_effect=AssertionError("rescore")) as entity_rescore,
        patch.object(EvidenceIntelligenceAdapter, "publish", side_effect=AssertionError("publish")) as publish,
        patch.object(SignalInterpretationEngine, "create", side_effect=AssertionError("signal")) as signal,
        patch.object(CatalystClassifier, "classify", side_effect=AssertionError("catalyst")) as catalyst,
        redirect_stdout(output),
    ):
        result = record_main([
            "--scoring-receipt-path", str(scoring_path),
            "--governance-ledger-path", str(governance_path),
            "--pack-fingerprint", scoring.pack_fingerprint,
            "--assumption", "Reported order data remains comparable across periods.",
            "--kill-switch-json", kill_json,
            "--monitoring-signal", "Quarterly order intake growth",
            "--analyst", "Human Analyst",
            "--rationale", "Explicit governance record.",
            "--governed-at", (scoring.analyzed_at + timedelta(minutes=5)).isoformat(),
        ])
    assert result == 0
    assert rescore.call_count == entity_rescore.call_count == 0
    assert publish.call_count == signal.call_count == catalyst.call_count == 0
    assert "No Evidence pack was rescored." in output.getvalue()
    stored = HistoricalComparisonEvidenceGovernanceLedger(governance_path).read_all()
    assert len(stored) == 1
    assert stored[0].pack_fingerprint == scoring.pack_fingerprint
    assert scoring_path.read_bytes() == scoring_before


def main():
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        scoring_path, scoring = make_scoring(root, audit_path)
        validate_ledger(root, scoring)
        validate_command(root, scoring_path, scoring)
    print("HISTORICAL EVIDENCE GOVERNANCE LEDGER: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
