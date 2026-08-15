"""
EIOS
Everest Investment Operating System

New Product / Platform Catalyst Pattern Test
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)

from modules.opportunity.catalyst.patterns.new_product_platform_patterns import (
    NEW_PRODUCT_PLATFORM_PATTERNS,
)


EXPECTED_PATTERN_IDS = {
    "PAT-NEW-PRODUCT-PLATFORM-LAUNCH",
    "PAT-NEW-PRODUCT-PLATFORM-CUSTOMER-QUALIFICATION",
    "PAT-NEW-PRODUCT-PLATFORM-BOOKINGS-INFLECTION",
    "PAT-NEW-PRODUCT-PLATFORM-REPEAT-ORDER",
    "PAT-NEW-PRODUCT-PLATFORM-MARGIN-MIX",
    "PAT-NEW-PRODUCT-PLATFORM-PLATFORM-ADOPTION",
}


EXPECTED_NAMES = {
    "New Product Launch",
    "Customer Qualification Inflection",
    "New Product Bookings Inflection",
    "Repeat Order Validation",
    "New Product Margin Mix Inflection",
    "Platform Adoption Inflection",
}


def main() -> None:

    # ======================================================
    # PATTERN COUNT
    # ======================================================

    assert (
        len(NEW_PRODUCT_PLATFORM_PATTERNS)
        == 6
    )

    # ======================================================
    # PATTERN TYPE INTEGRITY
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert isinstance(
            pattern,
            CatalystPattern,
        )

    # ======================================================
    # FAMILY INTEGRITY
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert (
            pattern.family
            == CatalystFamily.NEW_PRODUCT_PLATFORM
        )

    # ======================================================
    # UNIQUE PATTERN IDS
    # ======================================================

    pattern_ids = {
        pattern.pattern_id
        for pattern in NEW_PRODUCT_PLATFORM_PATTERNS
    }

    assert (
        len(pattern_ids)
        == 6
    )

    # ======================================================
    # CANONICAL PATTERN IDS
    # ======================================================

    assert (
        pattern_ids
        == EXPECTED_PATTERN_IDS
    )

    # ======================================================
    # PATTERN NAMES
    # ======================================================

    pattern_names = {
        pattern.name
        for pattern in NEW_PRODUCT_PLATFORM_PATTERNS
    }

    assert (
        pattern_names
        == EXPECTED_NAMES
    )

    # ======================================================
    # DESCRIPTION INTEGRITY
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.description
        assert isinstance(
            pattern.description,
            str,
        )

    # ======================================================
    # MECHANISM INTEGRITY
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.mechanism
        assert isinstance(
            pattern.mechanism,
            str,
        )

    # ======================================================
    # TRIGGER SIGNALS
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.trigger_signals
        assert isinstance(
            pattern.trigger_signals,
            list,
        )

    # ======================================================
    # LEADING INDICATORS
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.leading_indicators
        assert isinstance(
            pattern.leading_indicators,
            list,
        )

    # ======================================================
    # CONFIRMATION INDICATORS
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.confirmation_indicators
        assert isinstance(
            pattern.confirmation_indicators,
            list,
        )

    # ======================================================
    # EARNINGS CHANNELS
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.earnings_channels
        assert isinstance(
            pattern.earnings_channels,
            list,
        )

    # ======================================================
    # MARKET MISTAKE
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.market_mistake
        assert isinstance(
            pattern.market_mistake,
            str,
        )

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.disconfirming_evidence
        assert isinstance(
            pattern.disconfirming_evidence,
            list,
        )

    # ======================================================
    # KILL SWITCH
    # ======================================================

    for pattern in NEW_PRODUCT_PLATFORM_PATTERNS:

        assert pattern.kill_switch
        assert isinstance(
            pattern.kill_switch,
            str,
        )

    # ======================================================
    # RESULT
    # ======================================================

    print(
        "Pattern Count                    : PASS"
    )

    print(
        "Pattern Type Integrity           : PASS"
    )

    print(
        "Family Integrity                 : PASS"
    )

    print(
        "Unique Pattern IDs               : PASS"
    )

    print(
        "Pattern Names                    : PASS"
    )

    print(
        "Descriptions                     : PASS"
    )

    print(
        "Mechanisms                       : PASS"
    )

    print(
        "Trigger Signals                  : PASS"
    )

    print(
        "Leading Indicators               : PASS"
    )

    print(
        "Confirmation Indicators          : PASS"
    )

    print(
        "Earnings Channels                : PASS"
    )

    print(
        "Market Mistake                   : PASS"
    )

    print(
        "Disconfirming Evidence           : PASS"
    )

    print(
        "Kill Switches                    : PASS"
    )

    print(
        "Canonical Pattern IDs            : PASS"
    )

    print()
    print("---")
    print()

    print(
        "EIOS NEW PRODUCT / PLATFORM PATTERNS : PASS"
    )


if __name__ == "__main__":
    main()