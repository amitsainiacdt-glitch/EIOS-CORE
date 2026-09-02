"""Presentation-only missing-cell support. Never feeds the analysis engine."""
from copy import deepcopy
import math

MAPPING = {
    "total_debt": ("balance", "total_borrowings_ex_leases", "balance-sheet-history"),
    "operating_cash_flow": ("cash", "operating_cash_flow", "cash-flow-history"),
    "cash_and_equivalents": ("balance", "cash_equivalents", "balance-sheet-history"),
    "trade_receivables": ("balance", "trade_receivables", "balance-sheet-history"),
    "inventory": ("balance", "inventory", "balance-sheet-history"),
    "net_worth": ("balance", "total_equity", "balance-sheet-history"),
}
REASONS = {
    "total_debt": "Total debt not established. Current borrowings and lease liabilities are shown separately in the balance-sheet table.",
    "capex": "Comparable accounting capex not extracted. Cash fixed-asset purchases are available separately in the cash-flow table.",
    "ebitda": "Comparable EBITDA has not yet been extracted or reconciled for this year.",
}


def add_display_cells(history, cash=None, balance=None):
    result = deepcopy(history)
    if balance:
        for metric in result.get("metrics", []):
            if metric["key"] == "total_debt":
                metric["label"] = "Borrowings (excluding leases)"
    sources = {name: {p["period"]: p for p in (pack or {}).get("periods", [])}
               for name, pack in (("cash", cash), ("balance", balance))}
    for period in result["periods"]:
        cells = {}
        for key, value in period["values"].items():
            cell = {"value": value, "status": "EXISTING_HISTORY" if value is not None else "MISSING",
                    "reason": "Existing financial history; see its evidence references." if value is not None else REASONS.get(key, "Not yet extracted and reconciled."),
                    "source": None, "section": None}
            if value is None and key in MAPPING:
                pack, source_key, section = MAPPING[key]
                row = sources[pack].get(period["period"], {})
                fact = row.get("facts", {}).get(source_key)
                if (row.get("basis") == "STANDALONE" and row.get("review_status") == "PENDING_META_REVIEW"
                    and fact and type(fact.get("value")) in (int, float) and math.isfinite(fact["value"])
                    and fact.get("unit") == "INR_CRORE" and fact.get("document_hash") and fact.get("pdf_page")):
                    cell.update(value=fact["value"], status="PENDING_META_REVIEW", source=fact, section=section,
                                reason="Extracted from a preserved report; pending META review. Display only, not an approved verdict input.")
            cells[key] = cell
        period["displayCells"] = cells
    result["displayNote"] = "Amber figures fill display gaps from source-linked review records only. Original analysis inputs are unchanged. Missing is not zero."
    return result
