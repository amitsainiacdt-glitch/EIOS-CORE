# EIOS local source import

Use this path when an official company or exchange document cannot be collected automatically.

## What to provide

Place an official quarterly-results PDF in a known local folder. Keep the original file unchanged. The document should show the issuer, reporting quarter, units, and the source page for each figure.

## What EIOS does

EIOS preserves the original file, records its hash, extracts text, checks the quarter labels and numbers, and creates only a staged candidate. A source name alone cannot approve a figure. Incomplete extraction, mixed annual/quarterly periods, ambiguous units, or missing source references are held for review.

## Approval boundary

Only after source reconciliation, META review, and human authorization may a quarterly figure appear as governed intelligence. Until then the dashboard shows it as pending or missing.

## Current limitation

The Coromandel annual report currently stored in EIOS is not a quarterly-results document, so it cannot populate the quarterly table. An official quarterly-results PDF is still required.
