# ADR-008 — Research Decision Packet extension

Status: Approved as architecture; extension implementation deferred.

## Decision

The future Research Decision Packet will wrap the existing fingerprint-bound
`CausalFirstEIPDecisionPacket`. It will not replace or reinterpret the EIP core.
The historical EIP packet fingerprint remains authoritative and unchanged.

## Consequences

Additional research context will receive an outer fingerprint. Future AI output
must bind to both the outer research packet and the unchanged EIP core packet.

