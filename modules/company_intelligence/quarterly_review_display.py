"""Read review candidates for a separate unapproved dashboard panel."""
import hashlib
import json
from urllib.parse import urlsplit
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials
from modules.company_intelligence.quarterly_note_context import note_context
from modules.company_intelligence.quarterly_note_draft_display import attach_note_drafts
from modules.company_intelligence.quarterly_note_human_review import QuarterlyNoteReviewLedger
from modules.company_intelligence.quarterly_plain_english import explain_quarterly_financials
from modules.company_intelligence.quarterly_business_causes import load_quarterly_business_causes
from modules.company_intelligence.quarterly_cause_monitoring import build_quarterly_cause_monitoring
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger, attach_indicator_record_state


def display_reporting_notes(payload, document_hash, *, basis='', period_end=''):
    items, invalid, seen = [], 0, set()
    for note in payload.get('candidates', []):
        if (note.get('document_hash') != document_hash or type(note.get('pdf_page')) is not int
                or note['pdf_page'] < 1 or not isinstance(note.get('source_passage'), str)
                or not note['source_passage'].strip() or not isinstance(note.get('review_question'), str)
                or not isinstance(note.get('candidate_id'), str) or not isinstance(note.get('topic'), str)):
            invalid += 1
            continue
        if note['candidate_id'] in seen:
            continue
        seen.add(note['candidate_id'])
        items.append({'id': note['candidate_id'], 'topic': note['topic'], 'page': note['pdf_page'],
                      'context': note_context(note['source_passage'], basis=basis, period_end=period_end),
                      'passage': note['source_passage'], 'question': note['review_question'],
                      'humanReview': note.get('human_review')})
    return {'items': items, 'invalidCount': invalid}


def prior_comparable_figures(records, current):
    source = current.get('source_column', {})
    try:
        quarter, fiscal = source['quarter'].split('-FY')
        target = f'{quarter}-FY{int(fiscal)-1}'
    except (KeyError, ValueError, AttributeError):
        return None
    matches = [item for item in records.values() if item is not current
               and item.get('status') == 'CHECKED_PENDING_REVIEW'
               and item.get('source_column', {}).get('quarter') == target
               and item.get('source_column', {}).get('basis') == source.get('basis')]
    if len(matches) != 1:
        return None
    values = matches[0].get('values_inr_crore', {})
    return values if all(key in values for key in ('revenue','pat')) else None


def load_quarterly_review_display(root, ticker):
    directory = root / 'data/runtime/quarterly_intake'
    note_ledger = QuarterlyNoteReviewLedger(root / 'data/company_intelligence/quarterly_note_human_reviews.jsonl')
    items, seen, seen_content, invalid = [], set(), set(), 0
    for path in sorted(directory.rglob('quarterly-candidates.json'), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            queue = json.loads(path.read_text(encoding='utf-8'))
            for candidate in queue['candidates']:
                record = queue['quarterly_record_evidence'][candidate['candidate_id']]
                source = record['source_column']
                if source['ticker'].upper() != ticker.upper():
                    continue
                digest = source['document_hash']
                if candidate['document_hash'] != digest:
                    raise ValueError('Evidence mismatch')
                # Locate the preserved source in the candidate run, not an arbitrary supplied path.
                pdf = next((parent / 'source.pdf' for parent in (path.parent, path.parent.parent)
                            if (parent / 'source.pdf').is_file()), None)
                if pdf is None or hashlib.sha256(pdf.read_bytes()).hexdigest() != digest:
                    raise ValueError('Preserved PDF missing or changed')
                identity = (digest, source['pdf_page'], source['column_index'], source['quarter'], source['basis'])
                if identity in seen:
                    continue
                seen.add(identity)
                values = record.get('values_inr_crore', {})
                content_identity = (source['ticker'].upper(), source['quarter'], source['basis'],
                                    tuple((key, values.get(key)) for key in ('revenue','other_income','total_income','pat')))
                if content_identity in seen_content:
                    continue
                seen_content.add(content_identity)
                reviewed_notes = note_ledger.apply(queue.get('reporting_notes', {'candidates': []}),
                    document_hash=digest, company=queue['company'], period_end=source['period_end'], basis=source['basis'])
                review = assess_quarterly_financials(record, source_verification=queue.get('source_verification'),
                                                     reporting_notes=reviewed_notes)
                url = candidate.get('source_url', '')
                parsed = urlsplit(url)
                safe_url = url if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password else None
                causes = load_quarterly_business_causes(
                    root / 'data/company_intelligence/quarterly_business_causes.json',
                    ticker=ticker, period_end=source['period_end'], basis=source['basis'])
                items.append({'id': candidate['candidate_id'], 'period': review['period'], 'basis': review['basis'],
                    'summary': review['reviewer_summary'], 'figures': review['figures_for_review_inr_crore'],
                    'plainEnglish': explain_quarterly_financials(
                        review, reviewed_notes, prior_comparable_figures(queue['quarterly_record_evidence'], record)),
                    'businessCauses': causes,
                    'causeMonitoring': attach_indicator_record_state(
                        build_quarterly_cause_monitoring(causes),
                        PrimaryIndicatorLedger(root / 'data/company_intelligence/primary_indicator_records.jsonl')),
                    'assistantUnitReview': bool(source.get('header_evidence', {}).get('spanning_source_headers', {}).get('unit', {}).get('review_id')),
                    'checks': review['checks'], 'notChecked': review['not_checked'],
                    'reportingNotes': attach_note_drafts(root,
                        display_reporting_notes(reviewed_notes, digest,
                                                basis=source['basis'], period_end=source['period_end']),
                        ticker=ticker, document_hash=digest, period_end=source['period_end']),
                    'queuePath': str(path.resolve()), 'periodEnd': source['period_end'],
                    'sourceUrl': safe_url, 'sourcePage': source['pdf_page'], 'documentHash': digest,
                    'readings': source.get('raw_readings', []), 'status': review['decision']})
        except (OSError, ValueError, KeyError, TypeError):
            invalid += 1
    return {'items': items, 'invalidPacketCount': invalid, 'changesVerdict': False}
