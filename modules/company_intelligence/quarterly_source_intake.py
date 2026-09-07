"""Automatic, non-approving source-copy comparison for quarterly imports."""
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs
from modules.company_intelligence.quarterly_source_match import match_quarterly_source
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def verify_intake_source(original, digest, *, workspace, output_directory, ticker, company, source_url,
                         adapter_factory=TrustedPublicAcquisitionAdapter):
    output = Path(output_directory) / 'source-verification' / uuid4().hex
    result = {'status': 'HOLD_MISSING_COMPANY_SOURCE_CONTEXT', 'document_hash': digest,
              'checked_at': datetime.now(timezone.utc).isoformat(), 'requested_url': source_url,
              'ticker': ticker, 'creates_approved_facts': False, 'changes_verdict': False}
    if company and source_url:
        try:
            jobs = [job for job in load_company_coverage_jobs(Path(workspace) / 'data/company_intelligence')
                    if job.ticker.upper() == ticker.upper() and job.intent == 'OFFICIAL_DOCUMENT_DISCOVERY']
            if len(jobs) != 1 or jobs[0].company != company:
                raise ValueError('A unique configured company identity is required')
            job = jobs[0]
            registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition(
                'ISSUER-' + ticker.upper(), company, (job.entity_domain,), source_type='COMPANY_PRIMARY'),))
            registry.resolve(source_url)
            ledger = PublicSourceAcquisitionLedger(output / 'acquisitions.jsonl')
            adapter = adapter_factory(registry, ledger, timeout=15, max_redirects=2)
            result, body = match_quarterly_source(original, digest, source_url=source_url, adapter=adapter)
            result.update(ticker=ticker, acquisition_ledger=str(ledger.path), changes_verdict=False)
            if body is not None:
                output.mkdir(parents=True, exist_ok=True)
                (output / 'issuer-copy.pdf').write_bytes(body)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            result.update(status='SOURCE_CHECK_FAILED_HOLD', explanation=str(exc))
    output.mkdir(parents=True, exist_ok=True)
    result['result_path'] = str(output / 'verification.json')
    (output / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result
