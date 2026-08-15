"""
EIOS
Everest Investment Operating System

Fiscal / Tax Catalyst Patterns

Purpose:
Canonical machine-readable patterns beneath the
FISCAL_TAX CatalystFamily.

Design:
- Passive data only
- No scoring
- No ranking
- No valuation
- No investment decision
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


FISCAL_TAX_PATTERNS = [

    # ======================================================
    # 1. TAX RATE CHANGE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-RATE-CHANGE"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Tax Rate Change"
        ),
        description=(
            "A change in the applicable tax rate materially "
            "changes company earnings and free cash flow."
        ),
        trigger_signals=[
            "Budget announcement",
            "Tax rate proposal",
            "Tax legislation",
            "Corporate tax notification",
        ],
        mechanism=(
            "Tax rate change → effective tax rate change → "
            "net profit/FCF change → valuation impact."
        ),
        transmission_channels=[
            "Effective tax rate",
            "Net profit",
            "Free cash flow",
            "ROIC",
        ],
        leading_indicators=[
            "Budget proposals",
            "Tax consultation",
            "Legislative drafts",
        ],
        confirmation_indicators=[
            "Tax notification",
            "Reported effective tax rate",
            "Cash tax reduction/increase",
        ],
        typical_time_horizon=(
            "1-4 quarters"
        ),
        earnings_channels=[
            "Net Profit",
            "EPS",
            "FCF",
            "ROIC",
        ],
        market_mistake=(
            "Market reacts to headline tax rates but "
            "underestimates the actual earnings effect."
        ),
        second_order_effects=[
            "Higher reinvestment capacity",
            "Improved dividend capacity",
            "Faster deleveraging",
        ],
        disconfirming_evidence=[
            "Tax benefit does not apply to the company",
            "Effective tax rate remains unchanged",
            "Offsetting tax provisions",
        ],
        kill_switch=(
            "The announced tax change does not materially "
            "alter the company's effective cash tax burden."
        ),
    ),

    # ======================================================
    # 2. TAX INCENTIVE / CREDIT
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-INCENTIVE-CREDIT"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Tax Incentive / Credit"
        ),
        description=(
            "A tax incentive or credit improves economics "
            "for qualifying investment, production, or activity."
        ),
        trigger_signals=[
            "Tax credit announcement",
            "Investment incentive",
            "Production incentive",
            "Budget allocation",
        ],
        mechanism=(
            "Tax incentive → lower effective cost/tax burden → "
            "higher project returns → increased investment or earnings."
        ),
        transmission_channels=[
            "Project economics",
            "Effective tax rate",
            "ROIC",
            "FCF",
        ],
        leading_indicators=[
            "Policy proposal",
            "Eligible-sector announcement",
            "Draft guidelines",
        ],
        confirmation_indicators=[
            "Eligibility notification",
            "Approved claims",
            "Company disclosure of benefit",
        ],
        typical_time_horizon=(
            "1-3 years"
        ),
        earnings_channels=[
            "EBITDA",
            "Net Profit",
            "FCF",
            "ROIC",
        ],
        market_mistake=(
            "Market recognizes the headline incentive but "
            "underestimates its cumulative earnings effect."
        ),
        second_order_effects=[
            "Capacity expansion",
            "Higher industry investment",
            "Improved competitive position",
        ],
        disconfirming_evidence=[
            "Company fails eligibility criteria",
            "Benefit is immaterial",
            "Delayed reimbursement",
        ],
        kill_switch=(
            "The company cannot qualify for or economically "
            "capture the announced incentive."
        ),
    ),

    # ======================================================
    # 3. TAX EXEMPTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-EXEMPTION"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Tax Exemption"
        ),
        description=(
            "A new or expanded tax exemption materially "
            "reduces the tax burden on a business activity."
        ),
        trigger_signals=[
            "Exemption announcement",
            "Budget provision",
            "Tax notification",
            "Sector-specific exemption",
        ],
        mechanism=(
            "Tax exemption → reduced tax burden → "
            "higher post-tax economics → earnings/FCF improvement."
        ),
        transmission_channels=[
            "Tax expense",
            "Net profit",
            "FCF",
            "Project returns",
        ],
        leading_indicators=[
            "Budget proposal",
            "Draft legislation",
            "Industry consultation",
        ],
        confirmation_indicators=[
            "Final notification",
            "Company qualification",
            "Reported tax benefit",
        ],
        typical_time_horizon=(
            "1-4 quarters"
        ),
        earnings_channels=[
            "Net Profit",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "Market assumes the exemption is temporary or "
            "too small and misses its recurring effect."
        ),
        second_order_effects=[
            "Higher capital allocation capacity",
            "Improved project viability",
            "Industry investment acceleration",
        ],
        disconfirming_evidence=[
            "Exemption narrowly defined",
            "Company excluded",
            "Sunset clause limits benefit",
        ],
        kill_switch=(
            "The exemption does not apply to the company's "
            "relevant earnings or expires before meaningful benefit."
        ),
    ),

    # ======================================================
    # 4. INDIRECT TAX CHANGE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-INDIRECT-TAX"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Indirect Tax Change"
        ),
        description=(
            "A change in GST, excise, customs duty, or another "
            "indirect tax alters demand, pricing, or industry economics."
        ),
        trigger_signals=[
            "GST rate change",
            "Customs duty change",
            "Excise change",
            "Import duty notification",
        ],
        mechanism=(
            "Indirect tax change → consumer/input price change → "
            "demand or cost change → revenue/margin impact."
        ),
        transmission_channels=[
            "Demand",
            "Pricing",
            "Input costs",
            "Gross margin",
        ],
        leading_indicators=[
            "Budget proposals",
            "GST Council decisions",
            "Customs policy changes",
        ],
        confirmation_indicators=[
            "Final notification",
            "Price changes",
            "Volume response",
            "Margin impact",
        ],
        typical_time_horizon=(
            "1-4 quarters"
        ),
        earnings_channels=[
            "Revenue",
            "Gross Margin",
            "EBITDA",
            "EPS",
        ],
        market_mistake=(
            "Market focuses on the tax-rate headline without "
            "correctly estimating pass-through and volume effects."
        ),
        second_order_effects=[
            "Market-share shifts",
            "Demand acceleration",
            "Supplier substitution",
            "Pricing changes",
        ],
        disconfirming_evidence=[
            "Full pass-through neutralizes economics",
            "Demand destruction",
            "Competitors absorb the benefit",
        ],
        kill_switch=(
            "Actual pricing, volume, or cost effects differ "
            "materially from the expected transmission mechanism."
        ),
    ),

    # ======================================================
    # 5. FISCAL SPENDING / ALLOCATION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-SPENDING-ALLOCATION"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Fiscal Spending / Allocation"
        ),
        description=(
            "Government fiscal allocation creates or accelerates "
            "demand in targeted sectors."
        ),
        trigger_signals=[
            "Budget allocation",
            "Infrastructure spending",
            "Government programme",
            "Public investment plan",
        ],
        mechanism=(
            "Fiscal allocation → government demand/capex → "
            "industry orders → company revenue and earnings."
        ),
        transmission_channels=[
            "Government demand",
            "Order inflow",
            "Revenue",
            "Capacity utilisation",
        ],
        leading_indicators=[
            "Budget allocation",
            "Tender pipeline",
            "Project approvals",
            "Government capex data",
        ],
        confirmation_indicators=[
            "Tender awards",
            "Order wins",
            "Project execution",
            "Revenue conversion",
        ],
        typical_time_horizon=(
            "1-3 years"
        ),
        earnings_channels=[
            "Revenue",
            "EBITDA",
            "EPS",
            "FCF",
        ],
        market_mistake=(
            "Market treats budget announcements as headlines "
            "and underestimates actual execution and order conversion."
        ),
        second_order_effects=[
            "Capacity expansion",
            "Operating leverage",
            "Supplier ecosystem growth",
            "Market-share gains",
        ],
        disconfirming_evidence=[
            "Low budget execution",
            "Tender delays",
            "Project cancellations",
            "Weak order conversion",
        ],
        kill_switch=(
            "Fiscal allocation fails to translate into actual "
            "orders or executable projects."
        ),
    ),

    # ======================================================
    # 6. TAX REGIME STRUCTURAL CHANGE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-FISCAL-TAX-STRUCTURAL-REGIME"
        ),
        family=CatalystFamily.FISCAL_TAX,
        name=(
            "Tax Regime Structural Change"
        ),
        description=(
            "A structural change in the tax regime permanently "
            "alters relative economics across companies or industries."
        ),
        trigger_signals=[
            "Major tax reform",
            "New tax regime",
            "Structural tax legislation",
            "Multi-year tax reform",
        ],
        mechanism=(
            "Structural tax reform → persistent economics change → "
            "capital allocation shift → industry earnings re-rating."
        ),
        transmission_channels=[
            "Effective tax rate",
            "Capital allocation",
            "Industry economics",
            "Competitive position",
        ],
        leading_indicators=[
            "Tax reform proposal",
            "Legislative process",
            "Industry consultation",
        ],
        confirmation_indicators=[
            "Legislation enacted",
            "Implementation rules",
            "Company disclosures",
            "Multi-period financial impact",
        ],
        typical_time_horizon=(
            "2-5 years"
        ),
        earnings_channels=[
            "Net Profit",
            "FCF",
            "ROIC",
            "Valuation",
        ],
        market_mistake=(
            "Market treats structural tax reform as a one-off "
            "earnings event rather than a change in long-term economics."
        ),
        second_order_effects=[
            "Capital reallocation",
            "Industry consolidation",
            "Competitive advantage shifts",
            "Higher reinvestment",
        ],
        disconfirming_evidence=[
            "Frequent policy reversals",
            "Limited applicability",
            "No persistent earnings effect",
        ],
        kill_switch=(
            "The tax regime change fails to produce a persistent "
            "difference in after-tax economics."
        ),
    ),
]


__all__ = [
    "FISCAL_TAX_PATTERNS",
]