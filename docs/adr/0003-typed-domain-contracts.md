# ADR-0003: Communicate through versioned typed contracts

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Control plane, agent, integrations, and future persisted records will evolve independently.

## Decision

Subsystem boundaries exchange immutable, versioned Pydantic contracts and dependency-free typed identifiers instead of internal objects, vendor models, or ORM entities.

## Consequences

Validation and compatibility are explicit. Schema migrations and serialization stability require disciplined versioning, but implementation details remain replaceable.
