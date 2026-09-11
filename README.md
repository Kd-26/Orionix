# Orionix LLM Optimizer

Orionix is the repository foundation for a commercial platform that will automate the optimization of large-language-model inference deployments. It is an orchestration and intelligence layer above engines such as vLLM, SGLang, TensorRT-LLM, and related GPU infrastructure—not an inference engine.

```text
Control Plane
      ↓ versioned commands and contracts
Customer Agent
      ↓ local execution boundaries
Inference Engines / Customer GPUs
```

The planned lifecycle is **Inspect → Analyze → Benchmark → Optimize → Validate → Package → Deploy → Monitor → Re-optimize**. Customer model weights, prompts, and benchmark payloads remain customer-side by default.

> **Current status:** Phase 0 repository bootstrap only. Core execution and optimization functionality has not been implemented.

## Development

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required. A GPU, CUDA, model weights, Kubernetes, and cloud credentials are not required.

```bash
make setup
make check
uv run llmopt --help
```

See [local development](docs/development/local-development.md), [architecture](docs/architecture/overview.md), and [security](SECURITY.md).

## Repository map

- `packages/domain` — dependency-free identifiers and lifecycle enums.
- `packages/schemas` — versioned Pydantic wire/domain contracts.
- `packages/common` — shared errors, configuration, and logging setup.
- `packages/optimizer` — optimization ports only.
- `packages/benchmark` — benchmark planning and execution contracts only.
- `packages/capsule` — Execution Capsule metadata contracts only.
- `packages/integrations` — isolated future engine/provider adapters.
- `packages/telemetry` — no-op-by-default telemetry contracts.
- `agent` — customer-side agent boundary.
- `apps/cli` — command-line entry point.
- `services` — control-plane and worker boundaries.

This repository is proprietary and confidential. See [LICENSE.md](LICENSE.md).
