# Orionix LLM Optimizer

Orionix is the repository foundation for a commercial platform that will automate the optimization of large-language-model inference deployments. It is an orchestration and intelligence layer above engines such as vLLM, SGLang, TensorRT-LLM, and related GPU infrastructure—not an inference engine.

```text
Control Plane
      ↓ versioned commands and contracts
Customer Agent
      ↓ local execution boundaries
Inference Engines / Customer GPUs
```

The planned lifecycle is **Inspect → Analyze → Benchmark → Optimize → Validate → Package → Export → Monitor → Revalidate**. Customer model weights, prompts, evaluation datasets, and benchmark payloads remain customer-side by default. First-release deployment changes require manual approval.

> **Current status:** architecture-alignment and repository-foundation milestone only. The repository is architecturally prepared for staged implementation; core runtime functionality has not been implemented.

## Development

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required. A GPU, CUDA, model weights, Kubernetes, and cloud credentials are not required.

```bash
make setup
make check
uv run llmopt --help
```

See [local development](docs/development/local-development.md), [architecture](docs/architecture/overview.md), and [security](SECURITY.md).

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
