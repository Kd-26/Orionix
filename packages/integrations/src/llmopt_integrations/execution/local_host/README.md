# Local Ubuntu/NVIDIA execution

- **Purpose:** operate on an already available customer-controlled host without owning provider allocation.
- **Future responsibility/port:** implement `ExecutionBackend` for controlled host or Docker execution, discovery, lifecycle events, and cleanup; provisioning is a no-op outside this namespace.
- **Composition owner:** the persistent customer-agent composition root may instantiate it.
- **Constraints:** customer storage/path semantics and direct topology discovery apply; Docker socket access is privileged and cannot be assumed.
- **Prohibited leakage:** subprocess handles, Docker sockets, CUDA objects, raw identifiers/model paths, and customer credentials cannot cross the agent boundary or enter benchmark configuration.
- **Current status:** boundary only; no host, Docker, NVIDIA, CUDA, process, or discovery access.
- **Next milestone:** implement CPU-safe platform inspection without GPU probing.
