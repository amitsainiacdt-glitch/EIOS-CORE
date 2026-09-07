"""Archive and extract one local report; queue candidates without approving origin."""
import argparse
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.local_report_import import import_local_report
from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewQueueBuilder
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewWriter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry, TrustedPublicSourceDefinition
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate


def main():
    parser = argparse.ArgumentParser()
    for name in ('file', 'company', 'ticker', 'issuer-domain', 'source-url', 'sha256'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition('LOCAL-ISSUER', args.company,
        (args.issuer_domain,), source_type='COMPANY_PRIMARY'),))
    directory = ROOT / 'data/runtime/local_report_import'
    ledger = PublicSourceAcquisitionLedger(directory / 'acquisitions.jsonl')
    acquisition = import_local_report(ROOT / args.file, workspace=ROOT, source_url=args.source_url,
        expected_sha256=args.sha256, registry=registry, ledger=ledger)
    now = datetime.now(timezone.utc)
    version = CompanyDocumentArchive(directory / 'archive', directory / 'archive.jsonl').preserve(acquisition,
        company_id=args.ticker, document_id=acquisition.receipt.document_hash, acquired_at=now)
    extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(directory / 'extractions.jsonl')).extract(
        acquisition, extraction_id=acquisition.receipt.acquisition_id + '-TEXT', recorder='LOCAL_REPORT_IMPORT')
    report = {'acquisition_mode': 'LOCAL_FILE_IMPORT', 'network_downloaded': False,
        'archived': True, 'archive_change': version.change_status,
        'extraction_status': extraction.receipt.status.value, 'characters': extraction.receipt.character_count,
        'pages': extraction.receipt.page_count, 'warnings': list(extraction.receipt.warnings),
        'queued_candidates': 0, 'human_review_ready': 0, 'creates_approved_facts': False}
    if extraction.extracted_text:
        output = directory / acquisition.receipt.document_hash
        output.mkdir(parents=True, exist_ok=True)
        (output / 'extracted.txt').write_text(extraction.extracted_text, encoding='utf-8')
        admission = PublicObservationAdmissionGate(registry).preview(acquisition=acquisition, extraction=extraction,
            observations=(), title='Locally imported report', entity=args.company, category='LOCAL_COMPANY_REPORT', confidence=0)
        report['admission_reasons'] = list(admission.reason_codes)
        if admission.admissible:
            queue = CompanyFactReviewQueueBuilder(output / 'candidates.json').build(acquisition=acquisition,
                extraction=extraction, admission=admission, company=args.company, generated_at=now)
            assessments = CompanyCandidateMetaReviewWriter().write(queue, output_path=output / 'meta.json', reviewed_at=now)
            report['queued_candidates'] = len(queue)
            report['human_review_ready'] = sum(item.decision == 'READY_FOR_HUMAN_REVIEW' for item in assessments)
    heading = (extraction.extracted_text or '')[:2000]
    if re.search(r'financial results', heading, re.I) and re.search(r'quarter\s+(?:ended|and)', heading, re.I):
        try:
            from modules.company_intelligence.quarterly_pdf_intake import run_quarterly_intake
            report['quarterly_intake'] = run_quarterly_intake(ROOT / args.file, workspace=ROOT, ticker=args.ticker,
                                                           company=args.company, source_url=args.source_url)
        except (ImportError, OSError, ValueError) as exc:
            report['quarterly_intake'] = {'status': 'DEPENDENCY_OR_INPUT_HOLD', 'error': str(exc),
                                          'creates_approved_facts': False}
    (directory / 'latest.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if extraction.extracted_text else 1


if __name__ == '__main__':
    raise SystemExit(main())
