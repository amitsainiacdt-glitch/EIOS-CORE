# ADR-014 — Configured official-exchange disclosure discovery

Status: Approved and implemented as a bounded automatic intake path.

## Decision

An `EXCHANGE_DISCLOSURES` job may directly check exchange pages explicitly listed
for that company in the governed source manifest. This path runs independently
of general web search. It accepts only sources marked `EXCHANGE_OFFICIAL` with an
exchange filing/disclosure type, and the existing trusted registry restricts
retrieved links to official NSE/BSE domains.

The check is bounded to configured pages and a small document limit. Discovered
documents enter the existing acquisition receipt, immutable archive, duplicate
and version detection, extraction and review pipeline. Discovery or official
origin is provenance, not approval.

## Failure behaviour

Blocked pages, non-document responses, untrusted links and malformed content are
reported as failures or extraction holds. They do not create approved Facts,
Evidence, Catalysts, verdicts or trades. Existing governed browser/local fallback
rules remain available and must preserve the requested official URL.

## Initial coverage

The mechanism applies only where a company has an explicit exchange source in
the manifest. ANUP currently has a configured NSE financial-results page. This is
not a whole-market NSE/BSE collector and does not infer missing BSE codes or URLs.

