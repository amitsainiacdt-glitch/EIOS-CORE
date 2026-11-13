"""FOX auditable raw NSE multi-batch history collection.

Explicit trading dates only. A missing session is a failure, not an inferred holiday.
Produces raw-price CSV and provenance manifest, NEVER adjusted performance values.
"""
from __future__ import annotations
import argparse,csv,json
from datetime import date
from pathlib import Path
from modules.validation.fox_multiday_collect import collect,PILOT,MAX_DAYS

FIELDS=("ticker","isin","series","session","raw_open","raw_close","zip_sha256",
        "source_url","verified_adjusted","backtest_admissible")

def collect_history(sessions,output,fetch=None):
    dates=[date.fromisoformat(x) if isinstance(x,str) else x for x in sessions]
    if not dates or len(set(dates))!=len(dates):
        raise ValueError("Nonempty, unique, explicitly supplied trading sessions required")
    if dates!=sorted(dates):
        raise ValueError("Trading dates must be sorted")
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    all_rows=[];all_days=[];errors=[];seen={}
    for first in range(0,len(dates),MAX_DAYS):
        chunk=dates[first:first+MAX_DAYS]
        directory=out/f"batch_{first//MAX_DAYS+1:03d}"
        summary=collect(chunk,directory,fetch=fetch)
        all_days.extend(summary["collected_sessions"])
        errors.extend(summary["failed_dates"])
        with (directory/"pilot_raw_prices.csv").open(newline="",encoding="utf-8") as f:
            for row in csv.DictReader(f):
                k=(row["ticker"],row["session"])
                if k in seen:
                    errors.append({"date":row["session"],"error":f"Duplicate ticker/session: {k}"})
                else:
                    seen[k]=row
                    all_rows.append(row)
    all_rows.sort(key=lambda r:(r["session"],r["ticker"]))
    with (out/"raw_history.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(all_rows)
    actual_days={x["date"] for x in all_days}
    absent=sorted({x.isoformat() for x in dates}-actual_days)
    if absent:
        errors.append({"date":",".join(absent),"error":"Missing explicitly requested exchange session"})
    per_ticker={}
    for t in PILOT:
        rows=[x for x in all_rows if x["ticker"]==t]
        per_ticker[t]={"sessions":len(rows),
                       "series":sorted({x["series"] for x in rows}),
                       "isins":sorted({x["isin"] for x in rows}),
                       "missing_days":sorted(actual_days-{x["session"] for x in rows})}
    status="RAW_COMPLETE" if not errors else "RAW_INCOMPLETE"
    audit={"status":status,"requested_sessions":[x.isoformat() for x in dates],
           "verified_archive_sessions":sorted(actual_days),
           "failed_or_missing":errors,"raw_rows":len(all_rows),
           "companies_with_any_prices":sum(v["sessions"]>0 for v in per_ticker.values()),
           "coverage":per_ticker,
           "corporate_action_adjusted":False,"historical_returns_admissible":False,
           "capital_deployment_rupees":0}
    (out/"history_manifest.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    return audit

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--dates",required=True,help="Explicit comma-separated exchange session dates")
    a.add_argument("--output",default="fox_raw_history")
    args=a.parse_args()
    result=collect_history([x.strip() for x in args.dates.split(",")],args.output)
    print(json.dumps(result,indent=2))
    if result["status"]!="RAW_COMPLETE":
        raise SystemExit(2)
