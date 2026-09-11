# ADR-0001: Use a Python monorepo

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Contracts and multiple early subsystems will evolve together, while their boundaries must remain testable.

## Decision

Use a uv-managed Python monorepo with independently packaged modules and a single lockfile/quality gate.

## Consequences

Atomic contract changes and consistent tooling are simple. Package metadata preserves extraction options, while CI must actively enforce dependency direction and avoid accidental coupling.
