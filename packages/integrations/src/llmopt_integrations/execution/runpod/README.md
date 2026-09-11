# Runpod execution

Runpod Pods run a supplied container image; Docker Compose and nested Docker are not assumed inside a Pod. The future image includes the agent supervisor, engine environment, benchmark runner, and metrics collector. Persistent data commonly lives under the provider-mounted workspace path. Instance, datacenter, storage type, physical GPU, driver, and CUDA values enter the environment fingerprint.

Provisioning credentials stay in the control plane, never the execution worker. Initial certification targets the provider's production-oriented cloud class. Provider SDK types remain inside this adapter. Status: schemas/docs only; no SDK/API dependency or call. Next milestone: design credential-scoped provisioning and cancellation tests against a fake transport.
