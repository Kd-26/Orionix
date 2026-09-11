# Security Policy

## Reporting

Do not open a public issue for a suspected vulnerability. Report it privately to `security@example.invalid` until the organization configures its production security contact. Include affected versions, reproduction steps, and impact; do not include customer data or secrets.

## Baseline

- Model weights, prompts, and benchmark payloads stay in customer infrastructure by default.
- Secrets and raw model inputs are never logged by default.
- Evaluation datasets and raw model outputs stay customer-side by default.
- Provider credentials never enter workers; agent credentials are separate and narrowly scoped.
- Arbitrary remote shell execution is prohibited; future subprocess arguments are typed and allowlisted.
- The Docker socket is a privileged boundary.
- Control-plane and GPU-agent permissions remain separate and least-privileged.
- External telemetry is opt-in; this bootstrap transmits none.
- Artifacts and Execution Capsules will be versioned, signed, and integrity-checked before production use.
- Diagnostic bundles will be redacted and previewable before upload.

See `docs/security/` for the initial threat model and data/secrets policies.
