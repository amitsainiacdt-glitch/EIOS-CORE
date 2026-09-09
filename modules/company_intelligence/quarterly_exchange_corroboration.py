"""Bind an official exchange unit only when filing identity and period agree."""

import copy
from datetime import datetime

from modules.company_intelligence.quarterly_date_comparison import parse_date_cell
from modules.company_intelligence.quarterly_shared_headers import resolve_shared_headers


def apply_exchange_unit_corroboration(binding, page, report, *, ticker, pdf_document_hash):
    result = copy.deepcopy(binding)
    if not isinstance(report, dict) or report.get("status") != "EXCHANGE_CORROBORATION_CANDIDATE":
        return result
    metadata = report.get("metadata", {})
    if (metadata.get("ticker", "").upper() != ticker.upper()
            or metadata.get("currency", "").upper() != "INR"
            or metadata.get("rounding", "").casefold() not in {"lakh", "lakhs"}):
        return result
    try:
        period_end = datetime.strptime(metadata["period_end"], "%d-%m-%Y").date().isoformat()
    except (KeyError, TypeError, ValueError):
        return result
    context = page.get("statement_context", {})
    title_date = parse_date_cell(context.get("current_quarter_end_text"))
    basis = context.get("basis_candidates", [])
    if basis != [metadata.get("basis", "").upper()]:
        return result
    if title_date.get("date") and title_date["date"] != period_end:
        return result
    for table in result.get("tables", []):
        prior = table.get("unit_assessment", {})
        if "FOREIGN_OR_CONFLICTING_CURRENCY" in prior.get("issues", []):
            continue
        if prior.get("unit_candidates") not in ([], ["lakh"]):
            continue
        if any(span.get("kind") == "unit" for span in table.get("spans", [])):
            continue
        source_table = next((item for item in page.get("ruled_tables", [])
                             if item.get("table_id") == table.get("table_id")), None)
        if not source_table or not source_table.get("columns"):
            continue
        period_columns = [column for column in source_table["columns"]
                          if parse_date_cell(column.get("date_header_text")).get("date") == period_end]
        if len(period_columns) != 1:
            continue
        period_index = period_columns[0]["column_index"]
        source_binding = {"document_hash": pdf_document_hash, "pdf_page": page["pdf_page"],
                          "table_id": table["table_id"]}
        duration_spans = [span for span in table.get("spans", []) if span.get("kind") == "duration"
                          and span["first_column"] <= period_index <= span["last_column"]]
        if not duration_spans:
            table["spans"].append({**source_binding, "kind": "duration", "text": "Quarter ended",
                "first_column": period_index, "last_column": period_index,
                "status": "NSE_IXBRL_PERIOD_MATCH_PENDING_REVIEW",
                "exchange_document_hash": report["document_hash"], "exchange_source_url": report["source_url"]})
        table["spans"].append({**source_binding, "kind": "unit", "text": "INR lakh",
            "first_column": 0, "last_column": len(source_table["columns"]) - 1,
            "status": "NSE_IXBRL_CORROBORATED_PENDING_REVIEW",
            "exchange_document_hash": report["document_hash"], "exchange_source_url": report["source_url"]})
        table["exchange_unit_corroboration"] = {
            "status": "IDENTITY_BASIS_TABLE_PERIOD_UNIT_AGREE_PENDING_REVIEW",
            "exchange_document_hash": report["document_hash"], "exchange_source_url": report["source_url"],
            "creates_approved_facts": False,
        }
        for column in table["columns"]:
            source_column = next(item for item in source_table["columns"]
                                 if item["column_index"] == column["column_index"])
            dates = column.get("date_comparison", {})
            resolved = resolve_shared_headers({**source_binding, **source_column,
                "date_header_text": dates.get("native", {}).get("date") or source_column["date_header_text"]},
                table["spans"])
            if dates.get("status") != "DATE_READINGS_AGREE_PENDING_REVIEW":
                resolved = {**resolved, "status": "HOLD",
                            "issues": [*resolved.get("issues", []), "DATE_REVIEW_REQUIRED"]}
            column["resolution"] = resolved
    return result


__all__ = ["apply_exchange_unit_corroboration"]
