from dataclasses import dataclass


@dataclass
class ConfidenceResult:
    confidence: float
    grade: str
    evidence_items: int
    missing_items: int


class ConfidenceEngine:
    """
    Calculates confidence based on evidence completeness.

    Confidence is determined by:
    - Number of evidence items collected
    - Number of missing evidence items
    """

    GRADE_TABLE = [
        (90, "Very High"),
        (75, "High"),
        (60, "Moderate"),
        (40, "Low"),
        (0, "Very Low"),
    ]

    @classmethod
    def calculate(
        cls,
        evidence_items: int,
        expected_items: int,
    ) -> ConfidenceResult:

        if expected_items <= 0:
            raise ValueError("expected_items must be greater than zero.")

        if evidence_items < 0:
            raise ValueError("evidence_items cannot be negative.")

        if evidence_items > expected_items:
            evidence_items = expected_items

        confidence = round(
            (evidence_items / expected_items) * 100,
            2,
        )

        missing = expected_items - evidence_items

        grade = cls._grade(confidence)

        return ConfidenceResult(
            confidence=confidence,
            grade=grade,
            evidence_items=evidence_items,
            missing_items=missing,
        )

    @classmethod
    def _grade(cls, confidence: float) -> str:

        for threshold, grade in cls.GRADE_TABLE:
            if confidence >= threshold:
                return grade

        return "Very Low"