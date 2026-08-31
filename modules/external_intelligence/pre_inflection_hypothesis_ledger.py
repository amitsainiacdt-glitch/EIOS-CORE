"""Append-only hash-chained ledger for frozen pre-inflection hypotheses."""

import hashlib,json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection


class PreInflectionHypothesisLedger:
    GENESIS="0"*64
    def __init__(self,path):
        self.path=Path(path)
        if str(self.path).strip() in ("","."): raise ValueError("hypothesis ledger path must identify a file")

    def record(self,hypothesis):
        self._validate_hypothesis(hypothesis)
        existing=self.read_all()
        if any(item["hypothesis"]["hypothesis_id"]==hypothesis.hypothesis_id for item in existing): raise ValueError("hypothesis_id already exists")
        previous=existing[-1]["entry_hash"] if existing else self.GENESIS
        payload=self._hypothesis_payload(hypothesis); sequence=len(existing)+1
        entry_hash=self._entry_hash(sequence,previous,payload)
        entry={"schema_version":1,"sequence":sequence,"previous_entry_hash":previous,"hypothesis":payload,"entry_hash":entry_hash}
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open("a",encoding="utf-8") as stream: stream.write(json.dumps(entry,sort_keys=True,separators=(",",":"))+"\n")
        return entry

    def read_all(self):
        if not self.path.exists(): return ()
        if not self.path.is_file(): raise ValueError("hypothesis ledger path must be a file")
        result=[]; previous=self.GENESIS; identities=set()
        with self.path.open("r",encoding="utf-8") as stream:
            for number,line in enumerate(stream,1):
                if not line.strip(): continue
                try: entry=json.loads(line); hypothesis=self._parse_hypothesis(entry["hypothesis"])
                except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"Invalid hypothesis entry at line {number}: {exc}") from exc
                if entry.get("schema_version")!=1 or entry.get("sequence")!=number: raise ValueError(f"Invalid hypothesis sequence at line {number}")
                if entry.get("previous_entry_hash")!=previous: raise ValueError(f"Broken hypothesis hash chain at line {number}")
                expected=self._entry_hash(number,previous,self._hypothesis_payload(hypothesis))
                if entry.get("entry_hash")!=expected: raise ValueError(f"Invalid hypothesis entry hash at line {number}")
                if hypothesis.hypothesis_id in identities: raise ValueError(f"Duplicate hypothesis_id at line {number}")
                identities.add(hypothesis.hypothesis_id); result.append(entry); previous=expected
        return tuple(result)

    @classmethod
    def _entry_hash(cls,sequence,previous,payload):
        canonical={"sequence":sequence,"previous_entry_hash":previous,"hypothesis":payload}
        return hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

    @classmethod
    def _validate_hypothesis(cls,item):
        if not isinstance(item,FrozenPreInflectionHypothesis): raise ValueError("hypothesis must be FrozenPreInflectionHypothesis")
        if item.frozen_at.tzinfo is None or item.target_date.tzinfo is None or item.frozen_at>=item.target_date: raise ValueError("hypothesis must be frozen before target with timezone-aware dates")
        expected=FrozenPreInflectionHypothesis.fingerprint(hypothesis_id=item.hypothesis_id,case_id=item.case_id,metric_id=item.metric_id,geography_id=item.geography_id,direction=item.direction,threshold_value=item.threshold_value,baseline_value=item.baseline_value,target_date=item.target_date,frozen_at=item.frozen_at,confidence_percent=item.confidence_percent,evidence_fingerprints=item.evidence_fingerprints)
        if expected!=item.hypothesis_fingerprint: raise ValueError("hypothesis fingerprint mismatch")
        if not item.non_authority_statement.strip(): raise ValueError("non-authority statement is required")

    @staticmethod
    def _hypothesis_payload(item):
        payload=asdict(item); payload["direction"]=item.direction.value if isinstance(item.direction,HypothesisDirection) else str(item.direction); payload["target_date"]=item.target_date.isoformat(); payload["frozen_at"]=item.frozen_at.isoformat(); payload["evidence_fingerprints"]=list(item.evidence_fingerprints); return payload

    @classmethod
    def _parse_hypothesis(cls,value):
        item=FrozenPreInflectionHypothesis(value["hypothesis_id"],value["case_id"],value["metric_id"],value["geography_id"],HypothesisDirection(value["direction"]),float(value["threshold_value"]),None if value["baseline_value"] is None else float(value["baseline_value"]),datetime.fromisoformat(value["target_date"]),datetime.fromisoformat(value["frozen_at"]),float(value["confidence_percent"]),tuple(value["evidence_fingerprints"]),value["hypothesis_fingerprint"],value["non_authority_statement"])
        cls._validate_hypothesis(item); return item


__all__=["PreInflectionHypothesisLedger"]
