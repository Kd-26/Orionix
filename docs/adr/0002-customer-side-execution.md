# ADR-0002: Execute GPU work customer-side

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Models, prompts, GPU topology, and runtime artifacts are sensitive and environment-specific.

## Decision

Inspection, engine control, benchmarking, and future capsule generation occur in customer infrastructure by default; the control plane coordinates through minimal typed contracts.

## Consequences

Sensitive payloads need not leave the customer boundary. The agent becomes a high-trust component requiring strict permissions, authenticated commands, auditable egress, and careful upgrade compatibility.
