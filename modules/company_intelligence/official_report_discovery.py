"""Bounded direct discovery on configured issuer pages, without a search API."""
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlsplit
from uuid import uuid4

from modules.external_intelligence.search_result import ExternalSearchResult
from modules.external_intelligence.source_selection import SelectedSource


class ReportLinks(HTMLParser):
    def __init__(self, base_url, registry):
        super().__init__(convert_charrefs=True)
        self.base_url, self.registry, self.links = base_url, registry, []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        href = dict(attrs).get('href')
        if not href:
            return
        url = urldefrag(urljoin(self.base_url, href))[0]
        try:
            self.registry.resolve(url)
            if urlsplit(url).path.lower().endswith('.pdf') and url not in self.links:
                self.links.append(url)
        except ValueError:
            return


def discover_official_reports(job, manifest, adapter, *, acquired_at, cycle_id, max_documents=2):
    if type(max_documents) is not int or not 1 <= max_documents <= 5:
        raise ValueError('max_documents must be between 1 and 5')
    outcome = {'pages_checked': 0, 'pages_failed': 0, 'pdf_links_found': 0, 'selected_sources': [], 'errors': []}
    company = manifest.get('companies', {}).get(job.ticker.upper(), {})
    # Both modes are bounded configured-source checks, never broad crawling.
    if job.intent == 'EXCHANGE_DISCLOSURES':
        allowed_types = {'EXCHANGE_DISCLOSURE', 'EXCHANGE_FINANCIAL_FILING'}
        allowed_authority = 'EXCHANGE_OFFICIAL'
    else:
        allowed_types = {'ANNUAL_REPORT', 'QUARTERLY_RESULTS', 'INVESTOR_PRESENTATION'}
        allowed_authority = 'ISSUER_OFFICIAL'
    report_sources = [source for source in company.get('sources', [])
             if source.get('source_type') in allowed_types
             and source.get('authority') == allowed_authority]
    # Check quarterly results before presentations or annual indexes. A known
    # annual URL must not suppress discovery when there is capacity remaining.
    report_sources.sort(key=lambda source: source.get('source_type') != 'QUARTERLY_RESULTS')
    direct_urls = list(dict.fromkeys(url for source in report_sources for url in source.get('document_urls', [])))
    seeds = list(dict.fromkeys(source['url'] for source in report_sources if source.get('url')))[:2]
    for url in direct_urls[:max_documents]:
        try:
            adapter.registry.resolve(url)
            outcome['selected_sources'].append(SelectedSource(
                ExternalSearchResult(title=f'{job.company} configured official report', url=url,
                    snippet=f'Direct document URL configured by the {allowed_authority.lower()} source manifest; contents not yet verified.', source='EIOS_SOURCE_MANIFEST'),
                selection_reason='CONFIGURED_OFFICIAL_DOCUMENT_URL'))
        except ValueError as exc:
            outcome['errors'].append(str(exc))
    outcome['pdf_links_found'] += len(outcome['selected_sources'])
    for seed in seeds:
        if len(outcome['selected_sources']) >= max_documents:
            break
        outcome['pages_checked'] += 1
        try:
            adapter.registry.resolve(seed)
            acquired = adapter.acquire(acquisition_id=f'DISCOVERY-{uuid4().hex}', cycle_id=cycle_id,
                job_id=job.job_id, research_intent=job.intent, url=seed,
                recorder='EIOS_OFFICIAL_PAGE_DISCOVERY', requested_at=acquired_at)
            if acquired.document_bytes is None:
                raise ValueError(acquired.receipt.error_code or 'SOURCE_UNAVAILABLE')
            final_url = acquired.receipt.source_url
            if urlsplit(final_url).path.lower().endswith('.pdf'):
                links = [final_url]
            else:
                if 'html' not in acquired.retrieved_content.content_type.lower():
                    raise ValueError('Expected HTML investor page')
                parser = ReportLinks(final_url, adapter.registry)
                parser.feed(acquired.document_bytes.decode('utf-8', errors='replace'))
                links = parser.links
            outcome['pdf_links_found'] += len(links)
            # Preserve publisher page order; do not claim it is a verified latest-year ranking.
            for url in links:
                if len(outcome['selected_sources']) >= max_documents:
                    break
                if any(selected.result.url == url for selected in outcome['selected_sources']):
                    continue
                outcome['selected_sources'].append(SelectedSource(
                    ExternalSearchResult(title=f'{job.company} official report link', url=url,
                        snippet=f'Discovered on a configured {allowed_authority.lower()} page; contents not yet verified.', source=seed),
                    selection_reason='CONFIGURED_OFFICIAL_PAGE_LINK'))
        except (ValueError, TypeError, AttributeError, KeyError) as exc:
            outcome['pages_failed'] += 1
            outcome['errors'].append(str(exc))
    return outcome
