# Integrations

**Purpose:** quarantine engine, execution-provider, cache, and artifact details behind provider-neutral ports. **Responsibilities:** define `ExecutionBackend`, `ProvisioningBackend`, and `EngineAdapter`, then host future adapter implementations. **Non-responsibilities:** domain policy, candidate selection, orchestration state, credentials in workers, or leaking vendor objects. **Allowed dependencies:** `schemas`, standard library, and future adapter-local optional extras. **Prohibited dependencies:** agent/control-plane/web internals, ORMs, unrelated vendor SDKs, and mandatory GPU packages. **Status:** ports and documented namespaces only. **Next milestone:** implement CPU-safe local inspection and then a constrained vLLM adapter.

No vendor SDK or third-party source is installed or vendored.
