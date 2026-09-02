"""Bind borrowing totals to explicit note disclosures, not missing-row inference."""
import re
from decimal import Decimal
from modules.company_intelligence.local_cash_flow_extractor import PAIR, amount


def apply_borrowing_note(record, text, source):
    column = source["column_periods"].index(record["period"])
    if not re.search(r"in\s+lakhs", text, re.I):
        raise ValueError("Borrowing note units missing")
    start = re.search(r"18\.\s+Borrowings", text)
    if not start:
        raise ValueError("Borrowing note heading missing")
    note = text[start.start():]
    stop = re.search(r"19\.\s+Other financial liabilities", note)
    if stop:
        note = note[:stop.start()]

    def row(label):
        lines = [line for line in note.splitlines() if re.match(r"\s*" + label + r"\s", line)]
        if len(lines) > 1:
            raise ValueError("Ambiguous borrowing row")
        if not lines:
            return None
        pair = PAIR.search(lines[0])
        if not pair:
            raise ValueError("Unreadable borrowing row")
        return amount(pair.group(column + 1)), lines[0], pair.group(column + 1)

    short = row("Short term borrowings")
    long = row("Long term borrowings")
    if long is None:
        year = str(int(record["period"][2:6]) + 1)
        matches = [s for s in note.splitlines() if "There are no outstanding long-term borrowings" in s and year in s]
        if len(matches) != 1:
            raise ValueError("No explicit long-term borrowing disclosure for year")
        long = (Decimal(0), matches[0], "Nil (explicit narrative disclosure)")
    if short is None:
        raise ValueError("Short-term borrowing total missing")
    balance = record["facts"]["current_liabilities_borrowings"]
    if balance is None or Decimal(str(balance["value"])) != short[0] / 100:
        raise ValueError("Borrowing note disagrees with balance sheet")
    def fact(value, passage, raw):
        return {**source, "value": float(value / 100), "unit": "INR_CRORE", "raw_unit": "INR_LAKH",
                "raw_value": raw, "source_passage": passage, "column": column + 1}
    record["facts"]["non_current_liabilities_borrowings"] = fact(*long)
    record["facts"]["total_borrowings_ex_leases"] = {
        **fact(short[0] + long[0], short[1] + "\n" + long[1], None),
        "calculation": "Short-term plus long-term borrowings; excludes lease liabilities, trade payables and other liabilities.",
    }
    return record
