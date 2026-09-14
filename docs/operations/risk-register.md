# Product risk register

Risks are reviewed at each phase gate and before any support-profile status changes. Likelihood and impact are qualitative until operational evidence exists.

| Risk | Likelihood / impact | Mitigation and trigger | Evidence owner | Current state |
|---|---|---|---|---|
| Capability claims exceed evidence | High / Critical | Central support registry; block claims without profile evidence; trigger on docs/release changes | Product + certification owner | Open |
| Hardware/topology misclassification | Medium / High | Provenance, confidence, explicit unknowns, fixture/fault tests; trigger on discovery changes | Discovery lead | Open |
| Incompatible runtime or binary reuse | High / Critical | Layered fingerprint/invalidation, digest pinning, fail closed; trigger on any fingerprint change | Runtime + capsule leads | Open |
| Arbitrary or replayed worker command | Medium / Critical | Typed allowlist, auth, expiry, idempotency, leases, outbound-only transport; trigger on protocol work | Agent + security leads | Open |
| Restricted customer-data egress | Medium / Critical | Execution-side defaults, transfer allowlist, redaction tests, preview; trigger on any new event/diagnostic | Security owner | Open |
| Tenant data crossover | Medium / Critical | Authorization at every record/object/report/capsule boundary and adversarial tests | Control-plane owner | Open |
| Runaway provider cost/orphan compute | Medium / High | Hard budgets, termination deadlines, reconciliation, orphan scan, alerts; trigger on provisioning work | Provider lead | Open |
| Benchmark bias or irreproducibility | High / High | Canonical formulas, independent confirmation, variance/drift reporting, immutable provenance | Benchmark lead | Open |
| Optimizer OOM/failure loop | High / High | Candidate/time/GPU-hour/cost/OOM/failure limits and deterministic stop reasons | Optimizer lead | Open |
| Provider semantics leak into core logic | Medium / High | Port contract tests and adapter-local extensions; trigger on every provider change | Principal architect | Mitigated by boundary only |
| Multi-node partial failure leaks resources | High / Critical | Keep runtime experimental until cross-node cancel/cleanup/fault evidence passes | Distributed runtime lead | Deferred/P2 |
| Artifact supply-chain or extraction attack | Medium / Critical | SBOM/signing/digest verification, safe extraction, no executable payload support until review | Security + capsule leads | Payloads not implemented |
| Manual export causes production regression | Medium / High | Reviewable diff, explicit approval, reproduction and rollback evidence; no automatic mutation | Deployment lead + customer | Open |
| Schedule cannot meet Day-80 gates | Medium / High | Weekly evidence/gap review; cut profiles/features rather than relax gates | Product owner | Open |

Critical risks block the affected production claim. Risk acceptance must name scope, expiry, approver, compensating control, and rollback trigger; it cannot silently convert experimental evidence into certification.
