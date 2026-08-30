"""Append-only fingerprinted Price Recognition preview storage."""

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from modules.external_intelligence.price_recognition import PriceRecognitionPreview, PriceRecognitionState


@dataclass(frozen=True)
class StoredPriceRecognition:
    recognition_fingerprint: str
    preview: PriceRecognitionPreview


class PriceRecognitionRepository:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("Price Recognition repository path must identify a file")

    def add(self, preview):
        if not isinstance(preview, PriceRecognitionPreview): raise ValueError("preview must be PriceRecognitionPreview")
        if any(item.preview.snapshot_id == preview.snapshot_id for item in self.all()): raise ValueError("snapshot_id already exists")
        payload = self.preview_payload(preview); fingerprint = self.fingerprint_payload(payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps({"recognition_fingerprint": fingerprint, "preview": payload}, sort_keys=True, separators=(",", ":")) + "\n")
        return StoredPriceRecognition(fingerprint, preview)

    def all(self):
        if not self.path.exists(): return ()
        result, ids, fingerprints = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try:
                    envelope = json.loads(line); preview = self.parse_preview(envelope["preview"]); fingerprint = self._sha(envelope["recognition_fingerprint"])
                    if fingerprint != self.fingerprint_payload(self.preview_payload(preview)): raise ValueError("recognition fingerprint mismatch")
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Price Recognition at line {number}: {exc}") from exc
                if preview.snapshot_id in ids or fingerprint in fingerprints: raise ValueError(f"Duplicate Price Recognition at line {number}")
                ids.add(preview.snapshot_id); fingerprints.add(fingerprint); result.append(StoredPriceRecognition(fingerprint, preview))
        return tuple(result)

    @staticmethod
    def preview_payload(item):
        payload = {**item.__dict__, "state": item.state.value}
        for name in ("recognized_dimensions", "available_dimensions", "missing_dimensions", "reason_codes"): payload[name] = list(payload[name])
        return payload

    @staticmethod
    def parse_preview(value):
        if not isinstance(value, dict): raise ValueError("invalid Price Recognition payload")
        kwargs = dict(value)
        for name in ("recognized_dimensions", "available_dimensions", "missing_dimensions", "reason_codes"):
            if not isinstance(kwargs[name], list): raise ValueError(f"{name} must be a list")
            kwargs[name] = tuple(kwargs[name])
        kwargs["state"] = PriceRecognitionState(kwargs["state"])
        return PriceRecognitionPreview(**kwargs)
    @staticmethod
    def fingerprint_payload(value): return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()


__all__ = ["PriceRecognitionRepository", "StoredPriceRecognition"]
