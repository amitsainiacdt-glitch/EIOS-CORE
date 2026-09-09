"""Append-only, fingerprint-chained persistence for controlled writes."""

from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .contracts import (
    ActorOrigin, ActorType, AuthorityScope, ClassifiedInformationRecord,
    InformationClass, OriginType, SourceReference, ValidationStatus,
    WriteReceipt, WriteReceiptStatus,
)
from .fingerprints import verify_receipt_fingerprint, verify_record_fingerprint


@dataclass(frozen=True)
class ControlledWriteJournalEntry:
    schema_version: int
    sequence: int
    prior_entry_fingerprint: str | None
    receipt: WriteReceipt
    record: ClassifiedInformationRecord | None
    status_snapshot: tuple[tuple[str, ValidationStatus], ...]
    entry_fingerprint: str


class ControlledIntelligenceWriteJournal:
    """One JSONL chain containing receipts, new records, and lifecycle state."""

    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("controlled-write journal path must identify a file")

    def append(self, *, receipt, record, status_snapshot):
        if not verify_receipt_fingerprint(receipt):
            raise ValueError("cannot persist a receipt with an invalid fingerprint")
        if record is not None and not verify_record_fingerprint(record):
            raise ValueError("cannot persist a record with an invalid fingerprint")
        entries = self.read_all()
        sequence = len(entries) + 1
        prior = entries[-1].entry_fingerprint if entries else None
        statuses = tuple(sorted(status_snapshot, key=lambda item: item[0]))
        payload = {
            "schema_version": 1,
            "sequence": sequence,
            "prior_entry_fingerprint": prior,
            "receipt": self._receipt_payload(receipt),
            "record": self._record_payload(record) if record is not None else None,
            "status_snapshot": [[record_id, status.value] for record_id, status in statuses],
        }
        fingerprint = self._entry_fingerprint(payload)
        payload["entry_fingerprint"] = fingerprint
        entry = self._parse(payload, expected_sequence=sequence, expected_prior=prior)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as journal:
            journal.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
            journal.flush()
        return entry

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("controlled-write journal path must be a file")
        entries, prior = [], None
        with self.path.open("r", encoding="utf-8") as journal:
            for line_number, line in enumerate(journal, 1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                    entry = self._parse(raw, expected_sequence=len(entries) + 1, expected_prior=prior)
                except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                    raise ValueError(f"Invalid controlled-write journal entry at line {line_number}: {exc}") from exc
                entries.append(entry)
                prior = entry.entry_fingerprint
        return tuple(entries)

    @classmethod
    def _parse(cls, raw, *, expected_sequence, expected_prior):
        if not isinstance(raw, dict) or raw.get("schema_version") != 1:
            raise ValueError("unsupported controlled-write journal schema")
        if raw.get("sequence") != expected_sequence:
            raise ValueError("journal sequence is not contiguous")
        if raw.get("prior_entry_fingerprint") != expected_prior:
            raise ValueError("journal hash chain is broken")
        supplied = cls._sha(raw.get("entry_fingerprint"), "entry_fingerprint")
        unsigned = {key: value for key, value in raw.items() if key != "entry_fingerprint"}
        if supplied != cls._entry_fingerprint(unsigned):
            raise ValueError("journal entry fingerprint does not match content")
        receipt = cls._parse_receipt(raw["receipt"])
        if not verify_receipt_fingerprint(receipt):
            raise ValueError("receipt fingerprint does not match content")
        record = cls._parse_record(raw["record"]) if raw.get("record") is not None else None
        if record is not None and not verify_record_fingerprint(record):
            raise ValueError("record fingerprint does not match content")
        statuses = tuple((cls._text(item[0], "record_id"), ValidationStatus(item[1])) for item in raw["status_snapshot"])
        if len({item[0] for item in statuses}) != len(statuses):
            raise ValueError("status snapshot contains duplicate record IDs")
        if record is not None and receipt.record_id != record.record_id:
            raise ValueError("receipt does not bind to persisted record")
        return ControlledWriteJournalEntry(1, expected_sequence, expected_prior, receipt, record, statuses, supplied)

    @classmethod
    def _parse_receipt(cls, raw):
        return WriteReceipt(
            1, cls._text(raw["receipt_id"], "receipt_id"), cls._text(raw["command_id"], "command_id"),
            cls._text(raw["idempotency_key"], "idempotency_key"), WriteReceiptStatus(raw["status"]),
            raw["record_id"], raw["record_version"], raw["previous_record_id"],
            cls._sha(raw["request_fingerprint"], "request_fingerprint"), raw["result_fingerprint"],
            tuple(raw["validation_codes"]), tuple(raw["rejection_codes"]), datetime.fromisoformat(raw["recorded_at"]),
            cls._text(raw["recorder_version"], "recorder_version"), cls._sha(raw["receipt_fingerprint"], "receipt_fingerprint"),
        )

    @classmethod
    def _parse_record(cls, raw):
        actor_raw = raw["actor"]
        actor = ActorOrigin(
            cls._text(actor_raw["actor_id"], "actor_id"), ActorType(actor_raw["actor_type"]),
            cls._text(actor_raw["actor_version"], "actor_version"), cls._text(actor_raw["origin_id"], "origin_id"),
            OriginType(actor_raw["origin_type"]), tuple(AuthorityScope(item) for item in actor_raw["authority_scopes"]),
        )
        sources = tuple(SourceReference(**item) for item in raw["source_references"])
        return ClassifiedInformationRecord(
            1, cls._text(raw["record_id"], "record_id"), int(raw["record_version"]),
            cls._text(raw["company_id"], "company_id"), cls._text(raw["entity"], "entity"),
            InformationClass(raw["information_class"]), cls._text(raw["semantic_key"], "semantic_key"),
            raw["payload"], sources, raw["confidence"], ValidationStatus(raw["validation_status"]),
            actor, datetime.fromisoformat(raw["created_at"]), raw["prior_record_id"], raw["supersedes_record_id"],
            cls._sha(raw["request_fingerprint"], "request_fingerprint"), cls._sha(raw["record_fingerprint"], "record_fingerprint"),
        )

    @staticmethod
    def _receipt_payload(receipt):
        return {
            **receipt.__dict__, "status": receipt.status.value,
            "validation_codes": list(receipt.validation_codes), "rejection_codes": list(receipt.rejection_codes),
            "recorded_at": receipt.recorded_at.isoformat(),
        }

    @staticmethod
    def _record_payload(record):
        payload = dataclasses.asdict(record)
        payload["information_class"] = record.information_class.value
        payload["validation_status"] = record.validation_status.value
        payload["created_at"] = record.created_at.isoformat()
        payload["actor"]["actor_type"] = record.actor.actor_type.value
        payload["actor"]["origin_type"] = record.actor.origin_type.value
        payload["actor"]["authority_scopes"] = [item.value for item in record.actor.authority_scopes]
        return payload

    @staticmethod
    def _entry_fingerprint(payload):
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _sha(cls, value, name):
        value = cls._text(value, name).casefold()
        if len(value) != 64:
            raise ValueError(f"{name} must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError(f"{name} must be SHA-256") from exc
        return value


__all__ = ["ControlledIntelligenceWriteJournal", "ControlledWriteJournalEntry"]
