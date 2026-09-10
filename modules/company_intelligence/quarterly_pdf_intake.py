"""Local quarterly layout-to-OCR orchestration. All output remains research-held."""
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
from uuid import uuid4

from modules.company_intelligence.quarterly_pdf_layout import extract_pdf_layout
from modules.company_intelligence.quarterly_ocr_comparison import compare_page
from modules.company_intelligence.quarterly_alignment import estimate_alignment, validate_alignment
from modules.company_intelligence.quarterly_header_binding import bind_page_headers
from modules.company_intelligence.quarterly_header_region import extract_header_regions
from modules.company_intelligence.quarterly_unit_review import validated_unit_reviews, apply_unit_reviews
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import write_quarterly_review_queue
from modules.company_intelligence.quarterly_reporting_notes import extract_reporting_notes
from modules.company_intelligence.quarterly_source_intake import verify_intake_source


def run_header_fallback(report, *, workspace):
    """Preserve second readings separately; never substitute first-pass data."""
    pages = [item['pdf_page'] for item in report['ocr_pages']
             if any(column['resolution']['status'] == 'HOLD'
                    for table in item.get('header_binding', {}).get('tables', [])
                    for column in table['columns'])]
    if not pages:
        return {'status': 'NOT_REQUIRED', 'creates_approved_facts': False}
    try:
        return extract_header_regions(report['run_directory'], workspace=workspace, page_numbers=pages)
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        return {'status': 'HEADER_OCR_FAILED_HOLD', 'error': str(exc), 'creates_approved_facts': False}


def plan_ocr(layout, limit=3):
    if type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError('OCR page limit must be between 1 and 10')
    eligible = [page for page in layout['pages']
                if page['table_classification']['eligible_for_company_financial_mapping']
                and any(c['header_assessment']['status'] == 'HOLD' for c in page['columns'])]
    return eligible[:limit], [page['pdf_page'] for page in eligible[limit:]]


