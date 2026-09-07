"""Reuse document-specific assistant visual unit evidence, never human approval."""
import copy
import hashlib
import json
from pathlib import Path
from modules.company_intelligence.quarterly_shared_headers import resolve_shared_headers
from modules.company_intelligence.quarterly_unit_reading import assess_unit_reading


def _direct_validated_unit_reviews(root, document_hash):
    registry = root / 'data/company_intelligence/quarterly_unit_reviews.json'
    if not registry.exists():
        return []
    reviews = json.loads(registry.read_text(encoding='utf-8'))['reviews']
    valid = []
    for review in reviews:
        if review.get('document_hash') != document_hash:
            continue
        if review.get('reviewer_kind') != 'ASSISTANT_VISUAL_REVIEW' or review.get('status') != 'CANDIDATE_NOT_HUMAN_APPROVED':
            continue
        if assess_unit_reading(review.get('observed_text'))['status'] != 'UNIT_CANDIDATE_PENDING_REVIEW':
            continue
        try:
            evidence = (root / review['evidence_report']).resolve()
            if root not in evidence.parents:
                continue
            probe = json.loads(evidence.read_text(encoding='utf-8'))
            if any(probe.get(k) != review.get(k) for k in ('document_hash', 'pdf_page', 'table_id', 'crop_bbox', 'image_sha256')):
                continue
            image = Path(probe['image_path']).resolve()
            source = evidence.parent.parent / 'source.pdf'
            if root not in image.parents or root not in source.resolve().parents:
                continue
            if hashlib.sha256(image.read_bytes()).hexdigest() != review['image_sha256']:
                continue
            if hashlib.sha256(source.read_bytes()).hexdigest() != document_hash:
                continue
        except (OSError, ValueError, KeyError, TypeError):
            continue
        valid.append(review)
    return valid


def validated_unit_reviews(workspace, document_hash):
    root = Path(workspace).resolve()
    direct = _direct_validated_unit_reviews(root, document_hash)
    if direct:
        return direct
    capture_root = root / 'data/runtime/browser_source_capture'
    for provenance_path in capture_root.glob('*/provenance.json') if capture_root.is_dir() else ():
        try:
            provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
            if provenance.get('document_hash') != document_hash or provenance.get('status') != 'BROWSER_COPY_CORROBORATED_PENDING_REVIEW':
                continue
            source = (provenance_path.parent / provenance['preserved_file']).resolve()
            if provenance_path.parent.resolve() not in source.parents or hashlib.sha256(source.read_bytes()).hexdigest() != document_hash:
                continue
            comparison = json.loads((provenance_path.parent / provenance['comparison_file']).read_text(encoding='utf-8'))
            if comparison.get('original_hash') != provenance.get('original_upload_hash') or comparison.get('download_hash') != document_hash:
                continue
            originals = _direct_validated_unit_reviews(root, comparison['original_hash'])
            transferred = []
            for review in originals:
                page = next((item for item in comparison.get('pages', []) if item.get('page') == review['pdf_page']), None)
                if not page or page.get('text_exact_match') is not True or page.get('render_exact_match') is not True:
                    continue
                transferred.append({**review, 'document_hash': document_hash,
                    'review_id': review['review_id'] + '-render-equivalent-' + document_hash[:12],
                    'equivalent_original_hash': comparison['original_hash'],
                    'equivalence_status': 'EXACT_TEXT_AND_RENDER_MATCH_NOT_HUMAN_APPROVAL'})
            if transferred:
                return transferred
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return []


def apply_unit_reviews(binding, page, reviews, document_hash):
    result = copy.deepcopy(binding)
    for table in result.get('tables', []):
        matches = [r for r in reviews if (r.get('document_hash'),r.get('pdf_page'),r.get('table_id')) ==
                   (document_hash,page['pdf_page'],table['table_id'])]
        if len(matches) != 1:
            continue
        review = matches[0]
        if review.get('reviewer_kind') != 'ASSISTANT_VISUAL_REVIEW' or review.get('status') != 'CANDIDATE_NOT_HUMAN_APPROVED':
            continue
        assessment = assess_unit_reading(review.get('observed_text'))
        if assessment['status'] != 'UNIT_CANDIDATE_PENDING_REVIEW':
            continue
        prior = table.get('unit_assessment', {})
        if 'FOREIGN_OR_CONFLICTING_CURRENCY' in prior.get('issues', []):
            continue
        if prior.get('unit_candidates') and prior['unit_candidates'] != assessment['unit_candidates']:
            continue
        # Never overwrite an existing explicit unit reading.
        if any(s['kind'] == 'unit' for s in table['spans']):
            continue
        source_table = next(t for t in page['ruled_tables'] if t['table_id'] == table['table_id'])
        source_binding = {'document_hash': document_hash, 'pdf_page': page['pdf_page'], 'table_id': table['table_id']}
        table['unit_review_evidence'] = review
        table['spans'].append({**source_binding, 'kind': 'unit', 'text': review['observed_text'],
            'first_column': 0, 'last_column': len(source_table['columns']) - 1,
            'status': 'ASSISTANT_REVIEWED_UNIT_CANDIDATE', 'review_id': review['review_id']})
        for column in table['columns']:
            source_column = next(c for c in source_table['columns'] if c['column_index'] == column['column_index'])
            dates = column.get('date_comparison', {})
            native_date = dates.get('native', {}).get('date')
            resolved = resolve_shared_headers({**source_binding, **source_column,
                                               'date_header_text': native_date or source_column['date_header_text']}, table['spans'])
            if dates.get('status') != 'DATE_READINGS_AGREE_PENDING_REVIEW':
                resolved = {**resolved, 'status': 'HOLD', 'issues': [*resolved.get('issues', []), 'DATE_REVIEW_REQUIRED']}
            column['resolution'] = resolved
    return result
