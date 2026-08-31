import json
from dataclasses import replace
from datetime import datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection
from modules.external_intelligence.pre_inflection_hypothesis_ledger import PreInflectionHypothesisLedger


def _hypothesis(identity,threshold=1.0):
    values=dict(hypothesis_id=identity,case_id="C",metric_id="M",geography_id="INDIA",direction=HypothesisDirection.ABOVE,threshold_value=threshold,baseline_value=None,target_date=datetime(2026,9,30,tzinfo=timezone.utc),frozen_at=datetime(2026,8,31,tzinfo=timezone.utc),confidence_percent=65.0,evidence_fingerprints=("a"*64,))
    return FrozenPreInflectionHypothesis(**values,hypothesis_fingerprint=FrozenPreInflectionHypothesis.fingerprint(**values),non_authority_statement="Research only")


def main():
    with TemporaryDirectory() as directory:
        path=Path(directory)/"hypotheses.jsonl"; ledger=PreInflectionHypothesisLedger(path)
        first=ledger.record(_hypothesis("H-1")); second=ledger.record(_hypothesis("H-2",2.0)); assert first["previous_entry_hash"]==ledger.GENESIS and second["previous_entry_hash"]==first["entry_hash"] and len(ledger.read_all())==2
        try: ledger.record(_hypothesis("H-1"))
        except ValueError as exc: assert "already exists" in str(exc)
        else: raise AssertionError("duplicate hypothesis accepted")
        try: ledger.record(replace(_hypothesis("H-3"),threshold_value=9.0))
        except ValueError as exc: assert "fingerprint" in str(exc)
        else: raise AssertionError("tampered hypothesis accepted")
        rows=path.read_text(encoding="utf-8").splitlines(); altered=json.loads(rows[0]); altered["hypothesis"]["confidence_percent"]=99; rows[0]=json.dumps(altered); path.write_text("\n".join(rows)+"\n",encoding="utf-8")
        try: ledger.read_all()
        except ValueError as exc: assert "fingerprint" in str(exc) or "entry hash" in str(exc)
        else: raise AssertionError("tampered ledger accepted")
    print("PRE-INFLECTION HYPOTHESIS LEDGER: ALL TESTS PASSED")


if __name__=="__main__": main()
