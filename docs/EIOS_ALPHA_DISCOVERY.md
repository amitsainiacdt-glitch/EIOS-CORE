# EIOS ALPHA DISCOVERY — CANONICAL COMMAND

**Command:** `Run EIOS Alpha Discovery`
**Version:** 3.0 (named 2026-10-19)
**Canonical checklist:** [EIOS Daily Research Sequence](EIOS_DAILY_RESEARCH_SEQUENCE.md)

## Meaning of the command

Whenever the user says **Run EIOS Alpha Discovery**, retrieve the canonical daily sequence and apply it to the latest accessible Indian listed-equity information. Search independently across sectors and individual stocks, then analyze leading changes in customer/supplier relationships, capability adoption, capacity, contracts, utilisation, economics and earnings multiplication.

Treat previously discussed names and holdings solely as separate hypotheses, never as discovery anchors. The system searches for credible 2–4-quarter inflections; also evaluates 25–40% in 3–12 months, 50–100% in 1–2 years and longer-run 5–10x potential **without claiming those gains are probable**.

For each candidate: capture source, publication and as-of date, independent evidence, causal earnings bridge, scenario-based cash EPS incorporating capex, working capital, debt and dilution, price-implied expectations, contradictions and kill tests. Accept explainable temporary imperfections, reject thesis-breaking flaws, and reject/mark Too Late what the market has already priced.

Classify Research Now / Early Watch / EIP Watch / Earliest Investable Point / Buy-zone Candidate / Wait / Too Late / Reject; maintain separate EIP timing, structural 10x, and swing/re-rating research lanes. Research qualifications do not trigger deployment. In daily scans output concise material changes, registry ADD/UPGRADE/DOWNGRADE/REMOVE/NO CHANGE and explicit no-fresh-high-conviction result when appropriate.

## Reference implementation

- `modules/discovery/pre_inflection.py`: early EIP gate.
- `modules/discovery/earnings_multiplication.py`: scenario cash earnings and verified supplier-link research.
- `modules/discovery/test_pre_inflection.py` and `modules/discovery/test_earnings_multiplication.py`: regression tests.

## Actual operating boundary

This is a **durable command and project standard**, not evidence of automatic NSE/BSE universe ingestion or a deployed hosted scanner. GitHub code is not automatically executed by ChatGPT scheduled tasks. Never say an actual exhaustive scan, registry update or dashboard deploy happened unless verified. The daily scheduled research watch should reference this specification. Updating code and improving methodology requires real commits and test/validation evidence.
