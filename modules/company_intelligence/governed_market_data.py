"""Fail-closed contract for market data used by valuation and expectation analysis."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GovernedMarketData:
    ticker: str
    as_of: datetime
    current_price: float | None = None
    volume: float | None = None
    relative_performance_1y: float | None = None
    consensus_eps: float | None = None
    source_id: str | None = None
    status: str = "STAGED"

    def __post_init__(self) -> None:
        if not self.ticker.strip() or not isinstance(self.as_of, datetime):
            raise ValueError("ticker and timestamp are required")
        for name in ("current_price", "volume", "relative_performance_1y", "consensus_eps"):
            value = getattr(self, name)
            if value is not None and value < 0 and name in {"current_price", "volume"}:
                raise ValueError(f"{name} cannot be negative")
        if self.status == "GOVERNED" and not self.source_id:
            raise ValueError("governed market data requires a source identifier")

    @property
    def ready_for_valuation(self) -> bool:
        return self.status == "GOVERNED" and self.current_price is not None and self.consensus_eps is not None

    def gate(self) -> dict:
        return {
            "status": "READY" if self.ready_for_valuation else "BLOCKED_MISSING_MARKET_DATA",
            "ticker": self.ticker,
            "asOf": self.as_of.isoformat(),
            "sourceId": self.source_id,
            "requiredInputs": {
                "currentPrice": self.current_price is not None,
                "consensusEps": self.consensus_eps is not None,
                "volume": self.volume is not None,
                "relativePerformance": self.relative_performance_1y is not None,
            },
            "plainEnglish": "Price and expectations are ready for valuation." if self.ready_for_valuation else "Valuation remains blocked until a governed price and expectation benchmark share a timestamp.",
        }
