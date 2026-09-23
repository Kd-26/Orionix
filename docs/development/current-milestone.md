# Current milestone and decision register

**Current milestone: Day 4 pre-execution compatibility rules.** Days 1–3 remain frozen below.

## Implemented foundation

- Python 3.12 uv workspace with one lockfile, 16 src-layout distributions, synchronized pre-production versions, and PEP 561 markers.
- Explicit package/import mappings, direct-dependency allowlists, static import-direction and cycle checks, and CPU-only smoke imports for every distribution and integration namespace.
- Typed/versioned bootstrap contracts, configuration/error/logging conventions, provider/engine ports, CLI/help shell, CI, and development documentation inherited from the repository foundation.
- Capability-adaptive accelerator, node, interconnect, cluster, software, model, workload, requirement, job, candidate, benchmark, recommendation, and capsule contracts with synthetic golden JSON examples.
- Strict schema-version handling: missing or mismatched versions fail instead of being silently interpreted as current data.
- Versioned engine-capability, candidate-filter input, rule-result, and aggregate-result contracts with synthetic fixtures.
- Thirteen deterministic CPU-only checks for memory, architecture, precision, quantization, context, parallelism, topology, budget, engine features, speculative decoding, expert parallelism, and certification.
- Three-way `ALLOWED`, `REJECTED`, and `EXPERIMENTAL` decisions with stable customer-facing reason codes; unknown facts never become approval.
- Separate engine-compatibility and Orionix-certification decisions, with all invalid candidates filtered before any future execution boundary.

## Frozen architecture decisions

1. Architecture is capability-based, not GPU-name-based.
2. Discovery reports observed facts/provenance and does not independently declare support.
3. Engine compatibility and product certification are separate decisions.
4. Candidate generation consumes discovered capabilities and emits only feasible candidates.
5. Configurations are not assumed portable across accelerator architecture or topology.
6. Multi-node concepts exist in the first `ClusterSpec` schema version; single-node runtime precedes multi-node runtime.
7. Provisioning, execution, and engine translation are separate ports.
8. Execution Capsules use layered compatibility and invalidation.
9. A reference GPU is a repeatability fixture, not a product constraint.
10. Sensitive data remains in its owning execution/customer boundary by default.
11. Production support claims require retained, versioned evidence.
12. Enrollment, image/model acquisition, startup, baseline, and optimization timing are separate measurements.
13. Optimization uses explicit objectives and hard experiment budgets; no hidden balanced score.
14. Live deployment changes require manual customer approval initially.

ADRs [0007](../adr/0007-capability-adaptive-execution.md) and [0008](../adr/0008-risk-based-certification.md) record the new durable decisions.

## Not implemented

Cloud provisioning; agent networking; NVIDIA/NVML discovery; Docker/GPU access; engine or distributed launching; benchmarking/load generation; optimizer/search algorithms; quality inference; capsule payload/signing/restoration; database/auth/API/control-plane behavior; UI; deployment automation; Kubernetes controllers; autoscaling; billing; and continuous optimization.

## Delivery sequence

1. **Complete:** capability and cluster contract schemas with golden fixtures.
2. **Complete:** supplied-data pre-execution compatibility rules and synthetic customer-readable examples.
3. **Next:** control-plane persistence/authorization boundaries and secure fake-backed agent protocol.
4. Local CPU-safe discovery, then gated NVIDIA/topology discovery and constrained vLLM lifecycle.
5. Reproducible baseline/candidate benchmarking and canonical metrics.
6. Feasible candidate generation, bounded optimization, constraints, quality, and Pareto confirmation.
7. Reports, layered capsules, and reviewable deployment exports.
8. Provider adapters selected by evidence, followed by revalidation/history.
9. Security, compatibility, recovery, soak, and isolated paid-pilot gates.

## Open decisions

Do not resolve these by assumption. “Target” means the latest phase in which evidence must be approved before dependent implementation proceeds.

| Decision | Required evidence | Owner | Target |
|---|---|---|---|
| Exact vLLM release/image digest | Compatibility notes, image provenance/SBOM/signature, vulnerability review, smoke/soak results | Engine integration lead | Before vLLM implementation in P0 |
| CUDA/PyTorch/NCCL combination | Engine support declaration, driver matrix, topology tests, reproducible image build | Runtime lead | Before first certified profile |
| Reference validation environment | Hardware/provider access, customer demand, repeatability, cost and CI-operability | Platform lead | Before GPU validation |
| First certified models | Customer demand, architecture coverage, license/access, startup and benchmark evidence | Product + ML lead | Before paid beta |
| First production provider | Demand, regional capacity, isolation, storage/network behavior, API reliability, cost/cleanup evidence | Product + provider lead | Before hosted P0 backend |
| Affordable multi-GPU counts | Access/cost budget, representative topology, customer deployment shapes | Platform + finance owner | Before multi-GPU certification |
| Blackwell availability | Reliable access, engine/runtime compatibility, customer relevance | Platform lead | P1 expansion unless P0 demand changes |
| Multi-node launch timing | Customer demand, networking access, orchestration/failure complexity, launch-risk assessment | Principal architect | P0/P2 cut-line review |
| Customer cost model | Provider billing semantics, attribution accuracy, margin and customer interviews | Product + finance owner | Before cost objective is certified |
| Quality datasets/evaluators | Customer permission, representativeness, evaluator validity, privacy/license review | Quality lead | Before quality gate certification |
| Control-plane hosting | Residency, reliability, security, cost, operational ownership | Platform + security lead | Before control-plane deployment |
| Authentication/database vendors | Tenant isolation, audit, recovery, migration, security/compliance, cost | Control-plane + security lead | Before persistence/auth implementation |
