"""Governed weekly ingestion of official PIB crop-sowing releases."""
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
from urllib.parse import urlsplit
import uuid

from modules.company_intelligence.crop_sowing_indicator import crop_sowing_indicator_candidate,crop_mix_summary
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger
from modules.company_intelligence.quarterly_monitoring_job_provider import load_quarterly_monitoring_rules
from modules.external_intelligence.public_crop_area_record import PublicCropAreaPreview
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionAdapter
from modules.external_intelligence.trusted_public_crop_area_extractor import TrustedPublicCropAreaExtractor
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceRegistry

RULE_ID='india-crop-sowing-area'; TICKER='COROMANDEL'

def crop_area_urls_from_research(results):
    job_id=f'{TICKER}-PRIMARY-INDICATOR-{RULE_ID.upper()}'
    urls=[]
    for result in results or ():
        if getattr(result,'job_id',None)!=job_id: continue
        for selected in getattr(result,'selected_sources',()):
            url=getattr(getattr(selected,'result',None),'url','')
            parts=urlsplit(url)
            if parts.scheme=='https' and (parts.hostname or '').casefold().rstrip('.')=='www.pib.gov.in' and 'prid=' in parts.query.casefold():
                if url not in urls: urls.append(url)
    return tuple(urls[:3])

def run_automatic_crop_sowing_monitor(root, *, candidate_urls, now=None, force=False, acquirer=None, extractor=None):
    root=Path(root); now=now or datetime.now(timezone.utc)
    if now.tzinfo is None: raise ValueError('now must be timezone-aware')
    runtime=root/'data/runtime/primary_indicator_assets'; state_path=runtime/'crop_sowing_state.json'
    state=_read_state(state_path)
    if not force and state and now<datetime.fromisoformat(state['next_due_at']): return _result('NOT_DUE',state=state)
    urls=tuple(dict.fromkeys(candidate_urls or ()))[:3]
    if not urls: return _failure(state_path,now,'NO_SOURCE_DISCOVERED','No official PIB release URL was selected.')
    acquirer=acquirer or TrustedPublicAcquisitionAdapter(TrustedPublicSourceRegistry.india_primary_sources(),PublicSourceAcquisitionLedger(runtime/'crop_area_acquisitions.jsonl'))
    extractor=extractor or TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(runtime/'crop_area_extractions.jsonl'))
    job_id=f'{TICKER}-PRIMARY-INDICATOR-{RULE_ID.upper()}'; previews=[]; errors=[]
    for index,url in enumerate(urls):
        run_id=now.strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8]
        acquired=acquirer.acquire(acquisition_id=f'AGRI-SOWING-{run_id}-{index}',cycle_id=run_id,job_id=job_id,
            research_intent='PRIMARY_INDICATOR_MONITORING',url=url,recorder='EIOS_AUTOMATIC_PRIMARY_INDICATOR',requested_at=now)
        if acquired.retrieved_content is None: errors.append(f'{url}: acquisition held'); continue
        extracted=extractor.extract(acquired,extraction_id=f'AGRI-SOWING-TEXT-{run_id}-{index}',recorder='EIOS_AUTOMATIC_PRIMARY_INDICATOR')
        if extracted.extracted_text is None: errors.append(f'{url}: extraction held'); continue
        try: previews.append(TrustedPublicCropAreaExtractor().extract(acquired,extracted.receipt))
        except ValueError as exc: errors.append(f'{url}: {exc}')
    if not previews: return _failure(state_path,now,'CROP_AREA_VALUE_HELD','; '.join(errors)[:1000])
    preview=max(previews,key=lambda item:datetime.fromisoformat(item.period_label))
    binding=load_quarterly_monitoring_rules().get(job_id)
    if binding is None: raise ValueError('configured sowing monitoring rule was not found')
    _,rule=binding; candidate=crop_sowing_indicator_candidate(preview,ticker=TICKER,rule=rule)
    ledger=PrimaryIndicatorLedger(root/'data/company_intelligence/primary_indicator_records.jsonl')
    existing={item.record_id for item in ledger.read_all()}; record=ledger.record(candidate,recorded_at=now)
    saved={'schema_version':1,'status':'SUCCESS','checked_at':now.isoformat(),'next_due_at':(now+timedelta(days=7)).isoformat(),
           'source_url':record.source_url,'document_hash':record.content_fingerprint,'reporting_date':record.reporting_date,'record_id':record.record_id}
    _write_state(state_path,saved)
    return _result('ALREADY_RECORDED' if record.record_id in existing else 'RECORDED',state=saved,value=record.value,unit=record.unit,
        latest_signal=ledger.latest_alert(rule)['status'],crop_mix=crop_mix_summary(preview))

def _failure(path,now,status,detail):
    state={'schema_version':1,'status':status,'checked_at':now.isoformat(),'next_due_at':(now+timedelta(days=1)).isoformat(),'detail':detail}
    _write_state(path,state); return _result(status,state=state)
def _result(status,**values): return {'status':status,**values,'causes_rainfall':False,'creates_catalyst':False,'changes_verdict':False,'authorizes_trade':False}
def _read_state(path):
    if not Path(path).exists(): return None
    value=json.loads(Path(path).read_text(encoding='utf-8'))
    if value.get('schema_version')!=1 or not isinstance(value.get('next_due_at'),str): raise ValueError('invalid crop-sowing monitor state')
    datetime.fromisoformat(value['next_due_at']); return value
def _write_state(path,value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf-8'); temporary.replace(path)

__all__=['crop_area_urls_from_research','run_automatic_crop_sowing_monitor']
