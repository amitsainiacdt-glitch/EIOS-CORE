# Recovery Intelligence Engine — Experimental Pilot

Status: **research prototype; not deployed**, not a replacement for BRAVO v4.7.
Preserve v4.6 registry, current holdings and permanent BESS coverage.

## Goal
Find causal business recovery 2–4 quarters before reported earnings improve, *and* test whether the market price leaves enough asymmetric reward. An early signal is not a purchase recommendation.

## Data contract
One row per company, observation date and signal. Required:
- `ticker`, `sector`, `engine`, `observation_date`, `published_at` (timezone aware), `source_url`, `metric`, `observed_value`, `unit`
- `direction` (up/down), `prior_comparable_value`, `interpretation`, `counter_evidence`, `independently_verified`, `confidence`
- `price_asof`, `price`, `corporate_action_adjustment`, `diluted_shares`, `funding_gap`, `kill_test`, `action`
- Missing information must be NULL/UNKNOWN, never silently converted to zero.

### Hard anti-hindsight rule
An observation is eligible for a historical decision on date T **only if published_at <= T at the decision cutoff**. Never use the future report period date as the publication date. Store the original exchange notice URL and timestamp. Replays must use original available prices, with later corporate actions adjusted *consistently* for comparisons.

## Initial signal families
1. Capacity and physical utilisation
2. Order-to-dispatch-to-collection
3. Input/output pricing spreads and volume
4. New product/customer qualification and repeat orders
5. Lender delinquencies/collections/credit costs, including vintages
6. Receivables aging, inventory and operating cash conversion
7. Debt, productive financing and liquidity
8. Industry capacity closures and supply/demand
9. Business-model economics and recurring revenues
10. Cross-check superinvestor transactions only as discovery leads; never grant ADD points on investor identity

Use independent evidence across different *mechanisms*. Two press stories paraphrasing the same company statement are **one** signal, not two.

## Research score (not a calibrated probability)
- Causal leading evidence 25
- Evidence of improving trend 20
- Earnings sensitivity 15
- Cash/balance sheet 15
- Valuation asymmetry 15
- Market recognition gap 10

Each 0–5, weighted to 0–100. A high score permits further investigation **only**. Missing data -> unavailable, not an assumed neutral score. Material governance, opaque dilution or unfinanced cash deficits prohibit ADD irrespective of score.

## Pilot labels
- Fundamental recovery: next 4 quarters show sustainable improvement in relevant operating metric(s), not just PAT from exceptional items.
- Market outcome: 6/12/24-month *total* returns vs sector and Nifty 500, after corporate actions and realistic costs.
- Both labels reported separately. Include failed and flat recoveries, delisted stocks and names that ceased reporting.

## Training procedure
1. Freeze historical decision dates and the data sources available at those dates.
2. Assemble 100 episodes spanning 2016–2025 with all sectors, positive/negative/control cases.
3. Preserve timestamped price and exchange filings plus archived source documents.
4. Score blindly using only eligible observations; record missing data.
5. Evaluate precision, recall, false-positive rate, calibration after fitting a probability model, downside, drawdown, median excess returns and time-to-recognition.
6. Time-split train (earlier years) vs validation (later years); hold out entire companies to assess generalisation; avoid selecting episodes by eventual winners.
7. Run prospective shadow signals for at least two reporting cycles before contemplating use as an ADD input.

## Initial live shadow cohort
Time Technoplast (composites), Ujjivan SFB (credit), Gandhar Oil (spreads/cash), Kirloskar Pneumatic (order conversion), Sharda Cropchem (cycle), EPack Prefab (capacity), Pace Digitek (BESS finance and dispatch), Ashoka Buildcon (SPV sale/debt).
Add independent discovery names before repeating this cohort.

## Release gates
- Unit tests on date leakage, missing data and fatal flags.
- Data source completeness and corporate-action reconciliation.
- Published out-of-sample results; disclose if signal fails.
- Explicit user approval before adopting as production v4.8.
- CAPITAL DEPLOYMENT = ₹0. No trading execution.
