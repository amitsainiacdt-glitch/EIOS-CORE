# ADR-015 — Automatic NSE iXBRL review intake

Status: Approved and implemented as a non-approving exchange intake.

## Decision

The official-document pipeline recognizes HTML/iXBRL documents only on the exact
`nsearchives.nseindia.com` host. The acquired bytes must match their SHA-256
acquisition receipt. EIOS parses company identity, ISIN, currency, rounding,
reporting type, quarter, basis, period and a bounded set of income-statement
lines, then verifies ticker and company against the configured coverage job.

The resulting JSON is content-addressed by source hash and stored in the existing
company review-queue area. Reprocessing identical bytes is idempotent. Changed
saved content, invalid encoding, conflicting fields, unsupported currency/units,
wrong identity and lookalike domains fail closed.

## Authority

The output remains `EXCHANGE_CORROBORATION_CANDIDATE`, requires META and human
review, and explicitly cannot create approved Facts. Pipeline status separately
reports successful iXBRL candidates and held iXBRL documents. No EIP, verdict,
portfolio or trading authority is added.

## Limits

This covers configured NSE iXBRL result documents. It does not yet parse every
NSE/BSE disclosure format, discover companies without governed exchange sources,
or operate as a whole-market collector.

