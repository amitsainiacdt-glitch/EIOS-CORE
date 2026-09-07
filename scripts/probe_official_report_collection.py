"""Bounded live probe: one configured issuer page and at most one report download."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs
from modules.company_intelligence.company_document_archive import CompanyDocumentArchive
from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
from modules.company_intelligence.official_report_discovery import discover_official_reports
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', default='COROMANDEL')
    parser.add_argument('--collect', action='store_true')
    parser.add_argument('--quarterly-only', action='store_true', help='Restrict this probe to configured quarterly-results sources')
    args = parser.parse_args()
    job = next(job for job in load_company_coverage_jobs() if job.ticker.upper() == args.ticker.upper() and job.intent == 'OFFICIAL_DOCUMENT_DISCOVERY')
    now = datetime.now(timezone.utc)
    directory = ROOT / 'data/runtime/official_collection_probe'
    directory.mkdir(parents=True, exist_ok=True)
    ledger = PublicSourceAcquisitionLedger(directory / 'acquisitions.jsonl')
    adapter = TrustedPublicAcquisitionAdapter(AutomaticOfficialDocumentPipeline._registry(job), ledger)
    manifest = json.loads((ROOT / 'data/company_intelligence/company_source_manifest.json').read_text(encoding='utf-8'))
    if args.quarterly_only:
        company = manifest.get('companies', {}).get(args.ticker.upper(), {})
        company['sources'] = [source for source in company.get('sources', []) if source.get('source_type') == 'QUARTERLY_RESULTS']
    discovery = discover_official_reports(job, manifest, adapter, acquired_at=now, cycle_id=now.isoformat(), max_documents=1)
    sources = discovery.pop('selected_sources')
    report = {**discovery, 'selected_urls': [source.result.url for source in sources], 'recorded_at': now.isoformat()}
    if args.collect and sources:
        pipeline = AutomaticOfficialDocumentPipeline(CompanyDocumentArchive(directory / 'archive', directory / 'archive.jsonl'), ledger,
            extraction_ledger=PublicDocumentExtractionLedger(directory / 'extractions.jsonl'), review_queue_root=directory / 'review_queue')
        report['collection'] = asdict(pipeline.run([job], [SimpleNamespace(selected_sources=sources)], cycle_id=now.isoformat(), acquired_at=now))
    report['creates_approved_facts'] = False
    (directory / 'latest.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 1 if report['pages_failed'] or not sources or report.get('collection', {}).get('failed') else 0


if __name__ == '__main__':
    raise SystemExit(main())
