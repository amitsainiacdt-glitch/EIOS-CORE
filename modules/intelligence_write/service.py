"""In-memory validation service for the future controlled write boundary.

This checkpoint deliberately has no production persistence or engine wiring.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from typing import Mapping

from .contracts import (
    ActorType,
    AuthorityScope,
    ClassifiedInformationRecord,
    InformationClass,
    OriginType,
    ValidationStatus,
    WriteCommand,
    WriteOperation,
    WriteReceipt,
    WriteReceiptStatus,
)
from .fingerprints import command_fingerprint, receipt_fingerprint, record_fingerprint_payload
from .persistence import ControlledIntelligenceWriteJournal


class ControlledIntelligenceWriteService:
    """Fail-closed reference implementation; it does not write production state."""

    VERSION = "controlled-write-memory-v1"
    MACHINE_ACTORS = {ActorType.AI_MODEL, ActorType.EXTRACTION_SERVICE, ActorType.RESEARCH_JOB}
    OPERATION_CLASS = {
        WriteOperation.PROPOSE_FACT: InformationClass.FACT,
        WriteOperation.VERIFY_RECORD: InformationClass.FACT,
        WriteOperation.RECORD_DERIVED_METRIC: InformationClass.DERIVED_METRIC,
        WriteOperation.RECORD_INFERENCE: InformationClass.INFERENCE,
        WriteOperation.CREATE_DECISION_SNAPSHOT: InformationClass.DECISION,
    }
    OPERATION_AUTHORITY = {
        WriteOperation.PROPOSE_FACT: AuthorityScope.PROPOSE_FACT,
        WriteOperation.VERIFY_RECORD: AuthorityScope.VERIFY_FACT,
        WriteOperation.RECORD_DERIVED_METRIC: AuthorityScope.RECORD_DERIVED_METRIC,
        WriteOperation.RECORD_INFERENCE: AuthorityScope.RECORD_INFERENCE,
        WriteOperation.CREATE_DECISION_SNAPSHOT: AuthorityScope.CREATE_DECISION,
        WriteOperation.SUPERSEDE_RECORD: AuthorityScope.SUPERSEDE_INFORMATION,
    }

    def __init__(self, *, clock=None, journal=None):
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        if journal is not None and not isinstance(journal, ControlledIntelligenceWriteJournal):
            raise ValueError("journal must be a ControlledIntelligenceWriteJournal")
        self._journal = journal
        self._records: dict[str, ClassifiedInformationRecord] = {}
        self._record_order: list[str] = []
        self._current_status: dict[str, ValidationStatus] = {}
        self._receipts: list[WriteReceipt] = []
        self._idempotency: dict[str, tuple[str, str | None]] = {}
        self._conflicted_keys: set[tuple[str, str, str]] = set()
        if self._journal is not None:
            self._rehydrate(self._journal.read_all())

    def submit(self, command: WriteCommand) -> WriteReceipt:
        recorded_at = self._clock()
        if not isinstance(command, WriteCommand):
            raise ValueError("command must be a WriteCommand")
        try:
            request_fingerprint = command_fingerprint(command)
        except (TypeError, ValueError) as exc:
            return self._reject(command, "UNFINGERPRINTABLE_COMMAND", recorded_at, fallback=str(exc))

        if command.declared_request_fingerprint is not None and command.declared_request_fingerprint != request_fingerprint:
            return self._reject(command, "REQUEST_FINGERPRINT_MISMATCH", recorded_at, request_fingerprint)

        prior_attempt = self._idempotency.get(command.idempotency_key)
        if prior_attempt:
            if prior_attempt[0] != request_fingerprint:
                return self._reject(command, "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST", recorded_at, request_fingerprint)
            return self._receipt(
                command, request_fingerprint, recorded_at, WriteReceiptStatus.DUPLICATE_NO_CHANGE,
                prior_attempt[1], (), (), previous_record_id=prior_attempt[1],
            )

        try:
            errors = self._validate_common(command)
            errors.extend(self._validate_operation(command))
        except (AttributeError, TypeError, ValueError) as exc:
            receipt = self._reject(
                command, "MALFORMED_COMMAND_CONTRACT", recorded_at=recorded_at,
                request_fingerprint=request_fingerprint, fallback=str(exc),
            )
            self._idempotency[command.idempotency_key] = (request_fingerprint, None)
            return receipt
        if errors:
            receipt = self._reject(command, *errors, recorded_at=recorded_at, request_fingerprint=request_fingerprint)
            self._idempotency[command.idempotency_key] = (request_fingerprint, None)
            return receipt

        receipt = self._execute(command, request_fingerprint, recorded_at)
        self._idempotency[command.idempotency_key] = (request_fingerprint, receipt.record_id)
        return receipt

    def records(self) -> tuple[ClassifiedInformationRecord, ...]:
        return tuple(self.get_record(record_id) for record_id in self._record_order)

    def receipts(self) -> tuple[WriteReceipt, ...]:
        return tuple(self._receipts)

    def get_record(self, record_id: str) -> ClassifiedInformationRecord:
        record = self._records[record_id]
        status = self._current_status[record_id]
        return record if record.validation_status == status else dataclasses.replace(record, validation_status=status)

    def trusted_records(self) -> tuple[ClassifiedInformationRecord, ...]:
        result = []
        for record_id in self._record_order:
            record = self.get_record(record_id)
            key = (record.company_id.casefold(), record.information_class.value, record.semantic_key.casefold())
            if record.validation_status == ValidationStatus.VERIFIED and key not in self._conflicted_keys:
                result.append(record)
        return tuple(result)

    def _execute(self, command, request_fingerprint, recorded_at):
        if command.operation == WriteOperation.VERIFY_RECORD:
            prior = self._records[command.prior_record_id]
            return self._store(
                command, request_fingerprint, recorded_at, ValidationStatus.VERIFIED,
                record_version=prior.record_version + 1, previous_record_id=prior.record_id,
                validation_codes=("HUMAN_OR_AUTHORIZED_FACT_VERIFICATION",),
            )
        if command.operation == WriteOperation.SUPERSEDE_RECORD:
            prior = self._records[command.supersedes_record_id]
            self._current_status[prior.record_id] = ValidationStatus.SUPERSEDED
            receipt = self._store(
                command, request_fingerprint, recorded_at, ValidationStatus.VERIFIED,
                record_version=prior.record_version + 1, previous_record_id=prior.record_id,
                validation_codes=("RESTATEMENT_PRESERVES_SUPERSEDED_RECORD",),
            )
            self._clear_conflict_if_resolved(command)
            return receipt

        duplicate, conflicting = self._fact_identity_state(command)
        if duplicate:
            return self._receipt(
                command, request_fingerprint, recorded_at, WriteReceiptStatus.DUPLICATE_NO_CHANGE,
                duplicate.record_id, ("SEMANTIC_DUPLICATE",), (), previous_record_id=duplicate.record_id,
            )

        validation_codes: list[str] = []
        status = command.requested_validation_status
        if command.information_class == InformationClass.FACT and command.actor.actor_type in self.MACHINE_ACTORS:
            status = ValidationStatus.PROVISIONAL
            validation_codes.append("MACHINE_FACT_FORCED_PROVISIONAL")
        if conflicting:
            status = ValidationStatus.CONFLICTED
            key = (command.company_id.casefold(), command.information_class.value, command.semantic_key.casefold())
            self._conflicted_keys.add(key)
            for record in conflicting:
                self._current_status[record.record_id] = ValidationStatus.CONFLICTED
            receipt_status = WriteReceiptStatus.CONFLICT_RECORDED
            validation_codes.append("CONFLICTING_FACTS_PRESERVED")
        else:
            receipt_status = WriteReceiptStatus.ACCEPTED_PROVISIONAL if status in {
                ValidationStatus.PROVISIONAL, ValidationStatus.PENDING_REVIEW
            } else WriteReceiptStatus.ACCEPTED
        return self._store(
            command, request_fingerprint, recorded_at, status,
            record_version=1, previous_record_id=None,
            validation_codes=tuple(validation_codes), receipt_status=receipt_status,
        )

    def _store(self, command, request_fingerprint, recorded_at, status, *, record_version,
               previous_record_id, validation_codes, receipt_status=WriteReceiptStatus.ACCEPTED):
        record_id = hashlib.sha256(f"record\n{request_fingerprint}".encode()).hexdigest()
        normalized_payload = self._normalize_payload(command.payload)
        body = {
            "schema_version": 1, "record_id": record_id, "record_version": record_version,
            "company_id": command.company_id.strip(), "entity": command.entity.strip(),
            "information_class": command.information_class.value, "semantic_key": command.semantic_key.strip(),
            "payload": normalized_payload, "source_references": command.source_references,
            "confidence": command.confidence, "validation_status": status.value, "actor": command.actor,
            "created_at": recorded_at, "prior_record_id": command.prior_record_id,
            "supersedes_record_id": command.supersedes_record_id, "request_fingerprint": request_fingerprint,
        }
        result_fingerprint = record_fingerprint_payload(body)
        record = ClassifiedInformationRecord(
            1, record_id, record_version, command.company_id.strip(), command.entity.strip(),
            command.information_class, command.semantic_key.strip(), normalized_payload,
            command.source_references, command.confidence, status, command.actor, recorded_at,
            command.prior_record_id, command.supersedes_record_id, request_fingerprint, result_fingerprint,
        )
        self._records[record_id] = record
        self._record_order.append(record_id)
        self._current_status[record_id] = status
        return self._receipt(
            command, request_fingerprint, recorded_at, receipt_status, record_id,
            validation_codes, (), previous_record_id=previous_record_id,
            record_version=record_version, result_fingerprint=result_fingerprint,
        )

    def _validate_common(self, command):
        errors = []
        if command.schema_version != 1: errors.append("UNSUPPORTED_COMMAND_SCHEMA")
        for value, code in ((command.command_id, "COMMAND_ID_REQUIRED"), (command.idempotency_key, "IDEMPOTENCY_KEY_REQUIRED"),
                            (command.company_id, "COMPANY_ID_REQUIRED"), (command.entity, "ENTITY_REQUIRED"),
                            (command.semantic_key, "SEMANTIC_KEY_REQUIRED")):
            if not isinstance(value, str) or not value.strip(): errors.append(code)
        if not isinstance(command.operation, WriteOperation): errors.append("INVALID_WRITE_OPERATION")
        if not isinstance(command.information_class, InformationClass): errors.append("INVALID_INFORMATION_CLASS")
        if not isinstance(command.requested_validation_status, ValidationStatus): errors.append("INVALID_VALIDATION_STATUS")
        if not isinstance(command.requested_at, datetime): errors.append("REQUEST_TIMESTAMP_REQUIRED")
        elif command.requested_at.tzinfo is None: errors.append("REQUEST_TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
        if not isinstance(command.payload, Mapping) or not command.payload: errors.append("PAYLOAD_REQUIRED")
        if command.confidence is not None and (isinstance(command.confidence, bool) or not isinstance(command.confidence, (int, float))
                                               or not math.isfinite(command.confidence) or not 0 <= command.confidence <= 100):
            errors.append("INVALID_CONFIDENCE")
        actor = command.actor
        if not getattr(actor, "actor_id", "") or not getattr(actor, "origin_id", "") or not getattr(actor, "actor_version", ""):
            errors.append("ACTOR_ORIGIN_INCOMPLETE")
        if not isinstance(getattr(actor, "actor_type", None), ActorType): errors.append("INVALID_ACTOR_TYPE")
        if not isinstance(getattr(actor, "origin_type", None), OriginType):
            errors.append("INVALID_ORIGIN_TYPE")
        if not isinstance(getattr(actor, "authority_scopes", None), tuple) or not all(
            isinstance(scope, AuthorityScope) for scope in getattr(actor, "authority_scopes", ())
        ):
            errors.append("INVALID_AUTHORITY_SCOPE")
        if len(set(getattr(actor, "authority_scopes", ()))) != len(getattr(actor, "authority_scopes", ())):
            errors.append("DUPLICATE_AUTHORITY_SCOPE")
        source_ids = [source.source_id for source in command.source_references]
        if len(source_ids) != len(set(source_ids)): errors.append("DUPLICATE_SOURCE_REFERENCE")
        for source in command.source_references:
            if not source.source_id.strip() or not source.source_type.strip() or not source.source_url.startswith("https://"):
                errors.append("INVALID_SOURCE_REFERENCE"); break
            if source.document_hash is not None and not re.fullmatch(r"[0-9a-f]{64}", source.document_hash):
                errors.append("INVALID_DOCUMENT_HASH"); break
        return errors

    def _validate_operation(self, command):
        errors = []
        required_authority = self.OPERATION_AUTHORITY.get(command.operation)
        authorities = getattr(command.actor, "authority_scopes", ())
        if required_authority not in authorities:
            errors.append("ACTOR_NOT_AUTHORIZED_FOR_OPERATION")
        expected_class = self.OPERATION_CLASS.get(command.operation)
        if expected_class is not None and command.information_class != expected_class:
            errors.append("INFORMATION_CLASS_OPERATION_MISMATCH")
        payload_keys = set(command.payload) if isinstance(command.payload, Mapping) else set()
        schemas = {
            InformationClass.DERIVED_METRIC: ({"metric", "value", "unit", "formula", "input_record_ids"}, {"decision", "source_assertion"}),
            InformationClass.INFERENCE: ({"statement", "supporting_record_ids", "mechanism", "uncertainty"}, {"value", "formula", "decision"}),
            InformationClass.DECISION: ({"decision", "input_packet_fingerprint", "reason_codes"}, {"value", "formula", "mechanism"}),
        }
        if command.information_class in schemas:
            required, forbidden = schemas[command.information_class]
            if not required.issubset(payload_keys): errors.append("INFORMATION_CLASS_REQUIRED_FIELDS_MISSING")
            if forbidden & payload_keys: errors.append("INFORMATION_CLASS_MASQUERADE")
        if command.information_class == InformationClass.FACT and not command.source_references:
            errors.append("FACT_SOURCE_REQUIRED")
        if command.information_class == InformationClass.FACT and isinstance(command.payload, Mapping):
            forbidden = {"formula", "mechanism", "decision"}
            if forbidden & payload_keys:
                errors.append("INFORMATION_CLASS_MASQUERADE")
            quantitative = {"metric", "value", "unit", "period", "basis"}.issubset(payload_keys)
            event = {"statement", "event_type", "event_at", "statement_posture"}.issubset(payload_keys)
            if quantitative == event:
                errors.append("FACT_REQUIRES_EXACTLY_ONE_SUPPORTED_SHAPE")
            elif quantitative:
                scope_text = command.semantic_key.casefold()
                period = str(command.payload.get("period", "")).casefold()
                basis = str(command.payload.get("basis", "")).casefold()
                if period not in scope_text or basis not in scope_text:
                    errors.append("FACT_SEMANTIC_KEY_SCOPE_MISMATCH")
            elif event:
                scope_text = command.semantic_key.casefold()
                event_type = str(command.payload.get("event_type", "")).casefold()
                if event_type not in scope_text:
                    errors.append("FACT_SEMANTIC_KEY_SCOPE_MISMATCH")
        if command.operation == WriteOperation.CREATE_DECISION_SNAPSHOT and command.actor.actor_type != ActorType.DECISION_ORCHESTRATOR:
            errors.append("DECISION_ORCHESTRATOR_REQUIRED")
        if command.operation == WriteOperation.VERIFY_RECORD:
            if command.actor.actor_type == ActorType.AI_MODEL: errors.append("AI_CANNOT_VERIFY_FACT")
            errors.extend(self._validate_prior(command, command.prior_record_id, require_fact=True))
        if command.operation == WriteOperation.SUPERSEDE_RECORD:
            errors.extend(self._validate_prior(command, command.supersedes_record_id, require_fact=False))
            if command.requested_validation_status != ValidationStatus.VERIFIED:
                errors.append("SUPERSESSION_REQUIRES_VERIFIED_REPLACEMENT")
        if command.operation not in {WriteOperation.VERIFY_RECORD, WriteOperation.SUPERSEDE_RECORD} and command.requested_validation_status in {
            ValidationStatus.CONFLICTED, ValidationStatus.REJECTED, ValidationStatus.SUPERSEDED, ValidationStatus.STALE
        }:
            errors.append("SYSTEM_MANAGED_VALIDATION_STATUS")
        if command.information_class == InformationClass.FACT and command.actor.actor_type in self.MACHINE_ACTORS and command.requested_validation_status == ValidationStatus.VERIFIED:
            # This request is accepted only as provisional; the coercion is auditable.
            pass
        elif command.requested_validation_status == ValidationStatus.VERIFIED and command.information_class == InformationClass.FACT \
                and AuthorityScope.VERIFY_FACT not in command.actor.authority_scopes:
            errors.append("VERIFIED_FACT_REQUIRES_VERIFY_AUTHORITY")
        return errors

    def _validate_prior(self, command, record_id, *, require_fact):
        if not record_id or record_id not in self._records: return ["PRIOR_RECORD_NOT_FOUND"]
        prior = self._records[record_id]
        errors = []
        if prior.company_id != command.company_id or prior.entity != command.entity or prior.semantic_key != command.semantic_key:
            errors.append("PRIOR_RECORD_IDENTITY_MISMATCH")
        if prior.information_class != command.information_class: errors.append("PRIOR_RECORD_CLASS_MISMATCH")
        if require_fact and prior.information_class != InformationClass.FACT: errors.append("ONLY_FACTS_CAN_BE_VERIFIED")
        if not command.expected_current_revision or command.expected_current_revision != prior.record_fingerprint:
            errors.append("STALE_OR_MISSING_EXPECTED_REVISION")
        if command.operation == WriteOperation.VERIFY_RECORD and prior.actor.actor_id == command.actor.actor_id \
                and prior.actor.actor_type in self.MACHINE_ACTORS:
            errors.append("MACHINE_CANNOT_SELF_VERIFY")
        if command.operation == WriteOperation.VERIFY_RECORD and (
            dict(prior.payload) != dict(command.payload) or prior.source_references != command.source_references
        ):
            errors.append("VERIFICATION_CANNOT_CHANGE_RECORD")
        return errors

    def _fact_identity_state(self, command):
        if command.information_class != InformationClass.FACT or command.operation != WriteOperation.PROPOSE_FACT:
            return None, ()
        candidates = [self.get_record(record_id) for record_id in self._record_order
                      if self._records[record_id].company_id.casefold() == command.company_id.casefold()
                      and self._records[record_id].information_class == InformationClass.FACT
                      and self._records[record_id].semantic_key.casefold() == command.semantic_key.casefold()
                      and self._current_status[record_id] != ValidationStatus.SUPERSEDED]
        for record in candidates:
            if dict(record.payload) == self._normalize_payload(command.payload): return record, ()
        return None, tuple(candidates)

    def _clear_conflict_if_resolved(self, command):
        key = (command.company_id.casefold(), command.information_class.value, command.semantic_key.casefold())
        active = [record_id for record_id in self._record_order
                  if self._records[record_id].company_id.casefold() == key[0]
                  and self._records[record_id].information_class.value == key[1]
                  and self._records[record_id].semantic_key.casefold() == key[2]
                  and self._current_status[record_id] != ValidationStatus.SUPERSEDED]
        if len(active) <= 1:
            self._conflicted_keys.discard(key)

    @staticmethod
    def _normalize_payload(payload):
        """Use one JSON-safe shape so live and reloaded records are identical."""
        return json.loads(json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False))

    def _reject(self, command, *codes, recorded_at=None, request_fingerprint=None, fallback=None):
        recorded_at = recorded_at or self._clock()
        if request_fingerprint is None:
            try: request_fingerprint = command_fingerprint(command)
            except Exception: request_fingerprint = hashlib.sha256((fallback or "invalid command").encode()).hexdigest()
        return self._receipt(command, request_fingerprint, recorded_at, WriteReceiptStatus.REJECTED, None, (), tuple(dict.fromkeys(codes)))

    def _receipt(self, command, request_fingerprint, recorded_at, status, record_id,
                 validation_codes, rejection_codes, *, previous_record_id=None,
                 record_version=None, result_fingerprint=None):
        receipt_id = hashlib.sha256(f"receipt\n{request_fingerprint}\n{len(self._receipts) + 1}".encode()).hexdigest()
        provisional = WriteReceipt(
            1, receipt_id, command.command_id, command.idempotency_key, status, record_id,
            record_version, previous_record_id, request_fingerprint, result_fingerprint,
            tuple(validation_codes), tuple(rejection_codes), recorded_at, self.VERSION, "",
        )
        receipt = dataclasses.replace(provisional, receipt_fingerprint=receipt_fingerprint(provisional))
        if self._journal is not None:
            record = self._records.get(record_id) if result_fingerprint is not None else None
            self._journal.append(
                receipt=receipt, record=record,
                status_snapshot=tuple(self._current_status.items()),
            )
        self._receipts.append(receipt)
        return receipt

    def _rehydrate(self, entries):
        for entry in entries:
            receipt = entry.receipt
            if entry.record is not None:
                if entry.record.record_id in self._records:
                    raise ValueError("journal contains a duplicate controlled record")
                self._records[entry.record.record_id] = entry.record
                self._record_order.append(entry.record.record_id)
            for record_id, status in entry.status_snapshot:
                if record_id not in self._records:
                    raise ValueError("journal status references an unknown controlled record")
                self._current_status[record_id] = status
            self._receipts.append(receipt)
            self._idempotency.setdefault(
                receipt.idempotency_key, (receipt.request_fingerprint, receipt.record_id)
            )
        grouped = {}
        for record_id in self._record_order:
            record = self._records[record_id]
            if self._current_status.get(record_id) == ValidationStatus.CONFLICTED:
                key = (record.company_id.casefold(), record.information_class.value, record.semantic_key.casefold())
                grouped.setdefault(key, 0)
                grouped[key] += 1
        self._conflicted_keys = {key for key, count in grouped.items() if count >= 2}


__all__ = ["ControlledIntelligenceWriteService"]
