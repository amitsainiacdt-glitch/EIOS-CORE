"""Read review candidates for a separate unapproved dashboard panel."""
import hashlib
import json
from urllib.parse import urlsplit
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials
from modules.company_intelligence.quarterly_note_context import note_context
from modules.company_intelligence.quarterly_note_draft_display import attach_note_drafts


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
                      'passage': note['source_passage'], 'question': note['review_question']})
    return {'items': items, 'invalidCount': invalid}


def load_quarterly_review_display(root, ticker):
    directory = root / 'data/runtime/quarterly_intake'
    items, seen, invalid = [], set(), 0
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
                review = assess_quarterly_financials(record)
                url = candidate.get('source_url', '')
                parsed = urlsplit(url)
                safe_url = url if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password else None
                items.append({'id': candidate['candidate_id'], 'period': review['period'], 'basis': review['basis'],
                    'summary': review['reviewer_summary'], 'figures': review['figures_for_review_inr_crore'],
                    'assistantUnitReview': bool(source.get('header_evidence', {}).get('spanning_source_headers', {}).get('unit', {}).get('review_id')),
                    'checks': review['checks'], 'notChecked': review['not_checked'],
                    'reportingNotes': attach_note_drafts(root,
                        display_reporting_notes(queue.get('reporting_notes', {}), digest,
                                                basis=source['basis'], period_end=source['period_end']),
                        ticker=ticker, document_hash=digest, period_end=source['period_end']),
                    'sourceUrl': safe_url, 'sourcePage': source['pdf_page'], 'documentHash': digest,
                    'readings': source.get('raw_readings', []), 'status': 'UNAPPROVED_REVIEW_ONLY'})
        except (OSError, ValueError, KeyError, TypeError):
            invalid += 1
    return {'items': items, 'invalidPacketCount': invalid, 'changesVerdict': False}
