"""Passive contracts for the controlled EIOS intelligence-write boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Mapping


class InformationClass(str, Enum):
    FACT = "FACT"
    DERIVED_METRIC = "DERIVED_METRIC"
    INFERENCE = "INFERENCE"
    DECISION = "DECISION"


class ActorType(str, Enum):
    HUMAN = "HUMAN"
    EXTRACTION_SERVICE = "EXTRACTION_SERVICE"
    RESEARCH_JOB = "RESEARCH_JOB"
    AI_MODEL = "AI_MODEL"
    SYSTEM_ENGINE = "SYSTEM_ENGINE"
    DECISION_ORCHESTRATOR = "DECISION_ORCHESTRATOR"


class OriginType(str, Enum):
    HUMAN_REVIEW = "HUMAN_REVIEW"
    AUTOMATED_EXTRACTION = "AUTOMATED_EXTRACTION"
    SCHEDULED_RESEARCH = "SCHEDULED_RESEARCH"
    AI_ANALYSIS = "AI_ANALYSIS"
    DETERMINISTIC_ENGINE = "DETERMINISTIC_ENGINE"
    GOVERNED_DECISION = "GOVERNED_DECISION"


class AuthorityScope(str, Enum):
    PROPOSE_FACT = "PROPOSE_FACT"
    VERIFY_FACT = "VERIFY_FACT"
    RECORD_DERIVED_METRIC = "RECORD_DERIVED_METRIC"
    RECORD_INFERENCE = "RECORD_INFERENCE"
    CREATE_DECISION = "CREATE_DECISION"
    SUPERSEDE_INFORMATION = "SUPERSEDE_INFORMATION"


class ValidationStatus(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    PENDING_REVIEW = "PENDING_REVIEW"
    VERIFIED = "VERIFIED"
    CONFLICTED = "CONFLICTED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"
    STALE = "STALE"


class WriteOperation(str, Enum):
    PROPOSE_FACT = "PROPOSE_FACT"
    VERIFY_RECORD = "VERIFY_RECORD"
    RECORD_DERIVED_METRIC = "RECORD_DERIVED_METRIC"
    RECORD_INFERENCE = "RECORD_INFERENCE"
    CREATE_DECISION_SNAPSHOT = "CREATE_DECISION_SNAPSHOT"
    SUPERSEDE_RECORD = "SUPERSEDE_RECORD"


class WriteReceiptStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    ACCEPTED_PROVISIONAL = "ACCEPTED_PROVISIONAL"
    DUPLICATE_NO_CHANGE = "DUPLICATE_NO_CHANGE"
    CONFLICT_RECORDED = "CONFLICT_RECORDED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ActorOrigin:
    actor_id: str
    actor_type: ActorType
    actor_version: str
    origin_id: str
    origin_type: OriginType
    authority_scopes: tuple[AuthorityScope, ...]


@dataclass(frozen=True)
class SourceReference:
    source_id: str
    source_type: str
    source_url: str
    document_hash: str | None = None
    page_or_section: str | None = None


@dataclass(frozen=True)
class WriteCommand:
    schema_version: int
    command_id: str
    idempotency_key: str
    operation: WriteOperation
    actor: ActorOrigin
    requested_at: datetime
    company_id: str
    entity: str
    information_class: InformationClass
    semantic_key: str
    payload: Mapping[str, Any]
    source_references: tuple[SourceReference, ...]
    confidence: float | None
    requested_validation_status: ValidationStatus
    prior_record_id: str | None = None
    supersedes_record_id: str | None = None
    correlation_id: str | None = None
    causation_id: str | None = None
    expected_current_revision: str | None = None
    declared_request_fingerprint: str | None = None


@dataclass(frozen=True)
class ClassifiedInformationRecord:
    schema_version: int
    record_id: str
    record_version: int
    company_id: str
    entity: str
    information_class: InformationClass
    semantic_key: str
    payload: Mapping[str, Any]
    source_references: tuple[SourceReference, ...]
    confidence: float | None
    validation_status: ValidationStatus
    actor: ActorOrigin
    created_at: datetime
    prior_record_id: str | None
    supersedes_record_id: str | None
    request_fingerprint: str
    record_fingerprint: str


@dataclass(frozen=True)
class WriteReceipt:
    schema_version: int
    receipt_id: str
    command_id: str
    idempotency_key: str
    status: WriteReceiptStatus
    record_id: str | None
    record_version: int | None
    previous_record_id: str | None
    request_fingerprint: str
    result_fingerprint: str | None
    validation_codes: tuple[str, ...]
    rejection_codes: tuple[str, ...]
    recorded_at: datetime
    recorder_version: str
    receipt_fingerprint: str
