"""Build and evaluate non-advisory monitoring rules from quarterly cause evidence."""
from decimal import Decimal, InvalidOperation


FAMILIES = {'COMMODITY_INPUT', 'GOVERNMENT_POLICY', 'VOLUME', 'SEGMENT_MARGIN', 'WEATHER_DEMAND'}
DIRECTIONS = {'UP', 'DOWN'}


def build_quarterly_cause_monitoring(cause_packet):
    rules, invalid, seen = [], 0, set()
    for cause in cause_packet.get('items', []):
        for rule in cause.get('monitoring_rules', []):
            try:
                _validate(rule)
                if rule['id'] in seen:
                    raise ValueError('duplicate rule')
                seen.add(rule['id'])
                rules.append({**rule, 'cause_id': cause['id'], 'cause': cause['cause'],
                              'cause_effect': cause['effect'], 'latest_signal': 'AWAITING_NEW_OBSERVATION'})
            except (KeyError, TypeError, ValueError):
                invalid += 1
    return {
        'status': 'MONITORING_PLAN_READY' if rules else 'NO_VALID_MONITORING_RULES',
        'rules': rules, 'invalidCount': invalid,
        'summary': (f'{len(rules)} evidence-linked indicators are ready for the next automatic collection cycle. '
                    'A directional move is an alert for review—not a catalyst, verdict change or trade.') if rules
                   else 'No valid evidence-linked monitoring rules are available.',
        'creates_catalyst': False, 'changes_verdict': False, 'authorizes_trade': False,
    }


def evaluate_direction(rule, *, previous, current):
    """Classify a new numeric observation without inferring materiality or causation."""
    _validate(rule)
    before, now = _number(previous), _number(current)
    if now == before:
        state = 'UNCHANGED'
    elif (now > before) == (rule['favourable_direction'] == 'UP'):
        state = 'FAVOURABLE_DIRECTION'
    else:
        state = 'ADVERSE_DIRECTION'
    return {'status': state, 'previous': str(before), 'current': str(now),
            'creates_catalyst': False, 'changes_verdict': False, 'authorizes_trade': False,
            'boundary': 'Direction alone does not establish causation, materiality, durability or market mispricing.'}


def _validate(rule):
    required = ('id','indicator','family','unit','favourable_direction','source_requirement','source_domain',
                'cadence','improvement_meaning','deterioration_meaning')
    if any(not isinstance(rule.get(key), str) or not rule[key].strip() for key in required):
        raise ValueError('monitoring rule field missing')
    if rule['family'] not in FAMILIES or rule['favourable_direction'] not in DIRECTIONS:
        raise ValueError('invalid rule classification')
    if '/' in rule['source_domain'] or '.' not in rule['source_domain']:
        raise ValueError('source_domain must be a bare domain')
    if not isinstance(rule.get('unit_aliases'),list) or not rule['unit_aliases'] or not all(isinstance(item,str) and item for item in rule['unit_aliases']):
        raise ValueError('unit_aliases must be non-empty strings')
    if not isinstance(rule.get('match_terms'),list) or not rule['match_terms'] or not all(isinstance(item,str) and item for item in rule['match_terms']):
        raise ValueError('match_terms must be non-empty strings')


def _number(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError('observation must be numeric') from exc
    if not result.is_finite():
        raise ValueError('observation must be finite')
    return result


__all__ = ['build_quarterly_cause_monitoring', 'evaluate_direction']
