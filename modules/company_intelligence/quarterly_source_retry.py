"""Bounded retry planning over saved quarterly packets; never re-run OCR."""
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
from pathlib import Path
from modules.company_intelligence.quarterly_source_intake import verify_intake_source


def run_source_retries(workspace, *, now=None, offline=False, execute=False, verifier=verify_intake_source):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('Retry time must include timezone')
    root = Path(workspace)
    summary = {'status': 'OFFLINE' if offline else 'COMPLETED', 'attempted': 0, 'items': [],
               'creates_approved_facts': False, 'changes_verdict': False}
    if offline:
        return summary
    directory = root / 'data/runtime/quarterly_intake'
    seen = set()
    for packet in sorted(directory.rglob('quarterly-candidates.json'), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            queue = json.loads(packet.read_text(encoding='utf-8'))
            for candidate in queue['candidates']:
                source = queue['quarterly_record_evidence'][candidate['candidate_id']]['source_column']
                digest, ticker, url = source['document_hash'], source['ticker'], candidate['source_url']
                key = (digest, ticker, url)
                if key in seen:
                    continue
                seen.add(key)
                item = {'ticker': ticker, 'document_hash': digest, 'source_url': url, 'status': 'DUE'}
                summary['items'].append(item)
                pdf = next((p / 'source.pdf' for p in (packet.parent, packet.parent.parent) if (p / 'source.pdf').is_file()), None)
                if (candidate['document_hash'] != digest or candidate['company'] != queue['company']
                        or pdf is None or sha256(pdf.read_bytes()).hexdigest() != digest):
                    item['status'] = 'EVIDENCE_REVIEW_REQUIRED'
                    continue
                history = []
                # Include prior runs of this exact document, not just the newest packet.
                for path in (directory / digest).glob('**/source-verification/*/verification.json'):
                    entry = json.loads(path.read_text(encoding='utf-8'))
                    if entry.get('document_hash') == digest and entry.get('ticker') == ticker and entry.get('requested_url', entry.get('source_url')) == url:
                        stamp = datetime.fromisoformat(entry['checked_at'])
                        if stamp.tzinfo is None:
                            raise ValueError('Missing attempt timezone')
                        history.append((stamp, entry))
                history.sort(key=lambda row: row[0])
                if history:
                    last_time, last = history[-1]
                    if last['status'] == 'EXACT_ISSUER_COPY_MATCH':
                        item['status'] = 'MATCH_RECORDED_PENDING_REVIEW'
                    elif last['status'] != 'SOURCE_UNAVAILABLE' or (last.get('http_status') is not None and last['http_status'] < 500):
                        item['status'] = 'SOURCE_ACCESS_REQUIRES_ATTENTION'
                    elif len(history) >= 3:
                        item['status'] = 'RETRY_LIMIT_REACHED'
                    elif now < last_time + timedelta(hours=24):
                        item['status'] = 'WAITING_RETRY_WINDOW'
                        item['next_attempt_at'] = (last_time + timedelta(hours=24)).isoformat()
                if item['status'] != 'DUE' or not execute:
                    continue
                if summary['attempted'] >= 1:
                    item['status'] = 'DEFERRED_CYCLE_BUDGET'
                    continue
                summary['attempted'] += 1
                result = verifier(pdf.read_bytes(), digest, workspace=root, output_directory=pdf.parent,
                                  ticker=ticker, company=queue['company'], source_url=url)
                item.update(status=result['status'], result_path=result.get('result_path'))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            summary['items'].append({'status': 'INVALID_RETRY_EVIDENCE', 'packet': str(packet), 'reason': str(exc)})
    return summary
