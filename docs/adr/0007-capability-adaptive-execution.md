# ADR-0007: Use capability-adaptive execution

- **Status:** Accepted
- **Date:** 2026-09-13

## Context

Models and serving configurations interact with accelerator architecture, count, memory, topology, software, engine, provider, and workload. Treating one named GPU or fixed cluster shape as the product architecture would create unsafe compatibility assumptions and prevent future hardware/provider support.

## Decision

Use one provider-neutral architecture whose versioned contracts represent accelerator, node, interconnect, cluster, software, capability, and parallelism facts. Discovery reports facts with provenance; capability evaluation and engine adapters determine feasibility; candidate generation consumes those results. Recommendations and artifacts are scoped to layered compatibility fingerprints. Multi-node is represented in the first cluster-contract version, while single-node runtime is delivered first. A reference GPU is only a repeatable validation fixture.

## Consequences

Ampere, Hopper, Blackwell, future accelerators, variable GPU counts, and provider execution models can share control-plane and workflow contracts without implying equal runtime support. Contracts and adapters require explicit unknowns and extension metadata. Configuration portability must be validated, and schema design is more detailed than a GPU-name allowlist.
