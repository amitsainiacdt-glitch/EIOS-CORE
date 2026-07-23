"""
Capital Allocation Engine

Evaluates how management allocates capital.
"""


class CapitalAllocationEngine:

    def evaluate(
        self,
        capex,
        acquisitions,
        dividends,
        share_buybacks,
        debt_reduction,
    ):

        allocation = {
            "Capital Expenditure": capex,
            "Acquisitions": acquisitions,
            "Dividends": dividends,
            "Share Buybacks": share_buybacks,
            "Debt Reduction": debt_reduction,
        }

        return allocation

    def summary(self, allocation):

        print("\nCapital Allocation Summary")

        for item, value in allocation.items():
            print(f"{item}: {value}")