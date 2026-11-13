"""FOX raw historical-price continuity audit.

No inference from raw observations to investment returns. A fully populated
collection is still NOT adjusted or certified backtest-ready.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class CoverageResult:
    status: str
    observed_sessions: int
    company_sessions: int
    missing_ticker_sessions: tuple[str,...]
    identifier_changes: tuple[str,...]
    series_changes: tuple[str,...]
    backtest_admissible: bool = False

def check_raw_continuity(records: Iterable[dict], expected_sessions: list[str], ticker: str) -> CoverageResult:
    if not expected_sessions or sorted(set(expected_sessions)) != expected_sessions:
        raise ValueError("Expected sessions must be explicit, unique and sorted")
    rows=sorted((r for r in records if r.get("ticker")==ticker),key=lambda r:r.get("session",""))
    by_session={}
    duplicates=[]
    for row in rows:
        session=row["session"]
        if session in by_session:
            duplicates.append(session)
        by_session[session]=row
    missing=tuple(x for x in expected_sessions if x not in by_session)
    extra=tuple(x for x in by_session if x not in expected_sessions)
    id_changes=[]
    s_changes=[]
    previous=None
    for row in rows:
        if previous is not None:
            if row["isin"] != previous["isin"]:
                id_changes.append(previous["session"]+" -> "+row["session"]+": "+previous["isin"]+" -> "+row["isin"])
            if row["series"] != previous["series"]:
                s_changes.append(previous["session"]+" -> "+row["session"]+": "+previous["series"]+" -> "+row["series"])
        previous=row
    if duplicates or missing or extra:
        status="INCOMPLETE"
    elif id_changes or s_changes:
        status="NEEDS_LINEAGE_AND_LIQUIDITY_REVIEW"
    else:
        status="RAW_CONTINUOUS_UNADJUSTED"
    return CoverageResult(status,len(set(row["session"] for row in rows)),len(rows),
                          tuple([*missing,*("DUPLICATE:"+x for x in duplicates),
                                *("UNEXPECTED:"+x for x in extra)]),
                          tuple(id_changes),tuple(s_changes))
