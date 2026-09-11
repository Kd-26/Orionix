# Initial threat model

## Assets

Customer model weights, prompts, benchmark payloads/results, GPU infrastructure, credentials, Execution Capsules, optimization policies, and control-plane job metadata.

## Trust boundaries and threats

The control plane and customer agent are separate trust domains. Future threats include forged commands, excessive agent permissions, malicious model/artifact files, path traversal during capsule extraction, dependency compromise, sensitive logs/telemetry, replayed jobs, poisoned performance history, and incompatible or tampered binaries.

## Baseline mitigations

Least privilege, deny-by-default egress, explicit data classification, versioned contracts, idempotent commands, no raw prompts or secrets in logs, dependency review, customer-side execution, and future artifact signing/integrity verification. Cryptographic protocol, authentication, sandboxing, and production transport are intentionally undecided and unimplemented.
