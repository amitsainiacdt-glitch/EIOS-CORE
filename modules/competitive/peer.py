"""
Peer Model

Represents a competitor company used for benchmarking.
"""

from dataclasses import dataclass


@dataclass
class Peer:
    company: str
    revenue_growth: float = 0.0
    eps_growth: float = 0.0
    roce: float = 0.0
    roe: float = 0.0
    roiic: float = 0.0
    operating_margin: float = 0.0
    debt_to_equity: float = 0.0

    def to_dict(self):
        return {
            "Company": self.company,
            "Revenue Growth": self.revenue_growth,
            "EPS Growth": self.eps_growth,
            "ROCE": self.roce,
            "ROE": self.roe,
            "ROIIC": self.roiic,
            "Operating Margin": self.operating_margin,
            "Debt to Equity": self.debt_to_equity,
        }