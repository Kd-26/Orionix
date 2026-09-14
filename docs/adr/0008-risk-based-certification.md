# ADR-0008: Separate compatibility from risk-based certification

- **Status:** Accepted
- **Date:** 2026-09-13

## Context

Architectural representation and an engine vendor's compatibility claim do not demonstrate reliable startup, measurement, cleanup, recovery, reproducibility, security, or deployment for every model/environment combination. Exhaustively certifying a Cartesian product is also infeasible.

## Decision

Track `ARCHITECTURALLY_SUPPORTED`, `ENGINE_COMPATIBLE`, `CERTIFIED`, `EXPERIMENTAL`, and `UNSUPPORTED` independently from discovery facts. Certify immutable, versioned support profiles using risk-based representative coverage and retained evidence. Material fingerprint changes invoke layered invalidation and recertification. Planned matrix rows never carry a certified claim.

## Consequences

Production claims are narrow, auditable, expiring, and revocable. Customers may use permitted engine-compatible environments experimentally with warnings, but warnings cannot substitute for evidence. Certification operations and evidence retention add cost, so launch scope must be reduced rather than weakening gates.
