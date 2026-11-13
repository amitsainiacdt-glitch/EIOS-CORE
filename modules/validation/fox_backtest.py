"""FOX point-in-time backtest. Research only; no orders or trading authorization."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from bisect import bisect_right
from zoneinfo import ZoneInfo
from math import isfinite
from statistics import mean, median
from typing import Mapping, Sequence
import csv
import json

IST=ZoneInfo("Asia/Kolkata")
HORIZONS=(63,126,252)

@dataclass(frozen=True)
class Event:
    event_id:str
    ticker:str
    published_at_ist:str
    source_url:str
    action:str
    evidence_cutoff_ist:str
    sector:str=""
    control_group:str=""

@dataclass(frozen=True)
class PriceBar:
    session:str
    open:float
    close:float
    verified_adjusted:bool=True

@dataclass(frozen=True)
class Outcome:
    event_id:str
    ticker:str
    action:str
    entry_session:str|None
    entry_price:float|None
    returns_percent:dict[int,float|None]
    excess_return_percent:dict[int,float|None]
    status:str
    reason:str
    capital_deployment_rupees:int=0

def parse_ist(s):
    d=datetime.fromisoformat(s)
    if d.tzinfo is None:
        raise ValueError("Publication timestamp must contain an explicit timezone")
    return d.astimezone(IST)

def verify_event(e):
    if not e.event_id or not e.ticker:
        raise ValueError("Missing event identifier or ticker")
    if e.action not in ("INVESTIGATE","NO NEW INFLECTION","REJECT"):
        raise ValueError("Invalid triage action; research ADD belongs to another model")
    if not e.source_url.startswith("https://"):
        raise ValueError("Primary source URL required")
    p=parse_ist(e.published_at_ist)
    if parse_ist(e.evidence_cutoff_ist)>p:
        raise ValueError("Look-ahead: evidence cutoff after publication")
    return p

def valid_bars(bars):
    b=sorted(bars,key=lambda x:x.session)
    if len({x.session for x in b})!=len(b):
        raise ValueError("Duplicate trading session")
    for x in b:
        datetime.strptime(x.session,"%Y-%m-%d")
        if not x.verified_adjusted:
            raise ValueError("Unverified adjusted OHLCV is prohibited")
        if not all(isfinite(z) and z>0 for z in (x.open,x.close)):
            raise ValueError("Missing or nonpositive adjusted price")
    return b

def net_return(a,b,cost_bps):
    return 100*((b/a)*(1-cost_bps/10000)-1)

def replay_event(event,prices,benchmark=None,benchmark_key="NIFTY500",
                 cost_bps=40,as_of_session=None):
    published=verify_event(event)
    if not(isfinite(cost_bps) and 0<=cost_bps<10000):
        raise ValueError("Invalid total round-trip cost")
    bars=valid_bars(prices.get(event.ticker,()))
    empty={h:None for h in HORIZONS}
    if not bars:
        return Outcome(event.event_id,event.ticker,event.action,None,None,
                       empty,empty.copy(),"UNSCORABLE","No validated adjusted price history")
    # Strictly next daily session prevents same-session publication hindsight.
    idx=bisect_right([x.session for x in bars],published.date().isoformat())
    if idx==len(bars):
        return Outcome(event.event_id,event.ticker,event.action,None,None,
                       empty,empty.copy(),"CENSORED","No subsequent trading session")
    entry=bars[idx]
    if as_of_session is not None and entry.session>as_of_session:
        raise ValueError("Entry after backtest as-of date")
    bench=valid_bars((benchmark or {}).get(benchmark_key,()))
    bi={x.session:i for i,x in enumerate(bench)}
    entry_bi=bi.get(entry.session)
    returns,excess={},{}
    for h in HORIZONS:
        end_idx=idx+h
        if end_idx>=len(bars) or (as_of_session is not None and bars[end_idx].session>as_of_session):
            returns[h]=excess[h]=None
            continue
        end=bars[end_idx]
        returns[h]=round(net_return(entry.open,end.close,cost_bps),3)
        end_bi=bi.get(end.session)
        excess[h]=(round(returns[h]-net_return(bench[entry_bi].open,bench[end_bi].close,cost_bps),3)
                   if entry_bi is not None and end_bi is not None else None)
    complete=sum(v is not None for v in returns.values())
    status="MATURE" if complete==len(HORIZONS) else "PARTIAL" if complete else "CENSORED"
    return Outcome(event.event_id,event.ticker,event.action,entry.session,entry.open,
                   returns,excess,status,"" if complete else "Forward horizon not yet observable")

def summarize(outcomes,horizon=126):
    if horizon not in HORIZONS:
        raise ValueError("Unsupported horizon")
    observed=[o for o in outcomes if o.returns_percent[horizon] is not None]
    flagged=[o for o in observed if o.action=="INVESTIGATE"]
    negative=[o for o in observed if o.action!="INVESTIGATE"]
    def hit(items):
        return round(100*sum(o.returns_percent[horizon]>0 for o in items)/len(items),2) if items else None
    excess=[o.excess_return_percent[horizon] for o in flagged if o.excess_return_percent[horizon] is not None]
    return {"horizon_sessions":horizon,"events_total":len(outcomes),
            "observed_total":len(observed),"censored_or_unscorable":len(outcomes)-len(observed),
            "flagged_observed":len(flagged),"nonflagged_observed":len(negative),
            "flagged_hit_rate_percent":hit(flagged),
            "nonflagged_positive_return_rate_percent":hit(negative),
            "flagged_mean_net_return_percent":round(mean(o.returns_percent[horizon] for o in flagged),2) if flagged else None,
            "flagged_median_net_return_percent":round(median(o.returns_percent[horizon] for o in flagged),2) if flagged else None,
            "flagged_mean_excess_percent":round(mean(excess),2) if excess else None,
            "flagged_excess_hit_rate_percent":round(100*sum(x>0 for x in excess)/len(excess),2) if excess else None,
            "warnings":["Selection bias, overlapping events and multiple testing require separate controls",
                        "Missed opportunities require a predeclared complete opportunity universe",
                        "Not a research ADD engine, order simulator or causal estimate"],
            "capital_deployment_rupees":0}

def read_events(path):
    with open(path,newline="",encoding="utf-8") as f:
        return [Event(**r) for r in csv.DictReader(f)]

def read_prices(path):
    out={}
    with open(path,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            adjusted=r.get("verified_adjusted","").lower() in ("true","1","yes")
            out.setdefault(r["ticker"],[]).append(PriceBar(r["session"],float(r["open"]),float(r["close"]),adjusted))
    return out

def run(events,prices,benchmark=None,as_of_session=None,cost_bps=40):
    outcomes=[replay_event(e,prices,benchmark,cost_bps=cost_bps,as_of_session=as_of_session)
              for e in events]
    return {"status":"RESEARCH VALIDATION ONLY — NOT A TRADING SYSTEM",
            "outcomes":[asdict(o) for o in outcomes],
            "summary":{str(h):summarize(outcomes,h) for h in HORIZONS},
            "capital_deployment_rupees":0}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--events",required=True)
    p.add_argument("--prices",required=True)
    p.add_argument("--benchmarks")
    p.add_argument("--as-of-session")
    p.add_argument("--cost-bps",type=float,default=40)
    p.add_argument("--output")
    a=p.parse_args()
    report=run(read_events(a.events),read_prices(a.prices),
               read_prices(a.benchmarks) if a.benchmarks else None,
               a.as_of_session,a.cost_bps)
    result=json.dumps(report,indent=2)
    if a.output:
        with open(a.output,"w",encoding="utf-8") as f:
            f.write(result+"\n")
    else:
        print(result)
