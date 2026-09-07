"""Build the local dashboard snapshot from governed EIOS research artifacts."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.company_intelligence.discovery_change_classifier import classify_discovery_change
from modules.company_intelligence.plain_english_company_interpreter import PlainEnglishCompanyInterpreter
from modules.company_intelligence.ten_year_financial_interpreter import TenYearFinancialInterpreter
from modules.company_intelligence.financial_display import add_display_cells
from modules.company_intelligence.operating_earnings_review import validate_earnings_review
from modules.company_intelligence.quarterly_review_display import load_quarterly_review_display


ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "data" / "live_cases" / "india_kharif_2026" / "structured"
READINESS_PATH = CASE_DIR / "india_kharif_2026_pre_inflection_readiness.json"
QUEUE_PATH = CASE_DIR / "india_kharif_2026_evidence_queue.json"
OBSERVATIONS_PATH = ROOT / "data" / "observations.json"
COMPANY_SOURCE_MANIFEST_PATH = ROOT / "data" / "company_intelligence" / "company_source_manifest.json"
FACT_REVIEW_QUEUE_ROOT = ROOT / "data" / "company_intelligence" / "fact_review_queue"
FACT_HUMAN_REVIEW_LEDGER_PATH = ROOT / "data" / "company_intelligence" / "company_fact_human_reviews.jsonl"
GOVERNED_FACT_REPOSITORY_PATH = ROOT / "data" / "company_intelligence" / "governed_company_facts.jsonl"
COMPANY_EXTRACTION_PATHS = {
    "COROMANDEL": ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_2024_25_annual_report_extraction.json",
}
ANNUAL_REPORT_LIBRARY_PATHS = {
    "COROMANDEL": ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_annual_report_library.json",
}
ANNUAL_REPORT_STUDY_PATHS = {
    "COROMANDEL": ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_annual_report_study.json",
}
COMPANY_INTELLIGENCE_SNAPSHOT_PATHS = {
    "COROMANDEL": ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_company_intelligence_snapshot.json",
}
TEN_YEAR_FINANCIAL_HISTORY_PATHS = {
    "COROMANDEL": ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_ten_year_financial_history.json",
}
OUTPUT_PATH = ROOT / "local_status_dashboard" / "lib" / "live-status.json"
RUNTIME_STATUS_PATH = ROOT / "data" / "runtime" / "automatic_company_cycle_status.json"


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_json_lines(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_review_inbox(ticker: str) -> dict:
    reviews = {item["candidate_id"]: item for item in read_json_lines(FACT_HUMAN_REVIEW_LEDGER_PATH)}
    governed = {item["candidate_id"]: item for item in read_json_lines(GOVERNED_FACT_REPOSITORY_PATH)}
    items = []
    ticker_root = FACT_REVIEW_QUEUE_ROOT / ticker.upper()
    if ticker_root.is_dir():
        for queue_path in sorted(ticker_root.glob("*.json"), reverse=True):
            if queue_path.name.endswith(".meta.json"):
                continue
            queue_payload = read_json(queue_path)
            meta_path = queue_path.with_suffix(".meta.json")
            meta_payload = read_json(meta_path) if meta_path.is_file() else {}
            assessments = {item["candidate_id"]: item for item in meta_payload.get("assessments", [])}
            for candidate in queue_payload.get("candidates", []):
                candidate_id = candidate["candidate_id"]
                meta = assessments.get(candidate_id)
                human_review = reviews.get(candidate_id)
                governed_fact = governed.get(candidate_id)
                review_status = (
                    "GOVERNED_FACT" if governed_fact else
                    human_review.get("decision") if human_review else
                    meta.get("decision") if meta else
                    candidate.get("review_status", "PENDING_META_REVIEW")
                )
                items.append({
                    "candidateId": candidate_id,
                    "queuePath": queue_path.relative_to(ROOT).as_posix(),
                    "metaPath": meta_path.relative_to(ROOT).as_posix(),
                    "eventType": candidate.get("event_type", "UNCLASSIFIED"),
                    "statementPosture": candidate.get("statement_posture", "UNKNOWN"),
                    "sourcePassage": candidate.get("source_passage", ""),
                    "explicitAmounts": candidate.get("explicit_amounts", []),
                    "explicitDates": candidate.get("explicit_dates", []),
                    "pdfPage": candidate.get("pdf_page"),
                    "sourceUrl": candidate.get("source_url", ""),
                    "reviewStatus": review_status,
                    "meta": ({
                        "decision": meta["decision"],
                        "authorityStatus": meta["authority_status"],
                        "relevanceStatus": meta["relevance_status"],
                        "materialityStatus": meta["materiality_status"],
                        "causalityStatus": meta["causality_status"],
                        "contradictionStatus": meta["contradiction_status"],
                        "verdictImpact": meta["verdict_impact"],
                        "reasonCodes": meta.get("reason_codes", []),
                        "uncertaintyStatement": meta["uncertainty_statement"],
                    } if meta else None),
                })
    return {
        "total": len(items),
        "ready": sum(item["reviewStatus"] == "READY_FOR_HUMAN_REVIEW" for item in items),
        "held": sum(item["reviewStatus"] in {"HOLD", "HOLD_FOR_RESEARCH"} for item in items),
        "approved": sum(item["reviewStatus"] in {"APPROVE", "GOVERNED_FACT"} for item in items),
        "items": items,
    }


def main() -> None:
    readiness = read_json(READINESS_PATH)
    queue = read_json(QUEUE_PATH)
    observations = read_json(OBSERVATIONS_PATH)
    company_source_manifest = read_json(COMPANY_SOURCE_MANIFEST_PATH)
    runtime_status = read_json(RUNTIME_STATUS_PATH) if RUNTIME_STATUS_PATH.is_file() else {
        "status": "UNKNOWN", "job_count": None, "executed_jobs": None,
        "observations": None, "errors": ["Runtime status file is unavailable."],
    }

    assessment = readiness["assessment"]
    confidence = readiness["causal_interpretation_confidence_ceiling"]
    queue_items = queue.get("items", [])
    eligible_items = [item for item in queue_items if item.get("eligible_now")]

    company_aliases = {
        "The Anup Engineering Limited": {"ticker": "ANUP", "sector": "Industrial Engineering"},
        "Tata Motors": {"ticker": "TATAMOTORS", "sector": "Automobiles"},
        "KPIT Technologies": {"ticker": "KPITTECH", "sector": "Automotive Software"},
        "Coromandel International": {"ticker": "COROMANDEL", "sector": "Fertilizers & Agri Inputs"},
    }
    grouped_observations = defaultdict(list)
    for observation in observations:
        entity = observation.get("entity")
        if entity in company_aliases:
            grouped_observations[entity].append(observation)

    companies = []
    for entity, identity in company_aliases.items():
        evidence = grouped_observations.get(entity, [])
        source_record = company_source_manifest["companies"].get(identity["ticker"], {})
        official_sources = source_record.get("sources", [])
        extraction_path = COMPANY_EXTRACTION_PATHS.get(identity["ticker"])
        extraction = read_json(extraction_path) if extraction_path and extraction_path.is_file() else None
        annual_report_path = ANNUAL_REPORT_LIBRARY_PATHS.get(identity["ticker"])
        annual_report_library = read_json(annual_report_path) if annual_report_path and annual_report_path.is_file() else None
        annual_report_study_path = ANNUAL_REPORT_STUDY_PATHS.get(identity["ticker"])
        annual_report_study = read_json(annual_report_study_path) if annual_report_study_path and annual_report_study_path.is_file() else None
        intelligence_snapshot_path = COMPANY_INTELLIGENCE_SNAPSHOT_PATHS.get(identity["ticker"])
        intelligence_snapshot = read_json(intelligence_snapshot_path) if intelligence_snapshot_path and intelligence_snapshot_path.is_file() else None
        financial_history_path = TEN_YEAR_FINANCIAL_HISTORY_PATHS.get(identity["ticker"])
        financial_history = read_json(financial_history_path) if financial_history_path and financial_history_path.is_file() else None
        cash_review_path = financial_history_path.with_name("coromandel_cash_flow_review.json") if financial_history_path else None
        cash_review = read_json(cash_review_path) if cash_review_path and cash_review_path.is_file() else None
        balance_review_path = financial_history_path.with_name("coromandel_balance_sheet_review.json") if financial_history_path else None
        balance_review = read_json(balance_review_path) if balance_review_path and balance_review_path.is_file() else None
        earnings_path = financial_history_path.with_name("coromandel_operating_earnings_review.json") if financial_history_path else None
        earnings_review = validate_earnings_review(read_json(earnings_path)) if earnings_path and earnings_path.is_file() else None
        review_inbox = load_review_inbox(identity["ticker"])
        ordered = sorted(evidence, key=lambda item: item.get("timestamp", ""), reverse=True)
        discovery_changes = [classify_discovery_change(item, entity) for item in ordered]
        recent_discoveries = [
            {
                "title": change.title,
                "sourceUrl": change.source_url,
                "discoveredAt": change.discovered_at,
                "researchIntent": change.research_intent,
                "sourceQualityTier": change.source_quality_tier,
                "reviewStatus": change.review_status,
                "verdictImpact": change.verdict_impact,
            }
            for change in discovery_changes[:8]
        ]
        confidence_values = [
            float(item["confidence"])
            for item in evidence
            if isinstance(item.get("confidence"), (int, float)) and not isinstance(item.get("confidence"), bool)
        ]
        companies.append({
            "name": entity,
            "ticker": identity["ticker"],
            "sector": identity["sector"],
            "evidenceCount": len(evidence),
            "averageEvidenceConfidence": round(sum(confidence_values) / len(confidence_values), 1) if confidence_values else None,
            "latestEvidenceAt": ordered[0].get("timestamp") if ordered else None,
            "recentEvidence": [
                {
                    "title": item.get("title", "Untitled observation"),
                    "category": item.get("category", "Unclassified"),
                    "confidence": item.get("confidence"),
                }
                for item in ordered[:3]
            ],
            "recentDiscoveries": recent_discoveries,
            "plainEnglishAnalysis": PlainEnglishCompanyInterpreter().build(
                extraction=extraction,
                intelligence_snapshot=intelligence_snapshot,
                discoveries=recent_discoveries,
            ),
            "tenYearFinancials": {**add_display_cells(TenYearFinancialInterpreter().build(extraction, financial_history), cash_review, balance_review), "cashFlowReview": cash_review, "balanceSheetReviewData": balance_review, "operatingEarningsReview": earnings_review},
            "reviewInbox": review_inbox,
            "quarterlyReview": load_quarterly_review_display(ROOT, identity["ticker"]),
            "officialSourceCount": len(official_sources),
            "officialSourceTypes": sorted({item["source_type"] for item in official_sources}),
            "sourceDiscoveryStatus": "DISCOVERED_NOT_EXTRACTED" if official_sources else "NOT_STARTED",
            "extractedFactCount": len(extraction.get("facts", [])) if extraction else 0,
            "extractedFacts": [
                {
                    "factId": fact["fact_id"],
                    "kind": fact["kind"],
                    "statement": fact["statement"],
                    "period": fact.get("period"),
                    "sourcePage": fact.get("printed_pages"),
                }
                for fact in extraction.get("facts", [])
            ] if extraction else [],
            "extractionStatus": extraction.get("status") if extraction else "NOT_STARTED",
            "sourceProvenance": ({
                "sourceId": extraction["source"]["source_id"],
                "documentTitle": extraction["source"]["document_title"],
                "publisher": entity,
                "officialUrl": extraction["source"]["issuer_url"],
                "reportingPeriodEnd": extraction["source"]["reporting_period_end"],
                "documentHash": extraction["source"]["sha256"],
                "authority": extraction["source"]["authority"],
                "extractionId": extraction["extraction_id"],
                "extractionMethod": "PAGE_AWARE_STRUCTURED_EXTRACTION",
            } if extraction else None),
            "annualReportArchiveUrl": annual_report_library.get("official_archive_url") if annual_report_library else None,
            "annualReportGovernanceNote": annual_report_library.get("governance_note") if annual_report_library else None,
            "annualReports": [
                {
                    "financialYear": report["financial_year"],
                    "title": report["title"],
                    "officialUrl": report["official_url"],
                    "access": report["access"],
                    "status": report["status"],
                    "extractedFactCount": report["extracted_fact_count"],
                    "highlights": report.get("highlights", []),
                }
                for report in annual_report_library.get("reports", [])
            ] if annual_report_library else [],
            "annualReportStudy": {
                "status": annual_report_study["status"],
                "extractionCoveragePercent": annual_report_study["extraction_coverage_percent"],
                "availableYears": annual_report_study["available_years"],
                "extractedYears": annual_report_study["extracted_years"],
                "reviewedYears": annual_report_study["reviewed_years"],
                "metaStatus": annual_report_study["meta_status"],
                "metaPermittedConclusion": annual_report_study["meta_permitted_conclusion"],
                "verdictStatus": annual_report_study["verdict_status"],
                "findings": [
                    {
                        "findingId": finding["finding_id"],
                        "category": finding["category"],
                        "headline": finding["headline"],
                        "interpretation": finding["interpretation"],
                        "confidencePercent": finding["confidence_percent"],
                        "status": finding["status"],
                    }
                    for finding in annual_report_study["findings"]
                ],
                "missingWork": annual_report_study["missing_work"],
            } if annual_report_study else None,
            "intelligenceSnapshot": {
                "generatedAt": intelligence_snapshot["generated_at"],
                "verdictStatus": intelligence_snapshot["verdict_status"],
                "verdict": intelligence_snapshot.get("verdict"),
                "confidencePercent": intelligence_snapshot.get("confidence_percent"),
                "verdictReasons": intelligence_snapshot["verdict_reasons"],
                "unresolvedGaps": intelligence_snapshot["unresolved_gaps"],
                "requiresHumanReview": intelligence_snapshot["requires_human_review"],
                "layers": [
                    {
                        "name": name,
                        "status": layer["status"],
                        "summary": layer["summary"],
                        "coveragePercent": layer["coverage_percent"],
                    }
                    for name, layer in intelligence_snapshot["layers"].items()
                ],
                "longTerm": {
                    "status": intelligence_snapshot["layers"]["master_dossier"]["status"],
                    "permittedConclusion": "Ten-year business quality, management delivery, cash-flow durability, competitive advantage and valuation are not yet complete.",
                    "coveragePercent": round(sum(
                        intelligence_snapshot["layers"][name]["coverage_percent"]
                        for name in ("financials", "management", "competition", "risks_and_contradictions", "valuation", "master_dossier")
                    ) / 6),
                },
                "alpha": {
                    "status": "WEAK_SIGNAL_RESEARCH",
                    "permittedConclusion": annual_report_study["meta_permitted_conclusion"] if annual_report_study else "Alpha analysis has not started.",
                    "coveragePercent": round(sum(
                        intelligence_snapshot["layers"][name]["coverage_percent"]
                        for name in ("macro", "sector", "micro", "news_and_filings", "company_events", "meta_causality", "catalysts", "expectations")
                    ) / 8),
                },
                "news": {
                    "status": intelligence_snapshot["layers"]["news_and_filings"]["status"],
                    "items": [
                        {
                            "title": item.get("title", "Untitled discovery"),
                            "sourceUrl": item.get("source") or item.get("provenance", {}).get("source_url"),
                            "discoveredAt": item.get("timestamp"),
                            "researchIntent": item.get("provenance", {}).get("research_intent", "UNCLASSIFIED"),
                        }
                        for item in ordered
                        if item.get("provenance", {}).get("research_intent") in {
                            "CURRENT_NEWS", "EXCHANGE_DISCLOSURES", "OFFICIAL_DOCUMENT_DISCOVERY"
                        }
                    ][:8],
                    "statement": (
                        f"Automatic intake is connected and has preserved {len(evidence)} company discoveries. "
                        "They remain review candidates and cannot influence the verdict until META and human review approve them."
                    )
                },
            } if intelligence_snapshot else None,
            "researchLink": extraction.get("research_links", {}).get("india_kharif_2026") if extraction else None,
            "companyBridgeReady": False,
            "datedCatalystReady": False,
            "readiness": "EVIDENCE_ONLY" if evidence else ("EXTRACTED_PENDING_REVIEW" if extraction else ("SOURCES_DISCOVERED" if official_sources else "REGISTERED_ONLY")),
            "readinessLabel": "Evidence found — company case not yet proven" if evidence else ("Facts extracted — human review pending" if extraction else ("Official sources found — extraction pending" if official_sources else "Registered — governed evidence not yet attached")),
        })

    snapshot = {
        "caseId": readiness["inputs"]["case_id"],
        "stage": assessment["stage"],
        "permittedClaim": assessment["permitted_claim"],
        "confidenceCeilingPercent": confidence["maximum_confidence_percent"],
        "confidenceEligible": confidence["confidence_eligible"],
        "unresolvedGaps": readiness["inputs"]["unresolved_gaps"],
        "nextEvidencePriorities": assessment["next_evidence_priorities"],
        "queue": {
            "totalItems": len(queue_items),
            "eligibleNow": len(eligible_items),
            "waiting": len(queue_items) - len(eligible_items),
            "automaticExternalActions": queue["automatic_external_actions"],
        },
        "productionObservationCount": len(observations),
        "companies": companies,
        "generatedAt": queue["generated_at"],
        "requiresHumanReview": readiness["requires_human_review"],
        "createsObservation": readiness["creates_observation"],
        "nonAuthorityStatement": readiness["non_authority_statement"],
        "runtime": {
            "status": runtime_status.get("status", "UNKNOWN"),
            "startedAt": runtime_status.get("started_at"),
            "finishedAt": runtime_status.get("finished_at"),
            "jobCount": runtime_status.get("job_count"),
            "executedJobs": runtime_status.get("executed_jobs"),
            "observationCount": runtime_status.get("observations"),
            "errors": runtime_status.get("errors", []),
            "collectionOutcome": runtime_status.get("collection_outcome", {}),
        },
    }

    eligible_companies = [
        company for company in companies
        if (company.get("intelligenceSnapshot") or {}).get("verdictStatus") == "READY"
    ]
    research_candidates = [company for company in companies if company not in eligible_companies]
    snapshot["opportunityWatch"] = {
        "eligibilityRule": "Only companies with a READY governed intelligence verdict may enter Eligible Opportunities.",
        "eligibleTickers": [company["ticker"] for company in eligible_companies],
        "eligibleCount": len(eligible_companies),
        "researchCandidateTickers": [company["ticker"] for company in research_candidates],
        "researchCandidateCount": len(research_candidates),
    }
    snapshot["homeStatus"] = {
        "runtimeStatus": runtime_status.get("status", "UNKNOWN"),
        "earlyIntelligenceCaseCount": 1 if assessment.get("stage") else None,
        "confirmedOpportunityCount": len(eligible_companies),
        "deteriorationAlertCount": None,
        "deteriorationAlertState": "UNKNOWN_NOT_COMPUTED",
        "reviewReadyFactCount": sum(company["reviewInbox"]["ready"] for company in companies),
        "companySnapshotCount": sum(company["intelligenceSnapshot"] is not None for company in companies),
    }
    snapshot["governedBrief"] = {
        "status": "SNAPSHOT_SUMMARY_NOT_CIO_SYNTHESIS",
        "headline": "The strongest governed case concerns weather and crop conditions, not a proven company opportunity.",
        "summary": "Coromandel currently has the deepest company snapshot, while ten-year financials, company transmission, expectations and valuation remain incomplete.",
        "researchPriority": assessment["next_evidence_priorities"][0] if assessment.get("next_evidence_priorities") else "No governed research priority is available.",
        "sourceReferences": [readiness["inputs"]["case_id"], *[company["ticker"] for company in companies if company["intelligenceSnapshot"]]],
        "changesVerdict": False,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(
        f"Dashboard snapshot updated: {snapshot['caseId']} | "
        f"{snapshot['stage']} | {snapshot['productionObservationCount']} observations"
    )


if __name__ == "__main__":
    main()
