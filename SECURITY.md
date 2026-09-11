# Security Policy

## Reporting

Do not open a public issue for a suspected vulnerability. Report it privately to `security@example.invalid` until the organization configures its production security contact. Include affected versions, reproduction steps, and impact; do not include customer data or secrets.

## Baseline

- Model weights, prompts, and benchmark payloads stay in customer infrastructure by default.
- Secrets and raw model inputs are never logged by default.
- Control-plane and GPU-agent permissions remain separate and least-privileged.
- External telemetry is opt-in; this bootstrap transmits none.
- Artifacts and Execution Capsules will be versioned, signed, and integrity-checked before production use.

See `docs/security/` for the initial threat model and data/secrets policies.
