"""Generate a local review worksheet from existing Coromandel cash-flow sources."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.financial_review_examples import build_cash_flow_review_examples


def main():
    source = ROOT / 'data/company_intelligence/coromandel/coromandel_cash_flow_review.json'
    packet = build_cash_flow_review_examples(json.loads(source.read_text(encoding='utf-8')))
    output = ROOT / 'data/runtime/financial_review_examples.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2) + '\n', encoding='utf-8')
    lines = ['# EIOS: first real financial review examples', '', packet['meaning'], '',
             'All figures are standalone, in INR crore. These are review questions, not investment recommendations.', '']
    for example in reversed(packet['examples']):
        lines.extend([f"## {example['period']}", '', '| Item | Value | Original amount (lakh) | PDF page / column |',
                      '| --- | ---: | --- | --- |'])
        for key, label in [('operating_cash_flow', 'Operating cash'), ('cash_capex', 'Cash fixed-asset purchases')]:
            fact = example['inputs'][key]
            lines.append(f"| {label} | {fact['value']:,.2f} | {fact['raw_value']} | {fact['pdf_page']} / {fact['column']} |")
        fact = example['inputs']['operating_cash_flow']
        lines.extend(['', f"Calculated free cash flow: **INR {example['calculated_free_cash_flow']:,.2f} crore**. {example['meaning']}",
                      '', example['definition'], '', f"[Open source report]({fact['source_url']}#page={fact['pdf_page']})", '',
                      'Review the original PDF before making a decision:', ''])
        lines.extend(f'- {question}' for question in example['review_questions'])
        lines.extend(['', 'Decision: **not recorded**. Do not interpret this worksheet as approval.', ''])
    (ROOT / 'data/runtime/financial_review_examples.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"Prepared {packet['example_count']} real source-linked examples. No reviews or learning decisions recorded.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
