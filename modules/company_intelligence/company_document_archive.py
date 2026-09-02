"""Content-addressed, append-only archive for governed company documents."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


@dataclass(frozen=True)
class CompanyDocumentVersion:
    schema_version: int
    company_id: str
    document_id: str
    source_id: str
    source_url: str
    document_hash: str
    bytes_received: int
    content_type: str | None
    acquired_at: datetime
    archive_path: str
    version_number: int
    change_status: str
    acquisition_id: str


class CompanyDocumentArchive:
    """Preserve exact acquired bytes and an auditable version history."""

    def __init__(self, root: Path, ledger_path: Path):
        self.root = Path(root)
        self.ledger_path = Path(ledger_path)
        if str(self.root).strip() in {"", "."} or str(self.ledger_path).strip() in {"", "."}:
            raise ValueError("archive root and ledger path must be explicit")

    def preserve(
        self,
        result: TrustedPublicAcquisitionResult,
        *,
        company_id: str,
        document_id: str,
        acquired_at: datetime,
    ) -> CompanyDocumentVersion:
        company_id = self._identity(company_id, "company_id")
        document_id = self._identity(document_id, "document_id")
        if not isinstance(acquired_at, datetime):
            raise ValueError("acquired_at must be a datetime")
        if result.document_bytes is None or result.retrieved_content is None:
            raise ValueError("only a successfully retrieved document can be archived")
        receipt = result.receipt
        digest = sha256(result.document_bytes).hexdigest()
        if digest != receipt.document_hash or len(result.document_bytes) != receipt.bytes_received:
            raise ValueError("document bytes do not match the acquisition receipt")

        previous = [
            item for item in self.read_all()
            if item.company_id == company_id and item.document_id == document_id
        ]
        same_hash = next((item for item in previous if item.document_hash == digest), None)
        version_number = same_hash.version_number if same_hash else len({item.document_hash for item in previous}) + 1
        change_status = "UNCHANGED" if same_hash else ("NEW_VERSION" if previous else "FIRST_SEEN")

        suffix = self._suffix(receipt.content_type, receipt.source_url)
        relative_path = Path(company_id) / document_id / f"{digest}{suffix}"
        archive_path = self.root / relative_path
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        if archive_path.exists():
            if sha256(archive_path.read_bytes()).hexdigest() != digest:
                raise ValueError("archived content has been altered")
        else:
            archive_path.write_bytes(result.document_bytes)

        record = CompanyDocumentVersion(
            1, company_id, document_id, result.source.source_id, receipt.source_url,
            digest, receipt.bytes_received, receipt.content_type, acquired_at,
            relative_path.as_posix(), version_number, change_status, receipt.acquisition_id,
        )
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as ledger:
            payload = asdict(record)
            payload["acquired_at"] = acquired_at.isoformat()
            ledger.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return record

    def read_all(self) -> tuple[CompanyDocumentVersion, ...]:
        if not self.ledger_path.exists():
            return ()
        records = []
        for line_number, line in enumerate(self.ledger_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
                if payload.get("schema_version") != 1:
                    raise ValueError("unsupported schema")
                payload["acquired_at"] = datetime.fromisoformat(payload["acquired_at"])
                record = CompanyDocumentVersion(**payload)
                if not re.fullmatch(r"[0-9a-f]{64}", record.document_hash):
                    raise ValueError("invalid document hash")
                archived = self.root / record.archive_path
                if not archived.is_file() or sha256(archived.read_bytes()).hexdigest() != record.document_hash:
                    raise ValueError("archived bytes are missing or altered")
                records.append(record)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid company document archive record at line {line_number}: {exc}") from exc
        return tuple(records)

    @staticmethod
    def _identity(value: str, name: str) -> str:
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,99}", value.strip()):
            raise ValueError(f"{name} is invalid")
        return value.strip()

    @staticmethod
    def _suffix(content_type: str | None, url: str) -> str:
        if content_type and "pdf" in content_type.casefold():
            return ".pdf"
        suffix = Path(url.split("?", 1)[0]).suffix.lower()
        return suffix if suffix in {".pdf", ".html", ".htm", ".json", ".xml", ".txt"} else ".bin"


__all__ = ["CompanyDocumentArchive", "CompanyDocumentVersion"]
