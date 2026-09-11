# ADR-0006: Start with one modular control-plane deployable

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

The product needs several business modules but has no proven independent scaling or failure-isolation requirements.

## Decision

Organizations, projects, agents, jobs, experiments, capsules, schedules, and audit boundaries begin inside one deployable service, separated by internal modules and versioned contracts.

## Consequences

Operations remain simple and premature distributed infrastructure is avoided. Modules may be extracted later only from observed scaling, ownership, or reliability pressure.
