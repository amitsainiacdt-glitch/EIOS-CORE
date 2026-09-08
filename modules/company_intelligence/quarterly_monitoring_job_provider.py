"""Create recurring primary-source research jobs from validated quarterly monitoring rules."""
from pathlib import Path

from modules.company_intelligence.quarterly_business_causes import load_quarterly_business_causes
from modules.company_intelligence.quarterly_cause_monitoring import build_quarterly_cause_monitoring
from modules.external_intelligence.research_job import ResearchJob


ROOT = Path(__file__).resolve().parents[2]


def load_quarterly_monitoring_jobs(path=None):
    source = path or ROOT / 'data/company_intelligence/quarterly_business_causes.json'
    # Cause files may later include many companies. Load their contexts first, then
    # pass each through the same strict cause and rule validators.
    import json
    raw = json.loads(source.read_text(encoding='utf-8'))
    contexts = sorted({(item.get('ticker',''), item.get('period_end',''), item.get('basis',''))
                       for item in raw.get('items', [])})
    jobs, seen = [], set()
    for ticker, period_end, basis in contexts:
        causes = load_quarterly_business_causes(source, ticker=ticker, period_end=period_end, basis=basis)
        plan = build_quarterly_cause_monitoring(causes)
        for rule in plan['rules']:
            job_id = f"{ticker.upper()}-PRIMARY-INDICATOR-{rule['id'].upper()}"
            if job_id in seen:
                raise ValueError(f'duplicate quarterly monitoring job: {job_id}')
            seen.add(job_id)
            measurement_instruction = rule.get('collection_instruction','').strip()
            job = ResearchJob(
                job_id=job_id, company=ticker.upper(), ticker=ticker.upper(),
                question=(f"Check the latest official value and reporting date for {rule['indicator']}. "
                          f"Use only the primary authority domain {rule['source_domain']}; retain the exact unit {rule['unit']} and source passage. "
                          f"{measurement_instruction}").strip(),
                intent='PRIMARY_INDICATOR_MONITORING', frequency_minutes=_frequency(rule['cadence']),
                enabled=True, priority=95, max_sources=3,
                observation_category='Primary Indicator Candidate', observation_confidence=70.0,
                entity_domain=rule['source_domain'])
            job.validate(); jobs.append(job)
    return jobs


def load_quarterly_monitoring_rules(path=None):
    source = path or ROOT / 'data/company_intelligence/quarterly_business_causes.json'
    import json
    raw=json.loads(source.read_text(encoding='utf-8')); result={}
    for ticker,period,basis in sorted({(item.get('ticker',''),item.get('period_end',''),item.get('basis','')) for item in raw.get('items',[])}):
        causes=load_quarterly_business_causes(source,ticker=ticker,period_end=period,basis=basis)
        for rule in build_quarterly_cause_monitoring(causes)['rules']:
            result[f"{ticker.upper()}-PRIMARY-INDICATOR-{rule['id'].upper()}"]=(ticker,rule)
    return result


def _frequency(cadence):
    lowered = cadence.lower()
    if 'weekly' in lowered: return 10080
    if 'on every' in lowered or 'on new' in lowered: return 1440
    if 'quarterly' in lowered: return 43200
    raise ValueError(f'unsupported monitoring cadence: {cadence}')


__all__ = ['load_quarterly_monitoring_jobs','load_quarterly_monitoring_rules']
