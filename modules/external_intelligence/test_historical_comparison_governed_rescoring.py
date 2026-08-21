"""No-network validation for explicit governed Evidence pack rescoring."""

import io
from contextlib import redirect_stdout
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence import test_historical_comparison_audit_reader_summary as audit_test
from modules.external_intelligence.evidence_intelligence_adapter import EvidenceIntelligenceAdapter
from modules.external_intelligence.historical_comparison_evidence_governance_ledger import HistoricalComparisonEvidenceGovernanceLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_governed_scoring_ledger import HistoricalComparisonGovernedScoringLedger
from modules.external_intelligence.test_historical_comparison_evidence_governance_ledger import governance_values
from modules.external_intelligence.test_historical_comparison_evidence_pack_scoring import build_chain
from modules.opportunity.catalyst.catalyst_classifier import CatalystClassifier
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine
from scripts.rescore_historical_comparison_governed_evidence_pack import main as rescore_main


class FailingAnalyzer:
    def analyze(self, pack, governance):
        raise AssertionError("duplicate reached governed scoring engine")


def setup(root, audit_path):
    chain = build_chain(root, audit_path)
    pack, conversion = chain[4], chain[3]
    review_path, observation_path, assessment_path, conversion_path = chain[5]
    scoring_path = root / "scores.jsonl"
    _, scoring = HistoricalComparisonEvidencePackScoringLedger(scoring_path).analyze(
        pack,
        analyst="Scoring Analyst",
        analyzed_at=conversion.converted_at + timedelta(minutes=5),
    )
    governance_path = root / "governance.jsonl"
    governance = HistoricalComparisonEvidenceGovernanceLedger(governance_path).record(
        scoring, **governance_values(scoring)
    )
    return pack, scoring, governance, {
        "audit": audit_path,
        "review": review_path,
        "observation": observation_path,
        "assessment": assessment_path,
        "conversion": conversion_path,
        "scoring": scoring_path,
        "governance": governance_path,
    }


def validate_ledger(root, pack, governance):
    path = root / "direct-governed-scores.jsonl"
    ledger = HistoricalComparisonGovernedScoringLedger(path)
    rescored_at = governance.governed_at + timedelta(minutes=5)
    result, receipt = ledger.analyze(
        pack, governance, analyst="Governed Analyst", rescored_at=rescored_at
    )
    assert "No explicit assumptions documented." not in result.evidence_gaps
    assert "No explicit kill switches defined." not in result.evidence_gaps
    assert "No monitoring signals defined." not in result.evidence_gaps
    assert "No contradictory evidence documented." in result.evidence_gaps
    assert receipt.pack_fingerprint == governance.pack_fingerprint
    assert ledger.read_all() == (receipt,)
    before = path.read_bytes()
    try:
        ledger.analyze(
            pack, governance, analyst="Second", rescored_at=rescored_at,
            analyzer=FailingAnalyzer(),
        )
        raise AssertionError("duplicate governed score accepted")
    except ValueError as exc:
        assert "already rescored" in str(exc).casefold()
    assert path.read_bytes() == before


def validate_command(root, pack, scoring, governance, paths):
    governed_path = root / "command-governed.jsonl"
    before = {path: path.read_bytes() for path in paths.values()}
    args = []
    for name, path in paths.items():
        args.extend([f"--{name}-path", str(path)])
    args.extend([
        "--governed-path", str(governed_path),
        "--pack-fingerprint", scoring.pack_fingerprint,
        "--analyst", "Governed Analyst",
        "--rescored-at", (governance.governed_at + timedelta(minutes=5)).isoformat(),
    ])
    output = io.StringIO()
    with (
        patch.object(EvidenceIntelligenceAdapter, "publish", side_effect=AssertionError("publish")) as publish,
        patch.object(SignalInterpretationEngine, "create", side_effect=AssertionError("signal")) as signal,
        patch.object(CatalystClassifier, "classify", side_effect=AssertionError("catalyst")) as catalyst,
        redirect_stdout(output),
    ):
        result = rescore_main(args)
    assert result == 0
    assert publish.call_count == signal.call_count == catalyst.call_count == 0
    assert "Governed scoring receipt appended." in output.getvalue()
    stored = HistoricalComparisonGovernedScoringLedger(governed_path).read_all()
    assert len(stored) == 1
    for path, content in before.items():
        assert path.read_bytes() == content


def main():
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        audit_path = root / "audit.jsonl"
        audit_test.write_records(audit_path)
        pack, scoring, governance, paths = setup(root, audit_path)
        validate_ledger(root, pack, governance)
        validate_command(root, pack, scoring, governance, paths)
    print("HISTORICAL GOVERNED PACK RESCORING: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
