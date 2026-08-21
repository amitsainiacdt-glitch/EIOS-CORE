"""Append-only human decisions for exact promoted-stage Catalyst previews."""
from __future__ import annotations
import hashlib,json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview import HistoricalComparisonPromotedStageCatalystPreview
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_decision import HistoricalComparisonPromotedCatalystAssessmentDecision,HistoricalComparisonPromotedCatalystAssessmentDisposition

class HistoricalComparisonPromotedCatalystAssessmentLedger:
 def __init__(self,path):
  self.path=Path(path)
  if str(self.path).strip() in {"","."}:raise ValueError("promoted Catalyst assessment path must identify a file")
 def record(self,preview,*,disposition,conditions=(),monitoring_requirements=(),reviewer,rationale,reviewed_at):
  if not isinstance(preview,HistoricalComparisonPromotedStageCatalystPreview):raise ValueError("preview must be a promoted-stage Catalyst preview")
  try:disposition=disposition if isinstance(disposition,HistoricalComparisonPromotedCatalystAssessmentDisposition) else HistoricalComparisonPromotedCatalystAssessmentDisposition(disposition)
  except (TypeError,ValueError) as exc:raise ValueError("disposition must be Approved, Rejected, or Deferred") from exc
  if disposition==HistoricalComparisonPromotedCatalystAssessmentDisposition.APPROVED and not preview.promoted_meets_minimum:raise ValueError("a below-threshold promoted Catalyst preview cannot be approved")
  reviewed_at=self._datetime(reviewed_at,"reviewed_at");fingerprint=self.preview_fingerprint(preview)
  if any(x.preview_fingerprint==fingerprint for x in self.read_all()):raise ValueError("a decision already exists for this exact promoted Catalyst preview")
  decision=HistoricalComparisonPromotedCatalystAssessmentDecision(1,fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,preview.catalyst_id,preview.signal_ids,preview.promoted_signal_ids,disposition,self._texts(conditions,"conditions"),self._texts(monitoring_requirements,"monitoring_requirements"),self._text(reviewer,"reviewer"),self._text(rationale,"rationale"),reviewed_at)
  decision=self._parse(self._payload(decision));self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open("a",encoding="utf-8") as ledger:ledger.write(json.dumps(self._payload(decision),sort_keys=True,separators=(",",":"))+"\n")
  return decision
 def read_all(self):
  if not self.path.exists():return ()
  if not self.path.is_file():raise ValueError("promoted Catalyst assessment path must be a file")
  result=[];seen=set()
  with self.path.open("r",encoding="utf-8") as ledger:
   for number,line in enumerate(ledger,1):
    if not line.strip():continue
    try:item=self._parse(json.loads(line))
    except (KeyError,TypeError,ValueError) as exc:raise ValueError(f"Invalid promoted Catalyst assessment at line {number}: {exc}") from exc
    if item.preview_fingerprint in seen:raise ValueError(f"Duplicate promoted Catalyst assessment at line {number}")
    seen.add(item.preview_fingerprint);result.append(item)
  return tuple(result)
 @staticmethod
 def preview_fingerprint(preview):
  if not isinstance(preview,HistoricalComparisonPromotedStageCatalystPreview):raise ValueError("preview must be a promoted-stage Catalyst preview")
  payload={**preview.__dict__}
  for key in ("signal_ids","promoted_signal_ids","original_stages","effective_stages","reasons","warnings"):payload[key]=list(payload[key])
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @classmethod
 def _parse(cls,p):
  if not isinstance(p,dict) or p.get("schema_version")!=1:raise ValueError("unsupported promoted Catalyst assessment schema")
  try:d=HistoricalComparisonPromotedCatalystAssessmentDisposition(p["disposition"])
  except (TypeError,ValueError) as exc:raise ValueError("invalid disposition") from exc
  signal_ids=cls._texts(p["signal_ids"],"signal_ids");promoted=cls._texts(p["promoted_signal_ids"],"promoted_signal_ids")
  if not signal_ids or not promoted or not set(promoted).issubset(signal_ids):raise ValueError("promoted Signal IDs must be a non-empty subset of Signal IDs")
  return HistoricalComparisonPromotedCatalystAssessmentDecision(1,cls._sha(p["preview_fingerprint"],"preview_fingerprint"),cls._sha(p["promotion_fingerprint"],"promotion_fingerprint"),cls._sha(p["support_fingerprint"],"support_fingerprint"),cls._text(p["catalyst_id"],"catalyst_id"),signal_ids,promoted,d,cls._texts(p["conditions"],"conditions"),cls._texts(p["monitoring_requirements"],"monitoring_requirements"),cls._text(p["reviewer"],"reviewer"),cls._text(p["rationale"],"rationale"),cls._iso(p["reviewed_at"]))
 @staticmethod
 def _payload(x):return {**x.__dict__,"signal_ids":list(x.signal_ids),"promoted_signal_ids":list(x.promoted_signal_ids),"disposition":x.disposition.value,"conditions":list(x.conditions),"monitoring_requirements":list(x.monitoring_requirements),"reviewed_at":x.reviewed_at.isoformat()}
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
  if not isinstance(v,str):raise ValueError("reviewed_at must be ISO datetime")
  return cls._datetime(datetime.fromisoformat(v),"reviewed_at")

__all__=["HistoricalComparisonPromotedCatalystAssessmentLedger"]
