"""
Financial Rules

Defines the scoring rules used by FinancialScorecard.

Each metric contains:
- weight       : Maximum obtainable score
- thresholds   : (minimum value, awarded score)

Thresholds are evaluated from highest to lowest.
The first matching threshold is used.
"""

FINANCIAL_RULES = {

    "Revenue Growth": {
        "weight": 15,
        "thresholds": [
            (20, 15),
            (15, 12),
            (10, 9),
            (5, 6),
            (0, 3),
            (float("-inf"), 0),
        ],
    },

    "EPS Growth": {
        "weight": 20,
        "thresholds": [
            (25, 20),
            (20, 16),
            (15, 12),
            (10, 8),
            (0, 4),
            (float("-inf"), 0),
        ],
    },

    "ROCE": {
        "weight": 20,
        "thresholds": [
            (25, 20),
            (20, 16),
            (15, 12),
            (10, 8),
            (5, 4),
            (float("-inf"), 0),
        ],
    },

    "ROE": {
        "weight": 15,
        "thresholds": [
            (25, 15),
            (20, 12),
            (15, 9),
            (10, 6),
            (5, 3),
            (float("-inf"), 0),
        ],
    },

    "Debt to Equity": {
        "weight": 15,
        "thresholds": [
            (0, 15),
            (0.30, 12),
            (0.50, 9),
            (1.00, 6),
            (2.00, 3),
            (float("inf"), 0),
        ],
        "reverse": True,
    },

    "Free Cash Flow": {
        "weight": 15,
        "thresholds": [
            (1000, 15),
            (500, 12),
            (100, 9),
            (0, 6),
            (-100, 3),
            (float("-inf"), 0),
        ],
    },
}