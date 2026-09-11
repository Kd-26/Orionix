# Architecture overview

Orionix is split into a control plane and a customer-side execution agent. The control plane will plan and coordinate optimizations; the agent will inspect and execute within customer GPU infrastructure. Versioned typed contracts cross the boundary.

```text
Control Plane: orchestration, policy, history, reporting
                         │ secure versioned commands
                         ▼
Customer Agent: inspection, engine adapters, benchmarks, capsule metadata
                         │ local-only execution
                         ▼
Customer GPUs: inference engines, CUDA, NCCL, caches, model weights
```

The platform does not replace an inference engine. Phase 0 has no API, remote control, GPU discovery, benchmark runner, optimizer algorithm, persistence, or deployment automation.

The future performance dataset is conceptually `Model × Hardware × Workload × Configuration → Observed performance`. Contracts remain ORM-independent so storage can be selected later.
