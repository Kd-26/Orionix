# Customer data boundaries

## Execution-side by default

Model weights; raw prompts/completions; evaluation datasets; per-request and raw benchmark payloads; unredacted engine logs; customer secrets; raw device identifiers; and architecture-specific compiled/graph artifacts remain inside customer infrastructure or the isolated provider execution environment. Secrets and raw inputs are never logged. No item crosses the boundary merely because a job runs on hosted compute.

## Allowed control-plane metadata

The control plane may receive only aggregate benchmark measurements; redacted model metadata; redacted/hashed cluster and environment fingerprints; workload-distribution metadata; SLO, quality, cost, and error summaries; candidate configurations; state/lifecycle events; capsule metadata; and customer-approved redacted diagnostics. Each transfer is schema-validated, tenant-authorized, purpose-limited, auditable, and subject to retention/deletion policy.

Provider account credentials remain in the boundary that owns provisioning: control-plane-side for product-managed provisioning and customer-side for customer-managed environments. They never enter execution workers. Workers receive only narrowly scoped, short-lived agent/job credentials. Agent connections are outbound-only by default; commands are typed, versioned, authenticated, expiring, idempotent, and allowlisted. Arbitrary remote shell execution is prohibited.

Docker socket access is privileged. Diagnostic bundles are redacted, allowlisted, and previewable before upload. Tenant isolation covers database records, object storage, reports, capsules, diagnostics, audit events, and support evidence.

Product, benchmark, customer inference, and agent/system-health telemetry remain distinct. Data egress, retention, deletion, residency, access control, and audit policy must be approved before remote coordination ships.
