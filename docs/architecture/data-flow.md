# Data flow

The intended flow is model/hardware/workload/SLO and quality input → environment inspection → capability filtering → candidate planning → customer/provider-side benchmark → independent result and quality validation → Pareto ranking → serving configuration, Execution Capsule metadata, and reviewable deployment export → scheduled revalidation with manual approval.

Only explicit, allowlisted metadata may eventually return to the control plane. Model weights, prompts, evaluation datasets, raw benchmark payloads, and engine process details stay customer-side by default. Commands and transitions use versioned envelopes, leases, idempotency keys, and stable identifiers. There is no network or orchestration implementation in this milestone.
