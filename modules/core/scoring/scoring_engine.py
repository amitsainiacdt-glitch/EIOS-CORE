from .score_models import ScoreResult
from .rating_engine import RatingEngine


class ScoringEngine:
    """
    Universal Scoring Engine

    Responsible only for calculating standardized scores.

    Rating conversion is delegated to RatingEngine.
    """

    @classmethod
    def calculate(
        cls,
        score: float,
        max_score: float = 100.0,
    ) -> ScoreResult:
        """
        Convert a raw score into a standardized score.

        Args:
            score: Raw score obtained.
            max_score: Maximum possible score.

        Returns:
            ScoreResult
        """

        if max_score <= 0:
            raise ValueError("max_score must be greater than zero.")

        if score < 0:
            raise ValueError("score cannot be negative.")

        if score > max_score:
            raise ValueError("score cannot exceed max_score.")

        percentage = round((score / max_score) * 100, 2)

        grade = RatingEngine.get_grade(percentage)

        return ScoreResult(
            score=score,
            max_score=max_score,
            percentage=percentage,
            grade=grade,
        )