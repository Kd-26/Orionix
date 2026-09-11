# ADR-0004: Separate provider-neutral execution from adapters

- **Status:** Accepted
- **Date:** 2026-09-11

## Context

Persistent hosts, cloud VMs/Pods, and serverless environments have different lifecycle semantics.

## Decision

Use stable `ExecutionBackend`, `ProvisioningBackend`, and `EngineAdapter` ports with typed contracts. Provider and engine SDK types remain inside adapters.

## Consequences

Planning remains portable and test doubles are simple. Adapters must normalize events/fingerprints without hiding provider-specific latency or lifecycle facts.
