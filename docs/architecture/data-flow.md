# Data flow

The intended flow is model/workload/SLO/quality/cost input → execution-side environment and model inspection → representability, engine-compatibility, and certification evaluation → controlled baseline → feasible candidate planning → execution-side benchmark → independent constraint and quality validation → Pareto ranking → independent finalist confirmation → report, layered Execution Capsule metadata, and reviewable deployment export → optional scheduled revalidation with manual approval.

The [canonical workflow](product-workflow.md) defines inputs, outputs, owner, trust boundary, failure behavior, and egress for all 18 steps. The [customer data boundary](../security/customer-data-boundaries.md) is the authoritative transfer allowlist.

Commands and transitions use versioned envelopes, narrow credentials, leases, expirations, idempotency keys, and stable identifiers. Agent connections are outbound-only by default. No network, provisioning, GPU, engine, benchmark, optimizer, quality, persistence, deployment, or UI implementation exists in this milestone.
