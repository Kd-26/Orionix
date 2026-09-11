# ADR-0003: Communicate through typed, versioned contracts

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Control plane, agent, integrations, exported artifacts, and future persisted records evolve independently.

## Decision

Subsystem boundaries exchange immutable, versioned Pydantic contracts and common typed identifiers instead of internal objects, vendor models, shell strings, or ORM entities.

## Consequences

Validation and compatibility are explicit. Schema migrations and serialization stability require discipline, but implementations and transports remain replaceable.
