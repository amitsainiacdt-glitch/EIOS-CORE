"""Fail-closed classification of newly discovered company material for UI review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class DiscoveryChange:
    title: str
    source_url: str
    discovered_at: str | None
    research_intent: str
    source_quality_tier: str
    review_status: str
    verdict_impact: str = "NONE"


def classify_discovery_change(observation: Mapping, company_name: str) -> DiscoveryChange:
    provenance = observation.get("provenance") or {}
    title = str(observation.get("title") or "Untitled discovery")
    description = str(observation.get("description") or "")
    source_url = str(observation.get("source") or provenance.get("source_url") or "")
    intent = str(provenance.get("research_intent") or "UNCLASSIFIED")
    tier = str(provenance.get("source_quality_tier") or "UNRATED")
    entity_tokens = [token.casefold() for token in company_name.split() if len(token) >= 5]
    combined = f"{title} {description}".casefold()
    entity_mentioned = any(token in combined for token in entity_tokens)

    if not entity_mentioned:
        review_status = "LOW_RELEVANCE_HOLD"
    elif intent in {"OFFICIAL_DOCUMENT_DISCOVERY", "EXCHANGE_DISCLOSURES"} and tier != "TIER_1":
        review_status = "SOURCE_AUTHORITY_HOLD"
    else:
        review_status = "PENDING_HUMAN_REVIEW"

    return DiscoveryChange(
        title=title,
        source_url=source_url,
        discovered_at=observation.get("timestamp"),
        research_intent=intent,
        source_quality_tier=tier,
        review_status=review_status,
    )


__all__ = ["DiscoveryChange", "classify_discovery_change"]
