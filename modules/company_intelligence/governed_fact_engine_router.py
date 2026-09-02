"""Route governed company facts into analysis queues without running a verdict engine."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.governed_company_fact import GovernedCompanyFact


DIRECT_COMPANY_EVENTS = {"ORDER_CONTRACT", "TENDER", "REGULATORY_APPROVAL", "CAPACITY_CHANGE", "SUPPLIER_CUSTOMER", "EXECUTION_UPDATE"}
AGRI_SYSTEM_EVENTS = {"WEATHER_ANOMALY", "HYDROLOGY", "CROP_PROGRESS", "SATELLITE_CROP_CONDITION", "FERTILIZER_MARKET", "FOOD_STOCK_POLICY", "AGRI_PRICE_SUPPLY_CHAIN", "RURAL_DEMAND", "GLOBAL_INPUT_COST"}


@dataclass(frozen=True)
class GovernedFactEngineRoute:
    schema_version: int
    route_id: str
    fact_id: str
    company: str
    event_type: str
    target_layers: tuple[str, ...]
    target_analysis_queues: tuple[str, ...]
    required_follow_up: tuple[str, ...]
    routed_at: datetime
    status: str = "QUEUED_FOR_ENGINE_ANALYSIS"
    creates_evidence: bool = False
    creates_catalyst: bool = False
    changes_verdict: bool = False


class GovernedFactEngineRouter:
    def __init__(self, path: Path):
        self.path = Path(path)

    def route(self, fact: GovernedCompanyFact, *, routed_at: datetime) -> GovernedFactEngineRoute:
        if not isinstance(fact, GovernedCompanyFact) or fact.status != "GOVERNED_FACT":
            raise ValueError("routing requires a governed company fact")
        if any(item.fact_id == fact.fact_id for item in self.read_all()):
            raise ValueError("governed fact is already routed")
        layers, queues, follow_up = self._targets(fact)
        route = GovernedFactEngineRoute(
            1,
            sha256(f"{fact.fact_id}\nENGINE_ROUTE_V1".encode()).hexdigest(),
            fact.fact_id, fact.company, fact.event_type, layers, queues, follow_up,
            routed_at,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(route)
        payload["routed_at"] = routed_at.isoformat()
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return route

    def read_all(self) -> tuple[GovernedFactEngineRoute, ...]:
        if not self.path.is_file():
            return ()
        result, route_ids, fact_ids = [], set(), set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
                payload["target_layers"] = tuple(payload["target_layers"])
                payload["target_analysis_queues"] = tuple(payload["target_analysis_queues"])
                payload["required_follow_up"] = tuple(payload["required_follow_up"])
                payload["routed_at"] = datetime.fromisoformat(payload["routed_at"])
                item = GovernedFactEngineRoute(**payload)
                if item.schema_version != 1 or item.route_id in route_ids or item.fact_id in fact_ids:
                    raise ValueError("invalid or duplicate engine route")
                if item.creates_evidence or item.creates_catalyst or item.changes_verdict:
                    raise ValueError("engine route exceeded its authority")
                route_ids.add(item.route_id); fact_ids.add(item.fact_id); result.append(item)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid governed fact route at line {number}: {exc}") from exc
        return tuple(result)

    @staticmethod
    def _targets(fact: GovernedCompanyFact):
        layers = {"meta_causality", "risks_and_contradictions", "monitoring"}
        queues = {"META_CAUSALITY_ANALYSIS", "CONTRADICTION_SEARCH", "CONTINUOUS_MONITORING"}
        follow_up = {"Verify earnings transmission", "Search for disconfirming evidence"}
        if fact.event_type in DIRECT_COMPANY_EVENTS:
            layers.update({"news_and_filings", "company_events", "financials", "catalysts", "expectations", "valuation"})
            queues.update({"COMPANY_EVENT_ANALYSIS", "FINANCIAL_IMPACT_ANALYSIS", "CATALYST_READINESS", "EXPECTATION_GAP_ANALYSIS", "VALUATION_IMPACT_ANALYSIS"})
            follow_up.update({"Confirm timing and execution", "Compare against market expectations", "Quantify revenue, margin, cash-flow and valuation impact"})
        if fact.event_type == "CAPACITY_CHANGE":
            layers.add("management"); queues.add("CAPITAL_ALLOCATION_ANALYSIS"); follow_up.add("Test management capital-allocation discipline")
        if fact.event_type == "POLICY_REGULATION" or fact.event_type in AGRI_SYSTEM_EVENTS:
            layers.update({"macro", "sector", "micro", "catalysts", "expectations", "valuation"})
            queues.update({"MACRO_TRANSMISSION_ANALYSIS", "SECTOR_IMPACT_ANALYSIS", "COMPANY_EXPOSURE_ANALYSIS", "CATALYST_READINESS", "EXPECTATION_GAP_ANALYSIS", "VALUATION_IMPACT_ANALYSIS"})
            follow_up.update({"Prove sector-to-company transmission", "Check persistence and timing", "Compare against market expectations"})
        return tuple(sorted(layers)), tuple(sorted(queues)), tuple(sorted(follow_up))


__all__ = ["GovernedFactEngineRoute", "GovernedFactEngineRouter"]
