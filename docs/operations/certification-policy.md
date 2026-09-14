# Risk-based certification policy

Certification is evidence for an exact versioned support profile, not a general statement about a GPU family, provider, engine, or representable environment. Testing uses risk-based representative coverage rather than an infeasible Cartesian product.

## Certification unit

A profile binds:

- Provider and execution runtime, region/runtime class, storage semantics, and worker image.
- Accelerator architecture/count, node count, partitioning, and topology.
- OS/kernel, driver, CUDA, PyTorch, NCCL, engine version, and engine image digest.
- Model architecture, exact revision, precision/quantization, and enabled feature set.
- Parallelism/rank mapping, serving policy, workload class/envelope, and capsule schema.

The profile has an immutable identifier and fingerprint, status, evidence-manifest digest, owner, approval time, expiry/review time, known limitations, and revocation reason when applicable.

## Required evidence

1. Image/dependency provenance, compatibility declarations, vulnerability review, and configuration validation.
2. Startup, enrollment, discovery completeness/provenance, engine readiness, and normal cleanup.
3. Reproducible baseline and candidate execution with canonical metrics, sample policy, variance, and drift evidence.
4. OOM, timeout, malformed input, infrastructure failure, cancellation, connection loss, restart, reconciliation, and orphan-cleanup behavior.
5. Hard budget enforcement for candidate count, elapsed time, GPU-hours, cost where knowable, consecutive OOMs, repeated infrastructure failures, and finalist runs.
6. Constraint and approved quality evaluation, Pareto ranking, and at least the configured independent finalist confirmation count.
7. Capsule validation, integrity, compatibility/invalidation checks, and deployment reproduction on a clean target.
8. Restricted-data/redaction, tenant isolation, credential separation, audit, observability, backup/restore, rollback, and soak evidence where applicable.

## Representative matrix policy

Choose rows by customer demand and risk: accelerator architecture; memory tier; GPU count/topology; provider execution semantics; model architecture/size; precision/quantization; workload class; and features that materially change kernels, memory, scheduling, or collectives. Boundary values and highest-risk combinations receive direct evidence. Similarity may reduce testing only when a written equivalence argument identifies unchanged invalidation layers and is approved by the certification owner.

Example rows in [the support matrix](../supported-matrix.md) remain `PLANNED` or `EXPERIMENTAL` until all evidence exists. Architecture representation or an engine vendor's compatibility statement can never produce `CERTIFIED` by itself.

## Lifecycle

- A failed required test, expired evidence, security issue, material fingerprint change, or unsupported dependency revokes certification for the affected profile.
- Hardware, topology, provider, model, engine, driver, CUDA, library, feature, or workload changes invoke [layered invalidation](../architecture/compatibility-and-invalidation.md) and targeted recertification.
- Evidence is immutable, attributable, timestamped, reproducible, and retained according to an approved policy.
- Exceptions require documented risk acceptance with scope and expiry; customer warnings do not substitute for production evidence.
