# LMCache adapter

- **Purpose:** reserve cache-policy translation and normalized cache metrics.
- **Future responsibility/port:** implement a cache-adapter port after that provider-neutral port is defined; no cache port exists today.
- **Composition owner:** agent/engine-worker composition may instantiate it beside an engine adapter.
- **Constraints:** LMCache remains an optional, reviewed dependency and must honor the selected engine/runtime compatibility fingerprint.
- **Prohibited leakage:** LMCache types, cache internals, and SDK objects cannot enter optimizer policy, schemas, control-plane logic, or unrelated integrations.
- **Current status:** boundary only; no LMCache dependency or runtime implementation.
- **Next milestone:** deferred until reproducible vLLM baseline benchmarking exists.
