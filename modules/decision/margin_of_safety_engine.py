from dataclasses import dataclass


@dataclass(slots=True)
class MarginOfSafetyResult:
    intrinsic_value: float
    market_price: float
    margin_of_safety: float
    discount_percent: float
    premium_percent: float
    rating: str
    band: str


class MarginOfSafetyEngine:
    """
    Calculates Margin of Safety based on intrinsic value
    and current market price.
    """

    def calculate(
        self,
        intrinsic_value: float,
        market_price: float,
    ) -> MarginOfSafetyResult:

        if intrinsic_value <= 0:
            raise ValueError("Intrinsic value must be greater than zero.")

        if market_price <= 0:
            raise ValueError("Market price must be greater than zero.")

        mos = ((intrinsic_value - market_price) / intrinsic_value) * 100

        if market_price < intrinsic_value:
            discount = ((intrinsic_value - market_price) / intrinsic_value) * 100
            premium = 0.0
        else:
            discount = 0.0
            premium = ((market_price - intrinsic_value) / intrinsic_value) * 100

        if mos >= 40:
            rating = "Excellent"
            band = "Deep Value"

        elif mos >= 25:
            rating = "Good"
            band = "Attractive"

        elif mos >= 10:
            rating = "Fair"
            band = "Reasonable"

        elif mos >= 0:
            rating = "Thin"
            band = "Fully Valued"

        else:
            rating = "Overvalued"
            band = "Premium"

        return MarginOfSafetyResult(
            intrinsic_value=intrinsic_value,
            market_price=market_price,
            margin_of_safety=round(mos, 2),
            discount_percent=round(discount, 2),
            premium_percent=round(premium, 2),
            rating=rating,
            band=band,
        )