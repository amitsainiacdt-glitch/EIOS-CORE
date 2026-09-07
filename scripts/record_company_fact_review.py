"""Record one explicit human company-fact decision and optionally materialize it."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaAssessment
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate
from modules.company_intelligence.governed_company_fact import GovernedCompanyFactRepository
from modules.company_intelligence.governed_fact_engine_router import GovernedFactEngineRouter
from modules.company_intelligence.engine_analysis_intake import EngineAnalysisIntakeRepository
from modules.company_intelligence.initial_engine_consumers import InitialEngineAnalysisRepository
from modules.company_intelligence.quarterly_publication_gate import quarterly_approval_assessment
from modules.company_intelligence.governed_quarterly_financial import GovernedQuarterlyFinancialRepository


ROOT = Path(__file__).resolve().parents[1]


def inside_workspace(value: str) -> Path:
    path = (ROOT / value).resolve()
    if ROOT.resolve() not in path.parents:
        raise ValueError("paths must remain inside the EIOS workspace")
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Record an explicit human decision for one META-reviewed company fact candidate.")
    for name in ("queue", "meta", "candidate-id", "review-id", "decision", "rationale", "reviewer"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--approved-confidence", type=float)
    parser.add_argument("--review-ledger", default="data/company_intelligence/company_fact_human_reviews.jsonl")
    parser.add_argument("--fact-repository", default="data/company_intelligence/governed_company_facts.jsonl")
    parser.add_argument("--engine-route-ledger", default="data/company_intelligence/governed_fact_engine_routes.jsonl")
    parser.add_argument("--engine-intake-ledger", default="data/company_intelligence/engine_analysis_intake.jsonl")
    parser.add_argument("--initial-engine-results", default="data/company_intelligence/initial_engine_analysis_results.jsonl")
    parser.add_argument("--quarterly-note-review-ledger", default="data/company_intelligence/quarterly_note_human_reviews.jsonl")
    parser.add_argument("--quarterly-financial-repository", default="data/company_intelligence/governed_quarterly_financials.jsonl")
    args = parser.parse_args(argv)
    queue, meta_payload = json.loads(inside_workspace(args.queue).read_text(encoding="utf-8")), json.loads(inside_workspace(args.meta).read_text(encoding="utf-8"))
    candidate_payload = next((item for item in queue["candidates"] if item["candidate_id"] == args.candidate_id), None)
    assessment_payload = next((item for item in meta_payload["assessments"] if item["candidate_id"] == args.candidate_id), None)
    if candidate_payload is None or assessment_payload is None:
        raise ValueError("candidate must exist in both queue and META assessment")
    candidate_payload["explicit_amounts"] = tuple(candidate_payload["explicit_amounts"])
    candidate_payload["explicit_dates"] = tuple(candidate_payload["explicit_dates"])
    candidate = CompanyFactReviewCandidate(**candidate_payload)
    assessment_payload["reason_codes"] = tuple(assessment_payload["reason_codes"])
    assessment_payload["reviewed_at"] = datetime.fromisoformat(assessment_payload["reviewed_at"])
    meta = CompanyCandidateMetaAssessment(**assessment_payload)
    now = datetime.now(timezone.utc)
    quarterly_assessment = None
    if args.decision == 'APPROVE':
        quarterly_assessment = quarterly_approval_assessment(candidate, queue, inside_workspace(args.quarterly_note_review_ledger))
    review = CompanyFactHumanReviewLedger(inside_workspace(args.review_ledger)).record(
        candidate, meta, review_id=args.review_id, decision=args.decision,
        approved_confidence=args.approved_confidence, rationale=args.rationale,
        reviewed_at=now, reviewer=args.reviewer,
    )
    print(f"Human review recorded: {review.review_id} | {review.decision.value}")
    if review.decision.value == "APPROVE":
        fact = GovernedCompanyFactRepository(inside_workspace(args.fact_repository)).materialize(
            candidate, meta, review, created_at=now,
        )
        print(f"Governed fact created: {fact.fact_id}")
        if quarterly_assessment is not None:
            quarterly = GovernedQuarterlyFinancialRepository(inside_workspace(args.quarterly_financial_repository)).materialize(
                candidate, fact, queue['quarterly_record_evidence'][candidate.candidate_id], quarterly_assessment, created_at=now)
            print(f"Governed quarterly financial record created: {quarterly.record_id}")
        route = GovernedFactEngineRouter(inside_workspace(args.engine_route_ledger)).route(fact, routed_at=now)
        print(f"Fact routed to {len(route.target_analysis_queues)} governed analysis queues: {route.route_id}")
        work = EngineAnalysisIntakeRepository(inside_workspace(args.engine_intake_ledger)).dispatch(fact, route, created_at=now)
        print(f"Engine intake created: {len(work)} traceable work items")
        results = InitialEngineAnalysisRepository(inside_workspace(args.initial_engine_results)).consume_available(fact, work, completed_at=now)
        print(f"Initial governed engine results created: {len(results)}")
    print("No Evidence, Catalyst, verdict, recommendation or trade was created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
