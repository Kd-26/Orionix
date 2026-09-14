# Third-Party Notices

Import namespaces and documentation do not mean third-party software is bundled. vLLM, SGLang, TensorRT-LLM, CUDA, NCCL, PyTorch, LMCache, Foundry, provider SDKs, and other future dependencies are not included merely because an adapter namespace exists.

Before any runtime dependency or redistributed artifact enters a production distribution, its exact version, provenance, transitive dependencies, license obligations, notices, export constraints, and vulnerability posture require review. Actual notices and license texts are added only when the dependency is introduced.

Runpod, JarvisLabs, and Modal are documented provider boundaries only. No provider SDK, CLI, source, or API client is bundled. Engine and provider dependencies must remain optional and absent from the base CPU environment.

Foundry may later be evaluated as an Apache-2.0-licensed internal primitive for CUDA graph persistence, deterministic memory reconstruction, kernel binary restoration, and graph-template reconstruction. This statement is planning context, not confirmation that Foundry is bundled or that its license review is complete.
