"""
EIOS
Everest Investment Operating System

Asymmetry Engine

Purpose:
Evaluates the probability-weighted relationship between
upside, downside, permanent capital loss and time-to-thesis.

This is NOT a valuation engine.

Valuation answers:
    What may the business be worth?

Asymmetry answers:
    Is the potential payoff sufficiently attractive
    relative to the risks, probabilities and time required?

Architecture:

Mispricing
    ↓
Asymmetry Engine
    ↓
Scenario Distribution
    ↓
Expected Value
    ↓
Asymmetry Score
    ↓
Opportunity Ranking

Design Principles:
- Probability weighted.
- Explicit downside.
- Explicit permanent-loss risk.
- Explicit time-to-thesis.
- No investment recommendation.
- No mutation of source objects.
- Conservative treatment of uncertainty.
"""

from dataclasses import dataclass, field
from typing import List


# ==========================================================
# SCENARIO
# ==========================================================


@dataclass
class AsymmetryScenario:
    """
    One possible investment outcome.
    """

    name: str = ""

    probability: float = 0.0

    return_percent: float = 0.0

    time_months: int = 0

    permanent_loss: bool = False

    rationale: str = ""


# ==========================================================
# ASYMMETRY ASSESSMENT
# ==========================================================


@dataclass
class AsymmetryAssessment:
    """
    Institutional asymmetry assessment.
    """

    company: str = ""

    scenarios: List[AsymmetryScenario] = field(
        default_factory=list
    )

    expected_return: float = 0.0

    upside_probability: float = 0.0

    downside_probability: float = 0.0

    permanent_loss_probability: float = 0.0

    best_case_return: float = 0.0

    worst_case_return: float = 0.0

    expected_time_months: float = 0.0

    asymmetry_ratio: float = 0.0

    asymmetry_score: float = 0.0

    confidence: float = 0.0

    attractive: bool = False

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    disconfirming_evidence: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# ASYMMETRY ENGINE
# ==========================================================


