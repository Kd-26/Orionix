# Day-80 launch gates

The [Day-80 promise](../product-scope.md#day-80-promise) may be published only when every required gate below has an accountable approver and retained evidence. Repository scaffolding satisfies none of these runtime gates.

| Gate | Required measurable evidence | Status |
|---|---|---|
| Certified profiles | Each advertised profile has immutable fingerprint, evidence manifest, validity window, owner, and passing [certification policy](certification-policy.md) results | Not started |
| Secure tenancy/auth | Deny-by-default authorization tests across records, objects, reports, capsules, audit, and diagnostics; threat-model/security approval | Not implemented |
| Agent security | Enrollment, rotation, revocation, expiry, replay/idempotency, lease recovery, outbound-only networking, allowlisted command, and credential-scope tests pass | Not implemented |
| Discovery/compatibility | Required cluster/software facts have provenance; unknowns fail safely; support states and stale-evidence handling pass profile tests | Not implemented |
| Engine/provider lifecycle | Startup/readiness, cancellation, timeout, connection loss, shutdown, retry, orphan detection, and zero-leak cleanup pass for every profile | Not implemented |
| Benchmark validity | Canonical metric conformance, warm-up/edge cases, baseline repeatability threshold, variance reporting, and drift handling are approved | Not implemented |
| Optimization safety | Candidate/time/GPU-hour/cost/OOM/infra-failure/finalist limits demonstrably stop work and preserve evidence | Not implemented |
| Recommendation quality | Constraints and approved quality evaluators reject invalid candidates; Pareto/finalist confirmation is reproducible | Not implemented |
| Capsule/export integrity | Versioned manifest, canonical serialization, digest/signature verification, safe paths, required-secret-name handling, and clean reproduction pass | Not implemented |
| Data/observability | No restricted-data leakage in logs/events/metrics/diagnostics; bundles are redacted and previewable; alerts/SLOs are approved | Not implemented |
| Recovery/rollback | Backup restore meets approved RPO/RTO; software/schema/agent/config rollback rehearsal passes | Not implemented |
| Cost/resource control | Provider billing attribution, customer budgets, termination deadline, orphan scan, and alerting pass fault injection | Not implemented |
| Soak and paid pilot | Required profile soak completes without unresolved severity-1/2 defects; isolated pilot and manual deployment approval are signed off | Not started |

Experimental environments never inherit a certified claim. Any failed or expired gate removes the affected profile from `CERTIFIED` until evidence is renewed.
