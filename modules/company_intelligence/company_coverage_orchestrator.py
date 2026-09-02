"""Generate deterministic monitoring work for every governed EIOS company."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import urlparse

from modules.external_intelligence.research_job import ResearchJob


@dataclass(frozen=True)
class CompanyCoverageProfile:
    company_id: str
    name: str
    ticker: str
    exchange: str
    sector: str
    issuer_investor_url: str
    enabled: bool = True

    def __post_init__(self) -> None:
        required = (self.company_id, self.name, self.ticker, self.exchange, self.sector, self.issuer_investor_url)
        if any(not value.strip() for value in required):
            raise ValueError("company coverage identity fields must not be empty")
        if not self.issuer_investor_url.startswith("https://"):
            raise ValueError("issuer_investor_url must be an HTTPS issuer source")


@dataclass(frozen=True)
class CompanyCoveragePlan:
    schema_version: int
    profile: CompanyCoverageProfile
    jobs: tuple[ResearchJob, ...]
    preservation_policy: str
    extraction_policy: str
    review_policy: str

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["jobs"] = [asdict(job) for job in self.jobs]
        return payload


JOB_TEMPLATES = (
    ("OFFICIAL-DOCUMENTS", "OFFICIAL_DOCUMENT_DISCOVERY", 1440, 100, "Check the issuer site and exchange for new annual reports, quarterly results, presentations and transcripts"),
    ("EXCHANGE-DISCLOSURES", "EXCHANGE_DISCLOSURES", 360, 100, "Check official exchange disclosures for material company announcements"),
    ("ORDERS-CAPACITY", "ORDER_AND_CAPACITY", 720, 95, "Check for orders, tenders, contracts, capacity changes and project commissioning"),
    ("MANAGEMENT-CORPORATE", "MANAGEMENT_AND_CORPORATE", 1440, 90, "Check management changes, promoter actions, capital allocation and corporate events"),
    ("NEWS", "CURRENT_NEWS", 360, 85, "Check current company news and retain only source-grounded material developments"),
    ("SECTOR-COMPETITION", "INDUSTRY_AND_COMPETITIVE", 1440, 80, "Check sector, competitor, regulation, technology and market-share developments"),
    ("MACRO-TRANSMISSION", "MACRO_AND_CAUSAL_TRANSMISSION", 1440, 75, "Check macro, policy, commodity, weather and supply-chain variables with a plausible company transmission channel"),
    ("CATALYST-EXPECTATIONS", "CATALYST_AND_EXPECTATION_GAP", 720, 90, "Check dated catalysts, expectation changes, disconfirming evidence and kill switches"),
)


def build_company_coverage_plan(profile: CompanyCoverageProfile) -> CompanyCoveragePlan:
    """Create the standard monitoring plan without company-specific business logic."""
    jobs = []
    entity_domain = urlparse(profile.issuer_investor_url).hostname
    if not entity_domain:
        raise ValueError("issuer_investor_url must contain a domain")
    for suffix, intent, frequency, priority, question in JOB_TEMPLATES:
        job = ResearchJob(
            job_id=f"{profile.ticker.upper()}-{suffix}",
            company=profile.name,
            ticker=profile.ticker.upper(),
            question=question,
            intent=intent,
            frequency_minutes=frequency,
            enabled=profile.enabled,
            priority=priority,
            max_sources=10 if intent in {"OFFICIAL_DOCUMENT_DISCOVERY", "EXCHANGE_DISCLOSURES"} else 5,
            observation_category="Governed Company Intake",
            observation_confidence=70.0,
            entity_domain=entity_domain,
        )
        job.validate()
        jobs.append(job)
    return CompanyCoveragePlan(
        schema_version=1,
        profile=profile,
        jobs=tuple(jobs),
        preservation_policy="Store immutable source bytes by SHA-256 and retain version, issuer URL, retrieval time and document identity.",
        extraction_policy="Extract into typed staging records; never overwrite an earlier extraction and never create evidence automatically.",
        review_policy="Material facts, signals, catalysts and verdict changes require governed validation and human approval.",
    )


__all__ = ["CompanyCoveragePlan", "CompanyCoverageProfile", "build_company_coverage_plan"]
