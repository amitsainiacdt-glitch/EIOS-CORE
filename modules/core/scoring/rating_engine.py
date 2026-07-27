class RatingEngine:
    """
    Institutional Rating Engine

    Converts percentage scores into standardized
    institutional grades.
    """

    GRADE_TABLE = [
        (95, "A++"),
        (90, "A+"),
        (85, "A"),
        (80, "A-"),
        (75, "B+"),
        (70, "B"),
        (65, "B-"),
        (60, "C+"),
        (55, "C"),
        (50, "C-"),
        (40, "D"),
        (0, "F"),
    ]

    @classmethod
    def get_grade(cls, percentage: float) -> str:
        """
        Convert a percentage into an institutional grade.

        Args:
            percentage: Score percentage (0-100)

        Returns:
            Grade string
        """

        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        for threshold, grade in cls.GRADE_TABLE:
            if percentage >= threshold:
                return grade

        return "F"