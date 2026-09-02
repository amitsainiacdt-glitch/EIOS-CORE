"""Typed staging record for quarterly company financials."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuarterlyFinancialRecord:
    ticker: str
    quarter: str
    revenue: float | None = None
    ebitda: float | None = None
    pat: float | None = None
    operating_cash_flow: float | None = None
    source_id: str | None = None
    status: str = "STAGED"

    def __post_init__(self) -> None:
        if not self.ticker.strip() or not self.quarter.strip():
            raise ValueError("ticker and quarter are required")
        if self.status == "GOVERNED" and not self.source_id:
            raise ValueError("governed quarterly data requires a source identifier")
        for name in ("revenue", "ebitda", "pat", "operating_cash_flow"):
            value = getattr(self, name)
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric or null")

    @property
    def has_core_metrics(self) -> bool:
        return self.revenue is not None and self.pat is not None
