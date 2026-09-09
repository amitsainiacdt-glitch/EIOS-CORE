"""Canonical SHA-256 fingerprints for controlled-write contracts."""

from __future__ import annotations

import dataclasses
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Mapping

from .contracts import WriteCommand, WriteReceipt


def _canonical(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {field.name: _canonical(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _canonical(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"unsupported fingerprint value: {type(value).__name__}")


def _digest(payload: Any) -> str:
    encoded = json.dumps(_canonical(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def command_fingerprint(command: WriteCommand) -> str:
    if not isinstance(command, WriteCommand):
        raise ValueError("command must be a WriteCommand")
    payload = {field.name: getattr(command, field.name) for field in dataclasses.fields(command) if field.name != "declared_request_fingerprint"}
    return _digest(payload)


def record_fingerprint_payload(payload: Mapping[str, Any]) -> str:
    return _digest(payload)


def receipt_fingerprint(receipt: WriteReceipt) -> str:
    if not isinstance(receipt, WriteReceipt):
        raise ValueError("receipt must be a WriteReceipt")
    payload = {field.name: getattr(receipt, field.name) for field in dataclasses.fields(receipt) if field.name != "receipt_fingerprint"}
    return _digest(payload)


def verify_receipt_fingerprint(receipt: WriteReceipt) -> bool:
    return isinstance(receipt, WriteReceipt) and receipt.receipt_fingerprint == receipt_fingerprint(receipt)


__all__ = ["command_fingerprint", "receipt_fingerprint", "record_fingerprint_payload", "verify_receipt_fingerprint"]
