# Modal execution

Modal is not a persistent host agent. Optimization jobs map to a Function, Sandbox, or server-style workload, with the job runner and vLLM environment packaged into a Modal image. Storage, commit/reload, process lifecycle, cancellation, cold starts, and disk reporting are provider-specific. Provisioning, cold-start/model-load, and steady-state inference latency are recorded separately; GPU type/count and region enter the fingerprint.

Persistent `systemd`, a Docker socket, and host-filesystem semantics are not assumed. Provider SDK types remain inside this adapter. Status: schemas/docs only; no Modal dependency or call. Next milestone: define serverless event normalization using a fake adapter.
