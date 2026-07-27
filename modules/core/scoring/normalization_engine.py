class NormalizationEngine:
    """
    Normalizes scores from different scoring scales to a
    standard 0–100 percentage scale.

    Examples:
        8.5 / 10   -> 85.0
        42 / 50    -> 84.0
        170 / 200  -> 85.0
    """

    @staticmethod
    def normalize(score: float, maximum: float) -> float:
        """
        Convert a score from any scale to a percentage.

        Args:
            score: Actual score.
            maximum: Maximum possible score.

        Returns:
            Percentage score (0–100).
        """

        if maximum <= 0:
            raise ValueError("maximum must be greater than zero.")

        if score < 0:
            raise ValueError("score cannot be negative.")

        if score > maximum:
            raise ValueError("score cannot exceed maximum.")

        return round((score / maximum) * 100, 2)

    @staticmethod
    def denormalize(percentage: float, maximum: float) -> float:
        """
        Convert a percentage back to a target scale.

        Example:
            85% on a 50-point scale -> 42.5
        """

        if percentage < 0 or percentage > 100:
            raise ValueError("percentage must be between 0 and 100.")

        if maximum <= 0:
            raise ValueError("maximum must be greater than zero.")

        return round((percentage / 100) * maximum, 2)