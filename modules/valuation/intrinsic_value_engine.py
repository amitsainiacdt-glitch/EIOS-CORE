"""
EIOS
Everest Investment Operating System

Intrinsic Value Engine

Combines multiple valuation methods into one
institutional intrinsic value estimate.
"""

from modules.valuation.valuation_config import ValuationConfig


class IntrinsicValueEngine:
    """
    Produces a consolidated intrinsic value estimate
    from all available valuation methods.
    """

    def __init__(self):

        self.weights = ValuationConfig.METHOD_WEIGHTS

    def evaluate(self, valuation_results: dict):

        values = {}

        # =====================================================
        # OWNER EARNINGS
        # =====================================================

        owner = valuation_results.get("Owner Earnings")

        if owner:
            values["Owner Earnings"] = owner.get(
                "Owner Earnings",
                0,
            )

        # =====================================================
        # DCF
        # =====================================================

        dcf = valuation_results.get("DCF")

        if dcf:
            values["DCF"] = dcf.fair_value

        # =====================================================
        # EPV
        # =====================================================

        epv = valuation_results.get("EPV")

        if epv:
            values["EPV"] = epv.fair_value

        # =====================================================
        # WEIGHTED FAIR VALUE
        # =====================================================

        weighted_value = 0
        total_weight = 0

        for method, value in values.items():

            weight = self.weights.get(method, 0)

            weighted_value += value * weight
            total_weight += weight

        fair_value = (
            weighted_value / total_weight
            if total_weight > 0
            else 0
        )

        # =====================================================
        # RANGE
        # =====================================================

        if values:

            low_estimate = min(values.values())
            high_estimate = max(values.values())

        else:

            low_estimate = 0
            high_estimate = 0

        # =====================================================
        # PRIMARY METHOD
        # =====================================================

        primary_method = max(
            self.weights,
            key=self.weights.get,
        )

        # =====================================================
        # AGREEMENT
        # =====================================================

        if high_estimate == 0:

            spread = 0

        else:

            spread = (
                high_estimate - low_estimate
            ) / high_estimate

        thresholds = (
            ValuationConfig.AGREEMENT_THRESHOLDS
        )

        if spread <= thresholds["Strong"]:

            agreement = "Strong"

        elif spread <= thresholds["Moderate"]:

            agreement = "Moderate"

        else:

            agreement = "Weak"

        # =====================================================
        # CONFIDENCE
        # =====================================================

        confidence = 80

        if agreement == "Moderate":

            confidence = 70

        elif agreement == "Weak":

            confidence = 60

        # =====================================================
        # RESULT
        # =====================================================

        return {

            "Fair Value": round(fair_value, 2),

            "Low Estimate": round(low_estimate, 2),

            "High Estimate": round(high_estimate, 2),

            "Primary Method": primary_method,

            "Method Agreement": agreement,

            "Confidence": confidence,

            "Supporting Methods": values,

        }