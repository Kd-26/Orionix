# Execution backends

`ProvisioningBackend`, `ExecutionBackend`, and `EngineAdapter` are separate ports. Their ownership and prohibitions are canonical in [component ownership](component-ownership.md). Provider differences are normalized into capability, lifecycle, timing, and fingerprint contracts; they never leak into benchmark formulas, candidate ranking, or core domain types.

## Local/customer Ubuntu

- A persistent outbound-only host agent controls an isolated host process or Docker environment with the NVIDIA runtime.
- Discovery reads the available cluster directly; model/cache storage is customer-owned.
- Docker socket access is a privileged trust boundary and is never assumed or granted casually.
- Customer paths, raw identifiers, weights, inputs, and unredacted logs remain local.

## Runpod

- A Pod is already a provider-managed container; nested Docker and Docker Compose are not assumed.
- A future worker image contains the supervisor, job runner, engine runtime, benchmark runner, and metrics collector.
- Datacenter, storage type, physical GPU facts, driver, CUDA, image digest, and runtime class enter the compatibility fingerprint.
- Provider credentials remain control-plane-side. The worker receives only narrow, expiring job credentials.

## JarvisLabs

- VM or bare-metal mode may use the host-agent model; managed-run mode may package the job runner and engine together.
- Pause/resume requires rediscovery and a new compatibility decision; the prior environment fingerprint is not reused.
- Provisioning credentials and agent credentials remain separate. Time/cost shutdown, reconciliation, and orphan cleanup are certification requirements.

## Modal

- Modal does not imply a persistent agent, `systemd`, Docker socket, or ordinary host filesystem.
- Jobs map to a Function, Sandbox, or server workload through a dedicated adapter whose image contains the worker and engine runtime.
- Scheduling, cold start, image/model acquisition, model load, and steady-state inference are separate measurements.
- Volume/disk semantics, cancellation, GPU type/count, region, runtime class, and image identity enter the fingerprint.

All current adapters are documentation/namespace placeholders without SDKs, API calls, provisioning, process control, or GPU access. Adding a provider requires fake-backed lifecycle tests, threat-model review, credential separation, budget enforcement, cleanup evidence, and a versioned support profile.
