"""Append-only explicit Signal creation with no downstream publication."""
from __future__ import annotations
import hashlib, json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine

class HistoricalComparisonSignalCreationLedger:
    SCHEMA_VERSION=1
    def __init__(self,path):
        self.path=Path(path)
        if str(self.path).strip() in {"","."}: raise ValueError("Signal creation receipt path must identify a file")

    def materialize(self,interpretation,conversion,*,signal_id,creator,created_at,engine=None):
        if not isinstance(interpretation,HistoricalComparisonSignalInterpretation): raise ValueError("interpretation must be an approved historical Signal interpretation")
        if not isinstance(conversion,HistoricalComparisonEvidenceConversionReceipt): raise ValueError("conversion must be an Evidence conversion receipt")
        if interpretation.evidence_id!=conversion.evidence_id: raise ValueError("interpretation and conversion bind different EvidenceItems")
        signal_id=self._text(signal_id,"signal_id"); creator=self._text(creator,"creator"); created_at=self._datetime(created_at,"created_at")
        try:
            if created_at<interpretation.interpreted_at or created_at<conversion.converted_at: raise ValueError("Signal creation timestamp precedes its approved inputs")
        except TypeError as exc: raise ValueError("Signal creation timestamps use inconsistent timezone awareness") from exc
        existing=self.read_all()
        if any(x.signal_id==signal_id for x in existing): raise ValueError("signal_id already has a creation receipt")
        if any((x.governed_input_fingerprint,x.evidence_id)==(interpretation.governed_input_fingerprint,interpretation.evidence_id) for x in existing): raise ValueError("this approved interpretation was already materialized")
        evidence=EvidenceItem(evidence_id=conversion.evidence_id,statement=conversion.statement,source=conversion.source,category=conversion.category,direction=conversion.direction,strength=conversion.strength,confidence=conversion.confidence,independent_confirmation=conversion.independent_confirmation,is_primary_source=conversion.is_primary_source,is_time_sensitive=conversion.is_time_sensitive,notes=conversion.notes)
        result=(engine or SignalInterpretationEngine()).create(evidence=evidence,interpretation=interpretation.interpretation,signal_id=signal_id)
        if not result.accepted or result.signal is None: raise ValueError(f"Signal creation rejected: {result.reason}")
        signal=result.signal
        fingerprint=self._fingerprint(signal)
        receipt=HistoricalComparisonSignalCreationReceipt(1,interpretation.governed_input_fingerprint,interpretation.pack_fingerprint,interpretation.evidence_id,signal.signal_id,fingerprint,signal.title,signal.domain.value,signal.signal_type.value,signal.direction.value,signal.stage.value,signal.horizon.value,creator,created_at)
        receipt=self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open("a",encoding="utf-8") as ledger: ledger.write(json.dumps(self._payload(receipt),sort_keys=True,separators=(",",":"))+"\n")
        return signal,receipt

    def read_all(self):
        if not self.path.exists(): return ()
        if not self.path.is_file(): raise ValueError("Signal creation receipt path must be a file")
        records=[]; ids=set(); inputs=set()
        with self.path.open("r",encoding="utf-8") as ledger:
            for number,line in enumerate(ledger,1):
                if not line.strip(): continue
                try: item=self._parse(json.loads(line))
                except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"Invalid Signal creation receipt at line {number}: {exc}") from exc
                key=(item.governed_input_fingerprint,item.evidence_id)
                if item.signal_id in ids or key in inputs: raise ValueError(f"Duplicate Signal creation receipt at line {number}")
                ids.add(item.signal_id); inputs.add(key); records.append(item)
        return tuple(records)

    @classmethod
    def _fingerprint(cls,signal):
        def clean(value):
            if isinstance(value,Enum): return value.value
            if isinstance(value,dict): return {k:clean(v) for k,v in value.items()}
            if isinstance(value,(list,tuple)): return [clean(v) for v in value]
            return value
        payload=json.dumps(clean(asdict(signal)),sort_keys=True,separators=(",",":"),ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
    @classmethod
    def _parse(cls,p):
        if not isinstance(p,dict) or p.get("schema_version")!=1: raise ValueError("unsupported Signal creation schema")
        return HistoricalComparisonSignalCreationReceipt(1,cls._sha(p["governed_input_fingerprint"],"governed_input_fingerprint"),cls._sha(p["pack_fingerprint"],"pack_fingerprint"),cls._text(p["evidence_id"],"evidence_id"),cls._text(p["signal_id"],"signal_id"),cls._sha(p["signal_fingerprint"],"signal_fingerprint"),cls._text(p["title"],"title"),cls._text(p["domain"],"domain"),cls._text(p["signal_type"],"signal_type"),cls._text(p["direction"],"direction"),cls._text(p["stage"],"stage"),cls._text(p["horizon"],"horizon"),cls._text(p["creator"],"creator"),cls._iso(p["created_at"]))
    @staticmethod
    def _payload(x): return {**x.__dict__,"created_at":x.created_at.isoformat()}
    @staticmethod
    def _text(v,n):
        if not isinstance(v,str) or not v.strip(): raise ValueError(f"{n} must not be empty")
        return v.strip()
    @classmethod
    def _sha(cls,v,n):
        v=cls._text(v,n)
        if len(v)!=64: raise ValueError(f"{n} must be SHA-256")
        try: int(v,16)
        except ValueError as exc: raise ValueError(f"{n} must be SHA-256") from exc
        return v.casefold()
    @staticmethod
    def _datetime(v,n):
        if not isinstance(v,datetime): raise ValueError(f"{n} must be a datetime")
        return v
    @classmethod
    def _iso(cls,v):
        if not isinstance(v,str): raise ValueError("created_at must be an ISO datetime")
        return cls._datetime(datetime.fromisoformat(v),"created_at")

__all__=["HistoricalComparisonSignalCreationLedger"]
