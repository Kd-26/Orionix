# Docker host execution

- **Purpose:** isolate typed engine jobs on a customer-controlled Docker host.
- **Future responsibility/port:** implement `ExecutionBackend` using allowlisted image digests and typed argument vectors; it never implements provider provisioning.
- **Composition owner:** the customer-agent composition root may instantiate it after privileged-access approval.
- **Constraints:** socket access is privileged; image provenance, user/volume/network policy, cancellation, timeout, and cleanup require certification evidence.
- **Prohibited leakage:** Docker SDK objects, socket handles, arbitrary shell strings, secrets, and host paths cannot enter domain/schema/optimizer packages.
- **Current status:** boundary only; no Docker dependency, socket access, image, process, or runtime implementation.
- **Next milestone:** define the image and argument allowlists against a fake Docker boundary.
