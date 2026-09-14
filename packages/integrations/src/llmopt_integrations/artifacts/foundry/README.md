# Foundry artifact boundary

- **Purpose:** reserve a future adapter for evaluated Foundry artifact persistence behavior.
- **Future responsibility/port:** implement a narrowly defined artifact persistence port, if approved, for graph/template and architecture-specific artifact references; no such port exists yet.
- **Composition owner:** only capsule/agent composition may instantiate the adapter.
- **Constraints:** license, security, integrity, compatibility, extraction, and portability reviews must precede any Foundry dependency or SAVE/LOAD behavior.
- **Prohibited leakage:** Foundry APIs, binaries, CUDA handles, methodology, and vendor objects cannot enter stable contracts or unrelated packages.
- **Current status:** boundary only; no source, package, runtime implementation, artifact, or API is bundled.
- **Next milestone:** none before capsule integrity and layered compatibility semantics are approved.
