# Initial threat model

## Assets

Customer model weights, prompts, benchmark payloads/results, GPU infrastructure, credentials, Execution Capsules, optimization policies, and control-plane job metadata.

## Trust boundaries and threats

The control plane, customer agent, provider provisioning plane, execution worker, Docker socket, and artifact store are separate trust domains. Future threats include forged commands, arbitrary shell execution, excessive permissions, leaked provider credentials, malicious model/artifact files, path traversal during capsule extraction, dependency compromise, sensitive logs/telemetry/diagnostics, replayed jobs, poisoned performance history, and incompatible or tampered binaries.

## Baseline mitigations

Least privilege, deny-by-default egress, explicit data classification, versioned/allowlisted commands, typed subprocess arguments, idempotency and leases, no raw prompts or secrets in logs, previewable redacted diagnostics, dependency review, customer-side execution, and future artifact signing/integrity verification. Production integrations require threat-model updates. Cryptographic protocol, authentication, sandboxing, and transport remain undecided and unimplemented.
