"""Append-only audit ledger for public-source acquisition attempts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from modules.external_intelligence.observation_deduplication_service import ObservationDeduplicationService
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionReceipt, PublicSourceAcquisitionStatus


class PublicSourceAcquisitionLedger:
    PUBLIC = "PUBLIC"

    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("acquisition ledger path must identify a file")

    def record(self, *, acquisition_id, cycle_id, job_id, research_intent, source_url, status, requested_at, completed_at, requested_url=None, access_classification="PUBLIC", http_status=None, content_type=None, source_document_id=None, document_hash=None, bytes_received=0, error_code=None, error_message=None, recorder):
        if access_classification != self.PUBLIC:
            raise ValueError("only confirmed PUBLIC information may enter acquisition")
        try:
            status = status if isinstance(status, PublicSourceAcquisitionStatus) else PublicSourceAcquisitionStatus(status)
        except (TypeError, ValueError) as exc:
            raise ValueError("status must be RETRIEVED or FAILED") from exc
        requested_at, completed_at = self._datetime(requested_at, "requested_at"), self._datetime(completed_at, "completed_at")
        try:
            if completed_at < requested_at:
                raise ValueError("completed_at precedes requested_at")
        except TypeError as exc:
            raise ValueError("acquisition timestamps use inconsistent timezone awareness") from exc
        source_url = self._text(source_url, "source_url")
        requested_url = self._text(requested_url or source_url, "requested_url")
        canonical_url = ObservationDeduplicationService.canonicalize_url(source_url)
        source_domain = (urlsplit(source_url).hostname or "").casefold().rstrip(".")
        if not source_domain:
            raise ValueError("source_url must contain a domain")
        document_hash = ObservationDeduplicationService.normalize_document_hash(document_hash)
        bytes_received = self._nonnegative_int(bytes_received, "bytes_received")
        http_status = self._optional_http_status(http_status)
        error_code, error_message = self._optional_text(error_code), self._optional_text(error_message)
        if status == PublicSourceAcquisitionStatus.RETRIEVED:
            if document_hash is None or bytes_received <= 0:
                raise ValueError("RETRIEVED acquisition requires document_hash and positive bytes_received")
            if error_code or error_message:
                raise ValueError("RETRIEVED acquisition cannot contain an error")
        else:
            if not error_code or not error_message:
                raise ValueError("FAILED acquisition requires error_code and error_message")
            if document_hash is not None:
                raise ValueError("FAILED acquisition cannot claim a document_hash")
        acquisition_id = self._text(acquisition_id, "acquisition_id")
        if any(item.acquisition_id == acquisition_id for item in self.read_all()):
            raise ValueError("acquisition_id already exists")
        receipt = PublicSourceAcquisitionReceipt(
            1, acquisition_id, self._text(cycle_id, "cycle_id"), self._text(job_id, "job_id"),
            self._text(research_intent, "research_intent"), requested_url, source_url, canonical_url,
            source_domain, self.PUBLIC, status, requested_at, completed_at, http_status,
            self._optional_text(content_type), self._optional_text(source_document_id),
            document_hash, bytes_received, error_code, error_message,
            self._text(recorder, "recorder"),
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def read_all(self):
        if not self.path.exists(): return ()
        if not self.path.is_file(): raise ValueError("acquisition ledger path must be a file")
        result, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid acquisition receipt at line {number}: {exc}") from exc
                if item.acquisition_id in seen: raise ValueError(f"Duplicate acquisition_id at line {number}")
                seen.add(item.acquisition_id); result.append(item)
        return tuple(result)

    @classmethod
    def receipt_fingerprint(cls, receipt):
        if not isinstance(receipt, PublicSourceAcquisitionReceipt): raise ValueError("receipt must be a PublicSourceAcquisitionReceipt")
        return hashlib.sha256(json.dumps(cls._payload(receipt), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported acquisition schema")
        status = PublicSourceAcquisitionStatus(value["status"])
        if value["access_classification"] != cls.PUBLIC: raise ValueError("acquisition is not PUBLIC")
        source_url = cls._text(value["source_url"], "source_url")
        requested_url = cls._text(value["requested_url"], "requested_url")
        canonical_url = ObservationDeduplicationService.canonicalize_url(source_url)
        source_domain = (urlsplit(source_url).hostname or "").casefold().rstrip(".")
        if value["canonical_url"] != canonical_url or value["source_domain"] != source_domain:
            raise ValueError("acquisition URL identity does not match its source URL")
        requested_at, completed_at = cls._iso(value["requested_at"]), cls._iso(value["completed_at"])
        try:
            if completed_at < requested_at:
                raise ValueError("completed_at precedes requested_at")
        except TypeError as exc:
            raise ValueError("acquisition timestamps use inconsistent timezone awareness") from exc
        receipt = PublicSourceAcquisitionReceipt(
            1, cls._text(value["acquisition_id"], "acquisition_id"), cls._text(value["cycle_id"], "cycle_id"),
            cls._text(value["job_id"], "job_id"), cls._text(value["research_intent"], "research_intent"),
            requested_url, source_url, canonical_url, source_domain, cls.PUBLIC, status,
            requested_at, completed_at,
            cls._optional_http_status(value["http_status"]), cls._optional_text(value["content_type"]),
            cls._optional_text(value["source_document_id"]), ObservationDeduplicationService.normalize_document_hash(value["document_hash"]),
            cls._nonnegative_int(value["bytes_received"], "bytes_received"), cls._optional_text(value["error_code"]),
            cls._optional_text(value["error_message"]), cls._text(value["recorder"], "recorder"),
        )
        if status == PublicSourceAcquisitionStatus.RETRIEVED and (not receipt.document_hash or receipt.bytes_received <= 0 or receipt.error_code or receipt.error_message): raise ValueError("invalid RETRIEVED acquisition")
        if status == PublicSourceAcquisitionStatus.FAILED and (not receipt.error_code or not receipt.error_message or receipt.document_hash): raise ValueError("invalid FAILED acquisition")
        return receipt

    @staticmethod
    def _payload(item): return {**item.__dict__, "status": item.status.value, "requested_at": item.requested_at.isoformat(), "completed_at": item.completed_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @staticmethod
    def _optional_text(value):
        if value is None: return None
        if not isinstance(value, str): raise ValueError("optional text value must be a string")
        return value.strip() or None
    @staticmethod
    def _datetime(value, name):
        if not isinstance(value, datetime): raise ValueError(f"{name} must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str): raise ValueError("timestamp must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), "timestamp")
    @staticmethod
    def _nonnegative_int(value, name):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0: raise ValueError(f"{name} must be a non-negative integer")
        return value
    @staticmethod
    def _optional_http_status(value):
        if value is None: return None
        if isinstance(value, bool) or not isinstance(value, int) or not 100 <= value <= 599: raise ValueError("http_status must be between 100 and 599")
        return value


__all__ = ["PublicSourceAcquisitionLedger"]
