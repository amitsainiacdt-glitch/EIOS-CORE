"""Page-scoped, fail-closed extraction of cash-flow review candidates.

Reconciliation is a numerical check, not META/human approval. These records
must not automatically become governed evidence or investment verdict inputs.
"""
from __future__ import annotations

import re
from decimal import Decimal


NUMBER = r"(?:\(?-?\d[\d,]*(?:\.\d+)?\)?|[-–—])"
PAIR = re.compile(rf"(?<![\w,])({NUMBER})\s+({NUMBER})\s*$")
LABELS = {
    "operating_cash_flow": r"^Net cash.*operating activities",
    "investing_cash_flow": r"^Net cash.*investing activities",
    "financing_cash_flow": r"^Net cash.*financing activities",
    "opening_cash": r"^Cash and cash equivalents at the beginning of the year",
    "closing_cash": r"^Cash and cash equivalents at the end of the year",
    "cash_capex": r"^Purchase of property, plant and equipment",
}
ACQUIRED_CASH = r"^Add:\s*Cash and cash equivalents acquired on account of common control business combination"


def amount(raw: str) -> Decimal:
    if raw in ("-", "–", "—"):
        return Decimal(0)
    value = Decimal(raw.strip("()").replace(",", ""))
    return -value if raw.startswith("(") else value


def extract_period(pages: dict[int, str], *, column: int, period: str,
                   source: dict) -> dict:
    if column not in (0, 1):
        raise ValueError("Only explicitly mapped two-column statements are supported")
    if source.get("column_periods", [None, None])[column] != period:
        raise ValueError("Requested period does not match the mapped source column")
    combined = "\n".join(pages.values())
    if not re.search(r"in\s+lakhs", combined, re.I):
        raise ValueError("Source units must explicitly state lakhs")
    end_year = int(period[2:6]) + 1
    if str(end_year) not in combined:
        raise ValueError(f"Missing statement year {end_year}")
    facts = {}
    for key, label in {**LABELS, "business_combination_cash": ACQUIRED_CASH}.items():
        matches = []
        for page, text in pages.items():
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if not re.search(label, line.strip(), re.I):
                    continue
                passage = line.strip()
                pair = PAIR.search(passage)
                # Cash capital expenditure labels often wrap over 2–3 lines.
                if key in ("cash_capex", "business_combination_cash"):
                    for following in lines[i + 1:i + 4]:
                        if pair:
                            break
                        if re.match(r"^(?:Purchase|Proceeds|Net cash|Cash and cash|Add:|Interest|Dividend)\b", following.strip(), re.I):
                            break
                        passage += " " + following.strip()
                        pair = PAIR.search(passage)
                if pair:
                    raw = pair.group(column + 1)
                    value = amount(raw)
                    if key == "cash_capex":
                        if value > 0:
                            raise ValueError("Purchase cash flow must be an outflow")
                        value = -value
                    matches.append({
                        "value": float(value / 100), "unit": "INR_CRORE",
                        "raw_value": raw, "raw_unit": "INR_LAKH",
                        "pdf_page": page, "column": column + 1,
                        "source_passage": passage, **source,
                    })
        if key == "business_combination_cash" and not matches:
            if re.search(label, combined, re.I | re.M):
                raise ValueError("Business-combination adjustment is present but unreadable")
            continue
        if len(matches) != 1:
            raise ValueError(f"{period}: expected one {key} row, found {len(matches)}")
        facts[key] = matches[0]
    values = {key: Decimal(str(fact["value"])) for key, fact in facts.items()}
    net = sum(values[key] for key in
              ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow"))
    adjustment = values.get("business_combination_cash", Decimal(0))
    residual = values["opening_cash"] + net + adjustment - values["closing_cash"]
    if abs(residual) > Decimal("0.01"):
        raise ValueError(f"{period}: cash bridge does not reconcile ({residual} crore)")
    return {
        "period": period, "basis": "STANDALONE", "facts": facts,
        "derived": {
            "net_cash_change": float(net),
            "free_cash_flow": float(values["operating_cash_flow"] - values["cash_capex"]),
            "free_cash_flow_definition": "Operating cash flow less cash purchases of PPE/intangibles including CWIP and capital advances; excludes separately reported leasehold land and acquisitions.",
        },
        "cash_bridge_residual": float(residual),
        "numerical_check": "RECONCILED", "review_status": "PENDING_META_REVIEW",
        "creates_evidence": False,
    }


def compare_cash_revisions(original: dict, revised: dict) -> dict:
    """Compare two source versions of ONE year without replacing either."""
    if original["period"] != revised["period"] or original["basis"] != revised["basis"]:
        raise ValueError("Revision comparison requires the same period and reporting basis")
    for record in (original, revised):
        f = {k: Decimal(str(v["value"])) for k, v in record["facts"].items()}
        residual = f["opening_cash"] + sum(f[k] for k in
            ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow")) + f.get("business_combination_cash", Decimal(0)) - f["closing_cash"]
        if abs(residual) > Decimal("0.01"):
            raise ValueError("Cannot compare an unreconciled source version")
    keys = (*LABELS, "business_combination_cash")
    deltas = {k: float(Decimal(str(revised["facts"].get(k, {}).get("value", 0))) -
                       Decimal(str(original["facts"].get(k, {}).get("value", 0)))) for k in keys}
    return {"period": original["period"], "deltas_crore": deltas,
            "original": original, "revised": revised,
            "status": "NUMERICALLY_RECONCILED_PENDING_META_REVIEW", "creates_evidence": False}


def continuity_warnings(periods: list[dict]) -> list[dict]:
    warnings = []
    for previous, current in zip(periods, periods[1:]):
        difference = round(current["facts"]["opening_cash"]["value"] -
                           previous["facts"]["closing_cash"]["value"], 2)
        if abs(difference) > 0.01:
            warnings.append({
                "period": current["period"], "difference_crore": difference,
                "meaning": "Opening cash differs from the preceding source's closing cash. Check restatement/business-combination notes before interpreting the cross-report trend.",
            })
    return warnings
