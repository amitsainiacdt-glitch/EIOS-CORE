"""Append-only human applicability decisions for quarterly reporting notes."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
from pathlib import Path


class QuarterlyNoteDecision(str, Enum):
    APPLIES = "APPLIES"
    DOES_NOT_APPLY = "DOES_NOT_APPLY"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class QuarterlyNoteReviewReceipt:
    schema_version: int
    review_id: str
    note_id: str
    note_fingerprint: str
    document_hash: str
    company: str
    period_end: str
    basis: str
    decision: QuarterlyNoteDecision
    rationale: str
    reviewed_at: datetime
    reviewer: str


class QuarterlyNoteReviewLedger:
    def __init__(self, path: Path):
        self.path = Path(path)

    def record(self, note, *, review_id, document_hash, company, period_end, basis,
               decision, rationale, reviewed_at, reviewer):
        self._validate_note(note, document_hash)
        decision = decision if isinstance(decision, QuarterlyNoteDecision) else QuarterlyNoteDecision(decision)
        existing = self.read_all()
        receipt = QuarterlyNoteReviewReceipt(
            1, self._text(review_id, 'review_id'), note['candidate_id'], self.note_fingerprint(note),
            document_hash, self._text(company, 'company'), self._text(period_end, 'period_end'),
            self._basis(basis), decision, self._rationale(rationale), self._datetime(reviewed_at),
            self._text(reviewer, 'reviewer'))
        if any(r.review_id == receipt.review_id for r in existing):
            raise ValueError("duplicate review identity")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(',', ':')) + '\n')
        return receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        result, review_ids = [], set()
        for line_number, line in enumerate(self.path.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if value.get('schema_version') != 1:
                    raise ValueError('unsupported schema')
                value['decision'] = QuarterlyNoteDecision(value['decision'])
                value['reviewed_at'] = datetime.fromisoformat(value['reviewed_at'])
                receipt = QuarterlyNoteReviewReceipt(**value)
                self._sha(receipt.note_fingerprint); self._sha(receipt.document_hash)
                self._basis(receipt.basis); self._rationale(receipt.rationale)
                key = (receipt.note_id, receipt.document_hash, receipt.period_end, receipt.basis)
                if receipt.review_id in review_ids:
                    raise ValueError('duplicate review identity')
                review_ids.add(receipt.review_id); result.append(receipt)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f'invalid quarterly note review at line {line_number}: {exc}') from exc
        return tuple(result)

    def apply(self, reporting_notes, *, document_hash, company, period_end, basis):
        candidates = reporting_notes.get('candidates', [])
        reviews = {(r.note_id, r.document_hash, r.period_end, r.basis): r for r in self.read_all()}
        resolved = []
        for note in candidates:
            self._validate_note(note, document_hash)
            receipt = reviews.get((note['candidate_id'], document_hash, period_end, basis))
            if receipt and receipt.company != company:
                raise ValueError('review does not bind to the current company')
            if receipt and receipt.note_fingerprint != self.note_fingerprint(note):
                raise ValueError('review does not bind to the current note passage')
            resolved.append({**note, 'human_review': self._payload(receipt) if receipt else None})
        complete = bool(candidates) and all(
            item['human_review'] and item['human_review']['decision'] != QuarterlyNoteDecision.UNRESOLVED.value
            for item in resolved)
        return {**reporting_notes, 'candidates': resolved, 'review_complete': complete,
                'reviewed_count': sum(item['human_review'] is not None for item in resolved),
                'review_context': {'company': company, 'document_hash': document_hash,
                                   'period_end': period_end, 'basis': basis}}

    @staticmethod
    def note_fingerprint(note):
        fields = {key: note.get(key) for key in ('candidate_id', 'document_hash', 'pdf_page', 'topic',
                                                  'source_passage', 'review_question')}
        return sha256(json.dumps(fields, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    @classmethod
    def _validate_note(cls, note, document_hash):
        if not isinstance(note, dict) or not cls._text(note.get('candidate_id'), 'note_id'):
            raise ValueError('invalid note candidate')
        cls._sha(document_hash)
        if note.get('document_hash') != document_hash:
            raise ValueError('note does not bind to document')
        cls._text(note.get('source_passage'), 'source_passage')

    @staticmethod
    def _payload(item):
        if item is None: return None
        return {**asdict(item), 'decision': item.decision.value, 'reviewed_at': item.reviewed_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f'{name} must not be empty')
        return value.strip()

    @classmethod
    def _rationale(cls, value):
        value = cls._text(value, 'rationale')
        if len(value) < 10: raise ValueError('rationale must contain at least 10 characters')
        return value

    @staticmethod
    def _basis(value):
        if value not in {'STANDALONE', 'CONSOLIDATED'}: raise ValueError('basis must be STANDALONE or CONSOLIDATED')
        return value

    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime) or value.tzinfo is None: raise ValueError('reviewed_at must be timezone-aware')
        return value

    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64: raise ValueError('fingerprint must be SHA-256')
        int(value, 16)


__all__ = ['QuarterlyNoteDecision', 'QuarterlyNoteReviewLedger', 'QuarterlyNoteReviewReceipt']
