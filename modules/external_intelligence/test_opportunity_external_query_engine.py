from modules.external_intelligence.opportunity_external_query_engine import (
    OpportunityExternalQueryEngine,
)

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)


def main() -> None:

    intake = OpportunityResearchIntake(
        company="Tata Motors",
        ticker="TATAMOTORS",
        sector="Automobile",
        industry="Automotive",
        catalysts=[
            "EV adoption"
        ],
        concerns=[
            "Demand slowdown"
        ],
        risks=[
            "Margin pressure"
        ],
        strengths=[
            "Market leadership"
        ],
    )

    engine = (
        OpportunityExternalQueryEngine()
    )

    # ======================================================
    # ENGINE
    # ======================================================

    assert engine is not None

    print(
        "Opportunity External Query Engine : PASS"
    )

    # ======================================================
    # BUILD
    # ======================================================

    queries = engine.build(
        intake
    )

    assert queries

    print(
        "External Query Generation          : PASS"
    )

    # ======================================================
    # IDENTITY
    # ======================================================

    for query in queries:

        assert (
            query.company
            == "Tata Motors"
        )

        assert (
            query.ticker
            == "TATAMOTORS"
        )

    print(
        "Company / Ticker Preservation       : PASS"
    )

    # ======================================================
    # QUESTION PRESERVATION
    # ======================================================

    for query in queries:

        assert query.question

        assert (
            query.question
            in query.query
        )

    print(
        "Question Preservation               : PASS"
    )

    # ======================================================
    # INTENT
    # ======================================================

    for query in queries:

        assert (
            query.intent
            == "OPPORTUNITY_RESEARCH"
        )

    print(
        "Intent Assignment                   : PASS"
    )

    # ======================================================
    # DETERMINISM
    # ======================================================

    queries_again = engine.build(
        intake
    )

    assert queries == queries_again

    print(
        "Deterministic Output                : PASS"
    )

    # ======================================================
    # INTAKE IMMUTABILITY
    # ======================================================

    assert (
        intake.company
        == "Tata Motors"
    )

    assert (
        intake.ticker
        == "TATAMOTORS"
    )

    assert (
        intake.catalysts
        == ["EV adoption"]
    )

    assert (
        intake.concerns
        == ["Demand slowdown"]
    )

    print(
        "Intake Immutability                 : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        queries[0],
        "opportunity_score",
    )

    assert not hasattr(
        queries[0],
        "valuation",
    )

    assert not hasattr(
        queries[0],
        "signal_score",
    )

    print(
        "No Analytical Fabrication           : PASS"
    )

    # ======================================================
    # INVALID INPUT
    # ======================================================

    try:

        engine.build(
            None
        )

        raise AssertionError(
            "None intake was accepted"
        )

    except ValueError:
        pass

    print(
        "Invalid Input Protection            : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS OPPORTUNITY → EXTERNAL QUERY "
        "ENGINE : PASS"
    )


if __name__ == "__main__":
    main()