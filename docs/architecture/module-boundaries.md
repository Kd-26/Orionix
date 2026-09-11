# Module boundaries

Dependency direction is inward toward stable primitives and contracts:

```text
common
  ↑
domain + schemas
  ↑
config / discovery / workload / benchmark / optimizer / quality / capsule / telemetry / deployment
  ↑
engine / execution / provider / cache / artifact integrations
  ↑
agent / CLI / control-plane / future web
```

- `common` has identifiers, errors, and safe logging only.
- `domain` may depend on `common`; it owns business states and concepts.
- `schemas` may depend on `common`, `domain`, and Pydantic; never implementations.
- `benchmark`, `optimizer`, and `capsule` consume contracts without importing one another's implementations.
- `integrations` translates at the edge and never exposes vendor objects across boundaries.
- `agent`, CLI, and the single modular control-plane service are composition layers.

Cross-module values use versioned contracts. No domain model imports vLLM, CUDA, Ray, FastAPI, a vendor SDK, or an ORM. Dependency inversion should be applied at execution edges; avoid generic frameworks and circular imports.
