"""
EIOS
Everest Investment Operating System

Asymmetry Engine Test
"""

from modules.opportunity.asymmetry_engine import (
    AsymmetryEngine,
    AsymmetryScenario,
)


def main():

    engine = AsymmetryEngine()

    print("=" * 60)
    print("EIOS ASYMMETRY ENGINE TEST")
    print("=" * 60)

    # ==========================================================
    # TEST 1 — HIGH ASYMMETRY
    # ==========================================================

    high_asymmetry = [
        AsymmetryScenario(
            name="Base Case",
            probability=60.0,
            return_percent=50.0,
            time_months=24,
            permanent_loss=False,
            rationale="Catalyst converts into earnings growth.",
        ),
        AsymmetryScenario(
            name="Bull Case",
            probability=25.0,
            return_percent=150.0,
            time_months=36,
            permanent_loss=False,
            rationale="Strong earnings acceleration and rerating.",
        ),
        AsymmetryScenario(
            name="Bear Case",
            probability=15.0,
            return_percent=-30.0,
            time_months=18,
            permanent_loss=False,
            rationale="Catalyst partially fails.",
        ),
    ]

    result = engine.analyze(
        company="Test Company A",
        scenarios=high_asymmetry,
        assumptions=[
            "Catalyst persists.",
            "Balance sheet remains sound.",
        ],
        invalidation_conditions=[
            "Order cycle reverses.",
            "Returns on capital deteriorate.",
        ],
    )

    print("\nTest 1 — High Asymmetry")

    print(
        f"Expected Return : "
        f"{result.expected_return:.2f}%"
    )

    print(
        f"Upside Probability : "
        f"{result.upside_probability:.2f}%"
    )

    print(
        f"Permanent Loss Probability : "
        f"{result.permanent_loss_probability:.2f}%"
    )

    print(
        f"Expected Time : "
        f"{result.expected_time_months:.2f} months"
    )

    print(
        f"Asymmetry Ratio : "
        f"{result.asymmetry_ratio:.2f}"
    )

    print(
        f"Asymmetry Score : "
        f"{result.asymmetry_score:.2f}"
    )

    print(
        f"Attractive : "
        f"{result.attractive}"
    )

    assert result.expected_return > 0
    assert result.upside_probability == 85.0
    assert result.permanent_loss_probability == 0.0
    assert result.asymmetry_ratio > 2.0
    assert result.attractive

    print("PASS")

    # ==========================================================
    # TEST 2 — FALSE ASYMMETRY
    # ==========================================================

    false_asymmetry = [
        AsymmetryScenario(
            name="Huge Upside",
            probability=20.0,
            return_percent=300.0,
            time_months=24,
            permanent_loss=False,
            rationale="Extreme bull case.",
        ),
        AsymmetryScenario(
            name="Permanent Loss",
            probability=50.0,
            return_percent=-70.0,
            time_months=24,
            permanent_loss=True,
            rationale="Business economics deteriorate permanently.",
        ),
        AsymmetryScenario(
            name="Weak Recovery",
            probability=30.0,
            return_percent=-10.0,
            time_months=18,
            permanent_loss=False,
            rationale="Recovery fails to materialize.",
        ),
    ]

    result = engine.analyze(
        company="Test Company B",
        scenarios=false_asymmetry,
        assumptions=[
            "Bull case requires successful execution.",
        ],
        invalidation_conditions=[
            "Debt becomes unsustainable.",
        ],
        disconfirming_evidence=[
            "High leverage.",
            "Weak cash conversion.",
        ],
    )

    print("\nTest 2 — False Asymmetry")

    print(
        f"Expected Return : "
        f"{result.expected_return:.2f}%"
    )

    print(
        f"Permanent Loss Probability : "
        f"{result.permanent_loss_probability:.2f}%"
    )

    print(
        f"Asymmetry Score : "
        f"{result.asymmetry_score:.2f}"
    )

    print(
        f"Attractive : "
        f"{result.attractive}"
    )

    assert result.permanent_loss_probability == 50.0
    assert not result.attractive

    print("PASS")

    # ==========================================================
    # TEST 3 — LONG DURATION / LOW RETURN
    # ==========================================================

    long_duration = [
        AsymmetryScenario(
            name="Base Case",
            probability=70.0,
            return_percent=20.0,
            time_months=60,
            permanent_loss=False,
            rationale="Slow operational improvement.",
        ),
        AsymmetryScenario(
            name="Bull Case",
            probability=15.0,
            return_percent=60.0,
            time_months=72,
            permanent_loss=False,
            rationale="Faster improvement.",
        ),
        AsymmetryScenario(
            name="Bear Case",
            probability=15.0,
            return_percent=-15.0,
            time_months=36,
            permanent_loss=False,
            rationale="Thesis stalls.",
        ),
    ]

    result = engine.analyze(
        company="Test Company C",
        scenarios=long_duration,
        assumptions=[
            "Improvement takes several years.",
        ],
        invalidation_conditions=[
            "Returns on capital fail to improve.",
        ],
    )

    print("\nTest 3 — Long Duration")

    print(
        f"Expected Return : "
        f"{result.expected_return:.2f}%"
    )

    print(
        f"Expected Time : "
        f"{result.expected_time_months:.2f} months"
    )

    print(
        f"Asymmetry Score : "
        f"{result.asymmetry_score:.2f}"
    )

    print(
        f"Attractive : "
        f"{result.attractive}"
    )

    assert result.expected_time_months > 48

    print("PASS")

    # ==========================================================
    # TEST 4 — INVALID PROBABILITY
    # ==========================================================

    invalid_scenarios = [
        AsymmetryScenario(
            name="Scenario A",
            probability=60.0,
            return_percent=50.0,
        ),
        AsymmetryScenario(
            name="Scenario B",
            probability=20.0,
            return_percent=-20.0,
        ),
    ]

    rejected = False

    try:

        engine.analyze(
            company="Invalid Test",
            scenarios=invalid_scenarios,
        )

    except ValueError:

        rejected = True

    assert rejected

    print("\nProbability Validation : PASS")

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n" + "=" * 60)
    print("ASYMMETRY ENGINE : ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()