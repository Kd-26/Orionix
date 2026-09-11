# Execution backends

`ExecutionBackend` manages a prepared execution environment; `ProvisioningBackend` separately manages compute allocation; `EngineAdapter` validates engine-neutral configuration and produces a typed launch specification.

- **Local Ubuntu/NVIDIA:** persistent host agent, controlled Docker/host processes, NVIDIA Container Toolkit, local model/cache paths, and topology fingerprinting. Docker socket access is privileged.
- **Runpod:** supplied Pod image containing supervisor, engine environment, benchmark runner, and metrics collector. No nested Docker/Compose assumption. Provider credentials remain control-plane-side; mounted workspace and physical environment enter the fingerprint.
- **JarvisLabs:** VM/bare-metal can follow host-agent/Docker semantics; managed runs may colocate agent and engine. Pause/resume invalidates the old fingerprint; cost/time shutdown is required later.
- **Modal:** serverless Function/Sandbox/server workload, not a persistent host agent. Image, storage, process, cancellation, cold start, and disk semantics are provider-specific; provisioning, model-load, and steady-state latency remain separate.

All adapters are placeholders without SDKs or external calls.
