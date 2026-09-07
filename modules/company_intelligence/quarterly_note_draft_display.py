"""Attach explicitly unapproved assistant explanations to matching source notes."""
import json


def attach_note_drafts(root, notes, *, ticker, document_hash, period_end):
    matches = {}
    for path in sorted((root / 'data/company_intelligence').glob('*_quarterly_note_assessment_draft.json')):
        try:
            draft = json.loads(path.read_text(encoding='utf-8'))
            if (draft.get('ticker') != ticker.upper() or draft.get('document_hash') != document_hash
                    or draft.get('target_period_end') != period_end
                    or draft.get('status') != 'ASSISTANT_RESEARCH_DRAFT_NOT_HUMAN_APPROVED'
                    or draft.get('creates_approved_facts') is not False or draft.get('changes_verdict') is not False):
                continue
            for assessment in draft['assessments']:
                if (not isinstance(assessment.get('candidate_id'), str)
                        or type(assessment.get('local_pdf_page')) is not int
                        or not isinstance(assessment.get('explanation'), str)
                        or not assessment['explanation'].strip()):
                    continue
                key = (assessment['candidate_id'], assessment['local_pdf_page'])
                matches.setdefault(key, []).append({'explanation': assessment['explanation'],
                    'status': 'ASSISTANT_DRAFT_NOT_APPROVED'})
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            continue
    for note in notes['items']:
        found = matches.get((note['id'], note['page']), [])
        # Conflicting/duplicate drafts must not be chosen by file order.
        note['assistantDraft'] = found[0] if len(found) == 1 else None
    return notes
