# vLLM engine adapter

- **Purpose:** provide the first intended production engine translation for certified profiles.
- **Future responsibility/port:** implement `EngineAdapter` by declaring capabilities, validating model/cluster/serving combinations, and producing typed, allowlisted launch specifications.
- **Composition owner:** an agent or provider-worker composition root may instantiate it after compatibility policy approves the pinned runtime.
- **Constraints:** the exact image digest and capability surface remain open decisions; no GPU family is the sole target and engine compatibility is not product certification.
- **Prohibited leakage:** vLLM objects, CLI strings, engine internals, credentials, benchmark methodology, and optimization policy cannot enter schemas, control-plane internals, or unrelated adapters.
- **Current status:** boundary only; no vLLM dependency, image, process, or runtime implementation.
- **Next milestone:** select and document a pinned image and typed capability/launch surface from engine evidence and the reference validation environment.
