"""Process primary-indicator observations produced by one automatic cycle."""
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger, extract_primary_indicator
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_rules


def process_primary_indicator_results(results, *, ledger_path, recorded_at):
    rules=load_quarterly_monitoring_rules(); ledger=PrimaryIndicatorLedger(ledger_path)
    summary={'jobs_seen':0,'observations_seen':0,'recorded':0,'held':0,'alerts':[],'holds':[]}
    for result in results:
        binding=rules.get(getattr(result,'job_id',None))
        if not binding: continue
        summary['jobs_seen']+=1; ticker,rule=binding
        for observation in result.observations:
            summary['observations_seen']+=1
            extracted=extract_primary_indicator(observation,rule,ticker=ticker)
            if extracted['status']!='READY_TO_RECORD':
                summary['held']+=1; summary['holds'].append({'rule_id':rule['id'],'status':extracted['status']}); continue
            ledger.record(extracted['candidate'],recorded_at=recorded_at); summary['recorded']+=1
            alert=ledger.latest_alert(rule)
            if alert['status'] in {'FAVOURABLE_DIRECTION','ADVERSE_DIRECTION','UNCHANGED'}: summary['alerts'].append(alert)
    summary.update({'creates_catalyst':False,'changes_verdict':False,'authorizes_trade':False})
    return summary


__all__=['process_primary_indicator_results']
