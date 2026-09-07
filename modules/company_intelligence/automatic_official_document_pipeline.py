"""Archive approved official document candidates produced by a research cycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from urllib.parse import urlsplit

from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewQueueBuilder
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewWriter
from modules.company_intelligence.official_report_discovery import discover_official_reports
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


OFFICIAL_INTENTS = {"OFFICIAL_DOCUMENT_DISCOVERY", "EXCHANGE_DISCLOSURES"}
REGULATORY_DOMAINS = {"nseindia.com", "bseindia.com"}


@dataclass(frozen=True)
class OfficialDocumentCycleSummary:
    candidates_seen: int
    approved_urls: int
    archived: int
    unchanged: int
    new_versions: int
    failed: int
    extracted: int
    fact_candidates_queued: int
    extraction_holds: int
    meta_reviewed: int
    human_review_ready: int
    meta_holds: int
    discovery_pages_checked: int = 0
    discovery_pages_failed: int = 0
    discovery_pdf_links_found: int = 0


class AutomaticOfficialDocumentPipeline:
    def __init__(self, archive: CompanyDocumentArchive, acquisition_ledger: PublicSourceAcquisitionLedger, *, extraction_ledger: PublicDocumentExtractionLedger | None = None, review_queue_root=None, adapter_factory=TrustedPublicAcquisitionAdapter, source_manifest=None):
        self.archive = archive
        self.acquisition_ledger = acquisition_ledger
        self.adapter_factory = adapter_factory
        self.extraction_ledger = extraction_ledger
        self.review_queue_root = review_queue_root
        self.source_manifest = source_manifest

    def run(self, executed_jobs, results, *, cycle_id: str, acquired_at: datetime) -> OfficialDocumentCycleSummary:
        counts = {"candidates_seen": 0, "approved_urls": 0, "archived": 0, "unchanged": 0, "new_versions": 0, "failed": 0, "extracted": 0, "fact_candidates_queued": 0, "extraction_holds": 0, "meta_reviewed": 0, "human_review_ready": 0, "meta_holds": 0}
        counts.update(discovery_pages_checked=0, discovery_pages_failed=0, discovery_pdf_links_found=0)
        for job, result in zip(executed_jobs, results, strict=True):
            if job.intent not in OFFICIAL_INTENTS or not job.entity_domain:
                continue
            registry = self._registry(job)
            adapter = self.adapter_factory(registry, self.acquisition_ledger)
            selected_sources = result.selected_sources
            # A targeted search must not fall back to arbitrary annual/older PDFs.
            target_period = getattr(job, 'quarter_period_end', None)
            if target_period:
                from modules.company_intelligence.quarterly_search_target import quarterly_search_plan, assess_quarterly_search_results
                plan = quarterly_search_plan(job.company, job.entity_domain, target_period)
                screened = assess_quarterly_search_results([s.result for s in selected_sources], plan)
                selected_sources = [s for s, assessment in zip(selected_sources, screened['results'])
                                    if assessment['status'] == 'TARGET_QUARTER_CANDIDATE']
            if not target_period and job.intent == "OFFICIAL_DOCUMENT_DISCOVERY" and self.source_manifest:
                discovered = discover_official_reports(job, self.source_manifest, adapter,
                    acquired_at=acquired_at, cycle_id=cycle_id)
                counts["discovery_pages_checked"] += discovered['pages_checked']
                counts["discovery_pages_failed"] += discovered['pages_failed']
                counts["discovery_pdf_links_found"] += discovered['pdf_links_found']
                counts["failed"] += discovered['pages_failed']
                # Governed issuer locations are stronger acquisition candidates than
                # search results. Always consider them, even when search returned
                # weaker links, then supplement with search without fetching a URL
                # twice. Exact-quarter jobs remain excluded from this generic path.
                combined_sources = [*discovered['selected_sources'], *selected_sources]
                selected_sources = []
                combined_urls = set()
                for source in combined_sources:
                    if source.result.url in combined_urls:
                        continue
                    combined_urls.add(source.result.url)
                    selected_sources.append(source)
                    if len(selected_sources) >= job.max_sources:
                        break
            seen_urls = set()
            for selected in selected_sources:
                url = selected.result.url
                counts["candidates_seen"] += 1
                if url in seen_urls or not self._approved(url, job.entity_domain):
                    continue
                seen_urls.add(url)
                counts["approved_urls"] += 1
                token = sha256(f"{cycle_id}\n{job.job_id}\n{url}".encode()).hexdigest()[:20]
                try:
                    acquisition = adapter.acquire(
                        acquisition_id=f"COMPANY-DOC-{token}", cycle_id=cycle_id,
                        job_id=job.job_id, research_intent=job.intent, url=url,
                        recorder="EIOS_AUTOMATION", requested_at=acquired_at,
                        source_document_id=self._document_id(job.ticker, url),
                    )
                    if acquisition.document_bytes is None:
                        counts["failed"] += 1
                        continue
                    version = self.archive.preserve(
                        acquisition, company_id=f"IN-{job.ticker.upper()}",
                        document_id=self._document_id(job.ticker, url), acquired_at=acquired_at,
                    )
                except Exception as exc:
                    if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                        raise
                    counts["failed"] += 1
                    continue
                counts["archived"] += 1
                if version.change_status == "UNCHANGED":
                    counts["unchanged"] += 1
                elif version.change_status == "NEW_VERSION":
                    counts["new_versions"] += 1
                if version.change_status != "UNCHANGED" and self.extraction_ledger is not None and self.review_queue_root is not None:
                    try:
                        extraction_id = f"COMPANY-EXT-{token}"
                        extraction = TrustedPublicDocumentExtractionAdapter(self.extraction_ledger).extract(
                            acquisition, extraction_id=extraction_id, recorder="EIOS_AUTOMATION",
                        )
                        if extraction.extracted_text is None:
                            counts["extraction_holds"] += 1
                            continue
                        counts["extracted"] += 1
                        admission = PublicObservationAdmissionGate(registry).preview(
                            acquisition=acquisition, extraction=extraction, observations=(),
                            title=selected.result.title or "Official company document",
                            entity=job.company, category="COMPANY_OFFICIAL_DOCUMENT", confidence=80,
                        )
                        if not admission.admissible:
                            counts["extraction_holds"] += 1
                            continue
                        queue_path = self.review_queue_root / job.ticker.upper() / f"{self._document_id(job.ticker, url)}-{version.document_hash[:12]}.json"
                        queued = CompanyFactReviewQueueBuilder(queue_path).build(
                            acquisition=acquisition, extraction=extraction, admission=admission,
                            company=job.company, generated_at=acquired_at,
                        )
                        counts["fact_candidates_queued"] += len(queued)
                        assessments = CompanyCandidateMetaReviewWriter().write(
                            queued, output_path=queue_path.with_suffix(".meta.json"), reviewed_at=acquired_at,
                        )
                        counts["meta_reviewed"] += len(assessments)
                        counts["human_review_ready"] += sum(item.decision == "READY_FOR_HUMAN_REVIEW" for item in assessments)
                        counts["meta_holds"] += sum(item.decision == "HOLD_FOR_RESEARCH" for item in assessments)
                    except Exception as exc:
                        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                            raise
                        counts["extraction_holds"] += 1
                        continue
        return OfficialDocumentCycleSummary(**counts)

    @staticmethod
    def _registry(job):
        return TrustedPublicSourceRegistry((
            TrustedPublicSourceDefinition(
                f"ISSUER-{job.ticker.upper()}", job.company, (job.entity_domain,),
                source_type="COMPANY_PRIMARY",
            ),
            TrustedPublicSourceDefinition("NSE", "National Stock Exchange of India", ("nseindia.com",)),
            TrustedPublicSourceDefinition("BSE", "BSE India", ("bseindia.com",)),
        ))

    @staticmethod
    def _approved(url: str, entity_domain: str) -> bool:
        host = (urlsplit(url).hostname or "").casefold().rstrip(".")
        issuer = entity_domain.casefold().rstrip(".")
        return host == issuer or host.endswith("." + issuer) or any(host == domain or host.endswith("." + domain) for domain in REGULATORY_DOMAINS)

    @staticmethod
    def _document_id(ticker: str, url: str) -> str:
        return f"{ticker.upper()}-{sha256(url.encode()).hexdigest()[:16]}"


__all__ = ["AutomaticOfficialDocumentPipeline", "OfficialDocumentCycleSummary"]
