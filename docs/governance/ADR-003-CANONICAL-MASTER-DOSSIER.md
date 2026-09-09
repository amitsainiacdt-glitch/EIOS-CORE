# ADR-003 — Canonical Master Dossier ownership

Status: Approved; migration not authorized.

## Decision

`modules.master_dossier.MasterDossier` is the proposed authoritative domain
model because it is typed and used by the active application and analytical
engines. `core.domain.master_dossier.MasterDossier` will remain unchanged until
a separately approved compatibility adapter is implemented.

## Consequences

No dossier is migrated or deleted in this checkpoint. Existing JSON remains
unchanged. Future migration must use additive identity/version fields,
dual-read compatibility tests, and must not rewrite historical data in place.

