"""
EIOS
Everest Investment Operating System

Valuation Configuration

Central configuration for all valuation models.
"""


class ValuationConfig:
    """
    Central configuration for the Valuation Office.
    """

    # =====================================================
    # METHOD WEIGHTS
    # =====================================================

    METHOD_WEIGHTS = {
        "DCF": 0.50,
        "EPV": 0.30,
        "Owner Earnings": 0.20,
    }

    # =====================================================
    # CONFIDENCE THRESHOLDS
    # =====================================================

    CONFIDENCE_THRESHOLDS = {
        "High": 80,
        "Moderate": 60,
        "Low": 40,
    }

    # =====================================================
    # METHOD AGREEMENT THRESHOLDS
    # =====================================================

    AGREEMENT_THRESHOLDS = {
        "Strong": 0.10,
        "Moderate": 0.25,
        "Weak": 1.00,
    }

    # =====================================================
    # DEFAULT DCF SETTINGS
    # =====================================================

    DEFAULT_DISCOUNT_RATE = 0.12
    DEFAULT_TERMINAL_GROWTH = 0.05
    DEFAULT_FORECAST_YEARS = 10