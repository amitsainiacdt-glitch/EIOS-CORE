"""
EIOS
Everest Investment Operating System

Catalyst Coverage Analyzer Test

Purpose:
    Validate coverage of the canonical Catalyst Taxonomy
    by the currently registered Catalyst Pattern Registry.

Design Principles:
    - Uses the canonical CatalystFamily taxonomy.
    - Uses the canonical CatalystCoverageAnalyzer.
    - Performs no catalyst scoring.
    - Performs no catalyst ranking.
    - Performs no investment decision.
    - Does not invent catalyst patterns.
    - Reports coverage only.
"""

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.catalyst_coverage import (
    CatalystCoverageAnalyzer,
)


def main() -> None:

    # ======================================================
    # CANONICAL FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.family_count()
        == 30
    )

    # ======================================================
    # COVERED FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.covered_count()
        == 30
    )

    # ======================================================
    # UNCOVERED FAMILY COUNT
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.uncovered_count()
        == 0
    )

    # ======================================================
    # COVERAGE CONSISTENCY
    # ======================================================

    assert (
        CatalystCoverageAnalyzer.covered_count()
        + CatalystCoverageAnalyzer.uncovered_count()
        == CatalystCoverageAnalyzer.family_count()
    )

    # ======================================================
    # COVERED FAMILY LOOKUP
    # ======================================================

    covered = {
        item.family: item.pattern_count
        for item
        in CatalystCoverageAnalyzer.covered_families()
    }

    # ======================================================
    # COVERED FAMILY COUNTS
    # ======================================================

    assert (
        covered[
            CatalystFamily.CAPACITY_EXPANSION
        ]
        == 2
    )

    assert (
        covered[
            CatalystFamily.CAPACITY_UTILISATION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.ORDER_CONTRACT
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.CUSTOMER_ADDITION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.MARKET_SHARE
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.INDUSTRY_CAPITAL_CYCLE
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.SUPPLY_CONSTRAINT
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.COMPETITIVE_EXIT
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.NEW_PRODUCT_PLATFORM
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.TAM_EXPANSION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.REGULATORY_CHANGE
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.GOVERNMENT_POLICY
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.FISCAL_TAX
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.MONETARY_LIQUIDITY
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.COMMODITY
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.CURRENCY
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.TRADE_IMPORT_SUBSTITUTION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.REVENUE_GROWTH
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.VOLUME_GROWTH
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.PRICING
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.MARGIN_EXPANSION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.TECHNOLOGY_ADOPTION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.PRODUCT_MIX
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.COST_REDUCTION
        ]
        == 6
    )

    assert (
        covered[
            CatalystFamily.OPERATING_LEVERAGE
        ]
        == 6
    )

    # ======================================================
    # COVERED FAMILY PRESENCE
    # ======================================================

    expected_covered = {

        CatalystFamily.CAPACITY_EXPANSION,

        CatalystFamily.CAPACITY_UTILISATION,

        CatalystFamily.ORDER_CONTRACT,

        CatalystFamily.CUSTOMER_ADDITION,

        CatalystFamily.MARKET_SHARE,

        CatalystFamily.INDUSTRY_CAPITAL_CYCLE,

        CatalystFamily.SUPPLY_CONSTRAINT,

        CatalystFamily.COMPETITIVE_EXIT,

        CatalystFamily.NEW_PRODUCT_PLATFORM,

        CatalystFamily.TAM_EXPANSION,

        CatalystFamily.REGULATORY_CHANGE,

        CatalystFamily.GOVERNMENT_POLICY,

        CatalystFamily.FISCAL_TAX,

        CatalystFamily.MONETARY_LIQUIDITY,

        CatalystFamily.COMMODITY,

        CatalystFamily.CURRENCY,

        CatalystFamily.TRADE_IMPORT_SUBSTITUTION,

        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN,

        CatalystFamily.CORPORATE_ACTION_MA,

        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION,

        CatalystFamily.BALANCE_SHEET_CASH_FLOW,

        CatalystFamily.REVENUE_GROWTH,

        CatalystFamily.VOLUME_GROWTH,

        CatalystFamily.PRICING,

        CatalystFamily.MARGIN_EXPANSION,

        CatalystFamily.TECHNOLOGY_ADOPTION,

        CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,

        CatalystFamily.PRODUCT_MIX,

        CatalystFamily.COST_REDUCTION,

        CatalystFamily.OPERATING_LEVERAGE,
    }

    assert (
        len(expected_covered)
        == 30
    )

    assert (
        set(covered.keys())
        == expected_covered
    )

    # ======================================================
    # UNCOVERED FAMILY LOOKUP
    # ======================================================

    uncovered = {
        item.family: item.pattern_count
        for item
        in CatalystCoverageAnalyzer.uncovered_families()
    }

    # ======================================================
    # UNCOVERED FAMILY COUNT
    # ======================================================

    assert (
        len(uncovered)
        == 0
    )

    # ======================================================
    # COVERED FAMILIES MUST NOT BE UNCOVERED
    # ======================================================

    for family in expected_covered:

        assert (
            family not in uncovered
        )

    # ======================================================
    # COVERED / UNCOVERED EXCLUSIVITY
    # ======================================================

    assert (
        set(covered.keys()).isdisjoint(
            set(uncovered.keys())
        )
    )

    # ======================================================
    # COMPLETE TAXONOMY COVERAGE
    # ======================================================

    assert (
        set(covered.keys())
        | set(uncovered.keys())
        == set(CatalystFamily)
    )

    # ======================================================
    # COVERED + UNCOVERED = COMPLETE TAXONOMY
    # ======================================================

    assert (
        len(covered)
        + len(uncovered)
        == 30
    )

    # ======================================================
    # COVERED FAMILY PATTERNS MUST BE POSITIVE
    # ======================================================

    for family, pattern_count in covered.items():

        assert (
            pattern_count
            > 0
        )

    # ======================================================
    # UNCOVERED FAMILY PATTERNS MUST BE ZERO
    # ======================================================

    for family, pattern_count in uncovered.items():

        assert (
            pattern_count
            == 0
        )

    # ======================================================
    # COVERAGE RECORD INTEGRITY
    # ======================================================

    records = (
        CatalystCoverageAnalyzer.analyze()
    )

    assert (
        len(records)
        == 30
    )

    for record in records:

        assert (
            record.family
            in CatalystFamily
        )

        assert (
            record.pattern_count
            >= 0
        )

        if record.covered:

            assert (
                record.pattern_count
                > 0
            )

        else:

            assert (
                record.pattern_count
                == 0
            )

    # ======================================================
    # NEW PRODUCT / PLATFORM RECORD
    # ======================================================

    new_product_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.NEW_PRODUCT_PLATFORM
    ]

    assert (
        len(new_product_records)
        == 1
    )

    assert (
        new_product_records[0].covered
        is True
    )

    assert (
        new_product_records[0].pattern_count
        == 6
    )

    # ======================================================
    # TAM EXPANSION RECORD
    # ======================================================

    tam_expansion_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.TAM_EXPANSION
    ]

    assert (
        len(tam_expansion_records)
        == 1
    )

    assert (
        tam_expansion_records[0].covered
        is True
    )

    assert (
        tam_expansion_records[0].pattern_count
        == 6
    )

    # ======================================================
    # GOVERNMENT POLICY RECORD
    # ======================================================

    government_policy_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.GOVERNMENT_POLICY
    ]

    assert (
        len(government_policy_records)
        == 1
    )

    assert (
        government_policy_records[0].covered
        is True
    )

    assert (
        government_policy_records[0].pattern_count
        == 6
    )

    # ======================================================
    # FISCAL / TAX RECORD
    # ======================================================

    fiscal_tax_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.FISCAL_TAX
    ]

    assert (
        len(fiscal_tax_records)
        == 1
    )

    assert (
        fiscal_tax_records[0].covered
        is True
    )

    assert (
        fiscal_tax_records[0].pattern_count
        == 6
    )

    # ======================================================
    # MONETARY / LIQUIDITY RECORD
    # ======================================================

    monetary_liquidity_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.MONETARY_LIQUIDITY
    ]

    assert (
        len(monetary_liquidity_records)
        == 1
    )

    assert (
        monetary_liquidity_records[0].covered
        is True
    )

    assert (
        monetary_liquidity_records[0].pattern_count
        == 6
    )

    # ======================================================
    # COMMODITY RECORD
    # ======================================================

    commodity_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.COMMODITY
    ]

    assert (
        len(commodity_records)
        == 1
    )

    assert (
        commodity_records[0].covered
        is True
    )

    assert (
        commodity_records[0].pattern_count
        == 6
    )

    # ======================================================
    # CURRENCY RECORD
    # ======================================================

    currency_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.CURRENCY
    ]

    assert (
        len(currency_records)
        == 1
    )

    assert (
        currency_records[0].covered
        is True
    )

    assert (
        currency_records[0].pattern_count
        == 6
    )

    # ======================================================
    # TRADE / IMPORT SUBSTITUTION RECORD
    # ======================================================

    trade_import_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.TRADE_IMPORT_SUBSTITUTION
    ]

    assert (
        len(trade_import_records)
        == 1
    )

    assert (
        trade_import_records[0].covered
        is True
    )

    assert (
        trade_import_records[0].pattern_count
        == 6
    )


    # ======================================================
    # GEOPOLITICAL SUPPLY CHAIN RECORD
    # ======================================================

    geopolitical_supply_chain_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN
    ]

    assert (
        len(geopolitical_supply_chain_records)
        == 1
    )

    assert (
        geopolitical_supply_chain_records[0].covered
        is True
    )

    assert (
        geopolitical_supply_chain_records[0].pattern_count
        == 6
    )

    # ======================================================
    # CORPORATE ACTION / M&A RECORD
    # ======================================================

    corporate_action_ma_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.CORPORATE_ACTION_MA
    ]

    assert (
        len(corporate_action_ma_records)
        == 1
    )

    assert (
        corporate_action_ma_records[0].covered
        is True
    )

    assert (
        corporate_action_ma_records[0].pattern_count
        == 6
    )

    # ======================================================
    # MANAGEMENT CAPITAL ALLOCATION RECORD
    # ======================================================

    management_capital_allocation_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION
    ]

    assert (
        len(management_capital_allocation_records)
        == 1
    )

    assert (
        management_capital_allocation_records[0].covered
        is True
    )

    assert (
        management_capital_allocation_records[0].pattern_count
        == 6
    )

    # ======================================================
    # BALANCE SHEET / CASH FLOW RECORD
    # ======================================================

    balance_sheet_cash_flow_records = [
        record
        for record in records
        if record.family
        == CatalystFamily.BALANCE_SHEET_CASH_FLOW
    ]

    assert (
        len(balance_sheet_cash_flow_records)
        == 1
    )

    assert (
        balance_sheet_cash_flow_records[0].covered
        is True
    )

    assert (
        balance_sheet_cash_flow_records[0].pattern_count
        == 6
    )


    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Canonical Family Count              : PASS"
    )

    print(
        "Covered Family Count                : PASS"
    )

    print(
        "Uncovered Family Count              : PASS"
    )

    print(
        "Coverage Consistency                : PASS"
    )

    print(
        "Capacity Coverage                   : PASS"
    )

    print(
        "Capacity Utilisation Coverage       : PASS"
    )

    print(
        "Order Coverage                      : PASS"
    )

    print(
        "Customer Addition Coverage          : PASS"
    )

    print(
        "Market Share Coverage               : PASS"
    )

    print(
        "Industry Capital Cycle Coverage     : PASS"
    )

    print(
        "Supply Constraint Coverage          : PASS"
    )

    print(
        "Competitive Exit Coverage           : PASS"
    )

    print(
        "New Product / Platform Coverage     : PASS"
    )

    print(
        "TAM Expansion Coverage               : PASS"
    )

    print(
        "Regulatory Coverage                 : PASS"
    )

    print(
        "Government Policy Coverage          : PASS"
    )

    print(
        "Fiscal / Tax Coverage               : PASS"
    )

    print(
        "Monetary / Liquidity Coverage       : PASS"
    )

    print(
        "Commodity Coverage                  : PASS"
    )

    print(
        "Currency Coverage                   : PASS"
    )

    print(
        "Trade / Import Substitution Coverage : PASS"
    )

    print(
        "Geopolitical Supply Chain Coverage   : PASS"
    )

    print(
        "Corporate Action / M&A Coverage      : PASS"
    )

    print(
        "Management Capital Allocation Coverage : PASS"
    )

    print(
        "Revenue Growth Coverage             : PASS"
    )

    print(
        "Volume Growth Coverage              : PASS"
    )

    print(
        "Pricing Coverage                    : PASS"
    )

    print(
        "Margin Expansion Coverage           : PASS"
    )

    print(
        "Technology Adoption Coverage        : PASS"
    )

    print(
        "Market Recognition Coverage         : PASS"
    )

    print(
        "Product Mix Coverage                : PASS"
    )

    print(
        "Cost Reduction Coverage             : PASS"
    )

    print(
        "Operating Leverage Coverage         : PASS"
    )

    print(
        "Uncovered Family Detection          : PASS"
    )

    print(
        "Coverage Record Integrity            : PASS"
    )

    print(
        "New Product Record Integrity        : PASS"
    )

    print(
        "TAM Expansion Record Integrity      : PASS"
    )

    print(
        "Government Policy Record Integrity  : PASS"
    )

    print(
        "Fiscal / Tax Record Integrity       : PASS"
    )

    print(
        "Monetary / Liquidity Record Integrity : PASS"
    )

    print(
        "Commodity Record Integrity          : PASS"
    )

    print(
        "Currency Record Integrity           : PASS"
    )

    print(
        "Trade / Import Substitution Record Integrity : PASS"
    )

    print(
        "Geopolitical Supply Chain Record Integrity : PASS"
    )

    print(
        "Corporate Action / M&A Record Integrity : PASS"
    )

    print(
        "Management Capital Allocation Record Integrity : PASS"
    )

    print(
        "Balance Sheet / Cash Flow Coverage : PASS"
    )

    print(
        "Balance Sheet / Cash Flow Record Integrity : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS CATALYST COVERAGE : PASS"
    )


if __name__ == "__main__":
    main()