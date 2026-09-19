# Product risk register

Risks are reviewed at each phase gate and before any support-profile status changes. Likelihood and impact are qualitative until operational evidence exists.

## Three assumptions to validate first

These are the three highest-risk startup assumptions. They must be tested with
real access or customer evidence rather than treated as facts.

| Assumption | Why it could block the product | Validation required | Owner / deadline | Current state |
|---|---|---|---|---|
| Orionix can repeatedly access an affordable NVIDIA GPU profile suitable for certification | Without repeatable access, benchmark results, failure tests, and release evidence cannot be reproduced | Reserve or obtain the same model/GPU/software profile for repeated baseline, failure, and confirmation runs; record availability and monthly budget | Platform + product / before GPU implementation | Open |
| One pinned vLLM image is compatible and stable for the first model/GPU profile | A generally supported model can still fail because of the exact driver, CUDA, PyTorch, NCCL, kernel, or vLLM combination | Pin the image digest and full software fingerprint; pass clean startup, inference, benchmark, cancellation, and soak tests | Runtime lead / before first certified profile | Open |
| Target customers will install a narrowly scoped outbound Orionix agent in their environment | If customers reject the trust model, the customer-side execution architecture and onboarding flow must change | Conduct at least five interviews; show permissions, outbound endpoints, collected data, uninstall steps, and threat model; obtain two design-partner approvals | Product + security / before agent networking | Open |

If any assumption fails, narrow or change the launch plan before adding dependent
runtime behavior. Do not compensate by weakening security or certification gates.

## Product and delivery risks

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
