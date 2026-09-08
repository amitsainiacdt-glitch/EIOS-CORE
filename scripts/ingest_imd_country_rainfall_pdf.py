"""Acquire, extract and record one governed IMD country rainfall PDF reading."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import uuid

from modules.company_intelligence.imd_rainfall_pdf_indicator import extract_imd_rainfall_indicator_candidate
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_rules
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


ROOT = Path(__file__).resolve().parents[1]
RULE_ID = 'india-seasonal-rain-deficit'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Record a source-bound realized All-India rainfall reading.')
    parser.add_argument('--url', required=True)
    parser.add_argument('--ticker', default='COROMANDEL')
    parser.add_argument('--recorder', default='EIOS_AUTOMATIC_PRIMARY_INDICATOR')
    args = parser.parse_args(argv)
    bindings = load_quarterly_monitoring_rules()
    job_id = f'{args.ticker.upper()}-PRIMARY-INDICATOR-{RULE_ID.upper()}'
    ticker, rule = bindings.get(job_id, (None, None))
    if rule is None or ticker.upper() != args.ticker.upper():
        raise ValueError('configured rainfall monitoring rule was not found')
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex[:8]
    runtime = ROOT / 'data/runtime/primary_indicator_assets'
    acquisition = TrustedPublicAcquisitionAdapter(
        TrustedPublicSourceRegistry.india_primary_sources(),
        PublicSourceAcquisitionLedger(runtime / 'acquisitions.jsonl')).acquire(
            acquisition_id='IMD-RAINFALL-' + run_id, cycle_id=run_id, job_id=job_id,
            research_intent='PRIMARY_INDICATOR_MONITORING', url=args.url,
            recorder=args.recorder, requested_at=datetime.now(timezone.utc))
    if acquisition.retrieved_content is None:
        print(f'Acquisition held: {acquisition.receipt.error_code} {acquisition.receipt.error_message}')
        return 1
    extraction = TrustedPublicDocumentExtractionAdapter(
        PublicDocumentExtractionLedger(runtime / 'extractions.jsonl')).extract(
            acquisition, extraction_id='IMD-RAINFALL-TEXT-' + run_id, recorder=args.recorder)
    if extraction.extracted_text is None:
        print(f'Extraction held: {extraction.receipt.error_code} {extraction.receipt.error_message}')
        return 1
    candidate = extract_imd_rainfall_indicator_candidate(
        acquisition, extraction, ticker=args.ticker, rule=rule)
    record = PrimaryIndicatorLedger(
        ROOT / 'data/company_intelligence/primary_indicator_records.jsonl').record(
            candidate, recorded_at=datetime.now(timezone.utc))
    print(f'Recorded {record.rule_id}: {record.value}% through {record.reporting_date}')
    print(f'Source: {record.source_url}')
    print(f'Document hash: {record.content_fingerprint}')
    print('Status: monitoring history only; no catalyst, verdict, recommendation or trade changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
