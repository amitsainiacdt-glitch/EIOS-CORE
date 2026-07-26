"""
EIOS
Valuation Assumptions Builder

Builds standardized valuation assumptions from
financial analysis.
"""


class ValuationAssumptionsBuilder:

    def build(self, financial_data: dict, financial_summary: dict):

        free_cash_flow = (
            financial_summary["Cash Flow"]["Free Cash Flow"]
        )

        revenue_growth = (
            financial_summary["Revenue Growth"] / 100
        )

        roiic = financial_summary["ROIIC"]

        # Simple Version 1 assumptions
        growth_rate = min(revenue_growth, 0.20)

        discount_rate = 0.12

        terminal_growth_rate = 0.05

        normalized_earnings = free_cash_flow

        return {

            "dcf": {

                "current_fcf": free_cash_flow,
                "growth_rate": growth_rate,
                "discount_rate": discount_rate,
                "terminal_growth_rate": terminal_growth_rate,
                "forecast_years": 10,
            },

            "epv": {

                "normalized_earnings": normalized_earnings,
                "discount_rate": discount_rate,
            },

            "metadata": {

                "ROIIC": roiic,
                "Revenue Growth": revenue_growth,
            }
        }