# ADR-0005: Use an outbound, allowlisted agent protocol

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Inbound control and arbitrary commands increase risk inside customer infrastructure.

## Decision

The future agent initiates authenticated outbound communication and accepts only versioned, expiring, idempotent allowlisted commands. Generic remote shell execution is prohibited.

## Consequences

Customer firewall posture is simpler and command authority is auditable. Leases, at-least-once delivery, reconciliation, enrollment, rotation, and revocation must be designed before networking ships.
