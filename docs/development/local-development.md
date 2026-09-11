# Local development

Prerequisites are Python 3.12+, `uv`, GNU/compatible `make`, and Git.

```bash
make setup
make check
uv run llmopt --help
```

`make setup` synchronizes every workspace package and installs pre-commit hooks. Copy `.env.example` to `.env` only for local overrides; `.env` is ignored. CPU-only development needs no NVIDIA GPU, CUDA, engine, model weights, Kubernetes, cloud credentials, or database.
