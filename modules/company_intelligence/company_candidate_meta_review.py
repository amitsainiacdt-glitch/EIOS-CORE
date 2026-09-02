"""Fail-closed META triage for extracted company fact candidates."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate


MATERIAL_EVENT_TYPES = {
    "ORDER_CONTRACT", "TENDER", "REGULATORY_APPROVAL", "CAPACITY_CHANGE",
    "POLICY_REGULATION", "SUPPLIER_CUSTOMER", "EXECUTION_UPDATE",
    "WEATHER_ANOMALY", "HYDROLOGY", "CROP_PROGRESS", "FERTILIZER_MARKET",
    "FOOD_STOCK_POLICY", "AGRI_PRICE_SUPPLY_CHAIN", "RURAL_DEMAND", "GLOBAL_INPUT_COST",
}
DIRECT_COMPANY_EVENTS = {
    "ORDER_CONTRACT", "REGULATORY_APPROVAL", "CAPACITY_CHANGE",
    "SUPPLIER_CUSTOMER", "EXECUTION_UPDATE",
}


@dataclass(frozen=True)
class CompanyCandidateMetaAssessment:
    schema_version: int
    assessment_id: str
    candidate_id: str
    company: str
    authority_status: str
    relevance_status: str
    materiality_status: str
    causality_status: str
    contradiction_status: str
    verdict_impact: str
    decision: str
    reason_codes: tuple[str, ...]
    uncertainty_statement: str
    reviewed_at: datetime
    creates_evidence: bool = False
    creates_catalyst: bool = False
    changes_verdict: bool = False
    requires_human_review: bool = True
    requires_mandatory_meta: bool = True


class CompanyCandidateMetaReviewEngine:
    """Assess research eligibility without creating investment authority."""

    def assess(self, candidate: CompanyFactReviewCandidate, *, reviewed_at: datetime) -> CompanyCandidateMetaAssessment:
        if not isinstance(candidate, CompanyFactReviewCandidate):
            raise ValueError("candidate must be a CompanyFactReviewCandidate")
        if not isinstance(reviewed_at, datetime):
            raise ValueError("reviewed_at must be a datetime")
        reasons = []

        authority = "VERIFIED_PRIMARY_LINEAGE"
        if not re.fullmatch(r"[0-9a-f]{64}", candidate.document_hash) or not candidate.source_url.startswith("https://"):
            authority = "AUTHORITY_HOLD"
            reasons.append("PRIMARY_LINEAGE_INVALID")
        if candidate.source_url.casefold().split("?", 1)[0].endswith(".pdf") and candidate.pdf_page is None:
            authority = "AUTHORITY_HOLD"
            reasons.append("PDF_PAGE_CITATION_MISSING")

        company_tokens = [token.casefold() for token in candidate.company.split() if len(token) >= 5]
        relevant = any(token in candidate.source_passage.casefold() for token in company_tokens)
        relevance = "DIRECT_COMPANY_REFERENCE" if relevant else "COMPANY_CONTEXT_REVIEW_REQUIRED"
        if not relevant:
            reasons.append("DIRECT_COMPANY_REFERENCE_MISSING")

        material = candidate.event_type in MATERIAL_EVENT_TYPES and bool(
            candidate.explicit_amounts or candidate.explicit_dates or candidate.event_type in DIRECT_COMPANY_EVENTS
        )
        materiality = "MATERIAL_REVIEW_CANDIDATE" if material else "MATERIALITY_HOLD"
        if not material:
            reasons.append("MEASURABLE_MATERIALITY_NOT_ESTABLISHED")

        causality = "DIRECT_EVENT_ONLY_EARNINGS_IMPACT_UNPROVEN" if candidate.event_type in DIRECT_COMPANY_EVENTS else "COMPANY_TRANSMISSION_UNPROVEN"
        reasons.append("EARNINGS_AND_VALUATION_CAUSALITY_UNPROVEN")
        contradiction = "CONTRADICTION_SEARCH_REQUIRED"
        reasons.append("INDEPENDENT_CONTRADICTION_SEARCH_REQUIRED")
        if candidate.statement_posture == "NEGATED":
            reasons.append("NEGATED_STATEMENT_REQUIRES_CONTRADICTION_REVIEW")
        elif candidate.statement_posture == "UNCERTAIN":
            reasons.append("FORWARD_LOOKING_OR_UNCERTAIN_STATEMENT")

        decision = "READY_FOR_HUMAN_REVIEW"
        if authority != "VERIFIED_PRIMARY_LINEAGE" or relevance != "DIRECT_COMPANY_REFERENCE" or not material:
            decision = "HOLD_FOR_RESEARCH"
        assessment_id = sha256(f"{candidate.candidate_id}\n{candidate.document_hash}\nCANDIDATE_META_V1".encode()).hexdigest()
        return CompanyCandidateMetaAssessment(
            1, assessment_id, candidate.candidate_id, candidate.company,
            authority, relevance, materiality, causality, contradiction,
            "BLOCKED_PENDING_HUMAN_AND_MANDATORY_META", decision,
            tuple(dict.fromkeys(reasons)),
            "This assessment validates research eligibility only. Company earnings transmission, expectations, valuation and investment significance remain unproven.",
            reviewed_at,
        )


class CompanyCandidateMetaReviewWriter:
    def write(self, candidates, *, output_path: Path, reviewed_at: datetime):
        assessments = tuple(CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=reviewed_at) for item in candidates)
        payload = {
            "schema_version": 1,
            "reviewed_at": reviewed_at.isoformat(),
            "assessment_count": len(assessments),
            "ready_for_human_review": sum(item.decision == "READY_FOR_HUMAN_REVIEW" for item in assessments),
            "held_for_research": sum(item.decision == "HOLD_FOR_RESEARCH" for item in assessments),
            "assessments": [self._payload(item) for item in assessments],
            "creates_evidence": False,
            "creates_catalyst": False,
            "changes_verdict": False,
            "requires_human_review": True,
            "requires_mandatory_meta": True,
        }
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = output_path.with_suffix(output_path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output_path)
        return assessments

    @staticmethod
    def _payload(item):
        payload = asdict(item)
        payload["reviewed_at"] = item.reviewed_at.isoformat()
        payload["reason_codes"] = list(item.reason_codes)
        return payload


__all__ = ["CompanyCandidateMetaAssessment", "CompanyCandidateMetaReviewEngine", "CompanyCandidateMetaReviewWriter"]
