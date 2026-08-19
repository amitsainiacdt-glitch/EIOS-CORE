"""
EIOS
Everest Investment Operating System

Observation Novelty Engine Test
"""

from datetime import datetime, timedelta

from modules.observation.observation import (
    Observation,
)

from modules.observation.observation_novelty_engine import (
    ObservationNoveltyEngine,
)


# ==========================================================
# TEST HELPERS
# ==========================================================


def make_observation(
    *,
    title="Industrial Capex Accelerates",
    description="Industrial investment is increasing.",
    source="https://example.com/article",
    category="External Web",
    entity="The Anup Engineering Limited",
    confidence=90.0,
    timestamp=None,
):
    return Observation(
        title=title,
        description=description,
        source=source,
        category=category,
        entity=entity,
        confidence=confidence,
        timestamp=(
            timestamp
            or datetime.now()
        ),
    )


# ==========================================================
# MAIN
# ==========================================================


def main():

    print("=" * 60)
    print("EIOS OBSERVATION NOVELTY ENGINE TEST")
    print("=" * 60)

    engine = ObservationNoveltyEngine()

    # ======================================================
    # TEST 1 — FIRST OBSERVATION
    # ======================================================

    observation_1 = make_observation()

    result = engine.assess(
        observation_1,
        [],
    )

    assert result.is_new

    print(
        "Test 1 — First Observation : PASS"
    )

    # ======================================================
    # TEST 2 — EXACT DUPLICATE
    # ======================================================

    observation_2 = make_observation()

    result = engine.assess(
        observation_2,
        [observation_1],
    )

    assert not result.is_new

    assert (
        result.matched_observation
        is observation_1
    )

    print(
        "Test 2 — Exact Duplicate    : PASS"
    )

    # ======================================================
    # TEST 3 — DIFFERENT TIMESTAMP
    # ======================================================

    observation_3 = make_observation(
        timestamp=(
            observation_1.timestamp
            + timedelta(days=1)
        )
    )

    result = engine.assess(
        observation_3,
        [observation_1],
    )

    assert not result.is_new

    print(
        "Test 3 — New Timestamp      : PASS"
    )

    # ======================================================
    # TEST 4 — WHITESPACE / CASE
    # ======================================================

    observation_4 = make_observation(
        title=(
            "  INDUSTRIAL   CAPEX "
            "ACCELERATES  "
        ),
        description=(
            " Industrial investment "
            "is increasing. "
        ),
        source=(
            " HTTPS://EXAMPLE.COM/ARTICLE "
        ),
        category=" external web ",
        entity=(
            " THE ANUP ENGINEERING LIMITED "
        ),
    )

    result = engine.assess(
        observation_4,
        [observation_1],
    )

    assert not result.is_new

    print(
        "Test 4 — Normalized Duplicate: PASS"
    )

    # ======================================================
    # TEST 5 — DIFFERENT CONTENT
    # ======================================================

    observation_5 = make_observation(
        title="New Capacity Commissioned",
        description=(
            "The company commissioned "
            "additional manufacturing capacity."
        ),
    )

    result = engine.assess(
        observation_5,
        [observation_1],
    )

    assert result.is_new

    print(
        "Test 5 — New Information     : PASS"
    )

    # ======================================================
    # TEST 6 — DIFFERENT SOURCE
    # ======================================================

    observation_6 = make_observation(
        source="https://another-source.example/article",
    )

    result = engine.assess(
        observation_6,
        [observation_1],
    )

    assert result.is_new

    print(
        "Test 6 — Different Source    : PASS"
    )

    # ======================================================
    # TEST 7 — FINGERPRINT STABILITY
    # ======================================================

    fingerprint_1 = (
        engine.fingerprint(
            observation_1
        )
    )

    fingerprint_2 = (
        engine.fingerprint(
            observation_3
        )
    )

    assert (
        fingerprint_1
        == fingerprint_2
    )

    print(
        "Test 7 — Fingerprint Stability: PASS"
    )

    # ======================================================
    # TEST 8 — FINGERPRINT DIFFERENCE
    # ======================================================

    fingerprint_3 = (
        engine.fingerprint(
            observation_5
        )
    )

    assert (
        fingerprint_1
        != fingerprint_3
    )

    print(
        "Test 8 — Fingerprint Difference: PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "OBSERVATION NOVELTY ENGINE : ALL TESTS PASSED"
    )
    print("=" * 60)


# ==========================================================
# ENTRY POINT
# ==========================================================


if __name__ == "__main__":
    main()