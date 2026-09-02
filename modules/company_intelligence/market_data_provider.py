"""Provider boundary for governed market data; no provider-specific logic leaks into engines."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Protocol

from .governed_market_data import GovernedMarketData


class MarketDataProvider(Protocol):
    provider_id: str

    def fetch(self, ticker: str, *, as_of: datetime) -> GovernedMarketData: ...


@dataclass(frozen=True)
class UnconfiguredMarketDataProvider:
    provider_id: str = "UNCONFIGURED"

    def fetch(self, ticker: str, *, as_of: datetime) -> GovernedMarketData:
        """Return an explicit blocked record rather than silently returning fake data."""
        return GovernedMarketData(ticker=ticker, as_of=as_of, source_id=self.provider_id, status="STAGED")


@dataclass(frozen=True)
class JsonMarketDataProvider:
    path: Path
    provider_id: str = "LOCAL_APPROVED_FILE"

    def fetch(self, ticker: str, *, as_of: datetime) -> GovernedMarketData:
        payload = json.loads(Path(self.path).read_text(encoding="utf-8"))
        record = payload.get(ticker.upper()) or payload.get(ticker)
        if not isinstance(record, dict):
            raise KeyError(f"no market-data record for {ticker}")
        return GovernedMarketData(
            ticker=ticker.upper(), as_of=as_of,
            current_price=record.get("current_price"), volume=record.get("volume"),
            relative_performance_1y=record.get("relative_performance_1y"),
            consensus_eps=record.get("consensus_eps"), source_id=self.provider_id,
            status="GOVERNED" if record.get("approved") is True else "STAGED",
        )


__all__ = ["MarketDataProvider", "UnconfiguredMarketDataProvider", "JsonMarketDataProvider"]
