"""Safely discovers same-authority document links; it does not retrieve them."""

from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit

from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_document_extraction_receipt import PublicDocumentExtractionReceipt, PublicDocumentExtractionStatus
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_source_acquisition_receipt import PublicSourceAcquisitionStatus
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_source_discovery import TrustedPublicDiscoveryPreview, TrustedPublicDocumentCandidate
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self._href, self._text = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag.casefold() == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.casefold() == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._text).split())))
            self._href, self._text = None, []


class TrustedPublicSourceDiscoveryService:
    """Builds a deterministic, non-evidentiary research queue from HTML links."""

    DATE_PATTERN = re.compile(r"(?<!\d)(20\d{2})[-_/\.](0?[1-9]|1[0-2])[-_/\.](0?[1-9]|[12]\d|3[01])(?!\d)")
    DOCUMENT_EXTENSIONS = {".pdf": "PDF", ".csv": "CSV", ".json": "JSON", ".xml": "XML", ".xlsx": "XLSX", ".xls": "XLS"}

    def __init__(self, registry):
        if not isinstance(registry, TrustedPublicSourceRegistry):
            raise ValueError("registry must be a TrustedPublicSourceRegistry")
        self.registry = registry

    def discover(self, acquisition, extraction_receipt, *, query_topics=()):
        self._validate_inputs(acquisition, extraction_receipt)
        topics = self._topics(query_topics)
        parser = _LinkParser()
        parser.feed(acquisition.document_bytes.decode(self._encoding(acquisition), errors="replace"))
        accepted, rejected, seen = [], 0, set()
        for href, link_text in parser.links:
            try:
                url = self._approved_url(acquisition, href)
            except ValueError:
                rejected += 1
                continue
            if url in seen:
                continue
            seen.add(url)
            candidate = self._candidate(acquisition, url, link_text, topics)
            if candidate is not None:
                accepted.append(candidate)
        accepted.sort(key=lambda item: (
            self._tier_order(item.relevance_tier),
            0 if item.date_tokens else 1,
            -int(item.date_tokens[0].replace("-", "")) if item.date_tokens else 0,
            item.url,
        ))
        return TrustedPublicDiscoveryPreview(acquisition.source.source_id, acquisition.receipt.acquisition_id, topics, tuple(accepted), rejected)

    def _validate_inputs(self, acquisition, extraction):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, PublicDocumentExtractionReceipt):
            raise ValueError("extraction_receipt must be a PublicDocumentExtractionReceipt")
        receipt = acquisition.receipt
        if receipt.status != PublicSourceAcquisitionStatus.RETRIEVED or acquisition.document_bytes is None:
            raise ValueError("discovery requires a retrieved landing page")
        if hashlib.sha256(acquisition.document_bytes).hexdigest() != receipt.document_hash:
            raise ValueError("landing page bytes do not match the acquisition receipt")
        if extraction.status not in (PublicDocumentExtractionStatus.SUCCEEDED, PublicDocumentExtractionStatus.PARTIAL):
            raise ValueError("discovery requires a usable extraction receipt")
        if extraction.acquisition_id != receipt.acquisition_id or extraction.document_hash != receipt.document_hash:
            raise ValueError("extraction receipt does not bind to the landing page")
        if extraction.acquisition_fingerprint != PublicSourceAcquisitionLedger.receipt_fingerprint(receipt):
            raise ValueError("extraction receipt has a stale acquisition fingerprint")
        media = (receipt.content_type or "").split(";", 1)[0].strip().casefold()
        if media not in ("text/html", "application/xhtml+xml"):
            raise ValueError("source discovery requires an HTML landing page")

    def _approved_url(self, acquisition, href):
        if not isinstance(href, str) or not href.strip():
            raise ValueError("empty link")
        raw = href.strip()
        if raw.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
            raise ValueError("non-document link")
        url, _ = urldefrag(urljoin(acquisition.receipt.source_url, raw))
        source = self.registry.resolve(url)
        if source.source_id != acquisition.source.source_id:
            raise ValueError("link leaves the approved public authority")
        return url

    def _candidate(self, acquisition, url, link_text, topics):
        path = urlsplit(url).path.casefold()
        extension = next((ext for ext in self.DOCUMENT_EXTENSIONS if path.endswith(ext)), None)
        combined = f"{link_text} {url}".casefold()
        matched = tuple(topic for topic in topics if all(token in combined for token in topic.casefold().split()))
        date_tokens = tuple(sorted({f"{y}-{int(m):02d}-{int(d):02d}" for y, m, d in self.DATE_PATTERN.findall(combined)}, reverse=True))
        reasons = []
        if extension: reasons.append("DIRECT_DOCUMENT_LINK")
        if matched: reasons.append("TOPIC_MATCH")
        if date_tokens: reasons.append("DATED_LINK")
        if not reasons:
            return None
        tier = "HIGH" if extension and matched else "MEDIUM" if extension or matched else "LOW"
        payload = {
            "source_id": acquisition.source.source_id,
            "landing_acquisition_fingerprint": PublicSourceAcquisitionLedger.receipt_fingerprint(acquisition.receipt),
            "url": url, "link_text": link_text, "document_type": self.DOCUMENT_EXTENSIONS.get(extension, "HTML"),
            "date_tokens": date_tokens, "matched_topics": matched, "discovery_reasons": tuple(reasons), "relevance_tier": tier,
        }
        fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return TrustedPublicDocumentCandidate(
            1, f"DISC-{fingerprint[:16].upper()}", acquisition.source.source_id, acquisition.receipt.acquisition_id,
            payload["landing_acquisition_fingerprint"], acquisition.receipt.document_hash, url, link_text,
            payload["document_type"], date_tokens, matched, tuple(reasons), tier, fingerprint,
        )

    @staticmethod
    def _topics(values):
        if not isinstance(values, (list, tuple)):
            raise ValueError("query_topics must be a list or tuple")
        result = tuple(sorted({" ".join(value.split()) for value in values if isinstance(value, str) and value.strip()}, key=str.casefold))
        if len(result) != len(values):
            raise ValueError("query_topics must be non-empty unique strings")
        return result

    @staticmethod
    def _encoding(acquisition):
        content_type = acquisition.receipt.content_type or ""
        match = re.search(r"charset=([^;\s]+)", content_type, re.I)
        return match.group(1).strip('"\'') if match else "utf-8"

    @staticmethod
    def _tier_order(value):
        return {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[value]


__all__ = ["TrustedPublicSourceDiscoveryService"]
