# Documentation

Authoritative entry points:

- [First seven days execution guide](development/first-seven-days.md) explains the first week in simple, daily build-and-verification steps.
- [Product scope](product-scope.md) defines the product, first customer, Day-80 promise, and P0/P1/P2 cut line.
- [Product metrics](product-metrics.md) defines objectives, benchmark measurements, onboarding stages, and safety-budget hypotheses.
- [Support matrix](supported-matrix.md) defines support states and lists planned or evidence-backed profiles.
- [Product workflow](architecture/product-workflow.md) assigns every customer step to an owner and trust boundary.
- [Component ownership](architecture/component-ownership.md) separates common control concepts from capability-adaptive behavior.
- [Capability model](architecture/capability-model.md), [cluster topology](architecture/cluster-and-topology.md), and [compatibility/invalidation](architecture/compatibility-and-invalidation.md) define future contracts.
- [Contract versioning](architecture/contract-versioning.md) defines mandatory schema versions, golden examples, and ownership.
- [Certification policy](operations/certification-policy.md), [launch gates](operations/launch-gates.md), and the [risk register](operations/risk-register.md) govern production claims.
- [Customer data boundaries](security/customer-data-boundaries.md) and [data classification](security/data-classification.md) govern data movement.

`architecture/`, `development/`, `operations/`, `security/`, and `adr/` contain supporting design, engineering, operating, security, and durable decision records. Documentation labels intended behavior as planned; it is never evidence that a runtime capability is implemented or certified.
