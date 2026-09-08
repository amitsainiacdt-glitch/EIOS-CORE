"""Extract one governed cumulative All-India rainfall departure from an IMD PDF."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import re
from urllib.parse import urlsplit

from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionStatus
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionResult


_PERIOD = re.compile(
    r'PERIOD\s*:\s*(?P<start>\d{2}-\d{2}-20\d{2})\s+to\s+(?P<end>\d{2}-\d{2}-20\d{2})', re.I)
_COUNTRY = re.compile(
    r'COUNTRY\s+AS\s+A\s+WHOLE\s+'
    r'(?P<daily_actual>\d+(?:\.\d+)?)\s+(?P<daily_normal>\d+(?:\.\d+)?)\s+(?P<daily_departure>-?\d+(?:\.\d+)?)%\s+\S+\s+'
    r'(?P<cumulative_actual>\d+(?:\.\d+)?)\s+(?P<cumulative_normal>\d+(?:\.\d+)?)\s+(?P<cumulative_departure>-?\d+(?:\.\d+)?)%\s+\S+', re.I)


def parse_imd_country_rainfall_pdf_text(text: str) -> dict:
    """Parse the unique completed-period and country-total row; ambiguity is fatal."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError('extracted PDF text must not be empty')
    periods = {(match.group('start'), match.group('end')) for match in _PERIOD.finditer(text)}
    rows = list(_COUNTRY.finditer(text))
    if len(periods) != 1:
        raise ValueError('IMD PDF must contain one unique cumulative period')
    if len(rows) != 1:
        raise ValueError('IMD PDF must contain one unique country-as-a-whole row')
    start, end = next(iter(periods)); row = rows[0]
    try:
        reporting_date = datetime.strptime(end, '%d-%m-%Y').date().isoformat()
        period_start = datetime.strptime(start, '%d-%m-%Y').date().isoformat()
        values = {name: Decimal(row.group(name)) for name in (
            'daily_actual', 'daily_normal', 'daily_departure',
            'cumulative_actual', 'cumulative_normal', 'cumulative_departure')}
    except (ValueError, InvalidOperation) as exc:
        raise ValueError('IMD PDF contains an invalid date or number') from exc
    if any(not value.is_finite() for value in values.values()):
        raise ValueError('IMD PDF contains a non-finite value')
    if values['cumulative_normal'] <= 0:
        raise ValueError('IMD cumulative normal rainfall must be positive')
    calculated = ((values['cumulative_actual'] - values['cumulative_normal']) / values['cumulative_normal'] * 100)
    if abs(calculated - values['cumulative_departure']) > Decimal('0.15'):
        raise ValueError('IMD cumulative departure does not reconcile to actual and normal rainfall')
    deficit = max(Decimal('0'), -values['cumulative_departure'])
    passage = ' '.join(row.group(0).split())
    return {'period_start': period_start, 'reporting_date': reporting_date,
            **{key: format(value, 'f') for key, value in values.items()},
            'deficit_magnitude': format(deficit, 'f'), 'evidence_passage': passage}


def extract_imd_rainfall_indicator_candidate(acquisition, extraction, *, ticker, rule) -> dict:
    """Bind parsed PDF text to audited acquisition/extraction lineage and an indicator rule."""
    if not isinstance(acquisition, TrustedPublicAcquisitionResult):
        raise ValueError('acquisition must be a TrustedPublicAcquisitionResult')
    if not isinstance(extraction, TrustedPublicDocumentExtractionResult) or extraction.extracted_text is None:
        raise ValueError('extraction must contain audited PDF text')
    extraction_receipt = extraction.receipt
    if acquisition.receipt.status != PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None:
        raise ValueError('rainfall PDF requires a retrieved acquisition')
    if acquisition.source.source_id != 'IMD' or acquisition.source.source_type != 'WEATHER_AUTHORITY':
        raise ValueError('rainfall PDF requires the configured IMD authority')
    if extraction_receipt.status not in (PublicDocumentExtractionStatus.SUCCEEDED, PublicDocumentExtractionStatus.PARTIAL):
        raise ValueError('rainfall PDF requires a usable audited extraction')
    if extraction_receipt.acquisition_id != acquisition.receipt.acquisition_id or extraction_receipt.document_hash != acquisition.receipt.document_hash:
        raise ValueError('extraction is not bound to the acquired rainfall PDF')
    if sha256(acquisition.document_bytes).hexdigest() != acquisition.receipt.document_hash:
        raise ValueError('rainfall PDF bytes do not match the acquisition receipt')
    if rule.get('unit') != 'percent below long-period average' or rule.get('accepted_postures') != ['REALIZED'] or rule.get('accepted_measurements') != ['DIRECT_DEFICIT']:
        raise ValueError('rainfall rule is not configured for realized direct deficit')
    parsed = parse_imd_country_rainfall_pdf_text(extraction.extracted_text)
    domain = (urlsplit(acquisition.receipt.source_url).hostname or '').casefold().rstrip('.')
    expected_domain = rule.get('source_domain', '').casefold().rstrip('.')
    if domain != expected_domain:
        raise ValueError('rainfall PDF source domain does not match the indicator rule')
    job_id = f"{ticker.upper()}-PRIMARY-INDICATOR-{rule['id'].upper()}"
    return {'rule_id': rule['id'], 'job_id': job_id, 'ticker': ticker.upper(),
            'reporting_date': parsed['reporting_date'], 'value': parsed['deficit_magnitude'],
            'unit': rule['unit'], 'source_url': acquisition.receipt.source_url,
            'source_domain': expected_domain, 'evidence_passage': parsed['evidence_passage'],
            'content_fingerprint': acquisition.receipt.document_hash}


__all__ = ['parse_imd_country_rainfall_pdf_text', 'extract_imd_rainfall_indicator_candidate']
