"""Weekly unattended discovery and ingestion of IMD's country rainfall PDF."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import uuid

from modules.company_intelligence.imd_rainfall_pdf_indicator import extract_imd_rainfall_indicator_candidate
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_rules
from modules.external_intelligence.official_linked_asset_discovery import discover_official_linked_assets
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


DISCOVERY_URL = 'https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=8'
RULE_ID = 'india-seasonal-rain-deficit'


def run_automatic_imd_rainfall_monitor(root, *, now=None, force=False, acquirer=None, extractor=None):
    root = Path(root); now = now or datetime.now(timezone.utc)
    if now.tzinfo is None: raise ValueError('now must be timezone-aware')
    runtime = root / 'data/runtime/primary_indicator_assets'
    state_path = runtime / 'imd_country_rainfall_state.json'
    state = _read_state(state_path)
    if not force and state and now < datetime.fromisoformat(state['next_due_at']):
        return _result('NOT_DUE', state=state)

    acquisition_ledger = PublicSourceAcquisitionLedger(runtime / 'acquisitions.jsonl')
    extraction_ledger = PublicDocumentExtractionLedger(runtime / 'extractions.jsonl')
    acquirer = acquirer or TrustedPublicAcquisitionAdapter(TrustedPublicSourceRegistry.india_primary_sources(), acquisition_ledger)
    extractor = extractor or TrustedPublicDocumentExtractionAdapter(extraction_ledger)
    run_id = now.strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex[:8]
    ticker = 'COROMANDEL'; job_id = f'{ticker}-PRIMARY-INDICATOR-{RULE_ID.upper()}'
    page = acquirer.acquire(acquisition_id='IMD-RAIN-PAGE-' + run_id, cycle_id=run_id, job_id=job_id,
        research_intent='PRIMARY_INDICATOR_MONITORING', url=DISCOVERY_URL,
        recorder='EIOS_AUTOMATIC_PRIMARY_INDICATOR', requested_at=now)
    if page.retrieved_content is None:
        return _failure(state_path, now, 'DISCOVERY_ACQUISITION_FAILED', page.receipt.error_code)
    assets = discover_official_linked_assets(page.retrieved_content, approved_domain='mausam.imd.gov.in',
        relevance_terms=('subdivision_rainfall_distribution_country_india',), max_assets=3)
    pdfs = [item for item in assets if item.asset_type == 'PDF']
    if len(pdfs) != 1:
        return _failure(state_path, now, 'OFFICIAL_PDF_AMBIGUOUS', str(len(pdfs)))
    document = acquirer.acquire(acquisition_id='IMD-RAIN-PDF-' + run_id, cycle_id=run_id, job_id=job_id,
        research_intent='PRIMARY_INDICATOR_MONITORING', url=pdfs[0].url,
        recorder='EIOS_AUTOMATIC_PRIMARY_INDICATOR', requested_at=now, source_document_id=page.receipt.document_hash)
    if document.retrieved_content is None:
        return _failure(state_path, now, 'PDF_ACQUISITION_FAILED', document.receipt.error_code)
    if state and state.get('document_hash') == document.receipt.document_hash:
        saved = _success_state(now, document.receipt.source_url, document.receipt.document_hash,
                               state.get('reporting_date'), state.get('record_id'))
        _write_state(state_path, saved)
        return _result('UNCHANGED_DOCUMENT', state=saved)
    extraction = extractor.extract(document, extraction_id='IMD-RAIN-TEXT-' + run_id,
                                   recorder='EIOS_AUTOMATIC_PRIMARY_INDICATOR')
    if extraction.extracted_text is None:
        return _failure(state_path, now, 'PDF_EXTRACTION_FAILED', extraction.receipt.error_code)
    binding = load_quarterly_monitoring_rules().get(job_id)
    if binding is None: raise ValueError('configured rainfall monitoring rule was not found')
    _, rule = binding
    try:
        candidate = extract_imd_rainfall_indicator_candidate(document, extraction, ticker=ticker, rule=rule)
    except ValueError as exc:
        return _failure(state_path, now, 'PDF_VALUE_HELD', str(exc))
    ledger = PrimaryIndicatorLedger(root / 'data/company_intelligence/primary_indicator_records.jsonl')
    existing_ids = {item.record_id for item in ledger.read_all()}
    record = ledger.record(candidate, recorded_at=now)
    saved = _success_state(now, record.source_url, record.content_fingerprint, record.reporting_date, record.record_id)
    _write_state(state_path, saved)
    return _result('ALREADY_RECORDED' if record.record_id in existing_ids else 'RECORDED',
                   state=saved, value=record.value, unit=record.unit,
                   latest_signal=ledger.latest_alert(rule)['status'])


def _success_state(now, source_url, document_hash, reporting_date, record_id):
    return {'schema_version': 1, 'status': 'SUCCESS', 'checked_at': now.isoformat(),
            'next_due_at': (now + timedelta(days=7)).isoformat(), 'source_url': source_url,
            'document_hash': document_hash, 'reporting_date': reporting_date, 'record_id': record_id}


def _failure(path, now, status, detail):
    state = {'schema_version': 1, 'status': status, 'checked_at': now.isoformat(),
             'next_due_at': (now + timedelta(days=1)).isoformat(), 'detail': detail}
    _write_state(path, state); return _result(status, state=state)


def _result(status, **values):
    return {'status': status, **values, 'creates_catalyst': False, 'changes_verdict': False, 'authorizes_trade': False}


def _read_state(path):
    path = Path(path)
    if not path.exists(): return None
    value = json.loads(path.read_text(encoding='utf-8'))
    if value.get('schema_version') != 1 or not isinstance(value.get('next_due_at'), str):
        raise ValueError('invalid IMD rainfall monitor state')
    datetime.fromisoformat(value['next_due_at'])
    return value


def _write_state(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    temporary.replace(path)


__all__ = ['run_automatic_imd_rainfall_monitor']
