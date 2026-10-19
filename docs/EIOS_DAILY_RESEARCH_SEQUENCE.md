# EIOS DAILY RESEARCH SEQUENCE — CANONICAL OPERATING CHECKLIST
Version: 1.1 | Adopted: 2026-10-19 | Applies to each requested EIOS daily scan.

## Mission and boundary
Find overlooked Indian listed companies where independently verified leading changes imply materially higher per-share cash earnings in approximately 2–4 quarters, before earnings, consensus or price fully reflect them. No quotas, no forced candidates, no automatic capital deployment. The complete NSE/BSE listed universe is the intended discovery universe; do not claim exhaustive coverage unless coverage logs prove it.

## Daily sequence — run in this order
1. **Set point-in-time snapshot.** Record IST date/time, latest exchange close, data timestamps, source availability, listing identifiers, and the actual coverage universe. Never use information published later than the assessed timestamp. Flag stale and missing inputs.
2. **Build independent universe.** Begin with all accessible NSE/BSE listings by ISIN/ticker; cover each sector and subindustry independently. Holdings, watchlists and previously discussed names must not affect discovery priority. Deduplicate and log covered/not-covered names and reason.
3. **Ingest causal events.** Read dated NSE/BSE filings, reports, announcements, credit-rating rationales and relevant official industry/regulatory sources; collect commissioning, capability/customer qualification, large contracts, utilisation/dispatch, new products, policy, capacity economics, input costs, pricing and cash collections. Do not mistake routine PR for a catalyst.
4. **Evidence ledger.** For each event record ticker/ISIN, primary document URL, event date, published date, relevant excerpt/fact, company claim vs independent corroboration, confidence, economic materiality, source timestamp, contradicting evidence and next verification. No fabricated sources or metrics.
5. **Identify causal change and window.** Explicitly model event -> volumes/price/mix/cost -> margins -> working-capital/interest/tax/capex -> cash earnings per share, with a 2–4-quarter window. Validate capacity, customer offtake and practical constraints. Do not demand quarterly PAT recovery first.
6. **Screen financial reality and contradictions early.** Review cash conversion, accruals/other income, receivables, inventory, contract assets, debt, pledges, refinancing, dilution, related parties, auditors, capital allocation and industry conditions. Temporary explainable imperfections are allowed when returns justify risk. Severe governance, structurally uneconomic growth, uncontrolled funding or nonviable liquidity are hard fails.
7. **Quantify expectation gap.** Estimate conservative/base/upside and bear cash-earnings bridges, incremental ROCE and per-share outcomes; distinguish sensitivity from forecast. Record which assumptions are independently substantiated. Compare expected improvement with what consensus or market prices already imply where data permit.
8. **Strict price-recognition and valuation gate.** Use date-correct market price, EV, equity dilution and normalised earnings, and track returns/multiple changes since original catalyst. Reject or mark Too Late if materially priced in. A fall from a high or low P/E alone is never proof of mispricing. If prices or recognition cannot be verified, do not issue a confirmed EIP/Buy-zone assessment.
9. **Independent challenge and kill tests.** Require explicit bear explanation, falsifiable operational and governance kill tests, contradictory facts, material downside, and triggers that would upgrade/downgrade the thesis. Do not force perfect balance sheets or completed financial confirmation.
10. **Classify research, with no quota.** Research Now / Early Watch / EIP Watch / Earliest Investable Point / Buy-zone Candidate / Wait / Too Late / Reject. Distinguish evidence confidence from statistical return probabilities. When zero names qualify explicitly state: 'No fresh high-conviction opportunity qualified.'
11. **Update distinct registries.** (A) 10x/5–10-year Structural Re-rating: TAM, capability/capacity, orders/utilisation, earnings scalability, cash conversion, debt, dilution, governance, recognition and kill tests. (B) EIP/early timing: leading evidence, timing, expectation gap, valuation, price recognition, contradictions and exact triggers. Company may be in both if independently qualified. Record ADD/UPGRADE/DOWNGRADE/REMOVE/NO CHANGE with dates and sources. Do not imply that modifying a research registry buys a stock.
12. **Add horizon views without conflation.** Evaluate independently 25–40%/3–12-month repeatable swing and 50–100%/1–2-year major re-rating. These are aspirational research targets, not guarantees or probabilities. Portfolio holdings are evaluated separately with investment-thesis accountability.
13. **Separate deployment gate.** A Buy-zone Candidate is a research stage only. Fresh ADD/HOLD/REDUCE/EXIT instructions require independent current-price, downside, liquidity, diversification, concentration and risk-budget review, with stated uncertainty. Never infer an order from a registry status.
14. **Publish concise daily change log.** Show new material discovery, facts vs inference, source dates, leading indicators, expectation gap, mispricing/asymmetry, downside and kill tests, today's research class, changes in both registries and explicit capital status. Report universe coverage limitations and unresolved verification. Prefer no new candidate to weak watchlist filler.
15. **Record outcome and learn.** Preserve the point-in-time thesis and later results, missed catalysts, false positives, rerating or dilution, dated recommendations, and whether a prior user-reliant recommendation was mistaken. Backtest only with point-in-time information and include failed/delisted companies; do not leak later outcomes into research.

## Priority research streams
- Global/India customer qualification and high-value product adoption (Shivalik-style capability inflection).
- Capacity commissioning, utilisation, profitable order conversion (Welspun-style transformation).
- Temporary profit disappointment with intact leading demand and improving future unit economics (Cyient DLM-style opportunities).
- Industry pricing, supply, policy, asset recycling and economic structure change.
Never limit the universe to these themes.

## Output invariant
Each run ends with a dated summary, documented coverage, research-folder changes (or NO CHANGE), and explicit capital-deployment separation. **If nothing passes, say so.** 
Reference implementation: `modules/discovery/pre_inflection.py`.
Note: this checklist is the operating specification, not proof that live daily crawling or automated execution is deployed.

## Mandatory invocation protocol (v1.1 — 2026-10-19)
- For **every user-requested EIOS daily scan or full-scan continuation**, read this file first and follow steps 1–15 in order. This applies even if the user only says “run EIOS” or “daily research”.
- Start by confirming source/data availability. When live crawling, exhaustive universe scanning, or market prices are unavailable, disclose exactly what was and was not checked; never invent run counts, independent verification or registry updates.
- Keep **discovery results** distinct from **existing-holding reviews**, **EIP timing**, **10x structural potential**, and **capital deployment**. A decision in one lane never silently changes another.
- Keep **research registry changes** traceable with date, source and reason. “NO CHANGE” means no new qualifying evidence was established; it does not assert a freshly verified review of every company.
- After the scan, use a final checklist: (a) fresh independent discoveries, (b) leading cause and 2–4-quarter cash bridge, (c) price-recognition gate, (d) contradiction/kill test, (e) both-folder ADD/UPGRADE/DOWNGRADE/REMOVE/NO CHANGE, (f) separate capital verdict, (g) explicit no-fresh-qualifier statement if applicable.
- This checklist is durable repository documentation. It does not itself schedule or run research; automatic daily execution requires an independently deployed scheduler and verified data ingestion.
