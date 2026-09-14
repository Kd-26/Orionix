# Definition of done

A change is done when behavior and non-behavior are explicit; contracts are typed/versioned; dependency direction remains valid; security/data-boundary impacts are documented; tests cover success, failure, cancellation, and cleanup as applicable; `make check` and package builds pass; dependencies are pinned/reviewed/locked; links are valid; and user-facing documentation makes no unsupported capability claim.

Capability, GPU, engine, or provider work additionally requires:

- Observations include provenance, confidence, explicit unknowns, and a compatibility fingerprint.
- Architecture support, engine compatibility, experimental operation, and certification are not conflated.
- Variable GPU counts and multi-node representation are preserved even when runtime scope is narrower.
- Experiment time, GPU-hour, cost, OOM, failure, and confirmation limits are enforced where relevant.
- Tests identify the exact environment and include cleanup/resource-leak evidence; GPU tests remain outside default CI.
- Production claims identify a versioned support profile and retained certification evidence.
- Security review covers credentials, commands, logs, diagnostics, artifacts, tenant isolation, and data egress.

Documentation-only changes are complete when canonical ownership is clear, conflicting claims are removed, implementation status is explicit, Markdown/link checks pass, and the repository quality gate remains green.
