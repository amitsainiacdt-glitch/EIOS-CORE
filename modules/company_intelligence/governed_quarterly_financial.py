"""Append-only governed quarterly financial records created after every review gate."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.governed_company_fact import GovernedCompanyFact
from modules.company_intelligence.governed_quarterly_controlled_write_adapter import GovernedQuarterlyControlledWriteAdapter
from modules.intelligence_write import ControlledIntelligenceWriteJournal, ControlledIntelligenceWriteService, WriteReceiptStatus


@dataclass(frozen=True)
class GovernedQuarterlyFinancial:
    schema_version: int
    record_id: str
    fact_id: str
    candidate_id: str
    ticker: str
    company: str
    quarter: str
    period_start: str
    period_end: str
    basis: str
    figures_inr_crore: dict[str, str]
    source_url: str
    source_page: int
    document_hash: str
    financial_record_fingerprint: str
    human_review_id: str
    created_at: datetime
    status: str = 'GOVERNED_QUARTERLY_FINANCIAL'
    changes_verdict: bool = False
    creates_catalyst: bool = False
    authorizes_trade: bool = False
    controlled_write_receipt_id: str | None = None


class GovernedQuarterlyFinancialRepository:
    REQUIRED = ('revenue', 'other_income', 'total_income', 'pat')

    def __init__(self, path: Path, *, controlled_write_service=None, controlled_write_adapter=None):
        self.path = Path(path)
        self.controlled_write_service = controlled_write_service or ControlledIntelligenceWriteService(
            journal=ControlledIntelligenceWriteJournal(
                self.path.parent / 'controlled-intelligence-write-journal.jsonl'
            )
        )
        if not isinstance(self.controlled_write_service, ControlledIntelligenceWriteService):
            raise ValueError('controlled_write_service must be a ControlledIntelligenceWriteService')
        self.controlled_write_adapter = controlled_write_adapter or GovernedQuarterlyControlledWriteAdapter()
        if not isinstance(self.controlled_write_adapter, GovernedQuarterlyControlledWriteAdapter):
            raise ValueError('controlled_write_adapter must be a GovernedQuarterlyControlledWriteAdapter')

    def materialize(self, candidate, fact, evidence_record, assessment, *, created_at):
        if not isinstance(fact, GovernedCompanyFact) or fact.status != 'GOVERNED_FACT':
            raise ValueError('governed quarterly record requires a governed company fact')
        if candidate.candidate_id != fact.candidate_id or candidate.document_hash != fact.document_hash:
            raise ValueError('governed fact does not bind to quarterly candidate')
        if candidate.event_type != 'QUARTERLY_FINANCIAL_RESULT':
            raise ValueError('candidate is not a quarterly financial result')
        if assessment.get('decision') != 'READY_FOR_HUMAN_FACT_APPROVAL':
            raise ValueError('quarterly financial assessment is not cleared for human fact approval')
        if any(check.get('status') != 'PASS' for check in assessment.get('checks', [])) or len(assessment.get('checks', [])) != 6:
            raise ValueError('all six quarterly checks must pass')
        source = evidence_record.get('source_column', {})
        if source.get('document_hash') != fact.document_hash or source.get('pdf_page') != fact.pdf_page:
            raise ValueError('quarterly evidence does not bind to governed fact source')
        if assessment.get('record_fingerprint') != self.fingerprint(evidence_record):
            raise ValueError('financial assessment does not bind to current evidence record')
        figures = assessment.get('figures_for_review_inr_crore', {})
        normalized = {name: self._number(figures.get(name), name) for name in self.REQUIRED}
        if Decimal(normalized['revenue']) + Decimal(normalized['other_income']) != Decimal(normalized['total_income']):
            raise ValueError('quarterly income arithmetic no longer reconciles')
        if any(item.candidate_id == candidate.candidate_id for item in self.read_all()):
            raise ValueError('quarterly candidate is already materialized')
        record_id = sha256(f'{fact.fact_id}\n{assessment["record_fingerprint"]}\nGOVERNED_QUARTERLY_V1'.encode()).hexdigest()
        controlled_command = self.controlled_write_adapter.build_command(
            candidate=candidate, fact=fact, source=source, figures=normalized,
            record_id=record_id, created_at=created_at,
        )
        controlled_receipt = self.controlled_write_service.submit(controlled_command)
        if controlled_receipt.status not in {WriteReceiptStatus.ACCEPTED, WriteReceiptStatus.DUPLICATE_NO_CHANGE}:
            raise ValueError(
                'controlled quarterly Fact write blocked: '
                + ', '.join(controlled_receipt.rejection_codes or controlled_receipt.validation_codes)
            )
        item = GovernedQuarterlyFinancial(
            1, record_id, fact.fact_id, candidate.candidate_id, source['ticker'], fact.company,
            source['quarter'], source['period_start'], source['period_end'], source['basis'], normalized,
            fact.source_url, source['pdf_page'], fact.document_hash, assessment['record_fingerprint'],
            fact.human_review_id, created_at,
            controlled_write_receipt_id=controlled_receipt.receipt_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('a', encoding='utf-8') as stream:
            payload = asdict(item); payload['created_at'] = created_at.isoformat()
            stream.write(json.dumps(payload, sort_keys=True, separators=(',', ':')) + '\n')
        return item

    def read_all(self):
        if not self.path.exists(): return ()
        result, ids, candidates = [], set(), set()
        controlled_receipt_ids = {item.receipt_id for item in self.controlled_write_service.receipts()}
        for line_number, line in enumerate(self.path.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip(): continue
            try:
                value = json.loads(line); value['created_at'] = datetime.fromisoformat(value['created_at'])
                item = GovernedQuarterlyFinancial(**value)
                if item.schema_version != 1 or item.status != 'GOVERNED_QUARTERLY_FINANCIAL': raise ValueError('unsupported record')
                if item.record_id in ids or item.candidate_id in candidates: raise ValueError('duplicate record identity')
                if item.changes_verdict or item.creates_catalyst or item.authorizes_trade: raise ValueError('record exceeded its authority')
                if item.controlled_write_receipt_id is not None and item.controlled_write_receipt_id not in controlled_receipt_ids:
                    raise ValueError('controlled write receipt is missing')
                for name in self.REQUIRED: self._number(item.figures_inr_crore.get(name), name)
                ids.add(item.record_id); candidates.add(item.candidate_id); result.append(item)
            except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
                raise ValueError(f'invalid governed quarterly record at line {line_number}: {exc}') from exc
        return tuple(result)

    @staticmethod
    def fingerprint(record):
        return sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    @staticmethod
    def _number(value, name):
        try: number = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as exc: raise ValueError(f'{name} must be numeric') from exc
        if not number.is_finite(): raise ValueError(f'{name} must be finite')
        return format(number, 'f')


__all__ = ['GovernedQuarterlyFinancial', 'GovernedQuarterlyFinancialRepository']
