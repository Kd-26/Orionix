# Product scope

## Product definition

LLM Optimizer is a capability-adaptive platform that inspects a model, workload, service-level objectives (SLOs), quality constraints, cost constraints, GPU cluster, software environment, and provider environment; constructs only compatible serving candidates; benchmarks those candidates on the target infrastructure; validates performance and quality; recommends measured Pareto-optimal configurations; and generates versioned reproducibility and deployment artifacts.

The product sits above inference engines. It does not replace vLLM, SGLang, TensorRT-LLM, CUDA, NCCL, or GPU providers. Its value is hardware-, topology-, workload-, and engine-aware optimization; bounded experiment planning; reproducible benchmarking; SLO, quality, and cost validation; historical performance intelligence; reusable Execution Capsules; deployment configuration export; and revalidation after drift.

## First customer

- **Organization:** an AI company serving an open-weight LLM on rented or owned NVIDIA GPUs.
- **Primary user:** an ML platform engineer, inference engineer, or technical founder.
- **Current environment:** customer GPU servers or providers such as Runpod, JarvisLabs, or Modal.
- **Problem:** manually selecting engine, precision, parallelism, batching, cache, scheduler, and deployment settings is expensive and unreliable.
- **Outcome:** a measured, evidence-backed, reproducible recommendation for the customer's actual model, workload, cluster, and software environment.

The first release serves technically capable teams, not a no-code consumer persona. Customers review and apply exported configuration manually.

## Day-80 promise

For a published set of certified model, GPU-cluster, software, engine, and provider profiles, LLM Optimizer securely executes a bounded optimization workflow and returns an evidence-backed serving recommendation, constraint and quality results, a versioned Execution Capsule, and reproducible deployment configuration. Other engine-compatible environments may run in experimental mode with explicit warnings.

The architecture represents Ampere, Hopper, Blackwell, future accelerator architectures, any discovered GPU count, and multi-node clusters. The selected engine runtime determines compatibility. Initial runtime delivery prioritizes single-GPU and single-node multi-GPU execution; multi-node is represented from the first cluster-contract version but implemented and certified later. vLLM is the first production engine and SGLang is later or beta. Local Ubuntu/NVIDIA hosts, Runpod Pods, JarvisLabs VM or managed environments, and Modal Function/Sandbox/server workloads use specialized adapters.

A reference validation environment will be selected according to hardware access and customer demand for repeatable debugging and CI. It is not the only target, a support shortcut, or a product dependency.

## Scope cut line

### P0 — paid production beta

- Capability-adaptive contracts; cluster/topology discovery; and a secure agent/worker protocol.
- Local Ubuntu and at least one hosted-provider backend, with vLLM integration.
- Reproducible baseline and candidate benchmarking with bounded time, GPU-hour, cost, OOM, and failure limits.
- SLO and limited quality validation, Pareto ranking, finalist confirmation, reports, and layered capsule metadata.
- Reviewable engine/Docker configuration export; no automatic live deployment.
- Tenant-scoped control-plane jobs, history, audit, monitoring, backups, restore, rollback, and diagnostics.
- Retained certification evidence for every advertised profile.

### P1 — after P0 gates pass

- A second hosted provider and representative Ampere/Hopper/Blackwell expansion based on access and demand.
- Additional single-node multi-GPU profiles, Kubernetes/Helm export, scheduled revalidation, historical comparison, and more quality evaluators.

### P2 — experimental

- Modal production certification, SGLang, multi-node runtime, heterogeneous clusters, MoE/expert-parallel optimization, multiple agents per project, and advanced semantic evaluation.

### Deferred research

- TensorRT-LLM production support and Foundry SAVE/LOAD.
- Portable graph restoration, kernel extraction, deterministic memory reconstruction, and custom kernels.
- Learned predictors, automatic live deployment/rollback, a Kubernetes operator, autonomous autoscaling, billing, and enterprise identity lifecycle.

Architecture-level representation of multi-node and future GPU families is P0. Implementing and certifying every combination is not. The [support-state model](supported-matrix.md) and [certification policy](operations/certification-policy.md) control all support claims.

## Current implementation status

This milestone provides architecture, foundation contracts, tests, and documentation only. It does not yet discover GPUs, provision resources, launch engines, execute benchmarks, optimize configurations, evaluate quality, persist control-plane data, expose production APIs, authenticate users, deploy workloads, or implement a UI.
