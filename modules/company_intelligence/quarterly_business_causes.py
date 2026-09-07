"""Validate and select source-backed commercial explanations for quarterly movements."""
import json
from urllib.parse import urlsplit


ALLOWED_STATUS = {'CONFIRMED', 'SUPPORTED', 'CONTRADICTED', 'UNKNOWN'}
ALLOWED_EFFECT = {'PRESSURE', 'OFFSET', 'CONTEXT', 'CATALYST'}


def load_quarterly_business_causes(path, *, ticker, period_end, basis):
    """Return only evidence bound to the requested company, quarter and accounting basis."""
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError):
        return {'status': 'NO_VALID_CAUSE_EVIDENCE', 'items': [], 'invalidCount': 1,
                'summary': 'No validated business-cause evidence is available.'}
    items, invalid, seen = [], 0, set()
    for item in payload.get('items', []):
        try:
            _validate(item)
            if (item['ticker'].upper(), item['period_end'], item['basis']) != (ticker.upper(), period_end, basis):
                continue
            if item['id'] in seen:
                raise ValueError('duplicate cause id')
            seen.add(item['id'])
            selected = {key: item[key] for key in (
                'id', 'cause', 'status', 'effect', 'plain_english', 'financial_link',
                'evidence_summary', 'source_title', 'source_url', 'source_date',
                'alternative_explanations', 'what_would_confirm', 'decision_boundary')}
            selected['monitoring_rules'] = item.get('monitoring_rules', [])
            items.append(selected)
        except (KeyError, TypeError, ValueError):
            invalid += 1
    confirmed = sum(item['status'] == 'CONFIRMED' for item in items)
    return {
        'status': 'SOURCE_BACKED_CAUSES_AVAILABLE' if confirmed else 'CAUSES_NOT_CONFIRMED',
        'items': items, 'invalidCount': invalid,
        'summary': (f'{confirmed} commercial cause(s) are directly supported by official company evidence. '
                    'These explain the quarter but do not approve the figures or create an investment verdict.')
                   if confirmed else 'Possible causes remain hypotheses; EIOS is not presenting them as fact.',
    }


def _validate(item):
    required = ('id','ticker','period_end','basis','cause','status','effect','plain_english',
                'financial_link','evidence_summary','source_title','source_url','source_date',
                'alternative_explanations','what_would_confirm','decision_boundary')
    if any(not isinstance(item.get(key), str) or not item[key].strip() for key in required):
        raise ValueError('missing cause field')
    if item['status'] not in ALLOWED_STATUS or item['effect'] not in ALLOWED_EFFECT:
        raise ValueError('invalid classification')
    parsed = urlsplit(item['source_url'])
    if parsed.scheme != 'https' or parsed.hostname not in {'www.coromandel.biz', 'coromandel.biz'} or parsed.username or parsed.password:
        raise ValueError('source is not an allowed official URL')


__all__ = ['load_quarterly_business_causes']
