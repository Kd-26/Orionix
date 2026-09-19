# Orionix LLM Optimizer

Orionix is the repository foundation for LLM Optimizer, a capability-adaptive commercial platform for optimizing large-language-model inference deployments. It is an orchestration and intelligence layer above engines such as vLLM, SGLang, TensorRT-LLM, and related accelerator infrastructure—not an inference engine.

```text
Control Plane
      ↓ versioned commands and contracts
Customer Agent
      ↓ local execution boundaries
Inference Engines / Customer GPUs
```

The planned lifecycle is **Inspect → Analyze → Benchmark → Optimize → Validate → Package → Export → Monitor → Revalidate**. It evaluates the actual model, workload, constraints, cluster topology, software, engine, and provider environment; recommendations are valid only for their versioned compatibility fingerprint. Customer model weights, prompts, evaluation datasets, and benchmark payloads remain execution-side by default. First-release deployment changes require manual approval.

The common architecture represents Ampere, Hopper, Blackwell, future accelerator families, variable GPU counts, and multi-node clusters. Representation is not certification: production claims apply only to versioned support profiles with retained evidence. A reference GPU may be selected for repeatable validation, but it is a test fixture rather than a product dependency.

> **Current status:** architecture-alignment and repository-foundation milestone only. The repository is architecturally prepared for staged implementation; core runtime functionality has not been implemented.

## Development

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required. A GPU, CUDA, model weights, Kubernetes, and cloud credentials are not required.

```bash
make setup
make check-imports
make test-smoke
make check
uv run llmopt --help
```

`make setup` installs the locked CPU-only workspace. `make check-imports` verifies all 16 distributions and the provider/engine namespaces without loading optional SDKs. `make test-smoke` runs all CPU-safe package and CLI smoke checks. `make check` additionally validates the lockfile, formatting, linting, types, CPU test suite, internal documentation links, all package builds, and typed wheel contents.

See [product scope](docs/product-scope.md), [support status](docs/supported-matrix.md), [customer workflow](docs/architecture/product-workflow.md), [architecture](docs/architecture/overview.md), [local development](docs/development/local-development.md), and [security](SECURITY.md).

## Repository map

- `packages/common` — typed identifiers, shared errors, and safe logging.
- `packages/domain` — business lifecycle concepts and states.
- `packages/schemas` — versioned Pydantic transport/artifact contracts.
- `packages/config` — typed configuration and precedence.
- `packages/discovery` and `packages/workload` — inspection/profile ports.
- `packages/optimizer` — optimization ports only.
- `packages/benchmark` — benchmark planning and execution contracts only.
- `packages/quality` — customer-side quality-evaluation ports.
- `packages/capsule` — Execution Capsule metadata contracts only.
- `packages/integrations` — isolated future engine/provider adapters.
- `packages/telemetry` — no-op-by-default telemetry contracts.
- `packages/deployment` — deployment-export ports only.
- `agent` — customer-side agent boundary.
- `apps/cli` — command-line entry point.
- `services/control-plane` — one modular future cloud deployable.
- `apps/web` — documentation-only future presentation boundary.

This repository is proprietary and confidential. See [LICENSE.md](LICENSE.md).
