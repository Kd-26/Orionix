# Secrets policy

Secrets are supplied through environment variables or an approved runtime secret store—never committed configuration, CLI arguments that enter shell history, test fixtures, logs, benchmark output, capsule payloads, or exception messages. `.env.example` contains names and safe empty values only; `.env*` is ignored except for that template.

Use narrowly scoped, short-lived credentials. Separate control-plane credentials from agent/GPU permissions. Rotation, revocation, and incident procedures must be defined before production credentials are introduced.

Provider provisioning credentials remain in the control plane and are never embedded in execution images/workers. Generated deployment exports list required secret names but never values.
