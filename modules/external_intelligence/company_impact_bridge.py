"""Fail-closed bridge from a governed sector fact to a company hypothesis."""

from dataclasses import dataclass
from datetime import datetime,timezone
import re


@dataclass(frozen=True)
class GovernedSectorFact:
    fact_id: str
    indicator_id: str
    crop_ids: tuple[str,...]
    state_ids: tuple[str,...]
    product_ids: tuple[str,...]
    direction: str
    as_of: datetime
    public_source_ids: tuple[str,...]


@dataclass(frozen=True)
class CompanyExposureDisclosure:
    disclosure_id: str
    entity: str
    authority_id: str
    source_document_id: str
    source_url: str
    document_hash: str
    exact_passage: str
    as_of: datetime
    crop_ids: tuple[str,...]
    state_ids: tuple[str,...]
    product_ids: tuple[str,...]
    disclosed_revenue_exposure_pct: float | None
    transmission_mechanism: str | None
    public_information_only: bool = True


@dataclass(frozen=True)
class CompanyImpactBridgeAssessment:
    status: str
    company_hypothesis_ready: bool
    matched_dimensions: tuple[str,...]
    missing_controls: tuple[str,...]
    permitted_claim: str
    blocked_claims: tuple[str,...]


def assess_company_impact_bridge(fact, disclosure, *, assessed_at, max_disclosure_age_days=550):
    if not isinstance(fact,GovernedSectorFact) or not isinstance(disclosure,CompanyExposureDisclosure):
        raise ValueError("governed sector fact and company disclosure are required")
    if assessed_at.tzinfo is None: raise ValueError("assessed_at must be timezone-aware")
    missing=[]; matched=[]
    if not disclosure.public_information_only: missing.append("public-information-only disclosure")
    if disclosure.authority_id not in ("NSE","BSE","SEBI"): missing.append("exchange or securities-regulator authority")
    if not re.fullmatch(r"[0-9a-f]{64}",disclosure.document_hash): missing.append("valid SHA-256 document hash")
    if not disclosure.source_document_id.strip() or not disclosure.source_url.startswith("https://"): missing.append("traceable source document")
    if len(disclosure.exact_passage.split())<8: missing.append("substantive exact disclosure passage")
    if disclosure.as_of.tzinfo is None: missing.append("timezone-aware disclosure date")
    else:
        age=(assessed_at.astimezone(timezone.utc)-disclosure.as_of.astimezone(timezone.utc)).days
        if age<0 or age>max_disclosure_age_days: missing.append("current company disclosure")
    for label,left,right in (("CROP",fact.crop_ids,disclosure.crop_ids),("STATE",fact.state_ids,disclosure.state_ids),("PRODUCT",fact.product_ids,disclosure.product_ids)):
        if left and right and set(left)&set(right): matched.append(label)
    if fact.product_ids and "PRODUCT" not in matched: missing.append("matching product exposure")
    if fact.state_ids and "STATE" not in matched: missing.append("matching geographic exposure")
    if fact.crop_ids and "CROP" not in matched: missing.append("matching crop exposure")
    pct=disclosure.disclosed_revenue_exposure_pct
    if pct is None: missing.append("quantified revenue or volume materiality")
    elif isinstance(pct,bool) or not isinstance(pct,(int,float)) or not 0<pct<=100: missing.append("valid materiality percentage")
    if not disclosure.transmission_mechanism or len(disclosure.transmission_mechanism.split())<5: missing.append("explicit operating transmission mechanism")
    if not fact.public_source_ids: missing.append("governed sector-fact lineage")
    missing=tuple(dict.fromkeys(missing))
    if missing:
        status="SECTOR_ONLY" if not matched else "EXPOSURE_MAPPED_RESEARCH_HOLD"
        claim=f"{disclosure.entity} has a public disclosure matching {', '.join(matched).lower()} exposure; company impact remains unquantified." if matched else "The governed fact remains a sector-level research signal only."
    else:
        status="COMPANY_HYPOTHESIS_READY"; claim=f"A public disclosure maps {fact.indicator_id} to {disclosure.entity}'s disclosed exposure; direction, magnitude, timing, and earnings effect still require validation."
    return CompanyImpactBridgeAssessment(status,not missing,tuple(matched),missing,claim,(
        "the sector fact caused company revenue or profit to change",
        "the disclosed exposure guarantees a positive or negative earnings outcome",
        "revenue exposure equals profit sensitivity",
        "the market has not priced the information",
        "an investment recommendation, position, or trade",
    ))


__all__=["GovernedSectorFact","CompanyExposureDisclosure","CompanyImpactBridgeAssessment","assess_company_impact_bridge"]
