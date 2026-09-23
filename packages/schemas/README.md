# Schemas

This package owns Orionix's versioned, serialization-safe contracts between
components. It contains data definitions and validation only. It does not
inspect hardware, launch an engine, run a benchmark, rank candidates, access a
database, or call a provider.

## Contract ownership

| Saved format | Python owner | Current version |
|---|---|---:|
| Accelerator/GPU | `llmopt_schemas.hardware.AcceleratorSpec` | `1.0` |
| Machine/node | `llmopt_schemas.hardware.NodeSpec` | `1.0` |
| Interconnect | `llmopt_schemas.hardware.InterconnectSpec` | `1.0` |
| Cluster | `llmopt_schemas.hardware.ClusterSpec` | `1.0` |
| Software environment | `llmopt_schemas.hardware.SoftwareEnvironmentSpec` | `1.0` |
| Complete hardware environment | `llmopt_schemas.hardware.HardwareSpec` | `1.0` |
| Model | `llmopt_schemas.model.ModelSpec` | `1.0` |
| Workload | `llmopt_schemas.workload.WorkloadSpec` | `1.0` |
| Requirements and experiment budget | `llmopt_schemas.requirements.OptimizationRequirements` | `1.0` |
| Optimization job | `llmopt_schemas.optimization.OptimizationJobSpec` | `1.0` |
| Candidate configuration | `llmopt_schemas.optimization.CandidateConfiguration` | `1.0` |
| Candidate filter input | `llmopt_schemas.optimization.CandidateFilterInput` | `1.0` |
| Engine capability record | `llmopt_schemas.compatibility.EngineCapabilityRecord` | `1.0` |
| Rule result | `llmopt_schemas.compatibility.RuleResult` | `1.0` |
| Candidate filter result | `llmopt_schemas.compatibility.CandidateFilterResult` | `1.0` |
| Benchmark result | `llmopt_schemas.benchmark.BenchmarkResult` | `2.0` |
| Recommendation | `llmopt_schemas.optimization.Recommendation` | `1.0` |
| Execution Capsule manifest | `llmopt_capsule.manifest.ExecutionCapsuleManifest` | `2.0` |

Benchmark and capsule contracts retain their previously declared `2.0`
versions. The application remains pre-production; these golden examples are the
first serialization freeze for the current versions.

## Dependency rules

- Allowed dependencies: `common`, `domain`, Pydantic, and the standard library.
- Prohibited dependencies: feature packages, integrations, agents, services,
  engine/provider SDKs, CUDA, web frameworks, and database libraries.
- Provider and engine details use normalized fields or namespaced extension
  metadata; SDK objects never enter shared contracts.
- Raw hardware identifiers are prohibited. Only redacted or hashed identifiers
  may cross the execution boundary.

The synthetic golden JSON examples live under
`tests/fixtures/contracts/v1/`. Contract tests load, serialize, reload, and
compare every example.

Day 4 compatibility examples live under
`tests/fixtures/compatibility/v1/`. The pinned version in those fixtures is
explicitly synthetic and is not production vLLM or Orionix certification
evidence.
