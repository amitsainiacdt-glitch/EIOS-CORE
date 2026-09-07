"""Find source-bound reporting-note passages without treating matches as review."""
import re
from hashlib import sha256

TOPICS = (
    ('LIMITED_REVIEW', r'limited\s+review|do\s+not\s+express\s+an?\s+audit\s+opinion',
     'Check the assurance provided. A limited review must not be described as a full audit.'),
    ('COMPARABILITY', r'not\s+be\s+comparable|not\s+comparable|non[- ]comparable',
     'Check which periods and accounting basis are affected before interpreting growth.'),
    ('BALANCING_QUARTER', r'balancing\s+figures',
     'Check whether the quarter is derived from full-year figures less nine-month figures.'),
    ('IMPAIRMENT', r'\bimpairment\b',
     'Check the affected period and accounting basis. Do not automatically remove the charge from earnings.'),
    ('RESTATEMENT_OR_REGROUPING', r'\brestat(?:ed|ement|ements)\b|\bregrouped\b|\breclassified\b',
     'Inspect the passage for restatement or classification changes; a keyword alone does not confirm a change.'),
)


def extract_reporting_notes(pages, document_hash):
    if not re.fullmatch(r'[a-f0-9]{64}', document_hash):
        raise ValueError('Document hash required')
    candidates, missing = [], []
    for number, text in enumerate(pages, 1):
        if not text or not text.strip():
            missing.append(number)
            continue
        # Preserve original paragraph spans and offsets; no OCR correction.
        starts = sorted({0, *[m.start() for m in re.finditer(r'(?m)^\s*\d{1,2}[.)]?\s+(?=[A-Za-z])', text)]})
        for start, end in zip(starts, starts[1:] + [len(text)]):
            passage = text[start:end].strip()
            normalized = re.sub(r'\s+', ' ', passage)
            for code, pattern, explanation in TOPICS:
                if not re.search(pattern, normalized, re.I):
                    continue
                # Oversized table/text fragments are flagged, not silently truncated into a quotation.
                oversized = len(passage) > 6000
                identity = f'{document_hash}:{number}:{start}:{end}:{code}'
                candidates.append({'candidate_id': sha256(identity.encode()).hexdigest(),
                    'document_hash': document_hash, 'pdf_page': number, 'topic': code,
                    'source_passage': passage, 'text_start': start, 'text_end': end,
                    'review_question': explanation, 'status': 'LONG_PASSAGE_REVIEW_REQUIRED' if oversized else 'NOTE_CANDIDATE_PENDING_REVIEW',
                    'scope': 'DOCUMENT_LEVEL_PERIOD_AND_BASIS_NOT_YET_RESOLVED',
                    'creates_approved_facts': False})
    return {'status': 'REPORTING_NOTES_PENDING_REVIEW', 'candidates': candidates,
            'pages_without_text': missing, 'absence_proves_no_issue': False,
            'review_complete': False, 'changes_verdict': False}
