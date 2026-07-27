from dataclasses import dataclass


@dataclass
class WeightedScoreResult:
    total_score: float
    total_weight: float
    normalized_score: float


class WeightingEngine:
    """
    Applies weighted scoring across multiple categories.
    """

    @staticmethod
    def calculate(weighted_items):
        """
        weighted_items should be a list of tuples:
        (score, weight)

        Example:
        [
            (85, 25),
            (90, 20),
            (80, 20),
            (75, 15),
            (70, 10),
            (88, 10)
        ]
        """

        if not weighted_items:
            raise ValueError("No weighted items provided.")

        total_score = 0.0
        total_weight = 0.0

        for score, weight in weighted_items:

            if weight < 0:
                raise ValueError("Weight cannot be negative.")

            if score < 0 or score > 100:
                raise ValueError("Score must be between 0 and 100.")

            total_score += score * weight
            total_weight += weight

        if total_weight == 0:
            raise ValueError("Total weight cannot be zero.")

        normalized_score = round(total_score / total_weight, 2)

        return WeightedScoreResult(
            total_score=round(total_score, 2),
            total_weight=total_weight,
            normalized_score=normalized_score,
        )