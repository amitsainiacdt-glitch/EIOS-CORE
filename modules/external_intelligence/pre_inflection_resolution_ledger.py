"""Hash-chained ledger binding public outcomes to frozen hypotheses."""

import hashlib,json
from dataclasses import asdict
from pathlib import Path

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,PublicOutcomeMeasurement,resolve_hypothesis


class PreInflectionResolutionLedger:
    GENESIS="0"*64
    def __init__(self,path): self.path=Path(path)

    def record(self,*,hypothesis,hypothesis_entry_hash,outcome,evaluated_at):
        if not isinstance(hypothesis,FrozenPreInflectionHypothesis) or not isinstance(outcome,PublicOutcomeMeasurement): raise ValueError("frozen hypothesis and public outcome are required")
        if not self._sha(hypothesis_entry_hash): raise ValueError("valid hypothesis entry hash is required")
        resolution=resolve_hypothesis(hypothesis,outcome,evaluated_at=evaluated_at)
        existing=self.read_all()
        if any(item["hypothesis_id"]==hypothesis.hypothesis_id for item in existing): raise ValueError("hypothesis already resolved")
        previous=existing[-1]["entry_hash"] if existing else self.GENESIS; sequence=len(existing)+1
        outcome_payload=asdict(outcome); outcome_payload["reporting_date"]=outcome.reporting_date.isoformat(); outcome_payload["acquired_at"]=outcome.acquired_at.isoformat()
        resolution_payload=asdict(resolution); resolution_payload["evaluated_at"]=resolution.evaluated_at.isoformat(); resolution_payload["reason_codes"]=list(resolution.reason_codes)
        core={"sequence":sequence,"previous_entry_hash":previous,"hypothesis_id":hypothesis.hypothesis_id,"hypothesis_fingerprint":hypothesis.hypothesis_fingerprint,"hypothesis_entry_hash":hypothesis_entry_hash,"outcome":outcome_payload,"outcome_fingerprint":self._fingerprint(outcome_payload),"resolution":resolution_payload}
        entry={"schema_version":1,**core,"entry_hash":self._fingerprint(core)}
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open("a",encoding="utf-8") as stream: stream.write(json.dumps(entry,sort_keys=True,separators=(",",":"))+"\n")
        return entry

    def read_all(self):
        if not self.path.exists(): return ()
        result=[]; previous=self.GENESIS; identities=set()
        with self.path.open("r",encoding="utf-8") as stream:
            for number,line in enumerate(stream,1):
                if not line.strip(): continue
                try: entry=json.loads(line)
                except json.JSONDecodeError as exc: raise ValueError(f"Invalid resolution entry at line {number}") from exc
                if entry.get("schema_version")!=1 or entry.get("sequence")!=number: raise ValueError(f"Invalid resolution sequence at line {number}")
                if entry.get("previous_entry_hash")!=previous: raise ValueError(f"Broken resolution hash chain at line {number}")
                if not self._sha(entry.get("hypothesis_fingerprint")) or not self._sha(entry.get("hypothesis_entry_hash")): raise ValueError(f"Invalid hypothesis binding at line {number}")
                if self._fingerprint(entry.get("outcome"))!=entry.get("outcome_fingerprint"): raise ValueError(f"Invalid outcome fingerprint at line {number}")
                core={key:value for key,value in entry.items() if key not in ("schema_version","entry_hash")}
                if self._fingerprint(core)!=entry.get("entry_hash"): raise ValueError(f"Invalid resolution entry hash at line {number}")
                identity=entry.get("hypothesis_id")
                if identity in identities: raise ValueError(f"Duplicate resolution at line {number}")
                identities.add(identity); result.append(entry); previous=entry["entry_hash"]
        return tuple(result)

    @staticmethod
    def _fingerprint(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    @staticmethod
    def _sha(value): return isinstance(value,str) and len(value)==64 and all(char in "0123456789abcdef" for char in value)


__all__=["PreInflectionResolutionLedger"]
