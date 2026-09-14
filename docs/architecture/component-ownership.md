# Component ownership and adaptive boundaries

One architecture supports many accelerator families, GPU counts, cluster shapes, engines, and providers. The architecture is common; environment-specific choices are derived from discovered, provenance-bearing capabilities.

## Common product layer

The following remain stable across hardware and providers: control-plane concepts, agent protocol, domain contracts, job lifecycle, benchmark definitions, optimizer interfaces, constraint representation, quality-result format, report format, Execution Capsule manifest format, and security/data-boundary policy.

| Component | Owns | Must not own |
|---|---|---|
| Control plane | Tenancy, policy, orchestration, budgets, state/history, certification registry, reporting, audit | GPU processes, provider SDK objects, raw customer data |
| Agent/worker | Outbound protocol, leases, isolated workspace, command enforcement, lifecycle supervision, redacted results | Optimization policy, provider account credentials, arbitrary shell |
| Discovery | Observed provider/node/accelerator/topology/software facts and provenance | Support or certification decisions |
| Capability evaluator | Architectural representability and combination feasibility | Engine launch translation or certification evidence approval |
| Benchmark | Canonical plans, measurements, provenance, partial-run semantics | Provisioning, candidate ranking, fabricated results |
| Optimizer | Feasible candidate generation, explicit objectives, budgets, Pareto ranking | Engine/provider control, hidden scoring, quality inference |
| Quality | Local evaluation and normalized result contracts | Dataset export, ranking policy, engine lifecycle |
| Capsule/report | Reproducibility metadata, evidence references, layered validity | Unsafe binary loading, automatic deployment |
| Deployment export | Deterministic reviewable output without secrets | Live infrastructure mutation |

## Capability-adaptive layer

Discovered facts and adapter declarations select or generate the engine runtime/image, driver/CUDA compatibility, available kernels, precision/quantization, parallelism, batching/scheduling, KV-cache layout, CUDA graph policy, collective communication, multi-node launch plan, provider storage/provisioning behavior, compiled artifacts, and deployment configuration.

An optimized configuration is never presumed valid or optimal outside its [compatibility fingerprint](compatibility-and-invalidation.md). Hardware, topology, provider, model, engine, driver, CUDA, libraries, or workload changes require the applicable revalidation. Architecture-specific compiled artifacts are not automatically portable.

## Execution ports

- `ProvisioningBackend` creates, inspects, stops, or terminates provider compute. It is a no-op for an already available customer host, owns provider account API interaction, and does not benchmark or optimize.
- `ExecutionBackend` operates on available compute: it discovers the cluster, prepares an isolated job environment, starts/stops an engine from an allowlisted typed launch specification, emits lifecycle events, and cleans up. It does not choose the optimal configuration.
- `EngineAdapter` declares engine capabilities, validates model/cluster/configuration combinations, and translates a provider-neutral serving configuration into a typed `EngineLaunchSpec`. It does not provision resources or rank results.

The current Python ports are foundation interfaces and may evolve when capability contracts are implemented. No port may expose `execute_shell(command: str)` or vendor SDK types.
