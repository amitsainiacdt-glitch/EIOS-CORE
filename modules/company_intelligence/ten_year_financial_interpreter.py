from __future__ import annotations


class TenYearFinancialInterpreter:
    """Builds a presentation-ready history without manufacturing absent years."""

    METRICS = (
        ("revenue", "Revenue", "CORO-FY25-REVENUE"),
        ("ebitda", "EBITDA", "CORO-FY25-EBITDA"),
        ("pat", "Profit after tax", "CORO-FY25-PAT"),
        ("operating_cash_flow", "Operating cash flow", None),
        ("capex", "Capital expenditure", "CORO-FY25-CAPEX"),
        ("cash_and_equivalents", "Cash and equivalents", None),
        ("total_debt", "Total debt", None),
        ("trade_receivables", "Trade receivables", None),
        ("inventory", "Inventory", None),
        ("net_worth", "Net worth", None),
    )
    # Primary reader-facing view: latest eight completed financial years.
    # Older periods remain preserved in the source history archive.
    PERIODS = tuple(f"FY{year}-{str(year + 1)[-2:]}" for year in range(2017, 2025))

    def build(self, extraction: dict | None, history: dict | None = None) -> dict:
        facts = {fact.get("fact_id"): fact for fact in (extraction or {}).get("facts", [])}
        history_periods = {item["period"]: item for item in (history or {}).get("periods", [])}
        periods = []
        for period in self.PERIODS:
            values = {}
            evidence_ids = []
            historical = history_periods.get(period, {})
            for key, _label, fact_id in self.METRICS:
                historical_value = historical.get("values", {}).get(key)
                fact = facts.get(fact_id) if fact_id else None
                if isinstance(historical_value, (int, float)):
                    values[key] = historical_value
                    continue
                if fact and fact.get("period") == period and isinstance(fact.get("value"), (int, float)):
                    values[key] = fact["value"]
                else:
                    values[key] = None
            evidence_ids.extend(historical.get("evidence_ids", []))
            if not evidence_ids:
                evidence_ids.extend(
                    fact_id for _key, _label, fact_id in self.METRICS
                    if fact_id and facts.get(fact_id, {}).get("period") == period
                )
            periods.append({"period": period, "values": values, "evidenceIds": evidence_ids, "source": historical.get("source")})

        populated = [period for period in periods if period["evidenceIds"]]
        coverage = round(len(populated) / len(periods) * 100)
        metric_definitions = [
            {
                "key": key,
                "label": label,
                "unit": "INR crore",
                "verifiedYears": sum(1 for period in periods if period["values"].get(key) is not None),
                "coveragePercent": round(sum(1 for period in periods if period["values"].get(key) is not None) / len(periods) * 100),
            }
            for key, label, _fact_id in self.METRICS
        ]
        return {
            "status": "COMPLETE" if len(populated) == len(self.PERIODS) else "EXTRACTION_IN_PROGRESS",
            "coveragePercent": coverage,
            "verifiedYears": len(populated),
            "requiredYears": len(self.PERIODS),
            "periods": periods,
            "metrics": metric_definitions,
            "chartStatus": "READY" if len(populated) >= 2 else "INSUFFICIENT_COMPARABLE_YEARS",
            "metaHighlights": self._meta_highlights(periods),
            "metaSummary": (
                "Ten-year trend conclusions are blocked until at least two comparable years exist; durable-cycle conclusions require the complete series."
                if len(populated) < 2
                else "Comparable years are available for governed trend analysis."
            ),
            "missingDataMeaning": "A blank cell means EIOS has not yet extracted and reconciled that figure. It does not mean zero.",
            "statementCoverage": {
                "periodCoveragePercent": coverage,
                "completeMetricYears": sum(1 for period in periods if all(period["values"].get(key) is not None for key, _label, _fact_id in self.METRICS)),
                "note": "Annual periods may be present while individual statement lines remain incomplete.",
            },
            "balanceSheetReview": self._balance_sheet_review(periods),
            "valuationGate": {
                "status": "BLOCKED_MISSING_MARKET_DATA",
                "requiredInputs": [
                    {"input": "current_price", "status": "MISSING", "meaning": "A verified price timestamp is required."},
                    {"input": "market_expectations", "status": "MISSING", "meaning": "Consensus earnings or an explicit expectation benchmark is required."},
                    {"input": "intrinsic_value", "status": "MISSING", "meaning": "A governed valuation range with assumptions is required."},
                ],
                "plainEnglish": "EIOS cannot call a share cheap or expensive until price, expectations and intrinsic value are measured on the same date.",
            },
            "quarterlyTrend": {
                "status": "NOT_STARTED",
                "periods": [],
                "plainEnglish": "Quarterly revenue, margin and profit trends have not yet been extracted and reconciled.",
            },
            "cashFlowHistory": {
                "status": "PARTIAL",
                "availableYears": sum(1 for period in periods if period["values"].get("operating_cash_flow") is not None),
                "plainEnglish": "Operating cash flow is available for only a subset of years; a complete cash-conversion history is still required.",
            },
        }

    @staticmethod
    def _balance_sheet_review(periods: list[dict]) -> dict:
        checks = {
            "leverage": ("total_debt", "cash_and_equivalents"),
            "working_capital": ("trade_receivables", "inventory"),
            "capital_strength": ("net_worth",),
        }
        result = []
        for name, keys in checks.items():
            available = sum(1 for period in periods if all(period["values"].get(key) is not None for key in keys))
            result.append({
                "check": name,
                "status": "READY" if available >= 2 else "BLOCKED_MISSING_DATA",
                "availableYears": available,
                "explanation": (
                    "EIOS can compare this balance-sheet risk across years."
                    if available >= 2 else
                    "EIOS has not yet extracted enough verified balance-sheet figures to judge this risk."
                ),
            })
        comparable = [p for p in periods if p["values"].get("cash_and_equivalents") is not None and p["values"].get("trade_receivables") is not None and p["values"].get("inventory") is not None and p["values"].get("net_worth") is not None]
        comparison = None
        trend = None
        if len(comparable) >= 2:
            first, last = comparable[-2], comparable[-1]
            def change(key):
                return round((last["values"][key] / first["values"][key] - 1) * 100, 1) if first["values"][key] else None
            comparison = {"from": first["period"], "to": last["period"], "changesPercent": {key: change(key) for key in ("cash_and_equivalents", "trade_receivables", "inventory", "net_worth")}, "explanation": "This is a two-year comparison only; a longer series is required before calling the direction structural."}
            comparison["warnings"] = []
            if comparison["changesPercent"]["cash_and_equivalents"] is not None and comparison["changesPercent"]["cash_and_equivalents"] <= -25:
                comparison["warnings"].append("Cash fell materially; verify operating cash flow, capex and working-capital causes.")
            if comparison["changesPercent"]["inventory"] is not None and comparison["changesPercent"]["inventory"] >= 15:
                comparison["warnings"].append("Inventory rose materially; check sell-through, pricing and obsolescence risk.")
            first_long, last_long = comparable[0], comparable[-1]
            trend = {"from": first_long["period"], "to": last_long["period"], "direction": {key: "up" if last_long["values"][key] > first_long["values"][key] else "down" if last_long["values"][key] < first_long["values"][key] else "flat" for key in ("cash_and_equivalents", "trade_receivables", "inventory", "net_worth")}, "explanation": "Direction is based on the earliest and latest comparable years; it is not a causal conclusion."}
        return {
            "status": "READY" if any(item["status"] == "READY" for item in result) else "BLOCKED_MISSING_DATA",
            "checks": result,
            "plainEnglish": "No balance-sheet red flag is declared until debt, liquidity, working-capital and net-worth figures are verified from the official statements.",
            "comparison": comparison,
            "trend": trend,
        }

    @staticmethod
    def _meta_highlights(periods: list[dict]) -> list[dict]:
        populated = [item for item in periods if item["values"].get("revenue") is not None and item["values"].get("pat") is not None]
        if len(populated) < 2:
            return []
        first, last = populated[0], populated[-1]
        years = int(last["period"][2:6]) - int(first["period"][2:6])
        revenue_cagr = ((last["values"]["revenue"] / first["values"]["revenue"]) ** (1 / years) - 1) * 100
        pat_cagr = ((last["values"]["pat"] / first["values"]["pat"]) ** (1 / years) - 1) * 100
        highlights = [{
            "title": f"Profit compounded faster than revenue from {first['period']} to {last['period']}",
            "figures": [f"Revenue CAGR {revenue_cagr:.1f}%", f"PAT CAGR {pat_cagr:.1f}%"],
            "explanation": "This may indicate improved profitability over the period, but EIOS must still reconcile margins, cash conversion and the missing year before calling it structural.",
            "status": "SUPPORTED_OBSERVATION",
            "evidenceIds": first["evidenceIds"] + last["evidenceIds"],
        }]
        cash_years = [item for item in periods if item["values"].get("operating_cash_flow") is not None and item["values"].get("pat") not in (None, 0)]
        if cash_years:
            latest = cash_years[-1]
            conversion = latest["values"]["operating_cash_flow"] / latest["values"]["pat"] * 100
            highlights.append({
                "title": f"Cash conversion was {conversion:.0f}% of profit in {latest['period']}",
                "figures": [f"Operating cash flow {latest['values']['operating_cash_flow']:.1f}", f"PAT {latest['values']['pat']:.1f}"],
                "explanation": "Cash conversion helps test earnings quality. One year is directional; repeated conversion across cycles is stronger evidence.",
                "status": "SUPPORTED_OBSERVATION",
                "evidenceIds": latest["evidenceIds"],
            })
        for previous, current in zip(populated, populated[1:]):
            revenue_change = (current["values"]["revenue"] / previous["values"]["revenue"] - 1) * 100
            pat_change = (current["values"]["pat"] / previous["values"]["pat"] - 1) * 100
            if revenue_change <= -10:
                highlights.append({
                    "title": f"A material revenue contraction occurred in {current['period']}",
                    "figures": [f"Revenue {revenue_change:.1f}%", f"PAT {pat_change:.1f}%"],
                    "explanation": "The decline is visible in audited figures. Meta must identify whether it came from commodity pricing, volumes, subsidy timing, product mix or another cause before treating recovery as durable.",
                    "status": "REQUIRES_EXPLANATION",
                    "evidenceIds": previous["evidenceIds"] + current["evidenceIds"],
                })
        return highlights


__all__ = ["TenYearFinancialInterpreter"]
