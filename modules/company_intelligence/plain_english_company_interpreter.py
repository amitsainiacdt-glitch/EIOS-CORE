"""Explain governed company data in plain language without creating conclusions."""

from __future__ import annotations

import re


class PlainEnglishCompanyInterpreter:
    GAP_EXPLANATIONS = {
        "TEN_YEAR_HISTORY_MISSING": ("Ten-year history is missing", "We cannot yet tell whether recent growth is durable or only one strong year."),
        "QUARTERLY_HISTORY_MISSING": ("Quarterly trend is missing", "We cannot see whether sales, margins or working capital are improving or weakening right now."),
        "CASH_FLOW_SERIES_MISSING": ("Cash-flow history is missing", "Reported profit may look good, but we cannot yet judge how consistently that profit becomes cash."),
        "EXPECTATION_BENCHMARK_MISSING": ("Market expectation is unknown", "Without knowing what investors already expect, good news may already be reflected in the share price."),
        "TEN_YEAR_MANAGEMENT_ASSESSMENT_MISSING": ("Management record is incomplete", "We cannot yet compare management promises with actual delivery over a full cycle."),
        "COMPETITOR_COMPARISON_INCOMPLETE": ("Peer comparison is incomplete", "A company can improve while competitors improve faster, so relative strength is still unknown."),
    }

    def build(self, *, extraction: dict | None, intelligence_snapshot: dict | None, discoveries: list[dict]) -> dict:
        facts = extraction.get("facts", []) if extraction else []
        known = [self._fact_explanation(fact) for fact in facts[:8]]
        warnings = []
        seen = set()
        if intelligence_snapshot:
            for layer in intelligence_snapshot.get("layers", {}).values():
                for code in layer.get("warnings", []):
                    if code in self.GAP_EXPLANATIONS and code not in seen:
                        headline, explanation = self.GAP_EXPLANATIONS[code]
                        warnings.append({"headline": headline, "explanation": explanation, "trust_state": "INSUFFICIENT_EVIDENCE", "evidence_ids": []})
                        seen.add(code)
        balance_sheet = {
            "status": "INSUFFICIENT_EVIDENCE",
            "headline": "A reliable balance-sheet red-flag test cannot run yet",
            "explanation": "EIOS still needs a comparable history of debt, receivables, inventory, cash, liabilities and operating cash flow. Missing data is a research gap—not proof that the balance sheet is weak.",
            "checks_required": ["Debt growth versus profit growth", "Receivable days and collection quality", "Inventory build-up", "Operating cash flow versus reported profit", "Short-term obligations versus available liquidity", "Contingent liabilities and related-party exposure"],
        }
        news = [self._news_explanation(item) for item in discoveries[:6]]
        return {
            "knownFacts": known,
            "warningSignals": warnings,
            "balanceSheet": balance_sheet,
            "newsFundamentalMonitor": news,
            "numberComparisons": self._number_comparisons(facts),
            "decisionJourney": self._decision_journey(extraction, intelligence_snapshot, discoveries),
            "createsVerdict": False,
        }

    @staticmethod
    def _decision_journey(extraction, snapshot, discoveries):
        layers = snapshot.get("layers", {}) if snapshot else {}
        def layer(name):
            value = layers.get(name, {})
            return value.get("status", "NOT_STARTED"), value.get("summary", "This analysis has not started.")
        financial_status, financial_summary = layer("financials")
        macro_status, macro_summary = layer("macro")
        sector_status, sector_summary = layer("sector")
        micro_status, micro_summary = layer("micro")
        catalyst_status, catalyst_summary = layer("catalysts")
        expectation_status, expectation_summary = layer("expectations")
        valuation_status, valuation_summary = layer("valuation")
        risk_status, risk_summary = layer("risks_and_contradictions")
        fact_count = len(extraction.get("facts", [])) if extraction else 0
        verdict = snapshot.get("verdict_status", "RESEARCH_HOLD") if snapshot else "RESEARCH_HOLD"
        return [
            {"step": 1, "question": "What is the present decision?", "answer": verdict.replace("_", " "), "meaning": "EIOS has not received enough complete, reviewed evidence to support an investment action.", "decision_effect": "No action is permitted.", "status": verdict},
            {"step": 2, "question": "What do we actually know about the company?", "answer": f"{fact_count} company facts are extracted." if fact_count else "No reviewed company facts are available.", "meaning": "Extracted facts describe what the company reported; they do not automatically prove business quality.", "decision_effect": "Useful starting evidence, not a completed thesis.", "status": "PARTIAL" if fact_count else "INSUFFICIENT_EVIDENCE"},
            {"step": 3, "question": "Are the financials healthy?", "answer": financial_summary, "meaning": "EIOS looks beyond profit to growth quality, margins, debt, working capital and conversion of profit into cash.", "decision_effect": "Financial quality remains unproven until comparable history is complete.", "status": financial_status},
            {"step": 4, "question": "What is happening in the wider economy?", "answer": macro_summary, "meaning": "Macro forces such as rainfall, rates, policy, currencies and input costs can help or hurt a sector, but their company impact must be demonstrated.", "decision_effect": "Macro evidence may guide research; it cannot decide the stock alone.", "status": macro_status},
            {"step": 5, "question": "How is the sector affected?", "answer": sector_summary, "meaning": "EIOS checks demand, supply, pricing, competition and regulation before linking a broad event to one company.", "decision_effect": "Sector transmission is still a research gate.", "status": sector_status},
            {"step": 6, "question": "Does it truly reach this company?", "answer": micro_summary, "meaning": "The company must have relevant products, locations, customers and margins for the macro or sector change to matter.", "decision_effect": "Without this bridge, EIOS will not claim a company benefit or loss.", "status": micro_status},
            {"step": 7, "question": "Is current news changing fundamentals?", "answer": f"{len(discoveries)} news or filing candidates require review." if discoveries else "No current reviewed news candidate is available.", "meaning": "A headline matters only if it changes revenue, margins, cash flow, risk, management credibility or valuation.", "decision_effect": "Fundamental change is not proven from headline sentiment.", "status": "PARTIAL" if discoveries else "UNKNOWN"},
            {"step": 8, "question": "Is there a real catalyst?", "answer": catalyst_summary, "meaning": "A catalyst needs a dated trigger, probable earnings impact and evidence that the market has not already priced it in.", "decision_effect": "No opportunity promotion without a validated catalyst.", "status": catalyst_status},
            {"step": 9, "question": "What does the market already expect?", "answer": expectation_summary, "meaning": "Good business news creates opportunity only when reality may exceed what the current price already assumes.", "decision_effect": "Expectation gap cannot be judged yet.", "status": expectation_status},
            {"step": 10, "question": "Is the valuation attractive?", "answer": valuation_summary, "meaning": "EIOS compares price with business quality, expected cash generation, downside and the growth already implied by the market.", "decision_effect": "Valuation cannot support a decision until price and approved forecasts are available.", "status": valuation_status},
            {"step": 11, "question": "What could prove us wrong?", "answer": risk_summary, "meaning": "Contradictions and kill conditions are required so EIOS can reject its own attractive story.", "decision_effect": "Unresolved risks keep the decision on hold.", "status": risk_status},
        ]

    @staticmethod
    def _fact_explanation(fact: dict) -> dict:
        kind = fact.get("kind", "UNCLASSIFIED")
        statement = fact.get("statement", "No statement available.")
        if kind == "CAPITAL_ALLOCATION":
            meaning = "The company is spending more to expand or strengthen operations. This can support future growth, but only if projects finish on time and earn acceptable returns."
        elif kind == "ISSUER_DISCLOSED_RISK":
            meaning = "Management itself identifies this as a business risk. It deserves monitoring, but disclosure alone does not show that the risk is happening now."
        elif kind == "RISK_MITIGATION":
            meaning = "Management describes protection against a known risk. EIOS still needs evidence that the protection works in practice."
        elif kind == "DATED_MANAGEMENT_COMMITMENT":
            meaning = "This is a management promise with timing. EIOS should later compare the promise with actual delivery."
        elif kind in {"FINANCIAL_RESULT", "SEGMENT_RESULT", "OPERATING_RESULT"}:
            meaning = "This describes reported business performance. One period is useful, but a multi-year trend and cash-flow confirmation are needed before judging quality."
        else:
            meaning = "This is an extracted company statement. Its investment importance has not been established."
        return {"headline": statement, "explanation": meaning, "trust_state": "PROVISIONAL", "evidence_ids": [fact.get("fact_id", "UNKNOWN_FACT")]}

    @staticmethod
    def _number_comparisons(facts):
        by_id = {fact.get("fact_id"): fact for fact in facts}
        def growth(fact_id):
            statement = by_id.get(fact_id, {}).get("statement", "")
            match = re.search(r"(\d+(?:\.\d+)?)%", statement)
            return float(match.group(1)) if match else None
        revenue, ebitda, profit = growth("CORO-FY25-REVENUE"), growth("CORO-FY25-EBITDA"), growth("CORO-FY25-PAT")
        comparisons = []
        if revenue is not None and ebitda is not None and profit is not None:
            comparisons.append({
                "title": "Profit grew faster than sales",
                "figures": [{"label": "Revenue growth", "value": f"{revenue:g}%"}, {"label": "EBITDA growth", "value": f"{ebitda:g}%"}, {"label": "Profit growth", "value": f"{profit:g}%"}],
                "logic": "When operating profit and net profit grow faster than revenue, the business may be receiving some operating leverage or other cost benefit.",
                "impact": "Potentially positive, but one year is not enough. EIOS must verify margins, cash flow and whether the improvement repeats.",
                "status": "PROVISIONAL",
                "evidence_ids": ["CORO-FY25-REVENUE", "CORO-FY25-EBITDA", "CORO-FY25-PAT"],
            })
        capex = growth("CORO-FY25-CAPEX")
        if capex is not None and revenue is not None:
            comparisons.append({
                "title": "Investment spending rose much faster than revenue",
                "figures": [{"label": "Capital expenditure growth", "value": f"{capex:g}%"}, {"label": "Revenue growth", "value": f"{revenue:g}%"}],
                "logic": "Heavy capital spending can create future capacity and lower input dependence, but it also uses cash before the additional earnings arrive.",
                "impact": "Watch execution, project returns and cash generation. This is an opportunity and a risk—not automatically a red flag.",
                "status": "REQUIRES_MONITORING",
                "evidence_ids": ["CORO-FY25-CAPEX", "CORO-FY25-REVENUE"],
            })
        segment = growth("CORO-FY25-CROP-PROTECTION-REVENUE")
        if segment is not None and revenue is not None:
            comparisons.append({
                "title": "Crop Protection grew slower than the overall company",
                "figures": [{"label": "Crop Protection growth", "value": f"{segment:g}%"}, {"label": "Overall revenue growth", "value": f"{revenue:g}%"}],
                "logic": "A segment growing slower than the company can mean the growth mix is being led by other businesses.",
                "impact": "EIOS should check segment margins and volume before deciding whether the mix is improving or weakening.",
                "status": "PROVISIONAL",
                "evidence_ids": ["CORO-FY25-CROP-PROTECTION-REVENUE", "CORO-FY25-REVENUE"],
            })
        return comparisons

    @staticmethod
    def _news_explanation(item):
        headline = item.get("title", "Untitled discovery")
        text = headline.casefold()
        if any(word in text for word in ("order", "contract", "tender")):
            pathway = "Possible path: order book → future execution → revenue → profit and cash collection."
            confirm = "Confirm order value, delivery period, margin, cancellation terms and whether it is additional to existing expectations."
        elif any(word in text for word in ("capacity", "commission", "plant", "expansion")):
            pathway = "Possible path: capital spending → usable capacity → higher volume → revenue; delays or low utilisation can weaken returns."
            confirm = "Confirm commissioning, utilisation, customer demand, project cost, funding and expected return on capital."
        elif any(word in text for word in ("price", "pricing", "raw material", "input cost", "freight")):
            pathway = "Possible path: selling price or input cost change → gross margin → operating profit → cash flow."
            confirm = "Confirm the size, duration, product exposure, pass-through ability and competitor response."
        elif any(word in text for word in ("rain", "monsoon", "crop", "fertilizer")):
            pathway = "Possible path: weather and crop conditions → farmer demand and product mix → company volume and margins."
            confirm = "Prove state, crop and product exposure; compare soil moisture, irrigation, sowing, prices and channel inventory."
        elif any(word in text for word in ("management", "promoter", "director", "governance")):
            pathway = "Possible path: management action → execution quality or capital allocation → long-term cash returns and risk."
            confirm = "Compare the action with prior promises, related-party exposure, incentives and delivery history."
        else:
            pathway = "Possible fundamental pathway is not yet classified from the headline alone."
            confirm = "Read the primary source, identify the affected business driver, quantify the impact and search for contradictions."
        return {
            "headline": headline,
            "plain_english": "This item may matter, but EIOS has not yet proved that it changes revenue, margins, cash flow, risk or valuation.",
            "possible_pathway": pathway,
            "fundamental_status": "FUNDAMENTAL_CHANGE_NOT_PROVEN",
            "what_would_confirm": confirm,
            "source_url": item.get("sourceUrl", ""),
            "review_status": item.get("reviewStatus", "UNKNOWN"),
        }


__all__ = ["PlainEnglishCompanyInterpreter"]
