# Module boundaries

Dependency direction is inward toward contracts:

```text
domain ────────┐
               ├── schemas ──┬── benchmark ──┐
               │             ├── optimizer ──┼── agent / CLI / services
common ────────┤             ├── capsule ────┤
               │             └── integrations┘
telemetry ─────┘
```

- `domain` has only standard-library primitives.
- `schemas` may depend on `domain` and Pydantic; never on implementations.
- `common` is small and contains no business/domain behavior.
- `benchmark`, `optimizer`, and `capsule` consume contracts without importing one another's implementations.
- `integrations` translates at the edge and never exposes vendor objects across boundaries.
- `agent`, CLI, and services are composition layers.

Cross-module values use versioned contracts. No domain model imports vLLM, CUDA, Ray, FastAPI, a vendor SDK, or an ORM. Dependency inversion should be applied at execution edges; avoid generic frameworks and circular imports.
