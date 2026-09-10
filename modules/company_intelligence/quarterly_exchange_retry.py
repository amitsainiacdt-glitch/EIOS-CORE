"""Durable retry queue for issuer PDFs awaiting NSE corroboration."""
from __future__ import annotations
import json
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path

@dataclass(frozen=True)
class QuarterlyExchangeRetry:
    request_id:str;ticker:str;company:str;pdf_path:str;pdf_hash:str;source_url:str
    status:str;attempts:int;recorded_at:datetime;receipt_fingerprint:str

class QuarterlyExchangeRetryService:
    def __init__(self,path:Path,*,workspace:Path,runner=None):
        self.path=Path(path);self.workspace=Path(workspace).resolve();self.runner=runner

    def schedule(self,*,ticker,company,pdf_path,pdf_hash,source_url,recorded_at=None):
        path=self._path(pdf_path);self._verify_file(path,pdf_hash)
        request_id=sha256(f'{ticker.upper()}\n{pdf_hash}\n{source_url}'.encode()).hexdigest()
        latest=self.latest().get(request_id)
        if latest:return latest
        return self._append(request_id,ticker.upper(),company,path,pdf_hash,source_url,'WAITING_FOR_EXCHANGE',0,recorded_at)

    def retry_for(self,ticker,exchange_reports,*,recorded_at=None):
        reports=tuple(exchange_reports);results=[]
        if not reports:return ()
        for item in self.latest().values():
            if item.ticker!=ticker.upper() or item.status=='RECONCILED':continue
            try:
                path=self._path(item.pdf_path);self._verify_file(path,item.pdf_hash)
                if self.runner is None:
                    from modules.company_intelligence.quarterly_pdf_intake import run_quarterly_intake
                    runner=run_quarterly_intake
                else:runner=self.runner
                report=runner(path,workspace=self.workspace,ticker=item.ticker,company=item.company,
                    source_url=item.source_url,exchange_corroborations=reports)
                matched=int(report.get('exchange_corroboration_matches',0))
                status='RECONCILED' if matched>0 else 'WAITING_FOR_EXACT_MATCH'
            except Exception as exc:
                if isinstance(exc,(KeyboardInterrupt,SystemExit)):raise
                status='RETRY_FAILED_HOLD'
                path=self.workspace/item.pdf_path
            results.append(self._append(item.request_id,item.ticker,item.company,path,item.pdf_hash,
                item.source_url,status,item.attempts+1,recorded_at))
        return tuple(results)

    def latest(self):
        result={}
        for item in self.read_all():result[item.request_id]=item
        return result

    def read_all(self):
        if not self.path.exists():return ()
        result=[]
        for number,line in enumerate(self.path.read_text(encoding='utf-8').splitlines(),1):
            try:
                payload=json.loads(line);payload['recorded_at']=datetime.fromisoformat(payload['recorded_at'])
                item=QuarterlyExchangeRetry(**payload)
                if item.receipt_fingerprint!=self.fingerprint(item):raise ValueError('invalid receipt fingerprint')
                self._path(item.pdf_path)
                result.append(item)
            except (KeyError,TypeError,ValueError) as exc:raise ValueError(f'invalid quarterly exchange retry at line {number}: {exc}') from exc
        return tuple(result)

    def _append(self,request_id,ticker,company,path,pdf_hash,source_url,status,attempts,recorded_at):
        when=recorded_at or datetime.now(timezone.utc)
        relative=path.relative_to(self.workspace).as_posix()
        raw=QuarterlyExchangeRetry(request_id,ticker,company,relative,pdf_hash,source_url,status,attempts,when,'')
        item=QuarterlyExchangeRetry(**{**asdict(raw),'receipt_fingerprint':self.fingerprint(raw)})
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open('a',encoding='utf-8') as stream:
            payload=asdict(item);payload['recorded_at']=when.isoformat();stream.write(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n')
        return item

    def _path(self,value):
        path=Path(value);path=path if path.is_absolute() else self.workspace/path;path=path.resolve()
        if self.workspace not in path.parents:raise ValueError('retry PDF must remain inside workspace')
        return path

    @staticmethod
    def _verify_file(path,digest):
        if not path.is_file() or sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('retry PDF is missing or changed')
    @staticmethod
    def fingerprint(item):
        payload=asdict(item);payload.pop('receipt_fingerprint',None);payload['recorded_at']=item.recorded_at.isoformat()
        return sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

__all__=['QuarterlyExchangeRetry','QuarterlyExchangeRetryService']
