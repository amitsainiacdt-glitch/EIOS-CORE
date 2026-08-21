"""Append-only human decisions for exact read-only validation previews."""
from __future__ import annotations
import hashlib,json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision,HistoricalComparisonSignalValidationDisposition
from modules.external_intelligence.historical_comparison_signal_validation_preview import HistoricalComparisonSignalValidationPreview

class HistoricalComparisonSignalValidationDecisionLedger:
 SCHEMA_VERSION=1
 def __init__(self,path):
  self.path=Path(path)
  if str(self.path).strip() in {"","."}: raise ValueError("Signal validation decision path must identify a file")
 def record(self,preview,creation,*,disposition,conditions=(),monitoring_requirements=(),reviewer,rationale,reviewed_at):
  if not isinstance(preview,HistoricalComparisonSignalValidationPreview): raise ValueError("preview must be a Signal validation preview")
  if not isinstance(creation,HistoricalComparisonSignalCreationReceipt): raise ValueError("creation must be a Signal creation receipt")
  if (preview.signal_id,preview.signal_fingerprint,preview.governed_input_fingerprint,preview.evidence_id)!=(creation.signal_id,creation.signal_fingerprint,creation.governed_input_fingerprint,creation.evidence_id): raise ValueError("validation preview does not bind to the creation receipt")
  try: disposition=disposition if isinstance(disposition,HistoricalComparisonSignalValidationDisposition) else HistoricalComparisonSignalValidationDisposition(disposition)
  except (TypeError,ValueError) as exc: raise ValueError("disposition must be Approved, Rejected, or Deferred") from exc
  if disposition==HistoricalComparisonSignalValidationDisposition.APPROVED and (not preview.valid or preview.invalidation_reasons): raise ValueError("an invalid Signal validation cannot be approved")
  reviewed_at=self._datetime(reviewed_at,"reviewed_at")
  try:
   if reviewed_at<creation.created_at: raise ValueError("decision timestamp precedes Signal creation")
  except TypeError as exc: raise ValueError("decision timestamps use inconsistent timezone awareness") from exc
  fingerprint=self.validation_fingerprint(preview)
  if any(x.validation_fingerprint==fingerprint for x in self.read_all()): raise ValueError("a decision already exists for this exact validation result")
  decision=HistoricalComparisonSignalValidationDecision(1,fingerprint,preview.signal_fingerprint,preview.signal_id,preview.governed_input_fingerprint,preview.evidence_id,disposition,self._texts(conditions,"conditions"),self._texts(monitoring_requirements,"monitoring_requirements"),self._text(reviewer,"reviewer"),self._text(rationale,"rationale"),reviewed_at)
  decision=self._parse(self._payload(decision)); self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open("a",encoding="utf-8") as ledger: ledger.write(json.dumps(self._payload(decision),sort_keys=True,separators=(",",":"))+"\n")
  return decision
 def read_all(self):
  if not self.path.exists(): return ()
  if not self.path.is_file(): raise ValueError("Signal validation decision path must be a file")
  result=[];seen=set()
  with self.path.open("r",encoding="utf-8") as ledger:
   for number,line in enumerate(ledger,1):
    if not line.strip(): continue
    try:item=self._parse(json.loads(line))
    except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"Invalid Signal validation decision at line {number}: {exc}") from exc
    if item.validation_fingerprint in seen: raise ValueError(f"Duplicate Signal validation decision at line {number}")
    seen.add(item.validation_fingerprint);result.append(item)
  return tuple(result)
 @staticmethod
 def validation_fingerprint(preview):
  if not isinstance(preview,HistoricalComparisonSignalValidationPreview): raise ValueError("preview must be a Signal validation preview")
  payload={**preview.__dict__,"reasons":list(preview.reasons),"warnings":list(preview.warnings),"invalidation_reasons":list(preview.invalidation_reasons)}
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @classmethod
 def _parse(cls,p):
  if not isinstance(p,dict) or p.get("schema_version")!=1: raise ValueError("unsupported Signal validation decision schema")
  try:d=HistoricalComparisonSignalValidationDisposition(p["disposition"])
  except (TypeError,ValueError) as exc: raise ValueError("invalid disposition") from exc
  return HistoricalComparisonSignalValidationDecision(1,cls._sha(p["validation_fingerprint"],"validation_fingerprint"),cls._sha(p["signal_fingerprint"],"signal_fingerprint"),cls._text(p["signal_id"],"signal_id"),cls._sha(p["governed_input_fingerprint"],"governed_input_fingerprint"),cls._text(p["evidence_id"],"evidence_id"),d,cls._texts(p["conditions"],"conditions"),cls._texts(p["monitoring_requirements"],"monitoring_requirements"),cls._text(p["reviewer"],"reviewer"),cls._text(p["rationale"],"rationale"),cls._iso(p["reviewed_at"]))
 @staticmethod
 def _payload(x):return {**x.__dict__,"disposition":x.disposition.value,"conditions":list(x.conditions),"monitoring_requirements":list(x.monitoring_requirements),"reviewed_at":x.reviewed_at.isoformat()}
 @staticmethod
 def _text(v,n):
  if not isinstance(v,str) or not v.strip():raise ValueError(f"{n} must not be empty")
  return v.strip()
 @classmethod
 def _texts(cls,v,n):
  if not isinstance(v,(list,tuple)):raise ValueError(f"{n} must be a list")
  values=tuple(cls._text(x,n) for x in v)
  if len({x.casefold() for x in values})!=len(values):raise ValueError(f"{n} must not contain duplicates")
  return values
 @classmethod
 def _sha(cls,v,n):
  v=cls._text(v,n)
  if len(v)!=64:raise ValueError(f"{n} must be SHA-256")
  try:int(v,16)
  except ValueError as exc:raise ValueError(f"{n} must be SHA-256") from exc
  return v.casefold()
 @staticmethod
 def _datetime(v,n):
  if not isinstance(v,datetime):raise ValueError(f"{n} must be a datetime")
  return v
 @classmethod
 def _iso(cls,v):
  if not isinstance(v,str):raise ValueError("reviewed_at must be an ISO datetime")
  return cls._datetime(datetime.fromisoformat(v),"reviewed_at")

__all__=["HistoricalComparisonSignalValidationDecisionLedger"]
