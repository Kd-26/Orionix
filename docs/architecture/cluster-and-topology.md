# Cluster and topology architecture

GPU count changes candidate architecture; it does not merely multiply capacity. Candidate generation must enumerate only plans feasible for the discovered model, workload, cluster, software, engine, and constraints.

For an eight-GPU cluster, feasible alternatives might include one TP=8 replica, two TP=4 replicas, four TP=2 replicas, eight TP=1 replicas, pipeline-parallel plans, or expert-parallel plans for a supported MoE model. These are examples, not supported configurations or performance claims.

Feasibility depends on model weights and KV-cache memory, workload concurrency, latency SLO, accelerator memory/numeric formats, peer access, NVLink/PCIe topology, inter-node network, collective backend, engine capabilities, precision, and quantization. Candidate pruning records reasons and evidence rather than relying on GPU-name rules.

## Multi-node representation

The first `ClusterSpec` schema must represent cluster membership, stable node roles, rank-to-device mapping, rendezvous metadata, collective backend, InfiniBand/RDMA/Ethernet capabilities, node health and partial failure, cross-node cancellation/cleanup, and clock/metric-source metadata.

Single-node runtime implementation precedes multi-node runtime. Multi-node schemas do not imply distributed launch, NCCL tuning, Ray support, or certification. Those capabilities require explicit implementation, failure testing, cleanup evidence, and profile certification.

## Topology evidence

- Every link records endpoints, type, peer-access status, bandwidth/latency when available, and whether each value was reported, measured, or inferred.
- Topology and cluster fingerprints change when membership, device mapping, partitions, material link attributes, or provider runtime identity changes.
- Heterogeneous clusters are representable but P2 experimental unless a narrower profile is certified.
- Partial discovery produces an incomplete report and cannot be upgraded to certified compatibility without required evidence.

Parallelism and memory layout are scoped to rank mapping and topology. Changing GPU count or mapping invalidates those layers even when every device has the same model name.
