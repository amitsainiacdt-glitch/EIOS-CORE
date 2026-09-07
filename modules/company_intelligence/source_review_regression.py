"""Detect drift from assistant-checked examples; never grant financial approval."""
from hashlib import file_digest
import json
from pathlib import Path

from modules.company_intelligence.financial_review_examples import build_cash_flow_review_examples


def check_source_review_regression(root: Path, review_path: Path, pack_path: Path):
    root = Path(root).resolve()
    report = {'status': 'NO_REFERENCE_CHECKS', 'checked_examples': 0, 'issues': [],
              'human_approval': False, 'changes_verdict': False,
              'meaning': 'Consistency with saved assistant observations only; not independent review or learning on unseen reports.'}
    if not review_path.exists():
        return report
    try:
        review = json.loads(review_path.read_text(encoding='utf-8'))
        if (review.get('schema_version') != 1 or review.get('reviewer_type') != 'AI_ASSISTANT'
            or any(review.get(flag) is not False for flag in ('human_approval', 'meta_approval', 'creates_evidence', 'changes_verdict', 'counts_as_human_learning_feedback'))):
            raise ValueError('Invalid reference authority flags')
        examples = build_cash_flow_review_examples(json.loads(pack_path.read_text(encoding='utf-8')))
        by_id = {item['example_id']: item for item in examples['examples']}
        checks = review['checks']
        if not isinstance(checks, list):
            raise ValueError('Invalid checks collection')
        seen = set()
        for check in checks:
            identifier = check['example_id']
            if identifier in seen:
                raise ValueError('Duplicate reference example')
            seen.add(identifier)
            item = by_id.get(identifier)
            if item is None:
                report['issues'].append({'example_id': identifier, 'reason': 'EXTRACTION_CHANGED_OR_MISSING'})
                continue
            document = (root / check['local_document']).resolve()
            if root not in document.parents:
                raise ValueError('Reference document must remain inside workspace')
            if not document.is_file():
                report['issues'].append({'example_id': identifier, 'reason': 'SOURCE_FILE_MISSING'})
                continue
            with document.open('rb') as stream:
                digest = file_digest(stream, 'sha256').hexdigest()
            inputs = item['inputs']
            matches = (digest == check['document_hash'] and item['period'] == check['period']
                       and item['calculated_free_cash_flow'] == check['calculated_free_cash_flow_crore']
                       and inputs['operating_cash_flow']['value'] == check['operating_cash_crore']
                       and inputs['cash_capex']['value'] == check['fixed_asset_spending_magnitude_crore']
                       and all(fact['document_hash'] == digest and fact['pdf_page'] == check['pdf_page']
                               and fact['column'] == check['column'] for fact in inputs.values()))
            if not matches:
                report['issues'].append({'example_id': identifier, 'reason': 'SOURCE_OR_REFERENCE_CHANGED'})
            report['checked_examples'] += 1
        report['status'] = 'RECHECK_REQUIRED' if report['issues'] else ('SAVED_EXAMPLES_UNCHANGED' if checks else 'NO_REFERENCE_CHECKS')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        report['status'] = 'RECHECK_REQUIRED'
        report['issues'].append({'reason': 'REFERENCE_CHECK_FAILED', 'detail': str(exc)})
    return report
