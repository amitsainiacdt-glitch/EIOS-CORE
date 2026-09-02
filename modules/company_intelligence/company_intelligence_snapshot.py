"""Canonical backend-to-UI contract for one governed company intelligence state."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Mapping


class IntelligenceLayerStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PARTIAL = "PARTIAL"
    READY = "READY"
    RESEARCH_HOLD = "RESEARCH_HOLD"
    STALE = "STALE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class IntelligenceLayer:
    status: IntelligenceLayerStatus
    summary: str
    source_ids: tuple[str, ...] = ()
    fact_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    as_of: datetime | None = None
    coverage_percent: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.status, IntelligenceLayerStatus):
            raise ValueError("status must be an IntelligenceLayerStatus")
        if not self.summary.strip():
            raise ValueError("summary must not be empty")
        if not 0 <= self.coverage_percent <= 100:
            raise ValueError("coverage_percent must be between 0 and 100")
        if self.status == IntelligenceLayerStatus.READY and self.coverage_percent != 100:
            raise ValueError("a READY layer must have 100 percent coverage")
        if self.status == IntelligenceLayerStatus.READY and not self.source_ids:
            raise ValueError("a READY layer must cite at least one source")


MANDATORY_VERDICT_LAYERS = (
    "identity",
    "financials",
    "macro",
    "sector",
    "micro",
    "news_and_filings",
    "company_events",
    "meta_causality",
    "catalysts",
    "expectations",
    "management",
    "competition",
    "risks_and_contradictions",
    "valuation",
    "master_dossier",
    "monitoring",
)


@dataclass(frozen=True)
class CompanyIntelligenceSnapshot:
    schema_version: int
    snapshot_id: str
    company_name: str
    ticker: str
    generated_at: datetime
    layers: Mapping[str, IntelligenceLayer]
    verdict_status: str
    verdict: str | None = None
    confidence_percent: float | None = None
    verdict_reasons: tuple[str, ...] = ()
    unresolved_gaps: tuple[str, ...] = ()
    creates_recommendation: bool = False
    requires_human_review: bool = True

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("unsupported snapshot schema_version")
        if not self.snapshot_id.strip() or not self.company_name.strip() or not self.ticker.strip():
            raise ValueError("snapshot identity fields must not be empty")
        missing = set(MANDATORY_VERDICT_LAYERS) - set(self.layers)
        if missing:
            raise ValueError(f"mandatory layers are missing: {sorted(missing)}")
        if self.verdict_status == "READY":
            not_ready = [name for name in MANDATORY_VERDICT_LAYERS if self.layers[name].status != IntelligenceLayerStatus.READY]
            if not_ready:
                raise ValueError(f"verdict cannot be READY while layers are incomplete: {not_ready}")
            if not self.verdict or self.confidence_percent is None:
                raise ValueError("a READY verdict requires verdict text and confidence")
        if self.creates_recommendation:
            raise ValueError("snapshot assembly cannot itself create a recommendation")

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["generated_at"] = self.generated_at.isoformat()
        for layer in payload["layers"].values():
            layer["status"] = layer["status"].value
            if layer["as_of"] is not None:
                layer["as_of"] = layer["as_of"].isoformat()
            layer["source_ids"] = list(layer["source_ids"])
            layer["fact_ids"] = list(layer["fact_ids"])
            layer["warnings"] = list(layer["warnings"])
        payload["verdict_reasons"] = list(payload["verdict_reasons"])
        payload["unresolved_gaps"] = list(payload["unresolved_gaps"])
        return payload


def assess_verdict_readiness(layers: Mapping[str, IntelligenceLayer]) -> tuple[str, tuple[str, ...]]:
    gaps = []
    for name in MANDATORY_VERDICT_LAYERS:
        layer = layers.get(name)
        if layer is None:
            gaps.append(f"{name}: layer missing")
        elif layer.status != IntelligenceLayerStatus.READY:
            gaps.append(f"{name}: {layer.status.value}")
    return ("READY" if not gaps else "RESEARCH_HOLD", tuple(gaps))


__all__ = [
    "CompanyIntelligenceSnapshot",
    "IntelligenceLayer",
    "IntelligenceLayerStatus",
    "MANDATORY_VERDICT_LAYERS",
    "assess_verdict_readiness",
]
