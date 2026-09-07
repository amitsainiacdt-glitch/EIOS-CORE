"""Bridge checked quarterly extracts into existing governed review formats."""
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewWriter
from modules.company_intelligence.quarterly_column_reconciliation import reconcile_column
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials


def quarterly_review_candidate(record, *, company, source_url):
    if record.get('status') != 'CHECKED_PENDING_REVIEW':
        return None
    source = record['source_column']
    checked = reconcile_column(source)
    if checked['status'] != 'CHECKED_PENDING_REVIEW' or checked['values_inr_crore'] != record.get('values_inr_crore'):
        raise ValueError('Quarterly candidate failed repeat reconciliation')
    if not company or not isinstance(company, str) or not isinstance(source_url, str):
        raise ValueError('Company and source URL context required')
    # Include complete evidence in identity, not only a run ID or a ticker.
    fingerprint = sha256(json.dumps({'record': record, 'company': company, 'source_url': source_url},
                                   sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    # A labelled transcription, not a verbatim quotation or company identity proof.
    passage = f'Company context from governed intake (not table text): {company}\n'
    passage += 'Structured table transcription (not a verbatim passage):\n' + source['header_text'] + '\n'
    passage += '\n'.join(f"{cell['row_label']}: {cell['native_text']}" for cell in source['raw_readings'])
    return CompanyFactReviewCandidate(
        schema_version=1, candidate_id='QUARTERLY-' + fingerprint,
        company=company, event_type='QUARTERLY_FINANCIAL_RESULT', statement_posture='REPORTED',
        source_passage=passage,
        explicit_amounts=tuple(f'{key}={value} INR crore' for key,value in sorted(record['values_inr_crore'].items())),
        explicit_dates=(source['period_start'], source['period_end']), pdf_page=source['pdf_page'],
        source_url=source_url, document_hash=source['document_hash'], extraction_id=fingerprint,
        extraction_method='local_import_quarterly_reconciled_v1')


def write_quarterly_review_queue(report, *, output_directory, company, source_url):
    folder = Path(output_directory)
    folder.mkdir(parents=True, exist_ok=True)
    candidates, records, held = [], {}, 0
    for page in report['ocr_pages']:
        for record in page.get('record_candidates', {}).get('records', []):
            candidate = quarterly_review_candidate(record, company=company, source_url=source_url)
            if candidate is None:
                held += 1
                continue
            if candidate.candidate_id not in records:
                candidates.append(candidate)
                records[candidate.candidate_id] = record
    now = datetime.now(timezone.utc)
    queue_path, meta_path = folder / 'quarterly-candidates.json', folder / 'quarterly-candidates.meta.json'
    queue = {'schema_version': 1, 'company': company, 'generated_at': now.isoformat(),
             'candidate_count': len(candidates), 'candidates': [asdict(c) for c in candidates],
             'quarterly_record_evidence': records, 'held_extraction_count': held,
             'reporting_notes': report.get('reporting_notes', {'status': 'NOT_EXTRACTED', 'review_complete': False}),
             'source_verification': report.get('source_verification', {'status': 'NOT_RUN', 'creates_approved_facts': False}),
             'creates_evidence': False, 'requires_meta_review': True, 'requires_human_review': True}
    queue_path.write_text(json.dumps(queue, indent=2), encoding='utf-8')
    assessments = CompanyCandidateMetaReviewWriter().write(candidates, output_path=meta_path, reviewed_at=now)
    financial_assessments = {key: assess_quarterly_financials(record,
        source_verification=queue['source_verification'], reporting_notes=queue['reporting_notes'])
        for key,record in records.items()}
    financial_path = folder / 'quarterly-financial-review.json'
    financial_path.write_text(json.dumps({'schema_version': 1, 'assessments': financial_assessments,
        'creates_approved_facts': False, 'changes_verdict': False}, indent=2), encoding='utf-8')
    return {'status': 'QUEUED_FOR_RESEARCH_REVIEW', 'candidate_count': len(candidates),
            'held_extraction_count': held, 'queue_path': str(queue_path), 'meta_path': str(meta_path),
            'financial_review_path': str(financial_path),
            'human_review_ready': sum(a.decision == 'READY_FOR_HUMAN_REVIEW' for a in assessments),
            'meta_held_count': sum(a.decision == 'HOLD_FOR_RESEARCH' for a in assessments),
            'creates_approved_facts': False, 'changes_verdict': False}
