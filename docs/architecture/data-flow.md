# Data flow

The intended flow is model/hardware/workload/SLO input → environment inspection → analysis → candidate planning → customer-side benchmark → result analysis → validation → serving configuration and Execution Capsule metadata.

Only explicit, allow-listed metadata may eventually return to the control plane. Model weights, prompts, raw benchmark payloads, and engine process details stay customer-side by default. Job state transitions must be explicit and idempotent. There is no network or orchestration implementation in Phase 0.
