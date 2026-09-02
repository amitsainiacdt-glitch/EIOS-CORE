"""Build the current, strictly governed Coromandel annual-report study."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.company_intelligence.annual_report_study import AnnualReportStudy, StudyFinding, StudyStatus


ROOT = Path(__file__).resolve().parents[1]
COMPANY_DIR = ROOT / "data" / "company_intelligence" / "coromandel"
LIBRARY_PATH = COMPANY_DIR / "coromandel_annual_report_library.json"
EXTRACTION_PATH = COMPANY_DIR / "coromandel_2024_25_annual_report_extraction.json"
OUTPUT_PATH = COMPANY_DIR / "coromandel_annual_report_study.json"
HISTORY_PATH = COMPANY_DIR / "coromandel_ten_year_financial_history.json"


def main() -> None:
    library = json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))
    extraction = json.loads(EXTRACTION_PATH.read_text(encoding="utf-8"))
    history = json.loads(HISTORY_PATH.read_text(encoding="utf-8")) if HISTORY_PATH.exists() else {}
    facts = {fact["fact_id"]: fact for fact in extraction["facts"]}

    revenue = facts["CORO-FY25-REVENUE"]["value"]
    ebitda = facts["CORO-FY25-EBITDA"]["value"]
    pat = facts["CORO-FY25-PAT"]["value"]
    capex = facts["CORO-FY25-CAPEX"]["value"]
    crop_protection = facts["CORO-FY25-CROP-PROTECTION-REVENUE"]["value"]

    findings = (
        StudyFinding(
            "CORO-STUDY-FY25-GROWTH",
            "FINANCIAL_MOMENTUM",
            "Profit grew faster than revenue in FY2024-25",
            "Reported revenue grew 9%, EBITDA about 11%, and PAT about 13%. This is a positive one-year operating signal, but it is not yet a durable trend.",
            ("CORO-FY25-REVENUE", "CORO-FY25-EBITDA", "CORO-FY25-PAT"),
            85,
        ),
        StudyFinding(
            "CORO-STUDY-FY25-MARGINS",
            "UNIT_ECONOMICS",
            f"FY2024-25 EBITDA margin was {ebitda / revenue * 100:.1f}%",
            f"PAT margin was {pat / revenue * 100:.1f}%. EIOS needs the preceding nine years to distinguish structural improvement from a favourable cycle.",
            ("CORO-FY25-REVENUE", "CORO-FY25-EBITDA", "CORO-FY25-PAT"),
            90,
        ),
        StudyFinding(
            "CORO-STUDY-FY25-INVESTMENT",
            "CAPITAL_ALLOCATION",
            f"Capex equalled {capex / revenue * 100:.1f}% of revenue",
            "The investment is directed toward backward integration and capacity expansion. Returns and commissioning progress must be monitored before treating it as a catalyst.",
            ("CORO-FY25-CAPEX", "CORO-KAKINADA-EXPANSION", "CORO-BACKWARD-INTEGRATION-2026"),
            80,
        ),
        StudyFinding(
            "CORO-STUDY-FY25-DIVERSIFICATION",
            "BUSINESS_MIX",
            f"Crop Protection and bioproducts were {crop_protection / revenue * 100:.1f}% of standalone revenue",
            "This supplies a measurable diversification reference point; ten-year segment history is required to establish whether mix is strengthening.",
            ("CORO-FY25-CROP-PROTECTION-REVENUE", "CORO-FY25-REVENUE"),
            80,
        ),
        StudyFinding(
            "CORO-STUDY-MONSOON-EXPOSURE",
            "RISK_TRANSMISSION",
            "Monsoon conditions can transmit into turnover and profitability",
            "The issuer explicitly acknowledges the exposure and describes mitigation, but does not quantify current sensitivity by state, crop, product, revenue or margin.",
            ("CORO-MONSOON-RISK", "CORO-MONSOON-MITIGATION"),
            75,
        ),
    )

    reports = library["reports"]
    extracted_years = sum(1 for period in history.get("periods", []) if period.get("values"))
    extracted_years = max(extracted_years, sum(1 for report in reports if report["status"].startswith("EXTRACTED")))
    reviewed_years = sum(1 for report in reports if report["status"] == "HUMAN_REVIEWED")
    study = AnnualReportStudy(
        schema_version=1,
        company=library["company"],
        ticker=library["ticker"],
        requested_years=len(reports),
        available_years=len(reports),
        extracted_years=extracted_years,
        reviewed_years=reviewed_years,
        status=StudyStatus.PARTIAL,
        findings=findings,
        missing_work=(
            "Extract and reconcile the preceding nine annual reports.",
            "Build ten-year income statement, balance sheet and cash-flow series.",
            "Compare management commitments with subsequent delivery.",
            "Run cross-year contradiction, risk recurrence and segment-mix analysis.",
            "Complete human review before findings can influence a verdict.",
        ),
        meta_status="INSUFFICIENT_LONGITUDINAL_HISTORY",
        meta_permitted_conclusion="FY2024-25 shows positive one-year momentum and identifiable expansion and monsoon channels; persistence, causality and valuation implications remain unproven.",
    )
    OUTPUT_PATH.write_text(json.dumps(study.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Annual-report study written: {study.ticker} | {study.extraction_coverage_percent}% extracted | {study.verdict_status}")


if __name__ == "__main__":
    main()
