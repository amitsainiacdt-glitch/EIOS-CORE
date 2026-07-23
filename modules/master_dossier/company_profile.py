from dataclasses import dataclass


@dataclass
class CompanyProfile:
    name: str
    ticker: str
    sector: str
    industry: str

    def to_dict(self):
        return {
            "name": self.name,
            "ticker": self.ticker,
            "sector": self.sector,
            "industry": self.industry,
        }