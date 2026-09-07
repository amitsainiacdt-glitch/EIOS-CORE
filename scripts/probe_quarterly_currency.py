"""Bounded local OCR trial of the upper-right unit area; no approvals."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
from uuid import uuid4


def main():
    import pdfplumber
    from pypdf import PdfReader, PdfWriter
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    run = (root / args.run).resolve()
    if root not in run.parents:
        raise ValueError('Run must be in workspace')
    intake = json.loads((run / 'intake.json').read_text(encoding='utf-8'))
    original = (run / 'source.pdf').read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    if digest != intake['document_hash']:
        raise ValueError('Source hash mismatch')
    layout = json.loads((run / 'layout.json').read_text(encoding='utf-8'))
    pages = [p for p in layout['pages'] if p['table_classification']['eligible_for_company_financial_mapping']]
    if not pages or not pages[0].get('ruled_tables'):
        raise ValueError('No main table available')
    target = pages[0]
    table = target['ruled_tables'][0]
    folder = run / ('unit-probe-' + uuid4().hex)
    folder.mkdir()
    page = PdfReader(BytesIO(original)).pages[target['pdf_page'] - 1]
    page.rotate(-page.rotation)
    writer = PdfWriter()
    writer.add_page(page)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    with pdfplumber.open(buffer) as pdf:
        full = pdf.pages[0]
        left, top, right, _ = table['bbox']
        box = [max(full.bbox[0], right - 120), max(full.bbox[1], top - 18),
               min(full.bbox[2], right + 4), top]
        image = folder / 'unit-region.png'
        rendered = full.crop(box).to_image(resolution=600)
        rendered.save(str(image))
    image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
    report = {'document_hash': digest, 'pdf_page': target['pdf_page'], 'table_id': table['table_id'],
              'crop_bbox': box, 'resolution_dpi': 600, 'image_sha256': image_hash,
              'image_path': str(image), 'readings': [], 'creates_approved_facts': False,
              'status': 'DIAGNOSTIC_ONLY', 'report_path': str(folder / 'report.json')}
    for language in ('en-US', 'en-GB'):
        output = folder / (language + '.json')
        try:
            result = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                '-File', str(root / 'scripts/extract_windows_ocr.ps1'),
                '-ImagePath', str(image.relative_to(root)), '-OutputPath', str(output.relative_to(root)),
                '-Language', language], capture_output=True, text=True, timeout=45)
            if result.returncode:
                raise RuntimeError(result.stderr[-400:])
            ocr = json.loads(output.read_text(encoding='utf-8'))
            if ocr['input_sha256'] != image_hash:
                raise ValueError('OCR image hash mismatch')
            report['readings'].append({'language': language, 'text': [line['text'] for line in ocr['lines']]})
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            report['readings'].append({'language': language, 'error': str(exc)})
    (folder / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
