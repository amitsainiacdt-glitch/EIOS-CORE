"""Acquire a raw NSE UDiFF archive with provenance. No corporate action adjustment."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,time,urllib.request,zipfile
from datetime import date,datetime
from pathlib import Path

BASE="https://nsearchives.nseindia.com/content/cm/"
FIELDS={"TradDt","TckrSymb","SctySrs","OpnPric","ClsPric"}
def udiff_url(day:date):
    if day<date(2024,7,8):
        raise ValueError("UDiFF unavailable before 2024-07-08; use legacy importer")
    return BASE+f"BhavCopy_NSE_CM_0_0_0_{day:%Y%m%d}_F_0000.csv.zip"

def validate_archive(blob:bytes,day:date):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        if z.testzip() is not None:raise ValueError("Corrupt ZIP member")
        files=[x for x in z.namelist() if x.lower().endswith(".csv")]
        if len(files)!=1:raise ValueError("Expected exactly one CSV")
        with z.open(files[0]) as f:
            rd=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
            if not FIELDS.issubset(rd.fieldnames or ()):raise ValueError("Unexpected NSE UDiFF schema")
            count=0;eq_count=0;seen=set()
            for row in rd:
                count+=1
                dt=row["TradDt"].strip()
                parsed=None
                for fmt in ("%Y-%m-%d","%d-%m-%Y","%d-%b-%Y","%Y%m%d"):
                    try:parsed=datetime.strptime(dt,fmt).date();break
                    except ValueError:pass
                if parsed!=day:raise ValueError("Unexpected TradDt "+dt)
                if row["SctySrs"].strip()=="EQ":
                    eq_count+=1
                    ticker=row["TckrSymb"].strip()
                    if ticker in seen:raise ValueError("Duplicate EQ ticker")
                    seen.add(ticker)
            if count<100 or eq_count<100:raise ValueError("Insufficient daily bhavcopy rows")
            return {"rows":count,"eq_rows":eq_count,"columns":rd.fieldnames,"member":files[0]}

def download(day:date,dest:Path,tries=3,fetch=None):
    url=udiff_url(day)
    if fetch is None:
        def fetch(u):
            req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/zip","Referer":"https://www.nseindia.com/all-reports"})
            with urllib.request.urlopen(req,timeout=25) as response:
                if response.geturl()!=u:raise ValueError("Unexpected archive redirect")
                return response.read(8_000_001)
    error=None
    for attempt in range(tries):
        try:
            blob=fetch(url)
            if len(blob)>8_000_000:raise ValueError("Archive exceeds size guard")
            details=validate_archive(blob,day)
            dest.mkdir(parents=True,exist_ok=True)
            (dest/Path(url).name).write_bytes(blob)
            meta={"trade_date":day.isoformat(),"source_url":url,
                  "sha256":hashlib.sha256(blob).hexdigest(),"size_bytes":len(blob),
                  "archive_validation":details,
                  "publication_timestamp_verified":False,
                  "corporate_actions_adjusted":False,"research_backtest_admissible":False}
            (dest/"archive_manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
            return meta
        except Exception as exc:
            error=exc
            if attempt+1<tries:time.sleep(2*(attempt+1))
    raise RuntimeError("Archive acquisition/validation failed: "+str(error))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--date",required=True)
    p.add_argument("--output",default="fox_raw_archive")
    a=p.parse_args()
    print(json.dumps(download(date.fromisoformat(a.date),Path(a.output)),indent=2))
