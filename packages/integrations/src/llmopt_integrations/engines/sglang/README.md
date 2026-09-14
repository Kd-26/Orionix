# SGLang engine adapter

- **Purpose:** reserve a later/beta engine integration.
- **Future responsibility/port:** implement `EngineAdapter` capability declaration, validation, and typed launch translation for an approved SGLang runtime.
- **Composition owner:** agent or provider-worker composition may instantiate it only for an explicitly experimental or certified profile.
- **Constraints:** SGLang is later than the initial vLLM path and must remain an optional adapter-local dependency.
- **Prohibited leakage:** SGLang objects, shell strings, credentials, optimizer policy, and engine-specific fields cannot leak into core contracts or unrelated engines/providers.
- **Current status:** boundary only; no dependency, image, process, or runtime implementation.
- **Next milestone:** none before the vLLM foundation and SGLang support decision are approved.
