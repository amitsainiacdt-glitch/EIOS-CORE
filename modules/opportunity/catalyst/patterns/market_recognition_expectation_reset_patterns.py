"""
EIOS
Everest Investment Operating System

Market Recognition / Expectation Reset Catalyst Patterns

Purpose:
Canonical catalyst pattern definitions for situations where
market expectations about a company's future economics materially
change because new evidence becomes credible.

Design Principles:
- Definitions only.
- No scoring.
- No valuation.
- No ranking.
- No company-specific logic.
- No investment decision logic.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS = [

    # ======================================================
    # 1. EARNINGS EXPECTATION RESET
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-EARNINGS-RESET",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Earnings Expectation Reset",
        description=(
            "Forward earnings expectations change materially as "
            "new operating evidence causes the market to reassess "
            "the company's future earnings trajectory."
        ),
        trigger_signals=[
            "earnings estimate revisions",
            "improving forward indicators",
            "operating performance ahead of expectations",
            "management guidance changes",
        ],
        mechanism=(
            "New evidence changes assumptions about future earnings, "
            "causing analysts and investors to revise forward estimates."
        ),
        transmission_channels=[
            "earnings estimate revisions",
            "forward guidance",
            "analyst model changes",
            "investor expectation reset",
        ],
        leading_indicators=[
            "order momentum",
            "customer activity",
            "utilization changes",
            "forward pricing evidence",
        ],
        confirmation_indicators=[
            "consensus estimate revisions",
            "guidance upgrades",
            "earnings forecast increases",
            "broader analyst estimate convergence",
        ],
        typical_time_horizon="1-6 quarters",
        earnings_channels=[
            "higher expected earnings",
            "revised forward profitability",
            "improved earnings visibility",
        ],
        market_mistake=(
            "The market anchors to stale earnings expectations "
            "after the underlying business trajectory has changed."
        ),
        second_order_effects=[
            "analyst coverage upgrades",
            "higher institutional attention",
            "revised valuation assumptions",
            "greater investor confidence",
        ],
        disconfirming_evidence=[
            "forward indicators deteriorate",
            "estimate revisions reverse",
            "guidance fails to improve",
            "earnings improvement proves temporary",
        ],
        kill_switch=(
            "Subsequent operating evidence demonstrates that the "
            "assumed improvement in the forward earnings trajectory "
            "was not durable."
        ),
    ),


    # ======================================================
    # 2. GROWTH REACCELERATION RECOGNITION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-GROWTH-REACCELERATION",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Growth Reacceleration Recognition",
        description=(
            "The market recognizes that a period of temporary "
            "growth weakness is ending and that underlying growth "
            "drivers are returning."
        ),
        trigger_signals=[
            "improving sequential growth",
            "recovering demand indicators",
            "order recovery",
            "customer activity normalization",
        ],
        mechanism=(
            "Evidence shows that the prior slowdown was cyclical "
            "or temporary rather than structural, causing the market "
            "to revise its expectations for future growth."
        ),
        transmission_channels=[
            "growth estimate revisions",
            "forward revenue expectations",
            "earnings normalization",
            "investor sentiment reversal",
        ],
        leading_indicators=[
            "bookings",
            "customer enquiries",
            "capacity utilization",
            "inventory normalization",
        ],
        confirmation_indicators=[
            "sequential growth acceleration",
            "year-on-year growth recovery",
            "consensus growth upgrades",
            "sustained order recovery",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "revenue growth recovery",
            "earnings estimate upgrades",
            "improved operating leverage",
        ],
        market_mistake=(
            "The market treats a temporary slowdown as a permanent "
            "deterioration in the company's growth trajectory."
        ),
        second_order_effects=[
            "multiple normalization",
            "renewed institutional interest",
            "supplier confidence recovery",
            "capacity investment restart",
        ],
        disconfirming_evidence=[
            "growth recovery fails to persist",
            "orders remain weak",
            "customer demand deteriorates",
            "sequential improvement reverses",
        ],
        kill_switch=(
            "Multiple subsequent periods confirm that the expected "
            "growth reacceleration did not materialize."
        ),
    ),


    # ======================================================
    # 3. GROWTH DURABILITY RESET
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-DURABILITY-RESET",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Growth Durability Reset",
        description=(
            "The market materially changes its assumption about "
            "how long superior growth or economics can persist."
        ),
        trigger_signals=[
            "longer customer commitments",
            "persistent market-share gains",
            "structural demand evidence",
            "extended competitive advantage",
        ],
        mechanism=(
            "New evidence demonstrates that strong business economics "
            "are more durable than previously assumed, extending the "
            "expected duration of superior performance."
        ),
        transmission_channels=[
            "duration assumption",
            "long-term earnings expectations",
            "terminal growth expectations",
            "competitive-position reassessment",
        ],
        leading_indicators=[
            "customer retention",
            "market-share trends",
            "competitive behaviour",
            "reinvestment opportunities",
        ],
        confirmation_indicators=[
            "sustained superior growth",
            "persistent market-share gains",
            "stable competitive economics",
            "long-term guidance confidence",
        ],
        typical_time_horizon="2-10 years",
        earnings_channels=[
            "longer growth duration",
            "higher cumulative earnings",
            "greater reinvestment opportunity",
        ],
        market_mistake=(
            "The market underestimates the duration of the company's "
            "competitive advantage and therefore models excessive "
            "normalization too early."
        ),
        second_order_effects=[
            "longer reinvestment runway",
            "greater capital allocation opportunity",
            "higher strategic confidence",
            "reassessment of terminal economics",
        ],
        disconfirming_evidence=[
            "competitive intensity increases",
            "market-share gains reverse",
            "returns on reinvestment decline",
            "growth normalizes faster than expected",
        ],
        kill_switch=(
            "Clear evidence establishes that the competitive advantage "
            "cannot sustain the assumed duration of superior economics."
        ),
    ),


    # ======================================================
    # 4. GROWTH RUNWAY EXTENSION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-RUNWAY-EXTENSION",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Growth Runway Extension",
        description=(
            "Previously underappreciated markets, geographies, "
            "applications, customer segments, or distribution "
            "channels become credible sources of future growth."
        ),
        trigger_signals=[
            "new addressable markets",
            "new customer segments",
            "geographic expansion evidence",
            "new applications",
        ],
        mechanism=(
            "New evidence expands the market's understanding of "
            "the company's future opportunity beyond its previously "
            "recognized growth drivers."
        ),
        transmission_channels=[
            "TAM reassessment",
            "future revenue opportunity",
            "market-share opportunity",
            "long-term growth expectations",
        ],
        leading_indicators=[
            "new customer wins",
            "geographic traction",
            "application development",
            "distribution expansion",
        ],
        confirmation_indicators=[
            "commercial adoption in new markets",
            "revenue from new segments",
            "repeat customer activity",
            "market expansion evidence",
        ],
        typical_time_horizon="2-7 years",
        earnings_channels=[
            "expanded revenue opportunity",
            "longer growth runway",
            "higher future earnings potential",
        ],
        market_mistake=(
            "The market evaluates the company using its current "
            "addressable opportunity and underestimates credible "
            "future expansion avenues."
        ),
        second_order_effects=[
            "additional capacity investment",
            "new ecosystem development",
            "broader customer diversification",
            "greater reinvestment runway",
        ],
        disconfirming_evidence=[
            "new markets fail to scale",
            "customer adoption remains weak",
            "expansion economics are unattractive",
            "addressable market assumptions prove overstated",
        ],
        kill_switch=(
            "New growth avenues fail to demonstrate commercially "
            "scalable economics within the expected timeframe."
        ),
    ),


    # ======================================================
    # 5. CONSENSUS CONVERGENCE
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-CONSENSUS-CONVERGENCE",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Consensus Convergence",
        description=(
            "Previously wide-ranging market expectations converge "
            "toward a narrower and better-supported view of the "
            "company's future performance."
        ),
        trigger_signals=[
            "reduced estimate dispersion",
            "greater analyst agreement",
            "clearer operating visibility",
            "consistent evidence across periods",
        ],
        mechanism=(
            "Repeated evidence reduces uncertainty around the future "
            "business trajectory, causing divergent investor views "
            "to converge."
        ),
        transmission_channels=[
            "estimate dispersion reduction",
            "analyst model convergence",
            "risk perception change",
            "institutional participation",
        ],
        leading_indicators=[
            "improving disclosure",
            "more predictable operating metrics",
            "repeated guidance accuracy",
            "consistent customer behaviour",
        ],
        confirmation_indicators=[
            "narrower analyst estimates",
            "reduced earnings dispersion",
            "greater forecast consistency",
            "broader consensus agreement",
        ],
        typical_time_horizon="2-8 quarters",
        earnings_channels=[
            "greater earnings visibility",
            "lower forecast uncertainty",
            "more reliable forward estimates",
        ],
        market_mistake=(
            "The market applies an excessive uncertainty discount "
            "because investors disagree materially about the company's "
            "future trajectory."
        ),
        second_order_effects=[
            "greater institutional ownership",
            "lower perceived risk",
            "broader analyst coverage",
            "improved capital-market access",
        ],
        disconfirming_evidence=[
            "estimate dispersion remains high",
            "operating outcomes remain unpredictable",
            "guidance repeatedly misses",
            "new contradictory evidence emerges",
        ],
        kill_switch=(
            "Persistent evidence dispersion prevents the market "
            "from converging on a reliable forward business view."
        ),
    ),


    # ======================================================
    # 6. THESIS VALIDATION
    # ======================================================

    CatalystPattern(
        pattern_id="PAT-MARKET-EXPECTATION-THESIS-VALIDATION",
        family=CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET,
        name="Thesis Validation",
        description=(
            "Previously underappreciated leading indicators become "
            "confirmed by hard operating evidence, forcing a broader "
            "reassessment of the company's future trajectory."
        ),
        trigger_signals=[
            "leading indicators proving accurate",
            "customer behaviour confirmation",
            "capacity utilization confirmation",
            "order-to-revenue conversion",
        ],
        mechanism=(
            "Evidence that previously supported only a minority view "
            "becomes sufficiently strong and observable to force a "
            "broader market reassessment."
        ),
        transmission_channels=[
            "belief conversion",
            "estimate revisions",
            "institutional recognition",
            "forward expectation changes",
        ],
        leading_indicators=[
            "order flow",
            "customer commitments",
            "hiring",
            "capacity additions",
            "utilization",
        ],
        confirmation_indicators=[
            "reported earnings confirmation",
            "cash-flow confirmation",
            "market-share evidence",
            "repeat operating validation",
        ],
        typical_time_horizon="2-12 quarters",
        earnings_channels=[
            "higher earnings confidence",
            "revised growth expectations",
            "improved earnings visibility",
        ],
        market_mistake=(
            "The market dismisses early evidence because it is "
            "insufficiently confirmed, then fails to update rapidly "
            "when the evidence becomes conclusive."
        ),
        second_order_effects=[
            "analyst coverage expansion",
            "institutional recognition",
            "higher confidence in management",
            "faster expectation convergence",
        ],
        disconfirming_evidence=[
            "leading indicators fail to convert",
            "hard results contradict the thesis",
            "customer commitments are cancelled",
            "subsequent evidence weakens materially",
        ],
        kill_switch=(
            "Hard operating evidence directly contradicts the "
            "previously identified leading-indicator thesis."
        ),
    ),
]


__all__ = [
    "MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS",
]