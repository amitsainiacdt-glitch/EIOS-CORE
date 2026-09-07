"""Typed staging record for quarterly company financials."""
from dataclasses import dataclass
import math
import re


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
        if not isinstance(self.ticker, str) or not self.ticker.strip():
            raise ValueError("ticker and quarter are required")
        # FY names the year ending in March; do not mix quarters with annual/YTD rows.
        if not isinstance(self.quarter, str) or not re.fullmatch(r"Q[1-4]-FY[0-9]{4}", self.quarter):
            raise ValueError("quarter must use Q1-FY2025 format (financial year ending)")
        # A source identifier is provenance, not evidence of review or approval.
        # Governed data must be materialized through the separate review workflow.
        if self.status != "STAGED":
            raise ValueError("quarterly staging records cannot grant governed or approved status")
        if self.source_id is not None and (not isinstance(self.source_id, str) or not self.source_id.strip()):
            raise ValueError("source_id must be a nonblank string or null")
        for name in ("revenue", "ebitda", "pat", "operating_cash_flow"):
            value = getattr(self, name)
            if value is not None:
                if type(value) not in (int, float):
                    raise ValueError(f"{name} must be finite numeric data or null")
                try:
                    finite = math.isfinite(value)
                except OverflowError:
                    finite = False
                if not finite:
                    raise ValueError(f"{name} must be finite numeric data or null")

    @property
    def has_core_metrics(self) -> bool:
        return self.revenue is not None and self.pat is not None
