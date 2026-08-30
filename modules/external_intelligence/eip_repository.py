"""Append-only fingerprinted storage for governed EIP classifications."""

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from modules.external_intelligence.eip_classification import EIPClassificationPreview, EIPRiskDisposition, EIPStage, EIPValuationRoom


@dataclass(frozen=True)
class StoredEIPClassification:
    classification_fingerprint: str
    classification: EIPClassificationPreview


class EIPRepository:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("EIP repository path must identify a file")

    def add(self, classification):
        if not isinstance(classification, EIPClassificationPreview): raise ValueError("classification must be EIPClassificationPreview")
        if any(item.classification.classification_id == classification.classification_id for item in self.all()): raise ValueError("classification_id already exists")
        payload = self.classification_payload(classification); fingerprint = self.fingerprint_payload(payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps({"classification_fingerprint": fingerprint, "classification": payload}, sort_keys=True, separators=(",", ":")) + "\n")
        return StoredEIPClassification(fingerprint, classification)

    def all(self):
        if not self.path.exists(): return ()
        result, ids, fingerprints = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try:
                    envelope = json.loads(line); item = self.parse_classification(envelope["classification"]); fingerprint = self._sha(envelope["classification_fingerprint"])
                    if fingerprint != self.fingerprint_payload(self.classification_payload(item)): raise ValueError("classification fingerprint mismatch")
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid EIP classification at line {number}: {exc}") from exc
                if item.classification_id in ids or fingerprint in fingerprints: raise ValueError(f"Duplicate EIP classification at line {number}")
                ids.add(item.classification_id); fingerprints.add(fingerprint); result.append(StoredEIPClassification(fingerprint, item))
        return tuple(result)

    @staticmethod
    def classification_payload(item):
        payload = {**item.__dict__, "stage": item.stage.value, "risk_disposition": item.risk_disposition.value, "valuation_room": item.valuation_room.value}
        for name in ("reason_codes", "confirmation_requirements", "invalidation_conditions"): payload[name] = list(payload[name])
        return payload
    @staticmethod
    def parse_classification(value):
        kwargs = dict(value)
        for name in ("reason_codes", "confirmation_requirements", "invalidation_conditions"):
            if not isinstance(kwargs[name], list): raise ValueError(f"{name} must be a list")
            kwargs[name] = tuple(kwargs[name])
        kwargs["stage"] = EIPStage(kwargs["stage"]); kwargs["risk_disposition"] = EIPRiskDisposition(kwargs["risk_disposition"]); kwargs["valuation_room"] = EIPValuationRoom(kwargs["valuation_room"])
        return EIPClassificationPreview(**kwargs)
    @staticmethod
    def fingerprint_payload(value): return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()


__all__ = ["EIPRepository", "StoredEIPClassification"]
