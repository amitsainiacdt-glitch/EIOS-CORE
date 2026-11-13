"""FOX dataset admissibility audit. No market data is downloaded or invented.

A source ledger may include verified filings before prices have been obtained.
Only rows with validated timestamps and adjusted price data can enter replay.
"""
from __future__ import annotations
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

IST=ZoneInfo("Asia/Kolkata")
REQUIRED=("event_id","ticker","source_url","published_at_ist","source_timestamp_verified",
          "evidence_cutoff_ist","case_type","action","sector","price_adjustments_verified")
CASE_TYPES={"candidate","negative_control","missed_opportunity","delisted"}
ACTIONS={"INVESTIGATE","NO NEW INFLECTION","REJECT"}

@dataclass(frozen=True)
class Audit:
    total:int
    admissible:int
    blocked:int
    errors:tuple[str,...]
    counts_by_type:dict[str,int]
    counts_by_sector:dict[str,int]
    minimum_100_met:bool

def _dt(s):
    t=datetime.fromisoformat(s)
    if t.tzinfo is None:
        raise ValueError("Timestamp must include timezone")
    return t.astimezone(IST)

def audit(rows):
    problems=[]
    admissible=0
    ids=set()
    types=Counter()
    sectors=Counter()
    items=list(rows)
    for rowno,r in enumerate(items,2):
        errs=[]
        missing=[key for key in REQUIRED if key not in r]
        if missing:
            errs.append("Missing fields: "+", ".join(missing))
        ident=r.get("event_id","")
        if not ident or ident in ids:
            errs.append("Missing or duplicate event ID")
        ids.add(ident)
        kind=r.get("case_type","")
        if kind not in CASE_TYPES: errs.append("Invalid case_type")
        types[kind]+=1
        sectors[r.get("sector","unknown") or "unknown"]+=1
        if r.get("action") not in ACTIONS: errs.append("Invalid action")
        if not r.get("source_url","").startswith("https://"):
            errs.append("Missing HTTPS primary filing URL")
        if r.get("source_timestamp_verified","").lower() != "yes":
            errs.append("Publication timestamp unverified")
        if r.get("price_adjustments_verified","").lower() != "yes":
            errs.append("Adjusted prices unverified")
        try:
            t=_dt(r.get("published_at_ist",""))
            cutoff=_dt(r.get("evidence_cutoff_ist",""))
            if cutoff>t: errs.append("Look-ahead evidence")
        except (ValueError,TypeError):
            errs.append("Missing/invalid timestamp with UTC offset")
        if errs:
            problems.append(f"row {rowno} {ident}: "+"; ".join(errs))
        else:
            admissible+=1
    return Audit(len(items),admissible,len(items)-admissible,tuple(problems),
                 dict(types),dict(sectors),admissible>=100)

def audit_csv(path):
    with open(path,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or any(x not in reader.fieldnames for x in REQUIRED):
            raise ValueError("Missing required CSV headers")
        return audit(reader)

if __name__=="__main__":
    import argparse,json
    from dataclasses import asdict
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger")
    args=p.parse_args()
    print(json.dumps(asdict(audit_csv(args.ledger)),indent=2))
