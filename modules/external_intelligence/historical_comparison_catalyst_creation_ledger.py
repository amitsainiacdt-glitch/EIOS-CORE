"""Explicit Catalyst materialization with append-only creation receipts."""
from __future__ import annotations
import hashlib,json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_creation_receipt import HistoricalComparisonCatalystCreationReceipt
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_decision import HistoricalComparisonPromotedCatalystAssessmentDecision,HistoricalComparisonPromotedCatalystAssessmentDisposition
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.opportunity.catalyst_engine import Catalyst,CatalystEngine

class HistoricalComparisonCatalystCreationLedger:
 def __init__(self,path):
  self.path=Path(path)
  if str(self.path).strip() in {"","."}:raise ValueError("Catalyst creation receipt path must identify a file")
 def materialize(self,inputs,reviews,assessment,*,theme,cluster_id,catalyst_id,trigger,description,economic_impact,earnings_impact,valuation_impact,creator,rationale,created_at,builder=None):
  if not isinstance(assessment,HistoricalComparisonPromotedCatalystAssessmentDecision):raise ValueError("assessment must be a promoted Catalyst assessment")
  if assessment.disposition!=HistoricalComparisonPromotedCatalystAssessmentDisposition.APPROVED:raise ValueError("only an Approved promoted Catalyst assessment may be materialized")
  creator=self._text(creator,"creator");rationale=self._text(rationale,"rationale");created_at=self._datetime(created_at,"created_at")
  try:
   if created_at<assessment.reviewed_at:raise ValueError("Catalyst creation timestamp precedes its human assessment")
  except TypeError as exc:raise ValueError("Catalyst timestamps use inconsistent timezone awareness") from exc
  existing=self.read_all()
  if any(x.catalyst_id==catalyst_id for x in existing):raise ValueError("catalyst_id already has a creation receipt")
  assessment_fingerprint=self._assessment_fingerprint(assessment)
  if any(x.assessment_fingerprint==assessment_fingerprint for x in existing):raise ValueError("this approved assessment was already materialized")
  preview,catalyst=(builder or HistoricalComparisonPromotedStageCatalystPreviewBuilder()).build_with_catalyst(inputs,reviews,theme=theme,cluster_id=cluster_id,catalyst_id=catalyst_id,trigger=trigger,description=description,economic_impact=economic_impact,earnings_impact=earnings_impact,valuation_impact=valuation_impact)
  fingerprint=HistoricalComparisonPromotedCatalystAssessmentLedger.preview_fingerprint(preview)
  if (fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,preview.catalyst_id,preview.signal_ids,preview.promoted_signal_ids)!=(assessment.preview_fingerprint,assessment.promotion_fingerprint,assessment.support_fingerprint,assessment.catalyst_id,assessment.signal_ids,assessment.promoted_signal_ids):raise ValueError("assessment does not bind to the reconstructed promoted Catalyst preview")
  if not preview.promoted_meets_minimum or catalyst.catalyst_score<CatalystEngine.MINIMUM_CATALYST_SCORE:raise ValueError("approved promoted Catalyst no longer meets the minimum score")
  catalyst_fingerprint=self._fingerprint(catalyst)
  receipt=HistoricalComparisonCatalystCreationReceipt(1,fingerprint,assessment_fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,catalyst.catalyst_id,catalyst_fingerprint,preview.signal_ids,preview.promoted_signal_ids,catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,catalyst.catalyst_score,catalyst.confidence,creator,rationale,created_at)
  receipt=self._parse(self._payload(receipt));self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open("a",encoding="utf-8") as ledger:ledger.write(json.dumps(self._payload(receipt),sort_keys=True,separators=(",",":"))+"\n")
  return catalyst,receipt
 def read_all(self):
  if not self.path.exists():return ()
  if not self.path.is_file():raise ValueError("Catalyst creation receipt path must be a file")
  result=[];ids=set();assessments=set()
  with self.path.open("r",encoding="utf-8") as ledger:
   for number,line in enumerate(ledger,1):
    if not line.strip():continue
    try:item=self._parse(json.loads(line))
    except (KeyError,TypeError,ValueError) as exc:raise ValueError(f"Invalid Catalyst creation receipt at line {number}: {exc}") from exc
    if item.catalyst_id in ids or item.assessment_fingerprint in assessments:raise ValueError(f"Duplicate Catalyst creation receipt at line {number}")
    ids.add(item.catalyst_id);assessments.add(item.assessment_fingerprint);result.append(item)
  return tuple(result)
 @classmethod
 def _fingerprint(cls,catalyst):
  if not isinstance(catalyst,Catalyst):raise ValueError("materializer did not return a Catalyst")
  def clean(value):
   if isinstance(value,Enum):return value.value
   if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
   if isinstance(value,(list,tuple)):return [clean(v) for v in value]
   return value
  return hashlib.sha256(json.dumps(clean(asdict(catalyst)),sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @staticmethod
 def _assessment_fingerprint(assessment):
  payload={**assessment.__dict__,"disposition":assessment.disposition.value,"signal_ids":list(assessment.signal_ids),"promoted_signal_ids":list(assessment.promoted_signal_ids),"conditions":list(assessment.conditions),"monitoring_requirements":list(assessment.monitoring_requirements),"reviewed_at":assessment.reviewed_at.isoformat()}
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @classmethod
 def _parse(cls,p):
  if not isinstance(p,dict) or p.get("schema_version")!=1:raise ValueError("unsupported Catalyst creation schema")
  signals=cls._texts(p["signal_ids"],"signal_ids");promoted=cls._texts(p["promoted_signal_ids"],"promoted_signal_ids")
  if not signals or not promoted or not set(promoted).issubset(signals):raise ValueError("promoted Signal IDs must be a non-empty subset")
  return HistoricalComparisonCatalystCreationReceipt(1,cls._sha(p["preview_fingerprint"],"preview_fingerprint"),cls._sha(p["assessment_fingerprint"],"assessment_fingerprint"),cls._sha(p["promotion_fingerprint"],"promotion_fingerprint"),cls._sha(p["support_fingerprint"],"support_fingerprint"),cls._text(p["catalyst_id"],"catalyst_id"),cls._sha(p["catalyst_fingerprint"],"catalyst_fingerprint"),signals,promoted,cls._text(p["primary_catalyst_id"],"primary_catalyst_id"),cls._text(p["primary_family"],"primary_family"),cls._number(p["catalyst_score"],"catalyst_score"),cls._number(p["confidence"],"confidence"),cls._text(p["creator"],"creator"),cls._text(p["rationale"],"rationale"),cls._iso(p["created_at"]))
 @staticmethod
 def _payload(x):return {**x.__dict__,"signal_ids":list(x.signal_ids),"promoted_signal_ids":list(x.promoted_signal_ids),"created_at":x.created_at.isoformat()}
 @staticmethod
 def _text(v,n):
  if not isinstance(v,str) or not v.strip():raise ValueError(f"{n} must not be empty")
  return v.strip()
 @classmethod
 def _texts(cls,v,n):
  if not isinstance(v,(list,tuple)):raise ValueError(f"{n} must be a list")
  values=tuple(cls._text(x,n) for x in v)
  if len(set(values))!=len(values):raise ValueError(f"{n} must not contain duplicates")
  return values
 @staticmethod
 def _number(v,n):
  if isinstance(v,bool) or not isinstance(v,(int,float)):raise ValueError(f"{n} must be numeric")
  return float(v)
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
  if not isinstance(v,str):raise ValueError("created_at must be ISO datetime")
  return cls._datetime(datetime.fromisoformat(v),"created_at")

__all__=["HistoricalComparisonCatalystCreationLedger"]
