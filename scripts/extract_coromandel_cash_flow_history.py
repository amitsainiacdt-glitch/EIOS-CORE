"""Rebuild a source-linked cash-flow review pack from preserved local PDFs."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.local_cash_flow_extractor import extract_period, continuity_warnings, compare_cash_revisions

# Explicitly chosen standalone statement pages and printed column years.
SOURCES = (
    ("2017_18", (118, 119), (("FY2017-18", 0),)),
    ("2019_20", (77,), (("FY2018-19", 1), ("FY2019-20", 0))),
    ("2020_21", (74,), (("FY2020-21", 0),)),
    ("2021_22", (119,), (("FY2021-22", 0),)),
    ("2023_24", (137,), (("FY2022-23", 1), ("FY2023-24", 0))),
    ("2024_25", (141,), (("FY2024-25", 0),)),
)
REVISION_NOTES = {
    "2021_22": ("FY2020-21", 154, "47 Subsequent events", "48 Other statutory information",
        "Merger restatement", "The FY2021-22 report explicitly restates the prior year after the merger of LPFL and CSQM. The original and revised cash bridges explain the INR14.11 crore change. This is a change of reported basis, not evidence of cash disappearing."),
    "2024_25": ("FY2023-24", 168, "42. During the year", "43. Based on",
        "Accrued-interest reclassification", "Note 42 reclassifies accrued interest from other financial assets into cash, bank balances and loans. The revised FY2023-24 cash figure is INR1.83 crore higher. The note supplies the reporting explanation; the cash-specific allocation is inferred from the source-version comparison, not separately quoted by the note. The company states the reclassification does not affect profit or total equity."),
}


def main():
    directory = ROOT / "data/company_intelligence/coromandel"
    library = json.loads((directory / "coromandel_annual_report_library.json").read_text(encoding="utf-8"))
    reports = {r["financial_year"]: r for r in library["reports"]}
    periods = []
    revised_versions = {}
    notes = {}
    for suffix, page_numbers, columns in SOURCES:
        paths = list((ROOT / "tmp/pdfs").glob(f"*{suffix}.pdf"))
        if len(paths) != 1:
            raise ValueError(f"Expected exactly one preserved PDF for {suffix}")
        path = paths[0]
        reader = PdfReader(path)
        pages = {p: reader.pages[p - 1].extract_text() for p in page_numbers}
        report_year = suffix.replace("_", "-")
        report = reports[report_year]
        source = {
            "document_hash": hashlib.sha256(path.read_bytes()).hexdigest(),
            "local_document": path.relative_to(ROOT).as_posix(),
            "source_url": report["official_url"],
            "url_kind": report["access"], "report_year": report_year,
            "column_periods": [f"FY{report_year}", f"FY{int(suffix[:4]) - 1}-{suffix[2:4]}"],
        }
        for period, column in columns:
            periods.append(extract_period(pages, column=column, period=period, source=source))
        if suffix in REVISION_NOTES:
            period, page, start, end, reason, explanation = REVISION_NOTES[suffix]
            revised_versions[period] = extract_period(pages, column=1, period=period, source=source)
            note_text = reader.pages[page - 1].extract_text()
            if note_text.count(start) != 1 or note_text.count(end) != 1 or note_text.index(end) <= note_text.index(start):
                raise ValueError(f"Missing or ambiguous restatement note in {suffix}")
            notes[period] = {**source, "pdf_page": page,
                "source_passage": note_text.split(start, 1)[1].split(end, 1)[0].strip(),
                "note_heading": start, "reason": reason, "explanation": explanation}
    originals = {p["period"]: p for p in periods}
    revision_reviews = [{**compare_cash_revisions(originals[p], revised), "note": notes[p]}
                        for p, revised in revised_versions.items()]
    warnings = continuity_warnings(periods)
    for warning in warnings:
        previous_year = int(warning["period"][2:6]) - 1
        previous_period = f"FY{previous_year}-{str(previous_year + 1)[-2:]}"
        review = next((r for r in revision_reviews if r["period"] == previous_period), None)
        if review and abs(review["deltas_crore"]["closing_cash"] - warning["difference_crore"]) <= 0.01:
            warning.update({"meaning": review["note"]["explanation"], "reason": review["note"]["reason"],
                            "status": review["status"], "note": review["note"]})
    payload = {
        "schema_version": 1, "company": "Coromandel International",
        "ticker": "COROMANDEL", "periods": periods,
        "source_document_count": len(SOURCES),
        "extracted_fact_count": sum(len(p["facts"]) for p in periods),
        "review_status": "PENDING_META_REVIEW", "creates_evidence": False,
        "continuity_warnings": warnings,
        "revision_reviews": revision_reviews,
        "limitations": [
            "Reconciliation does not constitute META or human approval.",
            "Figures are from explicitly mapped local report pages; source discovery for new companies is not implemented by this script.",
            "Some source URLs resolve to the official archive rather than directly to the preserved PDF.",
            "Cross-report basis differences require review; do not combine with PAT to calculate cash conversion before confirming comparable reporting scope.",
        ],
    }
    output = directory / "coromandel_cash_flow_review.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "periods": len(periods),
                      "facts": payload["extracted_fact_count"],
                      "continuity_warnings": payload["continuity_warnings"]}, indent=2))


if __name__ == "__main__":
    main()
