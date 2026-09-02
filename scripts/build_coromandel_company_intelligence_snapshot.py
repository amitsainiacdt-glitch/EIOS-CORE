"""Materialize Coromandel's current backend intelligence coverage for the UI."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.company_intelligence.company_intelligence_snapshot import (
    CompanyIntelligenceSnapshot,
    IntelligenceLayer,
    IntelligenceLayerStatus,
    MANDATORY_VERDICT_LAYERS,
    assess_verdict_readiness,
)
from modules.company_intelligence.discovery_change_classifier import classify_discovery_change


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION_PATH = ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_2024_25_annual_report_extraction.json"
OUTPUT_PATH = ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_company_intelligence_snapshot.json"
FINANCIAL_HISTORY_PATH = ROOT / "data" / "company_intelligence" / "coromandel" / "coromandel_ten_year_financial_history.json"
OBSERVATIONS_PATH = ROOT / "data" / "observations.json"
RUNTIME_STATUS_PATH = ROOT / "data" / "runtime" / "automatic_company_cycle_status.json"


def make_layer(status, summary, *, sources=(), facts=(), warnings=(), coverage=0):
    return IntelligenceLayer(status, summary, tuple(sources), tuple(facts), tuple(warnings), coverage_percent=coverage)


def main() -> None:
    extraction = json.loads(EXTRACTION_PATH.read_text(encoding="utf-8"))
    financial_history = json.loads(FINANCIAL_HISTORY_PATH.read_text(encoding="utf-8")) if FINANCIAL_HISTORY_PATH.exists() else {}
    observations = json.loads(OBSERVATIONS_PATH.read_text(encoding="utf-8")) if OBSERVATIONS_PATH.exists() else []
    company_observations = [
        item for item in observations
        if str(item.get("entity", "")).casefold() == "coromandel international"
    ]
    runtime_status = json.loads(RUNTIME_STATUS_PATH.read_text(encoding="utf-8")) if RUNTIME_STATUS_PATH.exists() else {}
    classified_changes = [classify_discovery_change(item, "Coromandel International") for item in company_observations]
    reviewable_changes = [item for item in classified_changes if item.review_status == "PENDING_HUMAN_REVIEW"]
    observation_source_ids = tuple(
        item.get("provenance", {}).get("observation_fingerprint")
        for item in company_observations
        if item.get("provenance", {}).get("observation_fingerprint")
    )
    intents = {
        str(item.get("provenance", {}).get("research_intent", ""))
        for item in company_observations
    }
    fact_ids = tuple(fact["fact_id"] for fact in extraction["facts"])
    source_id = extraction["source"]["source_id"]

    layers = {
        name: make_layer(IntelligenceLayerStatus.NOT_STARTED, "Backend integration has not started for this layer.")
        for name in MANDATORY_VERDICT_LAYERS
    }
    layers["identity"] = make_layer(
        IntelligenceLayerStatus.READY,
        "Canonical issuer identity is registered.",
        sources=(source_id,),
        coverage=100,
    )
    requested_years = int(financial_history.get("requested_years", 10) or 10)
    periods = financial_history.get("periods", [])
    extracted_periods = [item for item in periods if item.get("values")]
    financial_coverage = round(len(extracted_periods) / requested_years * 100) if requested_years else 0
    financial_warnings = ["QUARTERLY_HISTORY_MISSING", "CASH_FLOW_SERIES_MISSING"]
    if len(extracted_periods) < requested_years:
        financial_warnings.insert(0, "TEN_YEAR_HISTORY_MISSING")
    layers["financials"] = make_layer(
        IntelligenceLayerStatus.READY if financial_coverage >= 100 else IntelligenceLayerStatus.PARTIAL,
        f"{len(extracted_periods)} of {requested_years} requested annual periods have governed financial data; missing values remain explicit.",
        sources=(source_id,),
        facts=fact_ids[:6],
        warnings=tuple(financial_warnings),
        coverage=financial_coverage,
    )
    layers["company_events"] = make_layer(
        IntelligenceLayerStatus.PARTIAL,
        "Two dated capacity and backward-integration commitments were extracted.",
        sources=(source_id,),
        facts=("CORO-KAKINADA-EXPANSION", "CORO-BACKWARD-INTEGRATION-2026"),
        warnings=("EVENT_COMPLETION_NOT_VERIFIED",),
        coverage=20,
    )
    layers["risks_and_contradictions"] = make_layer(
        IntelligenceLayerStatus.PARTIAL,
        "Issuer monsoon risk and mitigation statements were extracted; independent contradiction review is incomplete.",
        sources=(source_id,),
        facts=("CORO-MONSOON-RISK", "CORO-MONSOON-MITIGATION"),
        warnings=("INDEPENDENT_CONTRADICTION_SEARCH_MISSING",),
        coverage=15,
    )
    if "CURRENT_NEWS" in intents or "EXCHANGE_DISCLOSURES" in intents or "OFFICIAL_DOCUMENT_DISCOVERY" in intents:
        layers["news_and_filings"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            f"Automatic intake found {len(company_observations)} company items; META review is required before they become evidence.",
            sources=observation_source_ids,
            warnings=("UNREVIEWED_DISCOVERIES_PRESENT",),
            coverage=25,
        )
    if "MACRO_AND_CAUSAL_TRANSMISSION" in intents:
        layers["macro"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Automatic macro monitoring is connected; company transmission and source authority remain unproven.",
            sources=observation_source_ids,
            warnings=("CAUSAL_TRANSMISSION_NOT_VERIFIED", "PRIMARY_MACRO_SOURCE_REQUIRED"),
            coverage=15,
        )
    if "INDUSTRY_AND_COMPETITIVE" in intents:
        layers["sector"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Sector and competitive monitoring is collecting candidates; independent sector evidence remains incomplete.",
            sources=observation_source_ids,
            warnings=("SECTOR_EVIDENCE_REVIEW_REQUIRED",),
            coverage=15,
        )
        layers["competition"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Competitive-change candidates are being monitored but have not passed comparative validation.",
            sources=observation_source_ids,
            warnings=("COMPETITOR_COMPARISON_INCOMPLETE",),
            coverage=10,
        )
    if "MANAGEMENT_AND_CORPORATE" in intents:
        layers["management"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Management and corporate-event monitoring is connected; long-term promise-versus-delivery analysis remains incomplete.",
            sources=observation_source_ids,
            warnings=("TEN_YEAR_MANAGEMENT_ASSESSMENT_MISSING",),
            coverage=10,
        )
    if "CATALYST_AND_EXPECTATION_GAP" in intents:
        layers["catalysts"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Catalyst candidates are collected, but no dated catalyst with verified earnings transmission is approved.",
            sources=observation_source_ids,
            warnings=("CATALYST_NOT_VALIDATED",),
            coverage=10,
        )
        layers["expectations"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Expectation-gap monitoring is connected; market expectations and a measurable surprise threshold are not established.",
            sources=observation_source_ids,
            warnings=("EXPECTATION_BENCHMARK_MISSING",),
            coverage=10,
        )
    if classified_changes:
        layers["meta_causality"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            f"META triaged {len(classified_changes)} discoveries: {len(reviewable_changes)} await human review; none can change the verdict automatically.",
            sources=observation_source_ids,
            warnings=("HUMAN_REVIEW_REQUIRED", "VERDICT_IMPACT_BLOCKED"),
            coverage=20,
        )
    layers["master_dossier"] = make_layer(
        IntelligenceLayerStatus.RESEARCH_HOLD,
        "Master Dossier cannot advance until mandatory intelligence layers are ready.",
        warnings=("MANDATORY_INPUT_LAYERS_INCOMPLETE",),
        coverage=5,
    )
    if runtime_status.get("status") == "SUCCESS" and company_observations:
        layers["monitoring"] = make_layer(
            IntelligenceLayerStatus.READY,
            f"Automatic monitoring is active. The latest cycle executed {runtime_status.get('executed_jobs', 0)} jobs and preserved {len(company_observations)} Coromandel discoveries.",
            sources=observation_source_ids,
            coverage=100,
        )
    else:
        layers["monitoring"] = make_layer(
            IntelligenceLayerStatus.PARTIAL,
            "Official source locations are registered, but a successful automatic collection cycle is not yet verified.",
            sources=(source_id,),
            warnings=("AUTOMATIC_CYCLE_NOT_VERIFIED",),
            coverage=25,
        )

    verdict_status, gaps = assess_verdict_readiness(layers)
    snapshot = CompanyIntelligenceSnapshot(
        schema_version=1,
        snapshot_id="COROMANDEL-COMPANY-INTELLIGENCE-2026-08-31",
        company_name="Coromandel International",
        ticker="COROMANDEL",
        generated_at=datetime.now(timezone.utc),
        layers=layers,
        verdict_status=verdict_status,
        verdict=None,
        confidence_percent=None,
        verdict_reasons=("No verdict is permitted until all mandatory backend layers are ready.",),
        unresolved_gaps=gaps,
        creates_recommendation=False,
        requires_human_review=True,
    )
    OUTPUT_PATH.write_text(json.dumps(snapshot.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Snapshot written: {snapshot.snapshot_id} | {snapshot.verdict_status} | {len(gaps)} unresolved layers")


if __name__ == "__main__":
    main()
