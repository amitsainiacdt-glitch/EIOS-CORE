"""Import a hash-bound local public report without pretending it was downloaded."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import re
from uuid import uuid4

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult


def import_local_report(path, *, workspace, source_url, expected_sha256, registry, ledger):
    workspace, path = Path(workspace).resolve(), Path(path).resolve()
    if workspace not in path.parents or not path.is_file():
        raise ValueError('Report must be an existing file inside the workspace')
    if not re.fullmatch('[0-9a-fA-F]{64}', expected_sha256):
        raise ValueError('An expected SHA256 fingerprint is required')
    source = registry.resolve(source_url)
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError('Local report exceeds the 100 MB import limit')
    body = path.read_bytes()
    if not body.startswith(b'%PDF-'):
        raise ValueError('Only PDF reports are accepted')
    digest = sha256(body).hexdigest()
    if digest != expected_sha256.lower():
        raise ValueError('Local report does not match the expected document fingerprint')
    now = datetime.now(timezone.utc)
    receipt = ledger.record(acquisition_id=f'LOCAL-IMPORT-{uuid4().hex}', cycle_id=now.isoformat(),
        job_id='LOCAL_REPORT_IMPORT', research_intent='LOCAL_OFFICIAL_DOCUMENT_IMPORT',
        source_url=source_url, status='RETRIEVED', requested_at=now, completed_at=now,
        http_status=None, content_type='application/pdf', document_hash=digest,
        bytes_received=len(body), recorder='LOCAL_FILE_IMPORT_NOT_NETWORK_VERIFIED')
    # Status 0 is a local payload sentinel, not an HTTP response. No network request occurred.
    return TrustedPublicAcquisitionResult(source, receipt,
        RetrievedContent(source_url, 0, '', 'application/pdf', {'X-EIOS-Acquisition': 'LOCAL_FILE_IMPORT'}), body)
