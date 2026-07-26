from dataclasses import dataclass
from math import pow


@dataclass(slots=True)
class ExpectedReturnResult:
    years: int
    market_price: float
    intrinsic_value: float
    expected_cagr: float
    category: str


class ExpectedReturnEngine:
    """
    Calculates annualized expected return (CAGR).
    """

    def calculate(
        self,
        market_price: float,
        intrinsic_value: float,
        years: int,
    ) -> ExpectedReturnResult:

        if market_price <= 0:
            raise ValueError("Market price must be greater than zero.")

        if intrinsic_value <= 0:
            raise ValueError("Intrinsic value must be greater than zero.")

        if years <= 0:
            raise ValueError("Years must be greater than zero.")

        cagr = (pow(intrinsic_value / market_price, 1 / years) - 1) * 100

        if cagr >= 25:
            category = "Exceptional"

        elif cagr >= 18:
            category = "Excellent"

        elif cagr >= 12:
            category = "Good"

        elif cagr >= 8:
            category = "Average"

        else:
            category = "Poor"

        return ExpectedReturnResult(
            years=years,
            market_price=market_price,
            intrinsic_value=intrinsic_value,
            expected_cagr=round(cagr, 2),
            category=category,
        )

    def calculate_3y(self, market_price: float, intrinsic_value: float):
        return self.calculate(market_price, intrinsic_value, 3)

    def calculate_5y(self, market_price: float, intrinsic_value: float):
        return self.calculate(market_price, intrinsic_value, 5)

    def calculate_10y(self, market_price: float, intrinsic_value: float):
        return self.calculate(market_price, intrinsic_value, 10)