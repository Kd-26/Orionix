# Data classification

- **Restricted customer data:** model weights, prompts, completions, evaluation datasets, raw benchmark payloads, provider/agent credentials. Customer-side and never logged or exported by default.
- **Sensitive operational data:** resource identifiers, topology, diagnostic bundles, detailed benchmark results, capsule metadata. Minimized, hashed where possible, tenant-authorized, retained narrowly.
- **Internal product data:** normalized job state, configuration metadata, aggregate product telemetry. Tenant-scoped and audited.
- **Public data:** deliberately published documentation and synthetic examples only.

Classification changes require security review and an updated threat model.
