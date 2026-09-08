"""Process primary-indicator observations produced by one automatic cycle."""
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger, extract_primary_indicator
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_rules


def process_primary_indicator_results(results, *, ledger_path, recorded_at):
    observations=[]
    for result in results:
        observations.extend(getattr(result,'observations',()))
    return process_primary_indicator_observations(observations,ledger_path=ledger_path,recorded_at=recorded_at)


def process_primary_indicator_observations(observations, *, ledger_path, recorded_at):
    rules=load_quarterly_monitoring_rules(); ledger=PrimaryIndicatorLedger(ledger_path)
    existing_ids={item.record_id for item in ledger.read_all()}; jobs_seen=set(); seen_observations=set()
    summary={'jobs_seen':0,'observations_seen':0,'recorded':0,'already_recorded':0,'held':0,'alerts':[],'holds':[]}
    for observation in observations:
        provenance=getattr(observation,'provenance',None); job_id=getattr(provenance,'job_id',None)
        binding=rules.get(job_id)
        if not binding: continue
        fingerprint=getattr(provenance,'observation_fingerprint',None) or id(observation)
        if fingerprint in seen_observations: continue
        seen_observations.add(fingerprint); jobs_seen.add(job_id); ticker,rule=binding
        summary['observations_seen']+=1
        extracted=extract_primary_indicator(observation,rule,ticker=ticker)
        if extracted['status']!='READY_TO_RECORD':
            summary['held']+=1; summary['holds'].append({'rule_id':rule['id'],'status':extracted['status']}); continue
        record_id=ledger.fingerprint(extracted['candidate'])
        ledger.record(extracted['candidate'],recorded_at=recorded_at)
        if record_id in existing_ids: summary['already_recorded']+=1
        else: summary['recorded']+=1; existing_ids.add(record_id)
        alert=ledger.latest_alert(rule)
        if alert['status'] in {'FAVOURABLE_DIRECTION','ADVERSE_DIRECTION','UNCHANGED'}: summary['alerts'].append(alert)
    summary['jobs_seen']=len(jobs_seen)
    summary.update({'creates_catalyst':False,'changes_verdict':False,'authorizes_trade':False})
    return summary


__all__=['process_primary_indicator_results','process_primary_indicator_observations']
