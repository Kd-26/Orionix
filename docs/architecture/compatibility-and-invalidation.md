# Compatibility fingerprint and layered invalidation

Every recommendation, report, capsule, compiled artifact, and deployment export is scoped to a versioned compatibility fingerprint. Equality of GPU names is insufficient evidence of portability.

## Fingerprint contents

- Model identity, revision, architecture, and relevant format metadata.
- Cluster, node, accelerator, and topology fingerprints, including GPU architecture, compute capability, count, memory, partitions, and rank mapping.
- Provider, region, storage type, execution/runtime class, and redacted environment identity.
- OS/kernel, driver, CUDA, PyTorch, NCCL, engine version, engine image digest, and kernel-library versions.
- Precision, quantization, parallelism, collective backend, KV-cache layout version, and serving policy.
- Workload-policy version, constraint/evaluator versions, deployment target, and capsule schema version.

Fingerprint fields use canonical serialization and explicit unknown values. Architecture-specific binary digests remain execution-side unless a customer-approved artifact policy allows transfer.

## Invalidation layers

| Layer | Invalidated by examples | May remain reusable |
|---|---|---|
| `MODEL` | Model identity, revision, architecture, tokenizer-relevant change | Provider metadata unrelated to model |
| `HARDWARE` | Accelerator architecture/count/memory/partition or node change | Model identity |
| `KERNEL` | Compute capability, kernel library, precision/quantization change | Portable configuration metadata after reevaluation |
| `ENGINE_RUNTIME` | Engine version/image, driver, CUDA, PyTorch, NCCL change | Model/workload identity |
| `CUDA_GRAPH` | Runtime, kernel, address/layout, batch/shape assumptions change | Non-graph benchmark provenance |
| `MEMORY_LAYOUT` | GPU count, KV-cache layout, allocator, model/precision change | Higher-level objective/constraints |
| `PARALLELISM_TOPOLOGY` | Rank mapping, node membership, GPU count, links, collective backend change | Model identity and portable policy intent |
| `SERVING_POLICY` | Batching, scheduling, cache, speculative or request-policy change | Hardware observations |
| `WORKLOAD_POLICY` | Workload distribution, SLO, quality/cost policy version change | Model and environment identity |
| `PROVIDER_EXECUTION` | Provider, region, storage, runtime class, lifecycle semantics change | Provider-neutral model metadata |
| `DEPLOYMENT` | Export format, target runtime, secret requirements, image reference change | Confirmed benchmark evidence subject to lower layers |

Invalidation propagates from changed lower layers to dependent artifacts, but portable metadata can survive when its own inputs remain valid. The future algorithm must return affected layers, reasons, and required revalidation; it is not implemented on Day 1.

Examples:

- A workload change may invalidate the recommendation and serving policy without changing model identity.
- Moving providers requires execution, storage, environment, topology, cost, and timing revalidation.
- Moving from Ampere to Hopper or Blackwell invalidates architecture-specific kernels, graphs, and memory assumptions.
- Changing GPU count invalidates parallelism, rank mapping, topology, memory layout, and generally measured results.
- Runtime/library changes may invalidate compiled artifacts even on unchanged hardware.

Portable metadata is not proof that a configuration remains optimal. Revalidation policy, evidence age, and certification profile determine what may be reused.
