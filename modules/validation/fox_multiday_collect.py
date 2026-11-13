"""FOX bounded multi-session NSE collection; raw data, never adjusted or backtest-ready.

The requested date list is explicit: do not fill missing dates with invented bars.
Store individual archive manifests and a cross-session ISIN/ticker integrity report.
"""
from __future__ import annotations
import argparse,csv,json
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path
from modules.validation.fox_archive_collect import download,udiff_url
from modules.validation.fox_nse_import import parse_udiff_zip

PILOT=("ANUP","IRMENERGY","PIIND","SUPRIYA","TIMETECHNO","APTUS",
       "TANLA","DCBBANK","J&KBANK","ASHOKA","NCC","KEC","BLS","CLEAN",
       "SHARDACROP","CYIENTDLM","ELECON","CCL","V2RETAIL","GANDHAR")
MAX_DAYS=7

def _isin_rows(data):
    import io,zipfile
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        with z.open(next(n for n in z.namelist() if n.lower().endswith(".csv"))) as f:
            rd=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
            isin_col=next((x for x in ("ISIN","ISINCode","ISINCodeX","ISINCd") if x in (rd.fieldnames or ())),None)
            if not isin_col:
                raise ValueError("ISIN column not present: cannot certify identifier continuity")
            rows={}
            for r in rd:
                if r["SctySrs"].strip()!="EQ":continue
                ticker=r["TckrSymb"].strip()
                if ticker in PILOT:
                    rows[ticker]=r[isin_col].strip()
            return rows

def collect(days,output,fetch=None):
    requested=[date.fromisoformat(s) if isinstance(s,str) else s for s in days]
    if not requested or len(requested)>MAX_DAYS or len(set(requested))!=len(requested):
        raise ValueError("Specify 1–7 distinct trade dates")
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    collected=[];errors=[];records=[];seen_isins=defaultdict(set)
    for d in sorted(requested):
        day_dir=output/d.isoformat()
        try:
            metadata=download(d,day_dir,tries=1,fetch=fetch)
            archive_file=day_dir/Path(udiff_url(d)).name
            archive=archive_file.read_bytes()
            bars=parse_udiff_zip(archive,metadata["source_url"],tickers=PILOT)
            isins=_isin_rows(archive)
            for b in bars:
                identifier=isins.get(b.ticker,"")
                if not identifier:raise ValueError("Missing ISIN for "+b.ticker)
                seen_isins[b.ticker].add(identifier)
                records.append({"ticker":b.ticker,"isin":identifier,"session":b.session,
                                "raw_open":b.open,"raw_close":b.close,"zip_sha256":metadata["sha256"],
                                "source_url":metadata["source_url"],"verified_adjusted":"no",
                                "backtest_admissible":"no"})
            collected.append({"date":d.isoformat(),"rows":len(bars),"sha256":metadata["sha256"]})
        except Exception as exc:
            errors.append({"date":d.isoformat(),"error":str(exc)})
    with (output/"pilot_raw_prices.csv").open("w",newline="",encoding="utf-8") as f:
        fields=("ticker","isin","session","raw_open","raw_close","zip_sha256",
                "source_url","verified_adjusted","backtest_admissible")
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(records)
    summary={"requested_dates":[x.isoformat() for x in requested],
             "collected_sessions":collected,"failed_dates":errors,
             "rows":len(records),"distinct_tickers":len({x["ticker"] for x in records}),
             "missing_pilot_tickers":sorted(set(PILOT)-{x["ticker"] for x in records}),
             "identifier_conflicts":{k:sorted(v) for k,v in seen_isins.items() if len(v)>1},
             "corporate_action_adjusted":False,"backtest_admissible":False}
    (output/"collection_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--dates",required=True,help="Comma-separated explicit session dates, max seven")
    ap.add_argument("--output",default="fox_multiday_raw")
    args=ap.parse_args()
    result=collect([x.strip() for x in args.dates.split(",")],args.output)
    print(json.dumps(result,indent=2))
    if result["failed_dates"] or result["identifier_conflicts"]:
        raise SystemExit(2)
