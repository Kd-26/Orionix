# Modal execution

- **Purpose:** adapt Modal Function, Sandbox, or server workload semantics.
- **Future responsibility/ports:** control-plane composition may implement `ProvisioningBackend`-equivalent allocation while a packaged worker implements `ExecutionBackend` lifecycle/event normalization.
- **Composition owner:** the control plane creates the workload; the ephemeral Modal worker image composes job runner and engine adapter.
- **Constraints:** no persistent agent, `systemd`, Docker socket, ordinary host filesystem, or ordinary disk semantics are assumed. Scheduling, cold start, model load, and steady-state timing remain separate; GPU type/count, region, image, volume, and runtime class enter the fingerprint.
- **Prohibited leakage:** Modal SDK objects, provider credentials, storage handles, and serverless timing semantics cannot enter benchmark formulas, domain schemas, or optimizer policy.
- **Current status:** boundary only; no Modal dependency, API call, image, Function, Sandbox, volume, or runtime behavior.
- **Next milestone:** define fake-backed serverless event, storage, cancellation, and cleanup normalization.
