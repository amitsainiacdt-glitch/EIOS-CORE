from dataclasses import dataclass


@dataclass
class Company:
    name: str
    ticker: str
    sector: str
    industry: str


class CompanyRegistry:

    def __init__(self):
        self.companies = []

    def add_company(self, company):
        self.companies.append(company)

    def list_companies(self):
        return self.companies

    def count(self):
        return len(self.companies)