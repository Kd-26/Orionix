# Customer data boundaries

Model weights, prompts, completions, and raw benchmark payloads remain inside customer infrastructure by default. No benchmark payload or customer inference metric leaves that boundary unless a customer explicitly enables a documented, scoped export. Logs contain no raw model input by default; product, benchmark, inference, and health telemetry remain distinct.

Future control-plane messages should carry the minimum normalized metadata necessary. Data egress, retention, deletion, residency, access controls, and audit requirements must be decided and documented before remote agent coordination ships.
