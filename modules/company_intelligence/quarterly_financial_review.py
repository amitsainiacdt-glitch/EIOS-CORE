"""Financial-specific deterministic review, not investment or publication approval."""
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from modules.company_intelligence.quarterly_column_reconciliation import reconcile_extracted_column
from modules.company_intelligence.quarterly_ocr_comparison import numeric_reading
from modules.company_intelligence.quarterly_note_context import note_context


def assess_quarterly_financials(record, *, source_verification=None, reporting_notes=None):
    checks = []
    def check(code, passed, explanation):
        checks.append({'code': code, 'status': 'PASS' if passed else 'HOLD', 'explanation': explanation})
    source = record.get('source_column', {})
    repeated = reconcile_extracted_column(source)
    check('PERIOD_BASIS_UNIT_AND_TOTALS', repeated['status'] == 'CHECKED_PENDING_REVIEW',
          'Check the printed quarter, standalone/consolidated basis, currency scale and income arithmetic together.')
    check('NORMALIZED_VALUES_MATCH', repeated.get('values_inr_crore') == record.get('values_inr_crore')
          and bool(repeated.get('values_inr_crore')),
          'The saved figures must equal a fresh calculation from the source cells.')
    readings_ok = True
    for name in ('revenue', 'other_income', 'total_income', 'pat'):
        cell = source.get('cells', {}).get(name, {})
        reading = cell.get('source_reading', {})
        try:
            native = numeric_reading(reading.get('native_text', ''))
            ocr = numeric_reading(reading.get('ocr_text', ''))
            readings_ok = readings_ok and (
                reading.get('status') == 'READINGS_AGREE_PENDING_REVIEW' and native is not None
                and native == ocr == Decimal(str(cell.get('value')))
                and reading.get('pdf_page') == source.get('pdf_page')
                and reading.get('column_index') == source.get('column_index'))
        except (InvalidOperation, ValueError, TypeError):
            readings_ok = False
    check('FOUR_CORE_SOURCE_READINGS', bool(readings_ok),
          'Revenue, other income, total income and total net profit must retain matching text/image readings from the same column.')
    check('EXTRACTION_CANDIDATE_CHECKED', record.get('status') == 'CHECKED_PENDING_REVIEW' and not record.get('issues'),
          'An unresolved extraction warning cannot be cleared by this review.')
    source_verification = source_verification or {}
    source_ok = (source_verification.get('status') == 'ACQUISITION_RECEIPT_PRESERVED_PENDING_REVIEW'
                 and source_verification.get('provider_id') in {'DIRECT_TRUSTED_SOURCE', 'EIOS_CORROBORATED_BROWSER_CAPTURE'}
                 and source_verification.get('document_hash') == source.get('document_hash')
                 and source_verification.get('source_url', '').startswith('https://'))
    check('OFFICIAL_SOURCE_DELIVERY_PROVENANCE', source_ok,
          'The exact document bytes must retain a trusted direct receipt or corroborated browser-capture provenance for the official URL.')
    reporting_notes = reporting_notes or {}
    notes_complete = reporting_notes.get('review_complete') is True
    check('REPORTING_NOTES_AND_RESTATEMENTS', notes_complete,
          'Review the reporting notes, audit status and any restatement or balancing-quarter explanation before publication.')
    technical_ok = all(c['status'] == 'PASS' for c in checks[:4])
    fingerprint = sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    figures = record.get('values_inr_crore', {}) if technical_ok else {}
    note_assessments = [{**item, 'applicability': note_context(item.get('source_passage', ''),
        basis=source.get('basis', ''), period_end=source.get('period_end', ''))}
        for item in reporting_notes.get('candidates', [])]
    all_checks_pass = all(c['status'] == 'PASS' for c in checks)
    decision = ('READY_FOR_HUMAN_FACT_APPROVAL' if all_checks_pass else
                'HOLD_FOR_REPORTING_NOTE_REVIEW' if source_ok and not notes_complete else
                'HOLD_FOR_SOURCE_AND_FINANCIAL_REVIEW')
    return {'schema_version': 1, 'record_fingerprint': fingerprint,
            'method': 'DETERMINISTIC_FINANCIAL_CHECKS_V1', 'decision': decision,
            'technical_checks_passed': technical_ok, 'checks': checks,
            'reviewer_summary': ('The four core figures agree across both readings and reconcile. '
                                 + ('Delivery provenance passes; reporting notes still require human review.' if source_ok else 'Source delivery and reporting notes still require review.') if technical_ok else
                                 'Some financial extraction checks failed. Resolve the listed holds before source approval.'),
            'reporting_note_assessments': note_assessments,
            'figures_for_review_inr_crore': figures,
            'period': source.get('quarter'), 'basis': source.get('basis'),
            'not_checked': ['Cash flow and balance sheet completeness', 'Earnings quality',
                            'Historical trends', 'Valuation and investment verdict'],
            'requires_human_review': True, 'creates_approved_facts': False, 'changes_verdict': False}
