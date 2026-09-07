"""Read-only comparison of text and rendered pages, not document authentication."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import pdfplumber
from pypdf import PdfReader


def compare(original, downloaded):
    readers = [PdfReader(path) for path in (original, downloaded)]
    counts = [len(reader.pages) for reader in readers]
    if max(counts) > 80:
        raise ValueError('Quarterly comparison limited to 80 pages')
    result = {'original_hash':sha256(Path(original).read_bytes()).hexdigest(),
              'download_hash':sha256(Path(downloaded).read_bytes()).hexdigest(),
              'page_counts':counts, 'pages':[], 'render_dpi':120,
              'creates_approved_facts':False, 'digital_signatures_verified':False,
              'document_authentication_complete':False}
    with pdfplumber.open(original) as first, pdfplumber.open(downloaded) as second:
        for index in range(min(counts)):
            images = [pdf.pages[index].to_image(resolution=120).original.convert('RGB') for pdf in (first,second)]
            image_hashes = [sha256(image.tobytes()).hexdigest() for image in images]
            text = [reader.pages[index].extract_text() or '' for reader in readers]
            result['pages'].append({'page':index+1, 'text_exact_match':text[0]==text[1],
                'render_sizes':[list(image.size) for image in images], 'render_hashes':image_hashes,
                'render_exact_match':images[0].size==images[1].size and image_hashes[0]==image_hashes[1]})
            if index < 2:
                images[1].save(Path(downloaded).parent / f'comparison-page-{index+1}.png')
    result['all_pages_match_at_tested_resolution'] = (counts[0]==counts[1] and counts[0]>0
        and all(page['text_exact_match'] and page['render_exact_match'] for page in result['pages']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', required=True, type=Path)
    parser.add_argument('--downloaded', required=True, type=Path)
    args = parser.parse_args()
    result = compare(args.original, args.downloaded)
    (args.downloaded.parent/'page-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
