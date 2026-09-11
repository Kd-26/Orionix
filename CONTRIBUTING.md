# Contributing

## Workflow

- Use short-lived branches such as `feat/contract-versioning`, `fix/cli-help`, or `docs/threat-model`.
- Write imperative Conventional Commit-style messages (`feat: add workload contract`).
- Keep pull requests focused; describe intent, risks, test evidence, and migration impact.
- Add or update tests, types, and documentation with every behavior or contract change.
- Run `make check` before requesting review.

All public contracts and interfaces require type hints. Code must pass Ruff formatting/linting, mypy, and relevant pytest suites. New dependencies require a need statement, license/security review, exact direct-version pin, and lockfile update. GPU/engine dependencies must remain optional.

Major architecture changes, boundary changes, schema compatibility decisions, or new infrastructure require an ADR proposal before implementation. Never commit customer data, credentials, model weights, benchmark payloads, or generated capsule artifacts.
