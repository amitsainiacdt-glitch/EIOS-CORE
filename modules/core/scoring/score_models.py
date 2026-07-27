from dataclasses import dataclass


@dataclass
class ScoreResult:
    """
    Standard score object returned by all scoring engines.
    """

    score: float
    max_score: float
    percentage: float
    grade: str