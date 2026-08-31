import json
from datetime import datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection,PublicOutcomeMeasurement
from modules.external_intelligence.pre_inflection_resolution_ledger import PreInflectionResolutionLedger


def _objects(identity,value):
    frozen=datetime(2026,1,1,tzinfo=timezone.utc); target=datetime(2026,3,31,tzinfo=timezone.utc); evidence=("a"*64,)
    fields=dict(hypothesis_id=identity,case_id="C",metric_id="M",geography_id="INDIA",direction=HypothesisDirection.ABOVE,threshold_value=1.0,baseline_value=None,target_date=target,frozen_at=frozen,confidence_percent=60,evidence_fingerprints=evidence)
    hypothesis=FrozenPreInflectionHypothesis(**fields,hypothesis_fingerprint=FrozenPreInflectionHypothesis.fingerprint(**fields),non_authority_statement="Research only")
    outcome=PublicOutcomeMeasurement("O-"+identity,"M","INDIA",target,value,"AGRI_MINISTRY","DOC","https://agri.example/doc","b"*64,"Official outcome passage contains the measured value for India.",datetime(2026,4,1,tzinfo=timezone.utc))
    return hypothesis,outcome


def main():
    with TemporaryDirectory() as directory:
        path=Path(directory)/"resolutions.jsonl"; ledger=PreInflectionResolutionLedger(path); now=datetime(2026,4,2,tzinfo=timezone.utc)
        h1,o1=_objects("H1",2); first=ledger.record(hypothesis=h1,hypothesis_entry_hash="c"*64,outcome=o1,evaluated_at=now); h2,o2=_objects("H2",0)
        second=ledger.record(hypothesis=h2,hypothesis_entry_hash="d"*64,outcome=o2,evaluated_at=now); assert first["resolution"]["status"]=="CONFIRMED" and second["resolution"]["status"]=="DISCONFIRMED" and len(ledger.read_all())==2
        try: ledger.record(hypothesis=h1,hypothesis_entry_hash="c"*64,outcome=o1,evaluated_at=now)
        except ValueError as exc: assert "already resolved" in str(exc)
        else: raise AssertionError("duplicate resolution accepted")
        rows=path.read_text(encoding="utf-8").splitlines(); item=json.loads(rows[0]); item["outcome"]["observed_value"]=99; rows[0]=json.dumps(item); path.write_text("\n".join(rows)+"\n",encoding="utf-8")
        try: ledger.read_all()
        except ValueError as exc: assert "outcome fingerprint" in str(exc)
        else: raise AssertionError("tampered outcome accepted")
    print("PRE-INFLECTION RESOLUTION LEDGER: ALL TESTS PASSED")


if __name__=="__main__": main()
