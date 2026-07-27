"""
Custom exceptions for the EIOS Scoring Framework.
"""


class ScoringError(Exception):
    """Base exception for all scoring-related errors."""


class InvalidScoreError(ScoringError):
    """Raised when a score is invalid."""


class InvalidWeightError(ScoringError):
    """Raised when a weight is invalid."""


class InvalidConfidenceError(ScoringError):
    """Raised when confidence data is invalid."""


class NormalizationError(ScoringError):
    """Raised when normalization fails."""