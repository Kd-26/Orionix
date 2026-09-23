# Capability-adaptive domain model

This document freezes the capability model. Day 3 implements the core versioned
accelerator, node, interconnect, cluster, software-environment, model, workload,
requirement, job, candidate, benchmark, recommendation, and capsule contracts.
Day 4 implements supplied-data compatibility evaluation and keeps engine
compatibility separate from Orionix certification. Discovery remains
unimplemented. Unknown facts remain unknown; reported, measured, and inferred
values carry source and confidence.

## Required contracts

### `AcceleratorSpec`

Vendor, device name, redacted/hashed device identifier, architecture family, compute capability or vendor equivalent, VRAM, reliably available memory bandwidth, supported numeric formats, device partition/MIG information, available power and thermal limits, and driver-visible feature metadata.

### `NodeSpec`

Stable node identifier, CPU architecture/count, RAM, local storage, accelerators, NUMA topology, network interfaces, operating system, and container runtime.

### `InterconnectSpec`

Link type; endpoint nodes/devices; peer-access capability; reported or measured bandwidth and latency; RDMA capability; fabric metadata; and provenance distinguishing reported, measured, or inferred values. Link types include PCIe, NVLink, InfiniBand, Ethernet, and extensible future values.

### `ClusterSpec`

Nodes, accelerator count, homogeneous/heterogeneous status, intra-node and inter-node topology, collective capabilities, provider extension metadata, and a cluster fingerprint. Multi-node membership and topology are valid in schema version 1 even while the first runtime is single-node.

### `SoftwareEnvironmentSpec`

OS/kernel, driver/CUDA, PyTorch/NCCL, engine name/version/image digest, kernel-library versions, and container/provider runtime.

### `HardwareCapabilities`

Supported precision modes and quantization kernels, peer-to-peer and collective capabilities, CUDA graph capability, memory limits, engine-feature compatibility, known limitations, and a source/confidence for every derived capability.

### `ParallelismPlan`

Replica count; data, tensor, pipeline, expert, and context parallel sizes; rank-to-node/device mapping; and collective backend. Cross-field validation must ensure ranks and products match the selected cluster resources and engine capability.

## Contract rules

- Core contracts import no NVIDIA, vLLM, Runpod, Modal, JarvisLabs, Ray, Kubernetes, provider, or database SDK types.
- Provider/engine-specific details live in namespaced, versioned extension metadata and never replace normalized fields.
- Stable identifiers are redacted or hashed before control-plane transfer; raw serial/device identifiers remain execution-side.
- Discovery emits observations plus provenance and confidence. It does not infer product certification.
- Capability evaluation consumes the model, workload constraints, `ClusterSpec`, software environment, engine declaration, and certification registry.
- Unknown, stale, or conflicting evidence cannot silently become a positive compatibility decision.

## Support decision sequence

1. Validate that contracts can represent the environment (`ARCHITECTURALLY_SUPPORTED`).
2. Evaluate model/cluster/software/configuration feasibility.
3. Ask the pinned engine adapter whether the combination is `ENGINE_COMPATIBLE`.
4. Match the complete synthetic/profile fingerprint to retained certification evidence (`CERTIFIED`) or label permitted incomplete evidence `EXPERIMENTAL`.
5. Reject known invalid, prohibited, or out-of-bound combinations as `UNSUPPORTED` with reasons.

The canonical state definitions are in the [support matrix](../supported-matrix.md).
The implemented Day 4 behavior is in the
[pre-execution compatibility rules](compatibility-rules.md).
