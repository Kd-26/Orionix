# Test boundaries

- `unit/` contains isolated CPU-only behavior tests.
- `contract/` validates versioned serialization and safety invariants.
- `integration/` checks package dependency direction and interface composition without external services.
- `smoke/` verifies every workspace package, typed-package marker, integration namespace, and CLI shell imports in the CPU-only base environment.
- `e2e/` is reserved for real deployable-boundary workflows; none exist yet.
- `gpu/` requires explicitly managed CUDA-capable hardware and is excluded from default CI.
- `performance/` is reserved for evidence-backed regression tests, not fabricated benchmark results.
- `security/` enforces repository and trust-boundary invariants.
- `fixtures/` contains only safe synthetic, versioned test data.

Tests must never require customer data, model weights, provider credentials, Docker, cloud access, or optional engine/GPU SDKs unless their suite is explicitly isolated and documented.
