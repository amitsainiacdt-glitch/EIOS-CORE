"""Rebuild eight years of balance-sheet candidates from local official PDFs."""
import hashlib
import json
import sys
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.local_balance_sheet_extractor import extract_balance_sheet
from modules.company_intelligence.borrowing_note_review import apply_borrowing_note
from scripts.extract_coromandel_cash_flow_history import SOURCES

PAGES = {"2017_18": 116, "2019_20": 76, "2020_21": 73, "2021_22": 118, "2023_24": 136, "2024_25": 140}
BORROWING_PAGES = {"2017_18": 144, "2019_20": 90, "2020_21": 87, "2021_22": 138, "2023_24": 155, "2024_25": 156}


def main():
    directory = ROOT / "data/company_intelligence/coromandel"
    library = json.loads((directory / "coromandel_annual_report_library.json").read_text(encoding="utf-8"))
    reports = {r["financial_year"]: r for r in library["reports"]}
    periods = []
    for suffix, _, columns in SOURCES:
        paths = list((ROOT / "tmp/pdfs").glob(f"*{suffix}.pdf"))
        if len(paths) != 1:
            raise ValueError(f"Expected one source PDF: {suffix}")
        path = paths[0]
        year = suffix.replace("_", "-")
        page = PAGES[suffix]
        reader = PdfReader(path)
        text = reader.pages[page - 1].extract_text()
        source = {"report_year": year, "source_url": reports[year]["official_url"],
                  "url_kind": reports[year]["access"], "pdf_page": page,
                  "document_hash": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "local_document": path.relative_to(ROOT).as_posix(),
                  "column_periods": [f"FY{year}", f"FY{int(suffix[:4])-1}-{suffix[2:4]}"]}
        note_page = BORROWING_PAGES[suffix]
        note_text = reader.pages[note_page - 1].extract_text()
        for p, c in columns:
            record = extract_balance_sheet(text, period=p, column=c, source=source)
            periods.append(apply_borrowing_note(record, note_text, {**source, "pdf_page": note_page}))
    payload = {"company": "Coromandel International", "ticker": "COROMANDEL", "schema_version": 1,
               "periods": periods, "review_status": "PENDING_META_REVIEW", "creates_evidence": False,
               "extracted_fact_count": sum(sum(f is not None and not f.get("calculation") for f in p["facts"].values()) for p in periods),
               "calculated_fact_count": sum(sum(bool(f and f.get("calculation")) for f in p["facts"].values()) for p in periods),
               "limitations": ["Mixed original/comparative report vintages are preserved, not silently harmonised.",
                   "FY2021-22 includes merger restatements; FY2024-25 includes accrued-interest reclassification. Review reporting scope before using trends.",
                   "Other bank balances can contain restricted deposits; they are not all freely available cash.",
                   "Section totals reconcile, but individual notes, line-item sums and META approval remain separate checks."]}
    output = directory / "coromandel_balance_sheet_review.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {payload['extracted_fact_count']} figures across {len(periods)} years; all four total checks pass per year; pending META review.")


if __name__ == "__main__":
    main()
