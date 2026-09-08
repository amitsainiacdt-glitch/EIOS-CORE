"""Strict extraction and append-only history for primary monitoring indicators."""
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from modules.company_intelligence.quarterly_cause_monitoring import evaluate_direction


@dataclass(frozen=True)
class PrimaryIndicatorRecord:
    schema_version: int; record_id: str; rule_id: str; job_id: str; ticker: str
    reporting_date: str; value: str; unit: str; source_url: str; source_domain: str
    evidence_passage: str; content_fingerprint: str; recorded_at: datetime


class PrimaryIndicatorLedger:
    def __init__(self, path): self.path=Path(path)

    def record(self, candidate, *, recorded_at):
        item=self._parse({**candidate,'schema_version':1,'recorded_at':recorded_at.isoformat(),
                          'record_id':self.fingerprint(candidate)})
        existing=self.read_all()
        if any(row.record_id==item.record_id for row in existing): return item
        if any((row.rule_id,row.reporting_date)==(item.rule_id,item.reporting_date) and row.record_id!=item.record_id for row in existing):
            raise ValueError('conflicting value already exists for rule and reporting date')
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(self._payload(item),sort_keys=True,separators=(',',':'))+'\n')
        return item

    def read_all(self):
        if not self.path.exists(): return ()
        result=[]
        for number,line in enumerate(self.path.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): continue
            try: result.append(self._parse(json.loads(line)))
            except (KeyError,TypeError,ValueError,InvalidOperation) as exc: raise ValueError(f'invalid indicator record at line {number}: {exc}') from exc
        if len({item.record_id for item in result})!=len(result): raise ValueError('duplicate indicator record')
        return tuple(result)

    def latest_alert(self, rule):
        records=sorted((item for item in self.read_all() if item.rule_id==rule['id']),key=lambda item:item.reporting_date)
        if len(records)<2: return {'status':'AWAITING_COMPARABLE_OBSERVATION','creates_catalyst':False,'changes_verdict':False,'authorizes_trade':False}
        result=evaluate_direction(rule,previous=records[-2].value,current=records[-1].value)
        return {**result,'rule_id':rule['id'],'previous_date':records[-2].reporting_date,'current_date':records[-1].reporting_date}

    @staticmethod
    def fingerprint(candidate):
        payload={key:candidate[key] for key in ('rule_id','job_id','ticker','reporting_date','value','unit','source_url','source_domain','evidence_passage','content_fingerprint')}
        return sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

    @classmethod
    def _parse(cls,value):
        if value.get('schema_version')!=1: raise ValueError('unsupported schema')
        domain=(urlsplit(value['source_url']).hostname or '').casefold().rstrip('.')
        if domain!=value['source_domain'] or not value['source_url'].startswith('https://'): raise ValueError('source identity mismatch')
        number=Decimal(value['value'])
        if not number.is_finite(): raise ValueError('indicator value must be finite')
        datetime.fromisoformat(value['recorded_at']); datetime.fromisoformat(value['reporting_date'])
        if len(value['content_fingerprint'])!=64 or len(value['record_id'])!=64: raise ValueError('invalid fingerprint')
        if len(value['evidence_passage'].split())<5: raise ValueError('evidence passage is too short')
        return PrimaryIndicatorRecord(**{**value,'recorded_at':datetime.fromisoformat(value['recorded_at'])})

    @staticmethod
    def _payload(item): return {**asdict(item),'recorded_at':item.recorded_at.isoformat()}


def extract_primary_indicator(observation, rule, *, ticker):
    """Extract only one context-bound value and one explicit ISO reporting date."""
    provenance=getattr(observation,'provenance',None)
    expected_job=f"{ticker.upper()}-PRIMARY-INDICATOR-{rule['id'].upper()}"
    if (not provenance or provenance.job_id!=expected_job or provenance.research_intent!='PRIMARY_INDICATOR_MONITORING'
            or provenance.source_quality_tier!='TIER_1' or (provenance.source_domain or '').casefold()!=rule['source_domain']):
        return {'status':'HELD_SOURCE_BINDING'}
    text=observation.description
    dates=sorted(set(re.findall(r'\b20\d{2}-\d{2}-\d{2}\b',text)))
    if len(dates)!=1: return {'status':'HELD_REPORTING_DATE_AMBIGUOUS'}
    aliases=rule.get('unit_aliases',[])
    if not aliases: return {'status':'HELD_UNIT_CONFIGURATION'}
    unit_pattern='|'.join(re.escape(alias) for alias in aliases)
    numbers=[]
    for match in re.finditer(rf'(?P<value>-?\d[\d,]*(?:\.\d+)?)\s*(?P<unit>{unit_pattern})(?!\w)',text,re.I):
        window=text[max(0,match.start()-180):min(len(text),match.end()+180)].casefold()
        if all(term.casefold() in window for term in rule.get('match_terms',[])): numbers.append(match)
    if len(numbers)!=1: return {'status':'HELD_VALUE_AMBIGUOUS','candidateCount':len(numbers)}
    match=numbers[0]
    try: value=Decimal(match.group('value').replace(',',''))
    except InvalidOperation: return {'status':'HELD_VALUE_INVALID'}
    if not value.is_finite(): return {'status':'HELD_VALUE_INVALID'}
    passage=text[max(0,match.start()-180):min(len(text),match.end()+180)].strip()
    return {'status':'READY_TO_RECORD','candidate':{'rule_id':rule['id'],'job_id':expected_job,'ticker':ticker.upper(),
        'reporting_date':dates[0],'value':format(value,'f'),'unit':rule['unit'],'source_url':observation.source,
        'source_domain':rule['source_domain'],'evidence_passage':passage,
        'content_fingerprint':provenance.content_fingerprint}}


def attach_indicator_record_state(plan, ledger):
    """Add read-only latest-value/alert state to a dashboard monitoring plan."""
    records=ledger.read_all(); rules=[]
    for rule in plan.get('rules',[]):
        history=sorted((item for item in records if item.rule_id==rule['id']),key=lambda item:item.reporting_date)
        alert=ledger.latest_alert(rule)
        rules.append({**rule,'record_count':len(history),
                      'latest_value':history[-1].value if history else None,
                      'latest_date':history[-1].reporting_date if history else None,
                      'latest_signal':alert['status']})
    has_plan_history=any(rule['record_count'] for rule in rules)
    return {**plan,'rules':rules,'recordStatus':'HISTORY_AVAILABLE' if has_plan_history else 'CONNECTED_AWAITING_FIRST_RECORD'}


__all__=['PrimaryIndicatorLedger','PrimaryIndicatorRecord','extract_primary_indicator','attach_indicator_record_state']
