# Runpod execution

- **Purpose:** adapt Runpod Pod allocation and execution semantics.
- **Future responsibility/ports:** control-plane-side logic implements `ProvisioningBackend`; the supplied worker image implements `ExecutionBackend` lifecycle behavior.
- **Composition owner:** the control plane instantiates provisioning; the ephemeral worker composition root instantiates execution.
- **Constraints:** a Pod is already a provider-managed container, so nested Docker and Docker Compose are never assumed. Datacenter, storage type, physical GPU facts, driver, CUDA, image, and mounted workspace semantics enter the fingerprint.
- **Prohibited leakage:** provisioning credentials, provider SDK objects, raw resource identifiers, and provider fields cannot enter workers, benchmark configuration, domain contracts, or optimizer policy. Workers receive only narrow job credentials.
- **Current status:** boundary only; no Runpod SDK, API call, allocation, image, worker, or runtime behavior.
- **Next milestone:** specify fake-backed credential scope, cancellation, termination, reconciliation, and orphan-cleanup tests.
