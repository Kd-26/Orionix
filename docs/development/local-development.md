# Local development

Prerequisites are Python 3.12+, `uv`, GNU/compatible `make`, and Git.

```bash
make setup
make doctor
make check
uv run llmopt --help
```

`make setup` synchronizes every workspace package and installs pre-commit hooks. `make doctor` checks only CPU developer prerequisites. Copy `.env.example` to `.env` only for local overrides; `.env` is ignored. CPU-only development needs no NVIDIA GPU, CUDA, engine, model weights, Kubernetes, cloud credentials, hosted control plane, or database.

Common commands are `make format`, `make lint`, `make typecheck`, `make test`, `make test-unit`, `make test-contract`, `make test-integration`, `make test-gpu-smoke`, `make check`, `make build`, and `make clean`.

`make check` is the single pre-review CPU gate: it validates source quality,
types, tests, internal documentation links, package builds, and typed wheel
contents. `make build` remains available when only package artifacts need to be
rebuilt and inspected.

Five environments are documented: local CPU development; CPU-only pull-request CI; dedicated Ubuntu/NVIDIA GPU development; production-like staging control plane plus staging GPU agent; and isolated pilot production. Only the first two are currently configured. `dev-up`, `dev-down`, and `test-e2e` deliberately return unavailable until a real runtime exists.
