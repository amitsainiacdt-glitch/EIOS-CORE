"""FOX NSE UDiFF daily bhavcopy import with conservative adjustment provenance.

Input is an independently obtained ZIP from the official NSE UDiFF archive.
Original prices remain UNVERIFIED for historical return purposes until a
separate corporate-action ledger attests both its adjustments and coverage.
"""
from __future__ import annotations
import csv
import hashlib
import io
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REQUIRED={"TckrSymb","SctySrs","TradDt","OpnPric","ClsPric"}

@dataclass(frozen=True)
class RawExchangeBar:
    ticker:str
    series:str
    session:str
    open:float
    close:float
    archive_sha256:str
    source_archive:str
    verified_adjusted:bool=False

def _date(s):
    s=s.strip()
    for pattern in ("%Y-%m-%d","%d-%m-%Y","%d-%b-%Y","%Y%m%d"):
        try:return date.fromisoformat(__import__("datetime").datetime.strptime(s,pattern).date().isoformat()).isoformat()
        except ValueError:pass
    raise ValueError("Unknown trade-date representation: "+s)

def parse_udiff_zip(blob:bytes,source_url:str,series="EQ",tickers=None):
    if not source_url.startswith("https://nsearchives.nseindia.com/content/cm/"):
        raise ValueError("Official NSE archive provenance URL required")
    selected=set(tickers or ())
    digest=hashlib.sha256(blob).hexdigest()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names=[x for x in z.namelist() if x.lower().endswith(".csv") and not x.startswith("__MACOSX")]
        if len(names)!=1:raise ValueError("Expected exactly one UDiFF CSV in ZIP")
        rows=csv.DictReader(io.StringIO(z.read(names[0]).decode("utf-8-sig")))
        if not REQUIRED.issubset(set(rows.fieldnames or [])):
            raise ValueError("Unexpected UDiFF header; schema verification required")
        out=[]
        for r in rows:
            if r["SctySrs"].strip()!=series:continue
            ticker=r["TckrSymb"].strip()
            if selected and ticker not in selected:continue
            op=float(r["OpnPric"]); cl=float(r["ClsPric"])
            if not (op>0 and cl>0):raise ValueError("Nonpositive price in archive")
            out.append(RawExchangeBar(ticker,series,_date(r["TradDt"]),op,cl,digest,source_url))
    return out

def certify_adjusted(raw_bars,adjustment_factors,reviewed_tickers):
    """Explicit CA attestation required; factor is adjusted/raw price.

    This DOES NOT establish review authenticity. Operator must separately
    document split, bonus, rights and symbol-change history and keep evidence.
    """
    from modules.validation.fox_backtest import PriceBar
    reviewed=set(reviewed_tickers)
    out={}
    for b in raw_bars:
        if b.ticker not in reviewed:
            continue
        key=(b.ticker,b.session)
        if key not in adjustment_factors:
            continue
        factor=float(adjustment_factors[key])
        if factor<=0:raise ValueError("Invalid corporate-action factor")
        out.setdefault(b.ticker,[]).append(PriceBar(b.session,b.open*factor,b.close*factor,True))
    return out