def run_quarterly_intake(path, *, workspace, ticker, company=None, source_url=None,
                         source_verification_override=None, exchange_corroboration=None,
                         exchange_corroborations=()):
    from pypdf import PdfReader, PdfWriter
    import pdfplumber
    workspace = Path(workspace).resolve()
    path = Path(path).resolve()
    if workspace not in path.parents:
        raise ValueError('Input must be inside the workspace')
    original = path.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    unit_reviews = validated_unit_reviews(workspace, digest)
    reader = PdfReader(BytesIO(original))
    if len(reader.pages) > 80:
        raise ValueError('Quarterly intake page limit exceeded')
    reporting_notes = extract_reporting_notes([page.extract_text() or '' for page in reader.pages], digest)
    folder = workspace / 'data/runtime/quarterly_intake' / digest / uuid4().hex
    folder.mkdir(parents=True)
    # Extract from a byte-identical preserved copy, avoiding input-file races.
    source = folder / 'source.pdf'
    source.write_bytes(original)
    layout = extract_pdf_layout(source)
    (folder / 'layout.json').write_text(json.dumps(layout, indent=2), encoding='utf-8')
    selected, deferred = plan_ocr(layout)
    report = {'ticker': ticker, 'document_hash': digest, 'source_origin': 'LOCAL_FILE_IMPORT',
              'created_at': datetime.now(timezone.utc).isoformat(), 'run_directory': str(folder),
              'status': 'RESEARCH_HOLD', 'ocr_pages': [], 'deferred_pages': deferred,
              'creates_approved_facts': False, 'changes_verdict': False}
    report['exchange_corroboration_matches'] = 0
    report['reporting_notes'] = reporting_notes
    for candidate in selected:
        number = candidate['pdf_page']
        item = {'pdf_page': number, 'document_hash': digest, 'status': 'OCR_PENDING'}
        try:
            page = reader.pages[number - 1]
            rotation = page.rotation
            page.rotate(-rotation)
            writer = PdfWriter()
            writer.add_page(page)
            memory = BytesIO()
            writer.write(memory)
            memory.seek(0)
            image_path = folder / f'page-{number}.png'
            ocr_path = folder / f'page-{number}-ocr.json'
            with pdfplumber.open(memory) as pdf:
                normalized = pdf.pages[0]
                # Keep full-page renders below Windows OCR's 2600-pixel limit
                # while improving small financial print versus the initial 150 dpi.
                resolution = min(200, 2500 * 72 / max(normalized.width, normalized.height))
                rendered = normalized.to_image(resolution=resolution)
                rendered.save(str(image_path))
                width, height = rendered.original.size
                item['render_transform'] = {'rotation_removed': rotation,
                    'resolution_dpi': resolution,
                    'normalized_page_bbox': list(normalized.bbox),
                    'image_width': width, 'image_height': height,
                    'pixels_per_pdf_x': width / normalized.width,
                    'pixels_per_pdf_y': height / normalized.height}
            item['image_sha256'] = hashlib.sha256(image_path.read_bytes()).hexdigest()
            completed = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                '-File', str(workspace / 'scripts/extract_windows_ocr.ps1'),
                '-ImagePath', str(image_path.relative_to(workspace)), '-OutputPath', str(ocr_path.relative_to(workspace))],
                capture_output=True, text=True, timeout=60)
            if completed.returncode != 0:
                raise RuntimeError('Windows OCR failed: ' + completed.stderr[-500:])
            ocr = json.loads(ocr_path.read_text(encoding='utf-8'))
            if ocr['input_sha256'] != item['image_sha256']:
                raise ValueError('OCR image hash mismatch')
            item.update(status='OCR_EXTRACTED_PENDING_COMPARISON', line_count=len(ocr['lines']),
                        ocr_output=str(ocr_path))
            item['alignment_diagnostics'] = validate_alignment(estimate_alignment(candidate['page_words'], ocr, item['render_transform']))
            item['comparison'] = compare_page(candidate, ocr, item, digest, item['alignment_diagnostics'])
            item['header_binding'] = bind_page_headers(candidate, ocr, item, item['alignment_diagnostics'])
            item['header_binding'] = apply_unit_reviews(item['header_binding'], candidate, unit_reviews, digest)
            selected_exchange = exchange_corroboration
            if selected_exchange is None and exchange_corroborations:
                from modules.company_intelligence.quarterly_exchange_match import select_exchange_corroboration
                selected_exchange = select_exchange_corroboration(candidate, exchange_corroborations, ticker=ticker)
            if selected_exchange is not None:
                from modules.company_intelligence.quarterly_exchange_corroboration import apply_exchange_unit_corroboration
                item['header_binding'] = apply_exchange_unit_corroboration(
                    item['header_binding'], candidate, selected_exchange,
                    ticker=ticker, pdf_document_hash=digest)
                if any('exchange_unit_corroboration' in table for table in item['header_binding'].get('tables', [])):
                    report['exchange_corroboration_matches'] += 1
            item['record_candidates'] = build_record_candidates(
                candidate, item, ticker, digest, exchange_corroboration=selected_exchange)
            item['status'] = 'COMPARED_PENDING_REVIEW'
        except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
            item.update(status='OCR_FAILED_HOLD', error=str(exc))
        report['ocr_pages'].append(item)
    if not selected:
        report['reason'] = 'No identifiable main-table header OCR target; scanned/unclassified pages require a separate detection path.'
    (folder / 'intake.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    report['targeted_header_ocr'] = run_header_fallback(report, workspace=workspace)
    # One source request per imported document, not one per metric or column.
    # Persist extraction first so network failure never loses the review work.
    if source_verification_override is not None:
        report['source_verification'] = dict(source_verification_override)
    else:
        try:
            report['source_verification'] = verify_intake_source(original, digest, workspace=workspace,
                output_directory=folder, ticker=ticker, company=company, source_url=source_url)
        except OSError as exc:
            report['source_verification'] = {'status': 'SOURCE_CHECK_STORAGE_FAILED_HOLD',
                'explanation': str(exc), 'creates_approved_facts': False, 'changes_verdict': False}
    report['review_queue'] = (write_quarterly_review_queue(report, output_directory=folder,
                              company=company, source_url=source_url)
                             if company and source_url else {'status': 'HOLD_MISSING_COMPANY_SOURCE_CONTEXT',
                                                            'creates_approved_facts': False})
    (folder / 'intake.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
