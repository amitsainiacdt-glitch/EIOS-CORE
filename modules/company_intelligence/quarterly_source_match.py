"""Compare a preserved quarterly PDF with an independently acquired issuer copy.

This establishes byte identity only, never company-content or financial approval.
The caller supplies a guarded acquisition adapter and a configured issuer registry.
"""
from hashlib import sha256
from uuid import uuid4


def match_quarterly_source(local_bytes, expected_hash, *, source_url, adapter, source_kind='ISSUER'):
    if source_kind not in {'ISSUER', 'EXCHANGE'}:
        raise ValueError('Unsupported official source kind')
    if not local_bytes.startswith(b'%PDF-') or sha256(local_bytes).hexdigest() != expected_hash:
        raise ValueError('Preserved quarterly PDF is missing, changed or not a PDF')
    token = 'QUARTERLY-SOURCE-' + uuid4().hex
    acquired = adapter.acquire(acquisition_id=token, cycle_id=token, job_id=token,
                               research_intent='OFFICIAL_DOCUMENT_DISCOVERY', url=source_url,
                               recorder='EIOS_AUTOMATION')
    receipt, body = acquired.receipt, acquired.document_bytes
    result = {'schema_version': 1, 'document_hash': expected_hash,
              'acquisition_id': receipt.acquisition_id, 'source_url': receipt.source_url,
              'requested_url': source_url, 'source_kind': source_kind, 'checked_at': receipt.completed_at.isoformat(),
              'http_status': receipt.http_status, 'download_hash': None,
              'status': 'SOURCE_UNAVAILABLE', 'creates_approved_facts': False,
              'company_content_verified': False, 'reporting_notes_verified': False,
              'explanation': f'The {source_kind.lower()} copy could not be retrieved. Source verification remains incomplete.'}
    if receipt.status.value != 'RETRIEVED' or not body or receipt.http_status != 200:
        return result, None
    digest = sha256(body).hexdigest()
    result['download_hash'] = digest
    if digest != receipt.document_hash or len(body) != receipt.bytes_received:
        result.update(status='ACQUISITION_EVIDENCE_MISMATCH',
                      explanation='Downloaded bytes do not agree with their acquisition receipt.')
        return result, None
    if not body.startswith(b'%PDF-'):
        result.update(status='SOURCE_NOT_PDF', explanation='The website returned something other than a PDF.')
        return result, None
    if digest != expected_hash:
        result.update(status='DIFFERENT_DOCUMENT',
                      explanation='The issuer returned a different PDF. Do not replace or approve the uploaded report automatically.')
    else:
        result.update(status='EXACT_ISSUER_COPY_MATCH',
                      explanation='The uploaded PDF exactly matches the freshly downloaded issuer copy. Company details and reporting notes still require review.')
    if source_kind == 'EXCHANGE':
        result['explanation'] = result['explanation'].replace('issuer', 'exchange')
        if result['status'] == 'EXACT_ISSUER_COPY_MATCH':
            result['status'] = 'EXACT_EXCHANGE_COPY_MATCH'
    return result, body
