"""Append-only extraction receipts bound to public acquisition receipts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionReceipt, PublicSourceAcquisitionStatus


class PublicDocumentExtractionLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("extraction ledger path must identify a file")

    def record(self, acquisition, *, extraction_id, extraction_method, status, extracted_at, recorder, extracted_content=None, page_count=None, warnings=(), error_code=None, error_message=None):
        if not isinstance(acquisition, PublicSourceAcquisitionReceipt): raise ValueError("acquisition must be a PublicSourceAcquisitionReceipt")
        if acquisition.access_classification != PublicSourceAcquisitionLedger.PUBLIC: raise ValueError("extraction requires a PUBLIC acquisition")
        if acquisition.status != PublicSourceAcquisitionStatus.RETRIEVED or not acquisition.document_hash: raise ValueError("extraction requires a successfully retrieved document")
        try: status = status if isinstance(status, PublicDocumentExtractionStatus) else PublicDocumentExtractionStatus(status)
        except (TypeError, ValueError) as exc: raise ValueError("status must be SUCCEEDED, PARTIAL, or FAILED") from exc
        extraction_id = self._text(extraction_id, "extraction_id")
        if any(item.extraction_id == extraction_id for item in self.read_all()): raise ValueError("extraction_id already exists")
        if any(item.acquisition_fingerprint == PublicSourceAcquisitionLedger.receipt_fingerprint(acquisition) for item in self.read_all()): raise ValueError("this acquisition already has an extraction receipt")
        method = self._text(extraction_method, "extraction_method")
        extracted_at = self._datetime(extracted_at)
        try:
            if extracted_at < acquisition.completed_at: raise ValueError("extracted_at precedes acquisition completion")
        except TypeError as exc: raise ValueError("extraction timestamps use inconsistent timezone awareness") from exc
        warning_values = self._texts(warnings, "warnings")
        error_code, error_message = self._optional_text(error_code), self._optional_text(error_message)
        content_fingerprint = None
        character_count = 0
        if extracted_content is not None:
            if not isinstance(extracted_content, str): raise ValueError("extracted_content must be text")
            character_count = len(extracted_content)
            if character_count:
                content_fingerprint = hashlib.sha256(extracted_content.encode("utf-8")).hexdigest()
        page_count = self._optional_positive_int(page_count, "page_count")
        if status == PublicDocumentExtractionStatus.SUCCEEDED:
            if not content_fingerprint: raise ValueError("SUCCEEDED extraction requires non-empty extracted_content")
            if warning_values or error_code or error_message: raise ValueError("SUCCEEDED extraction cannot contain warnings or errors")
        elif status == PublicDocumentExtractionStatus.PARTIAL:
            if not content_fingerprint or not warning_values: raise ValueError("PARTIAL extraction requires content and warnings")
            if error_code or error_message: raise ValueError("PARTIAL extraction cannot contain a terminal error")
        else:
            if content_fingerprint or not error_code or not error_message: raise ValueError("FAILED extraction requires an error and no extracted content")
        receipt = PublicDocumentExtractionReceipt(
            1, extraction_id, acquisition.acquisition_id,
            PublicSourceAcquisitionLedger.receipt_fingerprint(acquisition),
            acquisition.document_hash, method, status, content_fingerprint,
            character_count, page_count, warning_values, error_code, error_message,
            extracted_at, self._text(recorder, "recorder"),
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def read_all(self):
        if not self.path.exists(): return ()
        if not self.path.is_file(): raise ValueError("extraction ledger path must be a file")
        result, ids, acquisitions = [], set(), set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid extraction receipt at line {number}: {exc}") from exc
                if item.extraction_id in ids or item.acquisition_fingerprint in acquisitions: raise ValueError(f"Duplicate extraction receipt at line {number}")
                ids.add(item.extraction_id); acquisitions.add(item.acquisition_fingerprint); result.append(item)
        return tuple(result)

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported extraction schema")
        status = PublicDocumentExtractionStatus(value["status"])
        warnings = cls._texts(value["warnings"], "warnings")
        fingerprint = cls._optional_sha(value["extracted_content_fingerprint"])
        characters = cls._nonnegative_int(value["character_count"], "character_count")
        error_code, error_message = cls._optional_text(value["error_code"]), cls._optional_text(value["error_message"])
        if status == PublicDocumentExtractionStatus.SUCCEEDED and (not fingerprint or characters <= 0 or warnings or error_code or error_message): raise ValueError("invalid SUCCEEDED extraction")
        if status == PublicDocumentExtractionStatus.PARTIAL and (not fingerprint or characters <= 0 or not warnings or error_code or error_message): raise ValueError("invalid PARTIAL extraction")
        if status == PublicDocumentExtractionStatus.FAILED and (fingerprint or characters or not error_code or not error_message): raise ValueError("invalid FAILED extraction")
        return PublicDocumentExtractionReceipt(
            1, cls._text(value["extraction_id"], "extraction_id"), cls._text(value["acquisition_id"], "acquisition_id"),
            cls._sha(value["acquisition_fingerprint"]), cls._sha(value["document_hash"]),
            cls._text(value["extraction_method"], "extraction_method"), status, fingerprint,
            characters, cls._optional_positive_int(value["page_count"], "page_count"), warnings,
            error_code, error_message, cls._iso(value["extracted_at"]), cls._text(value["recorder"], "recorder"),
        )

    @staticmethod
    def _payload(item): return {**item.__dict__, "status": item.status.value, "warnings": list(item.warnings), "extracted_at": item.extracted_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len({value.casefold() for value in result}) != len(result): raise ValueError(f"{name} must not contain duplicates")
        return result
    @staticmethod
    def _optional_text(value):
        if value is None: return None
        if not isinstance(value, str): raise ValueError("optional text value must be a string")
        return value.strip() or None
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("extracted_at must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str): raise ValueError("extracted_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))
    @staticmethod
    def _nonnegative_int(value, name):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0: raise ValueError(f"{name} must be a non-negative integer")
        return value
    @staticmethod
    def _optional_positive_int(value, name):
        if value is None: return None
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0: raise ValueError(f"{name} must be a positive integer")
        return value
    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "fingerprint")
        if len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()
    @classmethod
    def _optional_sha(cls, value): return None if value is None else cls._sha(value)


__all__ = ["PublicDocumentExtractionLedger"]
