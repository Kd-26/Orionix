# Architecture overview

Orionix is split into a control plane and an execution-side agent or provider worker. The control plane will plan and coordinate bounded optimizations; the execution component will inspect and run work within customer-controlled or isolated provider infrastructure. Versioned typed contracts cross the boundary.

```text
Control Plane: orchestration, policy, history, reporting
                         │ secure versioned commands
                         ▼
Agent / Provider Worker: discovery, engine lifecycle, benchmarks, capsule metadata
                         │ local-only execution
                         ▼
Customer GPUs: inference engines, CUDA, NCCL, caches, model weights
```

The platform does not replace an inference engine. Common control-plane, workflow, protocol, contract, metric, report, capsule, and security concepts are independent of a named GPU or provider. Runtime image, kernels, precision, parallelism, cache, scheduling, collectives, launch plan, and deployment output adapt to discovered capabilities. See [component ownership](component-ownership.md), the [capability model](capability-model.md), and [cluster topology](cluster-and-topology.md).

Every recommendation is scoped to a [layered compatibility fingerprint](compatibility-and-invalidation.md). Architecture representation, engine compatibility, and product certification are distinct [support states](../supported-matrix.md). A reference GPU is a repeatability fixture, not the product architecture.

The architecture separates contracts, configuration, discovery, workload definition, benchmarking, optimization, quality, capsules, telemetry, deployment export, integrations, agent/worker, control plane, CLI, and future web presentation. This milestone has no API, remote control, GPU discovery, benchmark runner, optimizer algorithm, persistence, or deployment automation.

The future performance dataset is conceptually `Model × Hardware × Workload × Configuration → Observed performance`. Contracts remain ORM-independent so storage can be selected later.
