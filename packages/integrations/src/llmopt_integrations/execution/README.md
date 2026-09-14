# Execution integrations

- **Purpose:** host execution- and provider-specific lifecycle implementations behind stable ports.
- **Future responsibility/ports:** execution adapters implement `ExecutionBackend`; provider allocation logic separately implements `ProvisioningBackend`.
- **Composition owner:** agents/provider workers instantiate execution adapters; the control plane may instantiate provisioning adapters.
- **Constraints:** persistent hosts, managed containers/VMs, and serverless workloads retain distinct lifecycle and storage semantics.
- **Prohibited leakage:** credentials, provider SDK objects, generic shell execution, benchmark policy, and provider-specific fields cannot enter core contracts or unrelated packages.
- **Current status:** namespaces and provider-neutral ports only; no provider SDK, Docker, cloud, process, or GPU behavior.
- **Next milestone:** CPU-safe local capability collection followed by fake-backed lifecycle conformance tests.
