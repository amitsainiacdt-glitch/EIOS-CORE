"""Append-only human stage review; never mutates canonical Signals."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview import HistoricalComparisonMultiSignalCatalystSupportPreview
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_stage_review import HistoricalComparisonSignalStageReview,HistoricalComparisonSignalStageReviewDisposition
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision,HistoricalComparisonSignalValidationDisposition
from modules.opportunity.signals.signal_model import SignalStage

class HistoricalComparisonSignalStageReviewLedger:
 def __init__(self,path):
  self.path=Path(path)
  if str(self.path).strip() in {"","."}:raise ValueError("Signal stage review path must identify a file")
 def record(self,support,interpretation,validation_decision,*,target_stage,disposition,conditions=(),monitoring_requirements=(),reviewer,rationale,reviewed_at):
  if not isinstance(support,HistoricalComparisonMultiSignalCatalystSupportPreview):raise ValueError("support must be a multi-Signal Catalyst support preview")
  if not isinstance(interpretation,HistoricalComparisonSignalInterpretation):raise ValueError("interpretation must be an approved Signal interpretation")
  if not isinstance(validation_decision,HistoricalComparisonSignalValidationDecision):raise ValueError("validation_decision must be a human Signal validation decision")
  try:target_stage=target_stage if isinstance(target_stage,SignalStage) else SignalStage(target_stage)
  except (TypeError,ValueError) as exc:raise ValueError("target_stage is invalid") from exc
  try:disposition=disposition if isinstance(disposition,HistoricalComparisonSignalStageReviewDisposition) else HistoricalComparisonSignalStageReviewDisposition(disposition)
  except (TypeError,ValueError) as exc:raise ValueError("disposition must be Approved, Rejected, or Deferred") from exc
  current=interpretation.interpretation.stage
  if current!=SignalStage.EMERGING or target_stage!=SignalStage.VALIDATED:raise ValueError("only Emerging Signal to Validated Signal review is supported")
  try:index=support.signal_ids.index(validation_decision.signal_id)
  except ValueError as exc:raise ValueError("Signal is not part of the exact multi-Signal support preview") from exc
  if support.signal_fingerprints[index]!=validation_decision.signal_fingerprint or support.validation_fingerprints[index]!=validation_decision.validation_fingerprint:raise ValueError("Signal review provenance differs from the support preview")
  if validation_decision.disposition!=HistoricalComparisonSignalValidationDisposition.APPROVED:raise ValueError("Signal validation decision is not Approved")
  if interpretation.evidence_id!=validation_decision.evidence_id:raise ValueError("interpretation and validation decision bind different EvidenceItems")
  if disposition==HistoricalComparisonSignalStageReviewDisposition.APPROVED and not (support.independently_supported and support.cluster_emerging and support.stage_promotion_required):raise ValueError("multi-Signal support does not justify stage promotion review approval")
  reviewed_at=self._datetime(reviewed_at,"reviewed_at")
  try:
   if reviewed_at<validation_decision.reviewed_at:raise ValueError("stage review timestamp precedes Signal validation approval")
  except TypeError as exc:raise ValueError("stage review timestamps use inconsistent timezone awareness") from exc
  key=(support.support_fingerprint,validation_decision.signal_fingerprint,target_stage)
  if any((x.support_fingerprint,x.signal_fingerprint,x.target_stage)==key for x in self.read_all()):raise ValueError("stage review already exists for this exact support, Signal, and target")
  review=HistoricalComparisonSignalStageReview(1,self._sha(support.support_fingerprint,"support_fingerprint"),validation_decision.signal_id,validation_decision.signal_fingerprint,validation_decision.validation_fingerprint,current,target_stage,disposition,self._texts(conditions,"conditions"),self._texts(monitoring_requirements,"monitoring_requirements"),self._text(reviewer,"reviewer"),self._text(rationale,"rationale"),reviewed_at)
  review=self._parse(self._payload(review));self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open("a",encoding="utf-8") as ledger:ledger.write(json.dumps(self._payload(review),sort_keys=True,separators=(",",":"))+"\n")
  return review
 def read_all(self):
  if not self.path.exists():return ()
  if not self.path.is_file():raise ValueError("Signal stage review path must be a file")
  result=[];seen=set()
  with self.path.open("r",encoding="utf-8") as ledger:
   for number,line in enumerate(ledger,1):
    if not line.strip():continue
    try:item=self._parse(json.loads(line))
    except (KeyError,TypeError,ValueError) as exc:raise ValueError(f"Invalid Signal stage review at line {number}: {exc}") from exc
    key=(item.support_fingerprint,item.signal_fingerprint,item.target_stage)
    if key in seen:raise ValueError(f"Duplicate Signal stage review at line {number}")
    seen.add(key);result.append(item)
  return tuple(result)
 @classmethod
 def _parse(cls,p):
  if not isinstance(p,dict) or p.get("schema_version")!=1:raise ValueError("unsupported Signal stage review schema")
  try:current=SignalStage(p["current_stage"]);target=SignalStage(p["target_stage"]);disposition=HistoricalComparisonSignalStageReviewDisposition(p["disposition"])
  except (TypeError,ValueError) as exc:raise ValueError("invalid stage review enum value") from exc
  if current!=SignalStage.EMERGING or target!=SignalStage.VALIDATED:raise ValueError("unsupported persisted stage transition")
  return HistoricalComparisonSignalStageReview(1,cls._sha(p["support_fingerprint"],"support_fingerprint"),cls._text(p["signal_id"],"signal_id"),cls._sha(p["signal_fingerprint"],"signal_fingerprint"),cls._sha(p["validation_fingerprint"],"validation_fingerprint"),current,target,disposition,cls._texts(p["conditions"],"conditions"),cls._texts(p["monitoring_requirements"],"monitoring_requirements"),cls._text(p["reviewer"],"reviewer"),cls._text(p["rationale"],"rationale"),cls._iso(p["reviewed_at"]))
 @staticmethod
 def _payload(x):return {**x.__dict__,"current_stage":x.current_stage.value,"target_stage":x.target_stage.value,"disposition":x.disposition.value,"conditions":list(x.conditions),"monitoring_requirements":list(x.monitoring_requirements),"reviewed_at":x.reviewed_at.isoformat()}
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

__all__=["HistoricalComparisonSignalStageReviewLedger"]
