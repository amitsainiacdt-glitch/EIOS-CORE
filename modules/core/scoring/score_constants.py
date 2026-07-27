"""
Institutional Scoring Constants

This module centralizes all scoring-related constants used
throughout the EIOS platform.
"""

# Standard score scale
DEFAULT_MAX_SCORE = 100.0

# Institutional grading thresholds
GRADE_THRESHOLDS = {
    "A++": 95,
    "A+": 90,
    "A": 85,
    "A-": 80,
    "B+": 75,
    "B": 70,
    "B-": 65,
    "C+": 60,
    "C": 55,
    "C-": 50,
    "D": 40,
    "F": 0,
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "Very High": 90,
    "High": 75,
    "Moderate": 60,
    "Low": 40,
    "Very Low": 0,
}

# Default engine weights
DEFAULT_ENGINE_WEIGHTS = {
    "Business": 25,
    "Financial": 20,
    "Management": 20,
    "Competitive": 15,
    "Risk": 10,
    "Valuation": 10,
}