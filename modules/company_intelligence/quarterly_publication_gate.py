"""Final pre-materialization gate for a reviewed quarterly fact candidate."""
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials
from modules.company_intelligence.quarterly_note_human_review import QuarterlyNoteReviewLedger


def quarterly_approval_assessment(candidate, queue, note_review_ledger):
    if candidate.event_type != 'QUARTERLY_FINANCIAL_RESULT':
        return None
    record = queue.get('quarterly_record_evidence', {}).get(candidate.candidate_id)
    if not record:
        raise ValueError('quarterly approval requires its exact financial evidence record')
    source = record.get('source_column', {})
    if source.get('document_hash') != candidate.document_hash:
        raise ValueError('quarterly financial record does not bind to candidate document')
    notes = QuarterlyNoteReviewLedger(note_review_ledger).apply(
        queue.get('reporting_notes', {'candidates': []}), document_hash=candidate.document_hash,
        company=candidate.company, period_end=source.get('period_end', ''), basis=source.get('basis', ''))
    assessment = assess_quarterly_financials(record, source_verification=queue.get('source_verification'),
                                              reporting_notes=notes)
    if assessment['decision'] != 'READY_FOR_HUMAN_FACT_APPROVAL':
        holds = ', '.join(check['code'] for check in assessment['checks'] if check['status'] != 'PASS')
        raise ValueError(f'quarterly approval is blocked by: {holds or assessment["decision"]}')
    return assessment


__all__ = ['quarterly_approval_assessment']
