# Coding standards

Use Python 3.12 syntax, small modules, explicit typed interfaces, composition, dependency injection at edges, and minimal global state. Public contracts and ports are typed. Ruff owns formatting/import order/linting; mypy runs in strict mode. Prefer immutable cross-boundary models. Avoid vendor types in public contracts and avoid speculative generic abstractions.

Names include units whenever confusion would be dangerous (`*_bytes`, `*_seconds`, `*_ms`, `*_tokens_per_second`, `*_requests_per_second`, `*_usd`). Engine processes are described by typed executable/argument-vector contracts; never accept a generic remote shell string.
