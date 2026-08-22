"""Deterministic semantic source classification policy."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class SourceQualityClassification:
    """Passive result returned by :class:`SourceQualityService`."""

    source_type: str
    quality_tier: str


class SourceQualityService:
    """Classify a URL without network access or content interpretation."""

    _REGULATORY_HOSTS = (
        "sec.gov", "sebi.gov.in", "rbi.org.in", "mca.gov.in",
        "bseindia.com", "nseindia.com",
    )
    _NEWS_HOSTS = (
        "reuters.com", "bloomberg.com", "ft.com", "wsj.com",
        "economictimes.indiatimes.com", "moneycontrol.com",
    )
    _RESEARCH_HOSTS = (
        "arxiv.org", "ssrn.com", "researchgate.net",
    )

    def classify(self, url: str, *, entity_domain: str | None = None) -> SourceQualityClassification:
        host = (urlparse(url).hostname or "").lower().rstrip(".")
        entity_host = (entity_domain or "").lower().rstrip(".")

        if self._matches(host, self._REGULATORY_HOSTS) or host.endswith(".gov") or ".gov." in host:
            return SourceQualityClassification("REGULATORY", "TIER_1")
        if entity_host and (host == entity_host or host.endswith("." + entity_host)):
            return SourceQualityClassification("COMPANY_PRIMARY", "TIER_1")
        if self._matches(host, self._RESEARCH_HOSTS) or host.endswith(".edu") or ".ac." in host:
            return SourceQualityClassification("RESEARCH", "TIER_2")
        if self._matches(host, self._NEWS_HOSTS):
            return SourceQualityClassification("NEWS", "TIER_2")
        return SourceQualityClassification("WEB", "TIER_3")

    @staticmethod
    def _matches(host: str, domains: tuple[str, ...]) -> bool:
        return any(host == domain or host.endswith("." + domain) for domain in domains)


__all__ = ["SourceQualityClassification", "SourceQualityService"]
