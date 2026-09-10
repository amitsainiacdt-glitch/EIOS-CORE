"""Stage official NSE iXBRL results as non-approving review candidates."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

from modules.company_intelligence.exchange_ixbrl_financial import parse_exchange_ixbrl_financial
from modules.company_intelligence.exchange_ixbrl_column_review import prepare_column_review


def is_nse_ixbrl_candidate(acquisition) -> bool:
    receipt = acquisition.receipt
    host = (urlsplit(receipt.source_url).hostname or "").casefold()
    media = (receipt.content_type or "").split(";", 1)[0].casefold()
    path = urlsplit(receipt.source_url).path.casefold()
    return host == "nsearchives.nseindia.com" and (
        media in {"text/html", "application/xhtml+xml"} or path.endswith((".html", ".htm")))


def stage_exchange_ixbrl_candidate(acquisition, *, ticker: str, company: str, output_root: Path):
    if not is_nse_ixbrl_candidate(acquisition):
        raise ValueError("acquisition is not an official NSE iXBRL candidate")
    body = acquisition.document_bytes
    if not body:
        raise ValueError("NSE iXBRL candidate has no document bytes")
    digest = sha256(body).hexdigest()
    if digest != acquisition.receipt.document_hash:
        raise ValueError("NSE iXBRL bytes do not match acquisition receipt")
    result = parse_exchange_ixbrl_financial(
        body.decode("utf-8", errors="strict"), source_url=acquisition.receipt.source_url,
        document_hash=digest)
    metadata = result["metadata"]
    if metadata["ticker"].casefold() != ticker.casefold() or metadata["company"].casefold() != company.casefold():
        raise ValueError("NSE iXBRL company identity does not match configured company")
    output = Path(output_root) / ticker.upper() / digest / "exchange-ixbrl-candidate.json"
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.read_text(encoding="utf-8") != payload:
        raise ValueError("saved NSE iXBRL candidate has been altered")
    if not output.exists():
        output.write_text(payload, encoding="utf-8")
    preview_path = output.with_name("exchange-ixbrl-column-review.json")
    preview_payload = json.dumps(prepare_column_review(result), sort_keys=True, separators=(",", ":")) + "\n"
    if preview_path.exists() and preview_path.read_text(encoding="utf-8") != preview_payload:
        raise ValueError("saved NSE iXBRL column review has been altered")
    if not preview_path.exists():
        preview_path.write_text(preview_payload, encoding="utf-8")
    return result, output


__all__ = ["is_nse_ixbrl_candidate", "stage_exchange_ixbrl_candidate"]
