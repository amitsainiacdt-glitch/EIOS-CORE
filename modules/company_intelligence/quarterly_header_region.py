"""Targeted local header OCR from a preserved quarterly intake run."""
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
from uuid import uuid4
from modules.company_intelligence.quarterly_header_consensus import reconcile_header_region


def extract_header_regions(run, *, workspace, page_numbers=None):
    import pdfplumber
    from pypdf import PdfReader, PdfWriter
    root = Path(workspace).resolve()
    run = (root / run).resolve()
    if root not in run.parents:
        raise ValueError('Run must be inside workspace')
    intake = json.loads((run / 'intake.json').read_text(encoding='utf-8'))
    source = (run / 'source.pdf').read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != intake['document_hash']:
        raise ValueError('Source PDF hash mismatch')
    layout = json.loads((run / 'layout.json').read_text(encoding='utf-8'))
    folder = run / ('header-ocr-' + uuid4().hex)
    folder.mkdir()
    report = {'document_hash': digest, 'regions': [], 'creates_approved_facts': False,
              'status': 'DIAGNOSTIC_ONLY_PENDING_REVIEW', 'report_path': str(folder / 'report.json')}
    reader = PdfReader(BytesIO(source))
    targets = [p for p in layout['pages'] if p['table_classification']['eligible_for_company_financial_mapping']
               and (page_numbers is None or p['pdf_page'] in page_numbers)][:3]
    for item in targets:
        number = item['pdf_page']
        page = reader.pages[number - 1]
        rotation = page.rotation
        page.rotate(-rotation)
        writer = PdfWriter()
        writer.add_page(page)
        memory = BytesIO()
        writer.write(memory)
        memory.seek(0)
        with pdfplumber.open(memory) as pdf:
            for table_index, table in enumerate(item.get('ruled_tables', [])[:2]):
                bounds = [c['date_header_bbox'] for c in table['columns']]
                if not bounds:
                    continue
                full = pdf.pages[0]
                box = (max(full.bbox[0], min(b[0] for b in bounds) - 12),
                       max(full.bbox[1], table['bbox'][1] - 16),
                       min(full.bbox[2], max(b[2] for b in bounds) + 12),
                       min(full.bbox[3], max(b[3] for b in bounds) + 6))
                crop = full.crop(box)
                dpi = min(450, 2450 * 72 / max(crop.width, crop.height))
                image = folder / f'page-{number}-table-{table_index}.png'
                output = image.with_suffix('.json')
                rendered = crop.to_image(resolution=dpi)
                rendered.save(str(image))
                width, height = rendered.original.size
                image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
                completed = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                    '-File', str(root / 'scripts/extract_windows_ocr.ps1'),
                    '-ImagePath', str(image.relative_to(root)), '-OutputPath', str(output.relative_to(root))],
                    capture_output=True, text=True, timeout=60)
                region = {'document_hash': digest, 'pdf_page': number, 'table_id': table['table_id'], 'crop_bbox': box,
                          'rotation_removed': rotation, 'image_sha256': image_hash, 'resolution_dpi': dpi,
                          'image_width': width, 'image_height': height,
                          'pixels_per_pdf_x': width / crop.width, 'pixels_per_pdf_y': height / crop.height,
                          'image_path': str(image), 'ocr_output': str(output),
                          'status': 'OCR_FAILED_HOLD'}
                if completed.returncode == 0:
                    ocr = json.loads(output.read_text(encoding='utf-8'))
                    if ocr['input_sha256'] != image_hash:
                        raise ValueError('Region OCR hash mismatch')
                    region.update(status='HEADER_OCR_PENDING_SPATIAL_REVIEW',
                                  text_lines=[line['text'] for line in ocr['lines']])
                    receipts = [r for r in intake['ocr_pages'] if r['pdf_page'] == number]
                    if len(receipts) == 1:
                        region['header_comparison'] = reconcile_header_region(item, receipts[0], region, ocr, digest)
                else:
                    region['error'] = completed.stderr[-500:]
                report['regions'].append(region)
    (folder / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
