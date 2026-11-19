"""BRAVO Recovery Intelligence pilot: no data fetching or trading."""
from __future__ import annotations
from datetime import datetime
from typing import Any

WEIGHTS = {
    "causal": 25, "trend": 20, "earnings_leverage": 15,
    "cash_balance": 15, "valuation": 15, "recognition_gap": 10,
}
FATAL_FLAGS = {"material_governance", "opaque_dilution", "unfunded_cash_deficit"}

def _timestamp(value: str) -> datetime:
    d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if d.tzinfo is None or d.utcoffset() is None:
        raise ValueError("Publication and cutoff timestamps require timezone offsets")
    return d

def eligible_evidence(records: list[dict[str, Any]], cutoff: str) -> list[dict[str, Any]]:
    """Enforce publication-time, not report-period, availability."""
    end = _timestamp(cutoff)
    return [r for r in records
            if r.get("published_at") and _timestamp(r["published_at"]) <= end
            and r.get("independently_verified") is True and r.get("source_url")]

def assess(scores: dict[str, int | None], evidence: list[dict[str, Any]],
           cutoff: str, fatal_flags: list[str] | None = None) -> dict[str, Any]:
    """Research priority only. Never emits an executable BUY instruction."""
    known = eligible_evidence(evidence, cutoff)
    missing = [k for k in WEIGHTS if scores.get(k) is None]
    for key, value in scores.items():
        if key not in WEIGHTS:
            raise ValueError(f"Unexpected score: {key}")
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 5):
            raise ValueError(f"Invalid 0..5 score for {key}")
    weighted = None if missing else round(sum(scores[k] * w / 5 for k, w in WEIGHTS.items()), 1)
    mechanisms = {r.get("mechanism") for r in known if r.get("mechanism")}
    fatal = sorted(set(fatal_flags or []) & FATAL_FLAGS)
    return {
        "score": weighted, "missing_dimensions": missing,
        "valid_evidence_count": len(known), "independent_mechanisms": len(mechanisms),
        "fatal_flags": fatal,
        "research_status": (
            "BLOCKED_RISK" if fatal else
            "INSUFFICIENT_DATA" if missing or len(mechanisms) < 2 else
            "PRIORITY_RESEARCH" if weighted >= 80 else
            "INVESTIGATE" if weighted >= 60 else "INSUFFICIENT_SIGNALS"
        ),
        "trading_instruction": False, "capital_deployment_inr": 0,
    }
