"""Append-only explicit taxonomy classification; never creates a Catalyst."""
from __future__ import annotations
import hashlib,json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_classification_receipt import HistoricalComparisonCatalystClassificationReceipt
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview import HistoricalComparisonCatalystEligibilityPreview
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview_builder import HistoricalComparisonCatalystEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision
from modules.opportunity.catalyst.catalyst_classifier import CatalystClassifier
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine

class HistoricalComparisonCatalystClassificationLedger:
 def __init__(self,path):
  self.path=Path(path)
  if str(self.path).strip() in {"","."}:raise ValueError("Catalyst classification receipt path must identify a file")
 def classify(self,creation,interpretation,conversion,decision,*,analyst,rationale,classified_at,classifier=None):
  eligibility=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,conversion,decision)
  if not eligibility.eligible_for_catalyst_review:raise ValueError("Signal is not eligible for Catalyst review")
  classified_at=self._datetime(classified_at,"classified_at")
  try:
   if classified_at<decision.reviewed_at or classified_at<creation.created_at:raise ValueError("classification timestamp precedes approved inputs")
  except TypeError as exc:raise ValueError("classification timestamps use inconsistent timezone awareness") from exc
  eligibility_fingerprint=self.eligibility_fingerprint(eligibility)
  if any(x.eligibility_fingerprint==eligibility_fingerprint for x in self.read_all()):raise ValueError("this exact eligible Signal was already classified")
  evidence=EvidenceItem(evidence_id=conversion.evidence_id,statement=conversion.statement,source=conversion.source,category=conversion.category,direction=conversion.direction,strength=conversion.strength,confidence=conversion.confidence,independent_confirmation=conversion.independent_confirmation,is_primary_source=conversion.is_primary_source,is_time_sensitive=conversion.is_time_sensitive,notes=conversion.notes)
  result=SignalInterpretationEngine().create(evidence=evidence,interpretation=interpretation.interpretation,signal_id=creation.signal_id)
  if not result.accepted or result.signal is None:raise ValueError(f"Signal reconstruction rejected: {result.reason}")
  signal=result.signal
  classification=(classifier or CatalystClassifier()).classify(signals=[signal],causal_chain=signal.causal_chain)
  primary_id=classification.primary.catalyst_id if classification.primary else ""
  primary_family=classification.primary.family.value if classification.primary else ""
  payload=self.classification_payload(classification)
  classification_fingerprint=self.classification_fingerprint(classification)
  receipt=HistoricalComparisonCatalystClassificationReceipt(1,eligibility_fingerprint,classification_fingerprint,creation.signal_id,creation.signal_fingerprint,decision.validation_fingerprint,primary_id,primary_family,tuple(payload["secondary_catalyst_ids"]),tuple(payload["secondary_families"]),float(classification.confidence),tuple(classification.reasoning),tuple(classification.matched_signals),tuple(classification.unclassified_signals),tuple(classification.warnings),self._text(analyst,"analyst"),self._text(rationale,"rationale"),classified_at)
  receipt=self._parse(self._payload(receipt));self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open("a",encoding="utf-8") as ledger:ledger.write(json.dumps(self._payload(receipt),sort_keys=True,separators=(",",":"))+"\n")
  return classification,receipt
 def read_all(self):
  if not self.path.exists():return ()
  if not self.path.is_file():raise ValueError("Catalyst classification receipt path must be a file")
  result=[];seen=set()
  with self.path.open("r",encoding="utf-8") as ledger:
   for number,line in enumerate(ledger,1):
    if not line.strip():continue
    try:item=self._parse(json.loads(line))
    except (KeyError,TypeError,ValueError) as exc:raise ValueError(f"Invalid Catalyst classification receipt at line {number}: {exc}") from exc
    if item.eligibility_fingerprint in seen:raise ValueError(f"Duplicate Catalyst classification receipt at line {number}")
    seen.add(item.eligibility_fingerprint);result.append(item)
  return tuple(result)
 @staticmethod
 def eligibility_fingerprint(preview):
  if not isinstance(preview,HistoricalComparisonCatalystEligibilityPreview):raise ValueError("preview must be a Catalyst eligibility preview")
  payload={**preview.__dict__,"blockers":list(preview.blockers),"conditions":list(preview.conditions),"monitoring_requirements":list(preview.monitoring_requirements)}
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @staticmethod
 def classification_payload(classification):
  primary_id=classification.primary.catalyst_id if classification.primary else ""
  primary_family=classification.primary.family.value if classification.primary else ""
  return {"primary_catalyst_id":primary_id,"primary_family":primary_family,"secondary_catalyst_ids":[x.catalyst_id for x in classification.secondary],"secondary_families":[x.family.value for x in classification.secondary],"confidence":classification.confidence,"reasoning":list(classification.reasoning),"matched_signals":list(classification.matched_signals),"unclassified_signals":list(classification.unclassified_signals),"warnings":list(classification.warnings)}
 @classmethod
 def classification_fingerprint(cls,classification):
  payload=cls.classification_payload(classification)
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 @classmethod
 def _parse(cls,p):
  if not isinstance(p,dict) or p.get("schema_version")!=1:raise ValueError("unsupported Catalyst classification schema")
  confidence=p["confidence"]
  if isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0<=float(confidence)<=100:raise ValueError("confidence must be between 0 and 100")
  return HistoricalComparisonCatalystClassificationReceipt(1,cls._sha(p["eligibility_fingerprint"],"eligibility_fingerprint"),cls._sha(p["classification_fingerprint"],"classification_fingerprint"),cls._text(p["signal_id"],"signal_id"),cls._sha(p["signal_fingerprint"],"signal_fingerprint"),cls._sha(p["validation_fingerprint"],"validation_fingerprint"),cls._optional(p["primary_catalyst_id"],"primary_catalyst_id"),cls._optional(p["primary_family"],"primary_family"),cls._texts(p["secondary_catalyst_ids"],"secondary_catalyst_ids"),cls._texts(p["secondary_families"],"secondary_families"),float(confidence),cls._texts(p["reasoning"],"reasoning"),cls._texts(p["matched_signals"],"matched_signals"),cls._texts(p["unclassified_signals"],"unclassified_signals"),cls._texts(p["warnings"],"warnings"),cls._text(p["analyst"],"analyst"),cls._text(p["rationale"],"rationale"),cls._iso(p["classified_at"]))
 @staticmethod
 def _payload(x):return {**x.__dict__,"secondary_catalyst_ids":list(x.secondary_catalyst_ids),"secondary_families":list(x.secondary_families),"reasoning":list(x.reasoning),"matched_signals":list(x.matched_signals),"unclassified_signals":list(x.unclassified_signals),"warnings":list(x.warnings),"classified_at":x.classified_at.isoformat()}
 @staticmethod
 def _text(v,n):
  if not isinstance(v,str) or not v.strip():raise ValueError(f"{n} must not be empty")
  return v.strip()
 @staticmethod
 def _optional(v,n):
  if not isinstance(v,str):raise ValueError(f"{n} must be text")
  return v.strip()
 @classmethod
 def _texts(cls,v,n):
  if not isinstance(v,(list,tuple)):raise ValueError(f"{n} must be a list")
  return tuple(cls._text(x,n) for x in v)
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
  if not isinstance(v,str):raise ValueError("classified_at must be ISO datetime")
  return cls._datetime(datetime.fromisoformat(v),"classified_at")

__all__=["HistoricalComparisonCatalystClassificationLedger"]