class AsymmetryEngine:
    """
    Calculates probability-weighted investment asymmetry.
    """

    MINIMUM_SCORE = 60.0

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        *,
        company: str,
        scenarios: List[AsymmetryScenario],
        assumptions: List[str] | None = None,
        invalidation_conditions: List[str] | None = None,
        disconfirming_evidence: List[str] | None = None,
    ) -> AsymmetryAssessment:
        """
        Evaluate scenario-based asymmetry.
        """

        result = AsymmetryAssessment()

        result.company = company

        result.scenarios = list(
            scenarios
        )

        result.assumptions = list(
            assumptions or []
        )

        result.invalidation_conditions = list(
            invalidation_conditions or []
        )

        result.disconfirming_evidence = list(
            disconfirming_evidence or []
        )

        if not scenarios:
            result.warnings.append(
                "No scenarios supplied."
            )

            return result

        # --------------------------------------------------
        # Validate probabilities
        # --------------------------------------------------

        self._validate_scenarios(
            scenarios
        )

        # --------------------------------------------------
        # Probability Metrics
        # --------------------------------------------------

        result.upside_probability = self._upside_probability(
            scenarios
        )

        result.downside_probability = self._downside_probability(
            scenarios
        )

        result.permanent_loss_probability = (
            self._permanent_loss_probability(
                scenarios
            )
        )

        # --------------------------------------------------
        # Return Metrics
        # --------------------------------------------------

        result.expected_return = (
            self._expected_return(
                scenarios
            )
        )

        result.best_case_return = max(
            scenario.return_percent
            for scenario in scenarios
        )

        result.worst_case_return = min(
            scenario.return_percent
            for scenario in scenarios
        )

        # --------------------------------------------------
        # Time
        # --------------------------------------------------

        result.expected_time_months = (
            self._expected_time(
                scenarios
            )
        )

        # --------------------------------------------------
        # Asymmetry
        # --------------------------------------------------

        result.asymmetry_ratio = (
            self._asymmetry_ratio(
                scenarios
            )
        )

        result.asymmetry_score = (
            self._asymmetry_score(
                result
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = (
            self._confidence(
                result
            )
        )

        # --------------------------------------------------
        # Decision State
        # --------------------------------------------------

        result.attractive = (
            result.asymmetry_score
            >= self.MINIMUM_SCORE
            and result.expected_return > 0
            and result.permanent_loss_probability
            < 30.0
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        self._build_reasoning(
            result
        )

        return result

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate_scenarios(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> None:

        total_probability = sum(
            scenario.probability
            for scenario in scenarios
        )

        if (
            total_probability < 99.0
            or total_probability > 101.0
        ):
            raise ValueError(
                "Scenario probabilities must sum "
                "to approximately 100."
            )

        for scenario in scenarios:

            if scenario.probability < 0:
                raise ValueError(
                    "Scenario probability cannot be negative."
                )

            if scenario.probability > 100:
                raise ValueError(
                    "Scenario probability cannot exceed 100."
                )

            if scenario.time_months < 0:
                raise ValueError(
                    "Scenario time cannot be negative."
                )

    # ======================================================
    # UPSIDE PROBABILITY
    # ======================================================

    def _upside_probability(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        return sum(
            scenario.probability
            for scenario in scenarios
            if scenario.return_percent > 0
        )

    # ======================================================
    # DOWNSIDE PROBABILITY
    # ======================================================

    def _downside_probability(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        return sum(
            scenario.probability
            for scenario in scenarios
            if scenario.return_percent < 0
        )

    # ======================================================
    # PERMANENT LOSS
    # ======================================================

    def _permanent_loss_probability(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        return sum(
            scenario.probability
            for scenario in scenarios
            if scenario.permanent_loss
        )

    # ======================================================
    # EXPECTED RETURN
    # ======================================================

    def _expected_return(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        return sum(
            (
                scenario.probability
                / 100.0
            )
            * scenario.return_percent
            for scenario in scenarios
        )

    # ======================================================
    # EXPECTED TIME
    # ======================================================

    def _expected_time(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        return sum(
            (
                scenario.probability
                / 100.0
            )
            * scenario.time_months
            for scenario in scenarios
        )

    # ======================================================
    # ASYMMETRY RATIO
    # ======================================================

    def _asymmetry_ratio(
        self,
        scenarios: List[AsymmetryScenario],
    ) -> float:

        weighted_upside = sum(
            (
                scenario.probability
                / 100.0
            )
            * scenario.return_percent
            for scenario in scenarios
            if scenario.return_percent > 0
        )

        weighted_downside = sum(
            (
                scenario.probability
                / 100.0
            )
            * abs(
                scenario.return_percent
            )
            for scenario in scenarios
            if scenario.return_percent < 0
        )

        if weighted_downside == 0:

            if weighted_upside > 0:
                return 100.0

            return 0.0

        return (
            weighted_upside
            / weighted_downside
        )

    # ======================================================
    # ASYMMETRY SCORE
    # ======================================================

    def _asymmetry_score(
        self,
        result: AsymmetryAssessment,
    ) -> float:
        """
        Convert asymmetry characteristics to a 0-100 score.

        This is deliberately not a simple return score.
        Permanent-loss risk and time-to-thesis matter.
        """

        expected_return_component = max(
            0.0,
            min(
                100.0,
                result.expected_return * 2.0,
            ),
        )

        ratio_component = min(
            100.0,
            result.asymmetry_ratio * 25.0,
        )

        upside_component = (
            result.upside_probability
        )

        permanent_loss_component = (
            100.0
            - result.permanent_loss_probability
        )

        time_component = max(
            0.0,
            min(
                100.0,
                100.0
                - (
                    result.expected_time_months
                    * 2.0
                ),
            ),
        )

        score = (
            expected_return_component * 0.30
            + ratio_component * 0.25
            + upside_component * 0.15
            + permanent_loss_component * 0.20
            + time_component * 0.10
        )

        return max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: AsymmetryAssessment,
    ) -> float:

        confidence = 70.0

        if len(
            result.scenarios
        ) < 3:

            confidence -= 15.0

        if result.disconfirming_evidence:

            confidence -= min(
                25.0,
                len(
                    result.disconfirming_evidence
                ) * 5.0,
            )

        if not result.assumptions:

            confidence -= 10.0

        if not result.invalidation_conditions:

            confidence -= 10.0

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # REASONING
    # ======================================================

    def _build_reasoning(
        self,
        result: AsymmetryAssessment,
    ) -> None:

        if result.expected_return > 0:

            result.reasons.append(
                "Probability-weighted expected return is positive."
            )

        else:

            result.warnings.append(
                "Probability-weighted expected return is not positive."
            )

        if result.asymmetry_ratio >= 2.0:

            result.reasons.append(
                "Weighted upside materially exceeds weighted downside."
            )

        elif result.asymmetry_ratio < 1.0:

            result.warnings.append(
                "Weighted downside exceeds weighted upside."
            )

        if result.permanent_loss_probability >= 30:

            result.warnings.append(
                "Permanent capital-loss probability is elevated."
            )

        if result.expected_time_months > 36:

            result.warnings.append(
                "Expected thesis duration exceeds three years."
            )

        if result.attractive:

            result.reasons.append(
                "Scenario distribution meets the current "
                "asymmetry threshold."
            )

        else:

            result.warnings.append(
                "Scenario distribution does not yet meet "
                "the institutional asymmetry threshold."
            )

        if result.disconfirming_evidence:

            result.warnings.append(
                "Disconfirming evidence must be reviewed."
            )