"""
EIOS
Everest Investment Operating System

Temporal Signal Intelligence Engine Test
"""

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDirection,
)

from modules.opportunity.signals.temporal_signal_engine import (
    TemporalSignalEngine,
    TemporalSignalEvolution,
)


def make_signal(
    signal_id: str,
    date: str,
    direction: SignalDirection,
    magnitude: float,
    confidence: float = 70.0,
    persistence: float = 70.0,
) -> Signal:

    return Signal(
        signal_id=signal_id,
        title=f"Test Signal {signal_id}",
        detected_date=date,
        direction=direction,
        magnitude=magnitude,
        relevance=70.0,
        probability=70.0,
        confidence=confidence,
        persistence=persistence,
    )


def main() -> None:

    engine = TemporalSignalEngine()

    # ======================================================
    # EMPTY INPUT
    # ======================================================

    result = engine.analyze([])

    assert isinstance(
        result,
        TemporalSignalEvolution,
    )

    assert result.observations == 0
    assert result.valid_observations == 0
    assert result.direction == SignalDirection.UNKNOWN
    assert result.warnings

    print(
        "Empty Input                     : PASS"
    )

    # ======================================================
    # SINGLE OBSERVATION
    # ======================================================

    single = [
        make_signal(
            "S1",
            "2026-01-01",
            SignalDirection.POSITIVE,
            50.0,
        )
    ]

    result = engine.analyze(single)

    assert result.observations == 1
    assert result.valid_observations == 1
    assert result.direction == SignalDirection.POSITIVE

    print(
        "Single Observation              : PASS"
    )

    # ======================================================
    # CHRONOLOGICAL ORDERING
    # ======================================================

    unordered = [
        make_signal(
            "S3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            80.0,
        ),
        make_signal(
            "S1",
            "2026-01-01",
            SignalDirection.NEGATIVE,
            30.0,
        ),
        make_signal(
            "S2",
            "2026-02-01",
            SignalDirection.NEUTRAL,
            40.0,
        ),
    ]

    result = engine.analyze(unordered)

    assert result.valid_observations == 3
    assert result.direction in (
        SignalDirection.POSITIVE,
        SignalDirection.MIXED,
    )

    print(
        "Chronological Ordering          : PASS"
    )

    # ======================================================
    # POSITIVE TREND
    # ======================================================

    positive_trend = [
        make_signal(
            "P1",
            "2026-01-01",
            SignalDirection.POSITIVE,
            40.0,
        ),
        make_signal(
            "P2",
            "2026-02-01",
            SignalDirection.POSITIVE,
            55.0,
        ),
        make_signal(
            "P3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            70.0,
        ),
        make_signal(
            "P4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            85.0,
        ),
    ]

    result = engine.analyze(
        positive_trend
    )

    assert result.direction == (
        SignalDirection.POSITIVE
    )

    assert result.trend

    print(
        "Positive Trend                  : PASS"
    )

    # ======================================================
    # ACCELERATION
    # ======================================================

    acceleration = [
        make_signal(
            "A1",
            "2026-01-01",
            SignalDirection.POSITIVE,
            20.0,
        ),
        make_signal(
            "A2",
            "2026-02-01",
            SignalDirection.POSITIVE,
            40.0,
        ),
        make_signal(
            "A3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            70.0,
        ),
        make_signal(
            "A4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            90.0,
        ),
    ]

    result = engine.analyze(
        acceleration
    )

    assert result.accelerating

    print(
        "Acceleration                    : PASS"
    )

    # ======================================================
    # DECELERATION
    # ======================================================

    deceleration = [
        make_signal(
            "D1",
            "2026-01-01",
            SignalDirection.POSITIVE,
            90.0,
        ),
        make_signal(
            "D2",
            "2026-02-01",
            SignalDirection.POSITIVE,
            70.0,
        ),
        make_signal(
            "D3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            40.0,
        ),
        make_signal(
            "D4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            20.0,
        ),
    ]

    result = engine.analyze(
        deceleration
    )

    assert result.decelerating

    print(
        "Deceleration                    : PASS"
    )

    # ======================================================
    # STABILISATION
    # ======================================================

    stabilization = [
        make_signal(
            "ST1",
            "2026-01-01",
            SignalDirection.NEGATIVE,
            80.0,
        ),
        make_signal(
            "ST2",
            "2026-02-01",
            SignalDirection.NEGATIVE,
            60.0,
        ),
        make_signal(
            "ST3",
            "2026-03-01",
            SignalDirection.NEUTRAL,
            45.0,
        ),
        make_signal(
            "ST4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            50.0,
        ),
    ]

    result = engine.analyze(
        stabilization
    )

    assert result.stabilizing

    print(
        "Stabilisation                   : PASS"
    )

    # ======================================================
    # INFLECTION
    # ======================================================

    inflection = [
        make_signal(
            "I1",
            "2026-01-01",
            SignalDirection.NEGATIVE,
            80.0,
        ),
        make_signal(
            "I2",
            "2026-02-01",
            SignalDirection.NEGATIVE,
            60.0,
        ),
        make_signal(
            "I3",
            "2026-03-01",
            SignalDirection.NEUTRAL,
            45.0,
        ),
        make_signal(
            "I4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            60.0,
        ),
    ]

    result = engine.analyze(
        inflection
    )

    assert result.inflection

    print(
        "Inflection                     : PASS"
    )

    # ======================================================
    # BOTTOMING
    # ======================================================

    bottoming = [
        make_signal(
            "B1",
            "2026-01-01",
            SignalDirection.NEGATIVE,
            80.0,
        ),
        make_signal(
            "B2",
            "2026-02-01",
            SignalDirection.NEGATIVE,
            50.0,
        ),
        make_signal(
            "B3",
            "2026-03-01",
            SignalDirection.NEUTRAL,
            30.0,
        ),
        make_signal(
            "B4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            45.0,
        ),
    ]

    result = engine.analyze(
        bottoming
    )

    assert result.bottoming

    print(
        "Bottoming                      : PASS"
    )

    # ======================================================
    # REVERSAL
    # ======================================================

    reversal = [
        make_signal(
            "R1",
            "2026-01-01",
            SignalDirection.NEGATIVE,
            80.0,
        ),
        make_signal(
            "R2",
            "2026-02-01",
            SignalDirection.NEGATIVE,
            60.0,
        ),
        make_signal(
            "R3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            50.0,
        ),
        make_signal(
            "R4",
            "2026-04-01",
            SignalDirection.POSITIVE,
            70.0,
        ),
    ]

    result = engine.analyze(
        reversal
    )

    assert result.reversal

    print(
        "Reversal                       : PASS"
    )

    # ======================================================
    # PERSISTENCE
    # ======================================================

    persistent = [
        make_signal(
            "PE1",
            "2026-01-01",
            SignalDirection.POSITIVE,
            60.0,
            persistence=80.0,
        ),
        make_signal(
            "PE2",
            "2026-02-01",
            SignalDirection.POSITIVE,
            65.0,
            persistence=80.0,
        ),
        make_signal(
            "PE3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            70.0,
            persistence=80.0,
        ),
    ]

    result = engine.analyze(
        persistent
    )

    assert result.persistent

    print(
        "Persistence                    : PASS"
    )

    # ======================================================
    # INVALID DATE HANDLING
    # ======================================================

    invalid_dates = [
        make_signal(
            "X1",
            "",
            SignalDirection.POSITIVE,
            50.0,
        ),
        make_signal(
            "X2",
            "not-a-date",
            SignalDirection.POSITIVE,
            60.0,
        ),
        make_signal(
            "X3",
            "2026-03-01",
            SignalDirection.POSITIVE,
            70.0,
        ),
    ]

    result = engine.analyze(
        invalid_dates
    )

    assert result.observations == 3
    assert result.valid_observations == 1
    assert result.warnings

    print(
        "Invalid Date Handling           : PASS"
    )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    assert (
        0.0
        <= result.confidence
        <= 100.0
    )

    print(
        "Confidence Range                : PASS"
    )

    # ======================================================
    # IMMUTABILITY / NO MUTATION
    # ======================================================

    original = make_signal(
        "IMM1",
        "2026-01-01",
        SignalDirection.NEGATIVE,
        60.0,
    )

    original_date = (
        original.detected_date
    )

    original_direction = (
        original.direction
    )

    engine.analyze(
        [
            original,
            make_signal(
                "IMM2",
                "2026-02-01",
                SignalDirection.POSITIVE,
                70.0,
            ),
        ]
    )

    assert (
        original.detected_date
        == original_date
    )

    assert (
        original.direction
        == original_direction
    )

    print(
        "Signal Immutability             : PASS"
    )

    # ======================================================
    # RESULT TYPE
    # ======================================================

    result = engine.analyze(
        positive_trend
    )

    assert isinstance(
        result,
        TemporalSignalEvolution,
    )

    print(
        "Result Type                     : PASS"
    )

    # ======================================================
    # REASONS / WARNINGS
    # ======================================================

    assert (
        result.reasons
        or result.warnings
    )

    print(
        "Transparent Reasoning           : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS TEMPORAL SIGNAL ENGINE : PASS"
    )


if __name__ == "__main__":
    main()