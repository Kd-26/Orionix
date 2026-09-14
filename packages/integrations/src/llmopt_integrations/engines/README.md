# Engine integrations

- **Purpose:** host engine-specific translation behind the provider-neutral `EngineAdapter` port.
- **Future responsibility/port:** declare engine capabilities, validate model/cluster/serving combinations, and produce typed `EngineLaunchSpec` values.
- **Composition owner:** the agent or provider-worker composition root selects and instantiates an adapter; optimizers consume only normalized contracts.
- **Constraints:** vLLM is first intended for production, SGLang is later/beta, and TensorRT-LLM is future. Dependencies are optional and adapter-local.
- **Prohibited leakage:** SDK objects, shell strings, credentials, orchestration state, benchmark formulas, and optimization policy cannot cross the adapter boundary.
- **Current status:** namespaces only; no engine or GPU dependency is installed.
- **Next milestone:** approve a pinned vLLM image and typed capability/launch surface before implementation.
