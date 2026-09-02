"""Extract mapped balance-sheet pages without granting evidence approval."""
import re
from decimal import Decimal
from modules.company_intelligence.local_cash_flow_extractor import PAIR, amount

FIELDS = {
    "total_assets": "Total assets", "total_equity": "Total equity",
    "total_liabilities": "Total liabilities", "total_equity_liabilities": "Total equity and liabilities",
    "property_plant_equipment": "Property, plant and equipment", "capital_work_in_progress": "Capital work-in-progress",
    "inventory": "Inventories", "trade_receivables": "Trade receivables",
    "subsidies_receivable": "Government subsidies receivable", "cash_equivalents": "Cash and cash equivalents",
    "other_bank_balances": "Bank balances other than cash and cash equivalents",
}
SECTIONS = {
    "non_current_assets": ("1 Non-current assets", "2 Current assets"),
    "current_assets": ("2 Current assets", "Total assets"),
    "non_current_liabilities": ("2 Non-current liabilities", "3 Current liabilities"),
    "current_liabilities": ("3 Current liabilities", "Total liabilities"),
}


def extract_balance_sheet(text: str, *, period: str, column: int, source: dict) -> dict:
    if column not in (0, 1) or source.get("column_periods", [None, None])[column] != period:
        raise ValueError("Period/column mapping mismatch")
    if not re.search(r"in\s+lakhs", text, re.I) or str(int(period[2:6]) + 1) not in text:
        raise ValueError("Missing units or year")
    # Isolate only the balance sheet, even on a two-page spread containing P&L.
    start = text.find("1 Non-current assets")
    end = text.find("Total equity and liabilities", start)
    if start < 0 or end < 0:
        raise ValueError("Balance sheet boundaries missing")
    text = text[start:end] + text[end:].splitlines()[0]
    facts = {}

    def fact(raw, passage):
        return {**source, "raw_value": raw, "raw_unit": "INR_LAKH", "unit": "INR_CRORE",
                "value": float(amount(raw) / 100), "source_passage": passage, "column": column + 1}

    def find_row(label, body):
        # Labels may wrap, but cannot consume a subsequent numbered row.
        pattern = r"(?m)^\s*(?:\([a-z]\)|[ivx]+\))?\s*" + r"\s+".join(map(re.escape, label.split())) + r"(?=\s|$)"
        found = []
        for match in re.finditer(pattern, body):
            suffix = body[match.end():].lstrip().splitlines()[0]
            pair = PAIR.search(suffix)
            if pair and not re.search(r"[A-Za-z]", suffix[:pair.start()]):
                found.append(fact(pair.group(column + 1), (match.group() + suffix).strip()))
        if len(found) > 1:
            raise ValueError(f"Ambiguous row: {label}")
        return found[0] if found else None

    def find_wrapped_row(label, body):
        pattern = r"(?m)^\s*(?:\([a-z]\)|[ivx]+\))?\s*" + r"\s+".join(map(re.escape, label.split())) + r"(?=\s|$)"
        found = []
        for match in re.finditer(pattern, body):
            passage = match.group().strip()
            for line in body[match.end():].splitlines()[:4]:
                if re.match(r"^\s*(?:\([a-z]\)|[ivx]+\))\s+[A-Za-z]", line, re.I):
                    break
                passage += " " + line.strip()
                pair = PAIR.search(passage)
                if pair:
                    found.append(fact(pair.group(column + 1), passage)); break
        if len(found) > 1:
            raise ValueError(f"Ambiguous wrapped row: {label}")
        return found[0] if found else None

    for key, label in FIELDS.items():
        facts[key] = find_row(label, text)
        if facts[key] is None:
            raise ValueError(f"Missing required row: {label}")
    sections = {}
    for key, (first, last) in SECTIONS.items():
        if text.count(first) != 1 or text.count(last) != 1:
            raise ValueError(f"Ambiguous section: {key}")
        body = text.split(first, 1)[1].split(last, 1)[0]
        sections[key] = body
        last_line = body.strip().splitlines()[-1].strip()
        pair = PAIR.fullmatch(last_line)
        if not pair:
            raise ValueError(f"Missing section subtotal: {key}")
        facts[key] = fact(pair.group(column + 1), f"{first} subtotal: {last_line}")
    for section in ("non_current_liabilities", "current_liabilities"):
        for key, label in (("borrowings", "Borrowings"), ("lease_liabilities", "Lease liabilities")):
            facts[f"{section}_{key}"] = find_row(label, sections[section])
        for key, label in (("provisions", "Provisions"), ("other_financial_liabilities", "Other financial liabilities"),
                           ("other_liabilities", "Other non-current liabilities" if section.startswith("non_") else "Other current liabilities")):
            facts[f"{section}_{key}"] = find_row(label, sections[section])
    current = sections["current_liabilities"]
    facts["trade_payables_msme"] = find_row("Total outstanding dues of micro enterprises and small enterprises", current)
    facts["trade_payables_other"] = find_wrapped_row("Total outstanding dues of creditors other than micro enterprises and", current)
    if facts["trade_payables_msme"] and facts["trade_payables_other"]:
        total = facts["trade_payables_msme"]["value"] + facts["trade_payables_other"]["value"]
        facts["trade_payables_total"] = {**facts["trade_payables_other"], "value": round(total, 2),
            "raw_value": None, "source_passage": "Calculated: MSME payables plus other trade payables",
            "calculation": "trade_payables_msme + trade_payables_other"}
    else:
        facts["trade_payables_total"] = find_row("Trade payables", current)

    value = lambda k: Decimal(str(facts[k]["value"]))
    checks = {
        "assets_equal_equity_plus_liabilities": value("total_assets") - value("total_equity") - value("total_liabilities"),
        "asset_subtotals": value("total_assets") - value("current_assets") - value("non_current_assets"),
        "liability_subtotals": value("total_liabilities") - value("current_liabilities") - value("non_current_liabilities"),
        "reported_grand_totals": value("total_assets") - value("total_equity_liabilities"),
    }
    if any(abs(v) > Decimal("0.01") for v in checks.values()):
        raise ValueError(f"Balance sheet does not reconcile: {checks}")
    return {"period": period, "basis": "STANDALONE", "facts": facts,
            "checks_residual_crore": {k: float(v) for k, v in checks.items()},
            "review_status": "PENDING_META_REVIEW", "creates_evidence": False,
            "missing_meaning": "Not separately reported/extracted; an absent borrowing or lease row is not asserted to be zero."}
