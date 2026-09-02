"""Create governed, fail-closed engine work items from routed company facts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.governed_company_fact import GovernedCompanyFact
from modules.company_intelligence.governed_fact_engine_router import GovernedFactEngineRoute


REQUIRED_INPUTS = {
    "META_CAUSALITY_ANALYSIS": ("temporal sequence", "company transmission evidence", "contradiction result"),
    "CONTRADICTION_SEARCH": ("independent corroborating or disconfirming sources",),
    "COMPANY_EVENT_ANALYSIS": (),
    "FINANCIAL_IMPACT_ANALYSIS": ("audited historical financial series", "segment mapping", "quantified earnings transmission"),
    "CAPITAL_ALLOCATION_ANALYSIS": ("project cost and funding", "expected return evidence", "management delivery history"),
    "CATALYST_READINESS": ("dated trigger", "earnings transmission evidence", "invalidation conditions"),
    "EXPECTATION_GAP_ANALYSIS": ("market expectation baseline", "consensus or comparable expectation evidence", "price recognition assessment"),
    "VALUATION_IMPACT_ANALYSIS": ("approved earnings impact", "current market price", "governed valuation snapshot"),
    "MACRO_TRANSMISSION_ANALYSIS": ("authoritative macro baseline", "persistence evidence", "historical comparison"),
    "SECTOR_IMPACT_ANALYSIS": ("sector supply-demand baseline", "peer evidence", "policy and pricing context"),
    "COMPANY_EXPOSURE_ANALYSIS": ("company exposure mapping", "geographic and product mix", "management or filing confirmation"),
    "CONTINUOUS_MONITORING": (),
}


@dataclass(frozen=True)
class EngineAnalysisWorkItem:
    schema_version: int
    work_item_id: str
    route_id: str
    fact_id: str
    company: str
    analysis_queue: str
    target_layers: tuple[str, ...]
    source_url: str
    required_inputs: tuple[str, ...]
    missing_inputs: tuple[str, ...]
    intake_status: str
    created_at: datetime
    creates_evidence: bool = False
    creates_catalyst: bool = False
    changes_verdict: bool = False


class EngineAnalysisIntakeRepository:
    def __init__(self, path: Path):
        self.path = Path(path)

    def dispatch(self, fact: GovernedCompanyFact, route: GovernedFactEngineRoute, *, created_at: datetime) -> tuple[EngineAnalysisWorkItem, ...]:
        if route.fact_id != fact.fact_id:
            raise ValueError("engine route does not bind to governed fact")
        existing = {(item.fact_id, item.analysis_queue) for item in self.read_all()}
        created = []
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for queue in route.target_analysis_queues:
            if (fact.fact_id, queue) in existing:
                continue
            required = REQUIRED_INPUTS.get(queue, ("engine-specific evidence contract",))
            status = "MONITORING_ACTIVE" if queue == "CONTINUOUS_MONITORING" else ("READY_FOR_ENGINE_ANALYSIS" if not required else "WAITING_FOR_REQUIRED_INPUTS")
            work = EngineAnalysisWorkItem(
                1, sha256(f"{route.route_id}\n{queue}\nENGINE_INTAKE_V1".encode()).hexdigest(),
                route.route_id, fact.fact_id, fact.company, queue, route.target_layers,
                fact.source_url, required, required, status, created_at,
            )
            payload = asdict(work); payload["created_at"] = created_at.isoformat()
            with self.path.open("a", encoding="utf-8") as ledger:
                ledger.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
            created.append(work)
        return tuple(created)

    def read_all(self) -> tuple[EngineAnalysisWorkItem, ...]:
        if not self.path.is_file():
            return ()
        result, identities = [], set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
                for key in ("target_layers", "required_inputs", "missing_inputs"):
                    payload[key] = tuple(payload[key])
                payload["created_at"] = datetime.fromisoformat(payload["created_at"])
                item = EngineAnalysisWorkItem(**payload)
                identity = (item.fact_id, item.analysis_queue)
                if item.schema_version != 1 or identity in identities:
                    raise ValueError("invalid or duplicate engine intake")
                if item.creates_evidence or item.creates_catalyst or item.changes_verdict:
                    raise ValueError("engine intake exceeded its authority")
                identities.add(identity); result.append(item)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid engine intake at line {number}: {exc}") from exc
        return tuple(result)


__all__ = ["EngineAnalysisIntakeRepository", "EngineAnalysisWorkItem", "REQUIRED_INPUTS"]
