"""Offline validation for governed valuation snapshot receipts."""

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.master_dossier.valuation_section import ValuationSection


def valuation():
    return ValuationSection(
        intrinsic_value=5250.0, fair_value=5100.0, valuation_method="DCF + EPV",
        confidence=82.0, score=80.0, source="ValuationEngine",
        evidence=["DCF", "EPV"], assumptions=["Normalized earnings persist."],
        metadata={"model_count": 2}, summary="Institutional valuation completed.",
    )


def main():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        ledger = HistoricalComparisonValuationSnapshotLedger(root / "valuations.jsonl")
        snapshot = valuation()
        with patch("modules.opportunity.mispricing_engine.MispricingEngine.analyze", side_effect=AssertionError("Mispricing forbidden")):
            receipt = ledger.record(snapshot, entity="Entity A", recorder="Valuation Steward", rationale="Approved engine output captured.", recorded_at=datetime(2026, 8, 22))
        assert receipt.valuation_fingerprint == ledger.valuation_fingerprint(snapshot)
        assert ledger.read_all() == (receipt,)
        try:
            ledger.record(snapshot, entity="Entity A", recorder="Other", rationale="Duplicate.", recorded_at=datetime(2026, 8, 23))
        except ValueError as exc:
            assert "already" in str(exc)
        else:
            raise AssertionError("duplicate snapshot accepted")
        for invalid, message in (
            (replace(snapshot, source="Manual"), "source"),
            (replace(snapshot, fair_value=0), "fair_value"),
            (replace(snapshot, confidence=101), "confidence"),
        ):
            try:
                HistoricalComparisonValuationSnapshotLedger(root / (message + ".jsonl")).record(invalid, entity="Entity A", recorder="Reviewer", rationale="Invalid.", recorded_at=datetime(2026, 8, 22))
            except ValueError as exc:
                assert message in str(exc)
            else:
                raise AssertionError(f"invalid {message} accepted")
    print("HISTORICAL VALUATION SNAPSHOT LEDGER: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
