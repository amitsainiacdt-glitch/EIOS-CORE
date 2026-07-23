"""
Owner Earnings Engine

Calculates Owner Earnings using Warren Buffett's approach.
"""


class OwnerEarningsEngine:

    def evaluate(self, financial_data: dict):

        operating_cash_flow = financial_data.get("operating_cash_flow", 0)
        capital_expenditure = financial_data.get("capital_expenditure", 0)

        owner_earnings = operating_cash_flow - capital_expenditure

        return {
            "Method": "Owner Earnings",
            "Owner Earnings": owner_earnings,
            "Operating Cash Flow": operating_cash_flow,
            "Capital Expenditure": capital_expenditure,
            "Confidence": 40
        }