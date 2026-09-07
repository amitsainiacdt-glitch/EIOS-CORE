"""One bounded official-source download, compared with a saved quarterly review packet."""
import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from modules.company_intelligence.company_coverage_job_provider import load_company_coverage_jobs
from modules.company_intelligence.quarterly_source_match import match_quarterly_source
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


def resolve_source_url(candidate_url, alternate_url, registry):
    selected = alternate_url or candidate_url
    registry.resolve(selected)
    return selected


def source_registry(job, *, exchange=False):
    if exchange:
        return TrustedPublicSourceRegistry((
            TrustedPublicSourceDefinition('BSE', 'BSE India', ('bseindia.com',)),
            TrustedPublicSourceDefinition('NSE', 'National Stock Exchange of India', ('nseindia.com',)),
        ))
    return TrustedPublicSourceRegistry((TrustedPublicSourceDefinition(
        'ISSUER-' + job.ticker.upper(), job.company, (job.entity_domain,), source_type='COMPANY_PRIMARY'),))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', required=True, type=Path)
    parser.add_argument('--source-url', help='Observed official URL; must pass the selected issuer or exchange registry')
    parser.add_argument('--exchange-source', action='store_true', help='Check an observed BSE/NSE filing URL instead of an issuer URL; does not verify company content')
    args = parser.parse_args()
    queue = json.loads(args.queue.read_text(encoding='utf-8'))
    candidates = queue['candidates']
    if not candidates:
        raise ValueError('No quarterly candidate to verify')
    candidate = candidates[0]
    record = queue['quarterly_record_evidence'][candidate['candidate_id']]
    source = record['source_column']
    if candidate['document_hash'] != source['document_hash']:
        raise ValueError('Candidate and extraction document hashes disagree')
    job = next(job for job in load_company_coverage_jobs()
               if job.ticker.upper() == source['ticker'].upper()
               and job.intent == 'OFFICIAL_DOCUMENT_DISCOVERY')
    if queue['company'] != job.company or candidate['company'] != job.company:
        raise ValueError('Candidate company does not match the configured company')
    if args.exchange_source and not args.source_url:
        raise ValueError('Exchange verification requires an explicit observed filing URL')
    registry = source_registry(job, exchange=args.exchange_source)
    source_url = resolve_source_url(candidate['source_url'], args.source_url, registry)
    pdf = next((parent / 'source.pdf' for parent in (args.queue.parent, args.queue.parent.parent)
                if (parent / 'source.pdf').is_file()), None)
    if pdf is None:
        raise ValueError('Preserved quarterly source missing')
    output = args.queue.parent / 'source-verification' / uuid4().hex
    ledger = PublicSourceAcquisitionLedger(output / 'acquisitions.jsonl')
    result, downloaded = match_quarterly_source(pdf.read_bytes(), source['document_hash'],
        source_url=source_url, adapter=TrustedPublicAcquisitionAdapter(registry, ledger, timeout=15),
        source_kind='EXCHANGE' if args.exchange_source else 'ISSUER')
    output.mkdir(parents=True, exist_ok=True)
    if downloaded is not None:
        (output / ('exchange-copy.pdf' if args.exchange_source else 'issuer-copy.pdf')).write_bytes(downloaded)
    result.update(candidate_id=candidate['candidate_id'], ticker=job.ticker,
                  candidate_source_url=candidate['source_url'],
                  acquisition_ledger=str(ledger.path))
    (output / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({**result, 'result_path': str(output / 'verification.json')}, indent=2))
    return 0 if result['status'] in {'EXACT_ISSUER_COPY_MATCH', 'EXACT_EXCHANGE_COPY_MATCH'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
