"""Compare header passes without merging readings or approving financial facts."""
import math
from modules.company_intelligence.quarterly_header_binding import bind_page_headers
from modules.company_intelligence.quarterly_crop_alignment import check_crop_alignment


def compare_header_passes(first, second):
    results = []
    second_tables = {table['table_id']: table for table in second.get('tables', [])}
    for table in first.get('tables', []):
        other = second_tables.get(table['table_id'], {})
        for column in table['columns']:
            index = column['column_index']
            fields = {}
            for kind in ('basis', 'duration', 'unit'):
                readings = []
                for current in (table, other):
                    readings.append(sorted({span['text'] for span in current.get('spans', [])
                        if span['kind'] == kind and span['first_column'] <= index <= span['last_column']}))
                left, right = readings
                source_issues = sorted({issue for current in (table, other)
                    for reading in current.get('readings', []) if index in reading['covered_columns']
                    for issue in reading.get('issues', []) if kind.upper() in issue})
                status = ('AMBIGUOUS_HOLD' if source_issues
                          else 'READINGS_AGREE_PENDING_REVIEW' if len(left) == 1 and left == right
                          else 'CONFLICT_HOLD' if left and right and left != right
                          else 'AMBIGUOUS_HOLD' if len(left) > 1 or len(right) > 1
                          else 'INCOMPLETE_HOLD')
                fields[kind] = {'first_pass': left, 'second_pass': right, 'status': status,
                                'source_issues': source_issues}
            results.append({'table_id': table['table_id'], 'column_index': index,
                            'fields': fields, 'status': 'RESEARCH_HOLD'})
    return {'status': 'DIAGNOSTIC_COMPARISON_ONLY', 'columns': results,
            'creates_approved_facts': False, 'changes_verdict': False}


def reconcile_header_region(page, first_receipt, region, ocr, document_hash):
    """Check transferred registration on fresh crop labels, then compare headers.

    Spatial agreement is not financial accuracy or permission to publish.
    """
    if (document_hash != first_receipt.get('document_hash')
            or region.get('document_hash') != document_hash
            or page['pdf_page'] != region.get('pdf_page')
            or first_receipt.get('pdf_page') != page['pdf_page']
            or region.get('image_sha256') != ocr.get('input_sha256')):
        raise ValueError('Targeted header source binding mismatch')
    tables = [table for table in page.get('ruled_tables', []) if table['table_id'] == region.get('table_id')]
    if len(tables) != 1:
        raise ValueError('Targeted header table binding mismatch')
    box = region['crop_bbox']
    if (len(box) != 4 or any(type(x) not in (int, float) or not math.isfinite(x) for x in box)
            or box[2] <= box[0] or box[3] <= box[1]):
        raise ValueError('Invalid header crop geometry')
    for axis, extent in (('x', box[2] - box[0]), ('y', box[3] - box[1])):
        dimension = 'image_width' if axis == 'x' else 'image_height'
        pixels = region[dimension]
        scale = region['pixels_per_pdf_' + axis]
        if (type(pixels) is not int or pixels <= 0 or ocr[dimension] != pixels
                or type(scale) not in (int, float) or not math.isfinite(scale)
                or not math.isclose(scale, pixels / extent, rel_tol=1e-6)):
            raise ValueError('Header crop scale/dimension mismatch')
    receipt = {**first_receipt, 'image_sha256': region['image_sha256'],
               'render_transform': {**region, 'normalized_page_bbox': box}}
    crop_check = check_crop_alignment(page.get('page_words', []), ocr, region,
                                     first_receipt['alignment_diagnostics'])
    alignment = first_receipt['alignment_diagnostics']
    if crop_check['status'] != 'CROP_ALIGNMENT_CHECKED_FOR_COMPARISON':
        alignment = {'status': 'HOLD_CROP_ALIGNMENT'}
    second = bind_page_headers({**page, 'ruled_tables': tables}, ocr, receipt, alignment)
    first = first_receipt.get('header_binding', {})
    first = {**first, 'tables': [t for t in first.get('tables', []) if t['table_id'] == region['table_id']]}
    return {**compare_header_passes(first, second), 'second_pass_binding': second,
            'registration_status': crop_check['status'], 'crop_alignment_check': crop_check,
            'document_hash': document_hash, 'pdf_page': page['pdf_page'],
            'table_id': region['table_id'], 'image_sha256': region['image_sha256']}
