"""Strict exchange iXBRL corroboration candidates; never approves company facts."""

from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re


class _Rows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self._row, self._cell, self._in_cell = [], None, None, False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "tr":
            self._row = []
        elif tag.lower() in {"th", "td"} and self._row is not None:
            self._cell, self._in_cell = [], True

    def handle_data(self, data):
        if self._in_cell:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag.lower() in {"th", "td"} and self._in_cell:
            self._row.append(_clean(" ".join(self._cell)))
            self._cell, self._in_cell = None, False
        elif tag.lower() == "tr" and self._row is not None:
            if any(self._row):
                self.rows.append(self._row)
            self._row = None


def _clean(value):
    return re.sub(r"\s+", " ", value or "").strip()


def _unique_field(rows, label):
    values = []
    for row in rows:
        positions = [i for i, value in enumerate(row) if _clean(value).casefold() == label.casefold()]
        for position in positions:
            values.extend(value for value in row[position + 1:] if value)
    distinct = list(dict.fromkeys(values))
    if len(distinct) != 1:
        raise ValueError(f"iXBRL field is missing or conflicting: {label}")
    return distinct[0]


def _amount(raw):
    text = _clean(raw)
    negative = text.startswith("(") and text.endswith(")")
    token = text[1:-1] if negative else text
    if not re.fullmatch(r"\d+(?:,\d{2,3})*(?:\.\d+)?", token):
        return None
    try:
        value = Decimal(token.replace(",", ""))
    except InvalidOperation:
        return None
    return -value if negative else value


def parse_exchange_ixbrl_financial(html, *, source_url, document_hash):
    if not isinstance(html, str) or not html.strip():
        raise ValueError("iXBRL HTML is required")
    if not re.fullmatch(r"[a-f0-9]{64}", document_hash or ""):
        raise ValueError("source SHA-256 is required")
    host = (urlsplit(source_url).hostname or "").casefold()
    if host != "nsearchives.nseindia.com":
        raise ValueError("only the official NSE archive is accepted")
    parser = _Rows()
    parser.feed(html)
    rows = parser.rows
    metadata = {
        "ticker": _unique_field(rows, "NSE Symbol"),
        "isin": _unique_field(rows, "ISIN"),
        "company": _unique_field(rows, "Name of company"),
        "currency": _unique_field(rows, "Description of presentation currency"),
        "rounding": _unique_field(rows, "Level of rounding used in financial results"),
        "reporting_type": _unique_field(rows, "Reporting Type"),
        "reporting_quarter": _unique_field(rows, "Reporting Quarter"),
        "basis": _unique_field(rows, "Nature of report standalone or consolidated"),
        "period_start": _unique_field(rows, "Date of start of reporting period"),
        "period_end": _unique_field(rows, "Date of end of reporting period"),
    }
    if metadata["currency"].upper() != "INR" or metadata["rounding"].casefold() not in {"lakh", "lakhs"}:
        raise ValueError("unsupported or conflicting iXBRL currency unit")
    metric_labels = {
        "revenue": "Revenue from operations",
        "other_income": "Other income",
        "total_income": "Total income",
        "raw_materials": "Cost of materials consumed",
        "total_expenses": "Total expenses",
        "profit_before_tax": "Total profit before tax",
        "pat": "Total profit (loss) for period",
    }
    metrics = {}
    for metric, label in metric_labels.items():
        candidates = []
        for row in rows:
            positions = [i for i, value in enumerate(row) if _clean(value).casefold() == label.casefold()]
            for position in positions:
                values = [_amount(value) for value in row[position + 1:]]
                values = [value for value in values if value is not None]
                if values:
                    candidates.append(values)
        unique = []
        for values in candidates:
            signature = tuple(values)
            if signature not in [tuple(item) for item in unique]:
                unique.append(values)
        if len(unique) != 1:
            raise ValueError(f"iXBRL metric is missing or conflicting: {label}")
        metrics[metric] = [str(value) for value in unique[0]]
    return {
        "schema_version": 1,
        "source_url": source_url,
        "document_hash": document_hash,
        "source_authority": "NSE_OFFICIAL_IXBRL",
        "metadata": metadata,
        "values_inr_lakh": metrics,
        "status": "EXCHANGE_CORROBORATION_CANDIDATE",
        "creates_approved_facts": False,
        "requires_meta_review": True,
        "requires_human_review": True,
    }


__all__ = ["parse_exchange_ixbrl_financial"]
