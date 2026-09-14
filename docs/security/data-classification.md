# Data classification

- **Restricted execution data:** model weights, raw prompts/completions, evaluation datasets, per-request payloads, unredacted engine logs, customer secrets, and architecture-specific binary artifacts. Execution-side by default; never logged or exported without a separately approved policy.
- **Restricted credentials:** provider account/provisioning credentials and agent/job credentials. They remain in their credential-owning boundary, are never logged, and are never bundled together. Provider credentials for product-managed provisioning stay control-plane-side; customer-managed credentials remain customer-side; workers receive only narrow credentials.
- **Sensitive operational data:** redacted/hashed resource identifiers, topology, diagnostic bundles, detailed benchmark results, capsule metadata, candidate configurations, and support evidence. Minimized, tenant-authorized, retained narrowly, and excluded from public telemetry.
- **Internal product data:** normalized job state, configuration metadata, aggregate product telemetry. Tenant-scoped and audited.
- **Public data:** deliberately published documentation and synthetic examples only.

Classification changes require security review and an updated threat model.
