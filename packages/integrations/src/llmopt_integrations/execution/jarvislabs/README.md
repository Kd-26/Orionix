# JarvisLabs execution

- **Purpose:** adapt JarvisLabs VM, bare-metal, and managed-run lifecycle semantics.
- **Future responsibility/ports:** provider allocation implements `ProvisioningBackend`; VM/host-agent or colocated managed-run behavior implements `ExecutionBackend`.
- **Composition owner:** the control plane instantiates provisioning; the persistent agent or managed worker composition instantiates execution.
- **Constraints:** VM mode may use a host-agent/Docker pattern. Pause/resume always requires rediscovery and a new compatibility decision; time/cost shutdown is mandatory before production.
- **Prohibited leakage:** provider API credentials, SDK/CLI objects, raw identifiers, and lifecycle-specific fields cannot enter agent credentials, benchmark configuration, domain types, or optimizer policy.
- **Current status:** boundary only; no JarvisLabs CLI/SDK/API call, allocation, agent, or runtime behavior.
- **Next milestone:** specify lifecycle reconciliation, credential separation, cancellation, and shutdown invariants with a fake provider.
